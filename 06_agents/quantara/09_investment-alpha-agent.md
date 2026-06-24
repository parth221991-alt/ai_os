# Investment Alpha Agent Specification (Tier 1)

**Agent ID:** `investment_alpha`  
**Status:** NOT IMPLEMENTED  
**Priority:** High — required for Investment Book operation (Phase 4)  
**Activation:** On demand — processes new data as it becomes available. Not time-bound.  
**Tier:** 1 — Alpha Generation Engine  
**Claude dependency:** YES — claude-sonnet-4-6 for investment thesis. This is the most capital-intensive Claude call in the system.

---

## Mission

Identify, analyze, and manage positions in quality Indian equities for 3-month to multi-year holds.

This agent applies an institutional CIO process: systematic stock scoring, structured investment thesis generation, valuation-driven entry, and thesis-based exit discipline. It does NOT exit on price — only on thesis break.

The Investment Book targets 40–60% of total capital. At ₹5 crore, this is ₹2–3 crore in quality long-term positions. This is the highest-stakes book.

---

## Inputs

| Input | Source | Schema | Frequency |
|---|---|---|---|
| Fundamental data | External (screener.in, BSE/NSE filings) | `FundamentalData` | Weekly batch |
| Price data | MongoDB `market_data` | `OHLCV` | Daily |
| Sector rankings | Intelligence Agent | `SectorRanking` | 3× daily |
| Macro context | Intelligence Agent | `MacroContext` | Daily |
| Portfolio state | Portfolio State Manager | `PortfolioState` | Per evaluation |
| Strategy stats | Portfolio State Manager | `StrategyStats` | On startup + after close |
| Claude thesis cache | MongoDB `ai_cache` | Investment thesis | Per position |

---

## Outputs

### `InvestmentSignal`
```python
@dataclass(frozen=True)
class InvestmentSignal:
    agent_id: str = "investment_alpha"
    trace_id: UUID
    timestamp: datetime
    
    symbol: str
    action: str          # INITIATE | ADD | REDUCE | EXIT | HOLD
    confidence: float    # 0.0 to 1.0
    
    # Entry (INITIATE / ADD)
    entry_zone_low: Optional[int]   # paise
    entry_zone_high: Optional[int]  # paise
    
    # Sizing
    position_size_pct: float        # % of investment book capital
    
    # Thesis
    thesis_id: str                  # References MongoDB thesis document
    key_catalysts: List[str]
    thesis_break_conditions: List[str]  # When to EXIT regardless of price
    
    # Valuation
    quality_score: float    # 0.0 to 1.0
    value_score: float      # 0.0 to 1.0
    growth_score: float     # 0.0 to 1.0
    momentum_score: float   # 0.0 to 1.0
    composite_score: float
    
    # Risk
    margin_of_safety_pct: float     # Must be > 15% for INITIATE
    sector: str
    market_cap_cr: float
```

### Investment Thesis Document (MongoDB `signals`)
```json
{
  "thesis_id": "...",
  "symbol": "HDFC Bank",
  "action": "INITIATE",
  "generated_at": "...",
  "model_used": "claude-sonnet-4-6",
  "cache_ttl_hours": 48,
  "investment_case": "...",
  "key_risks": ["..."],
  "thesis_break_conditions": ["..."],
  "valuation_summary": "...",
  "target_horizon_months": 12,
  "explainability": { ... }
}
```

---

## Stock Scoring Model

All factors computed deterministically. No Claude involved in scoring.

| Factor | Weight | Components |
|---|---|---|
| **Quality** | 30% | ROE, ROCE, debt/equity, interest coverage, promoter holding, governance rating |
| **Growth** | 25% | Revenue growth 3yr CAGR, earnings growth 3yr CAGR, margin expansion trend, management guidance quality |
| **Value** | 25% | PE vs sector median, PB ratio, EV/EBITDA, FCF yield, margin of safety |
| **Momentum** | 20% | Price momentum 12m (1m excluded), earnings revision direction, institutional accumulation (FII+DII net) |

**Minimum thresholds for ANY consideration:**

| Criterion | Minimum |
|---|---|
| Quality score | > 0.65 |
| Sector state | IMPROVING or STRONG |
| Margin of safety | > 15% |
| Market cap | > ₹5,000 Cr |
| Liquidity | Avg daily traded value > ₹50 Cr |

---

## Decision Types

| Action | Trigger | Claude Required | Analysis Depth |
|---|---|---|---|
| `INITIATE` | Composite score > 0.70, all minimums met, sector strength | **YES — Sonnet** | Full thesis: investment case, risks, thesis break conditions, valuation |
| `ADD` | Existing position, price dips to entry zone, thesis intact | Lighter (Haiku OK) | Confirm thesis still valid |
| `REDUCE` | Valuation or fundamentals deterioration | Sonnet (if complex) | Valuation review |
| `EXIT` | Thesis break condition triggered | Sonnet | Thesis break confirmation + postmortem |
| `HOLD` | Periodic review, no trigger | Haiku | Confirm thesis, document reason |

**EXIT is triggered by thesis break only — never by temporary price decline alone.**

**HOLD is not a default state.** Every HOLD must have a documented reason: "thesis intact, valuation still reasonable, await [catalyst]."

---

## Claude Usage

### INITIATE — Full Sonnet Thesis

**When:** New position initiation. Once per new INITIATE signal. Cached 48 hours.

**System prompt:** Large static context about Indian equity market, quality investing framework, valuation principles. Cached with `cache_control: ephemeral`.

**User message includes:**
- Fundamental data: ROE, ROCE, revenue growth, margins, debt levels
- Valuation metrics: PE vs sector, PB, EV/EBITDA, FCF yield
- Sector analysis (from Intelligence Agent)
- Recent management commentary (earnings concall key points — from Haiku pre-summary)
- Composite score breakdown
- Portfolio context: current sector exposure, concentration

**Output:**
```json
{
  "investment_case": "3-5 sentence thesis",
  "key_catalysts": ["...", "...", "..."],
  "key_risks": ["...", "...", "..."],
  "thesis_break_conditions": ["Revenue growth <10% for 2 consecutive quarters", "ROCE < 15%", "Promoter holding falls >5%"],
  "valuation_summary": "...",
  "target_horizon_months": 12,
  "confidence": 0.78
}
```

### HOLD — Haiku Confirmation

**When:** Weekly review of open positions. Batched (all open investment positions in one call).

**Output:** For each position: thesis_intact=true/false, concern_level=LOW/MEDIUM/HIGH, action_required=HOLD/FLAG_FOR_REVIEW.

### EXIT — Sonnet Postmortem

**When:** After position close. Batched with other recent closes (max 3 per call).

**Output:** What worked, what failed, what to update in the scoring model.

---

## Failure Modes

| Failure | Detection | Response |
|---|---|---|
| Claude API unavailable | SDK connection error | BLOCK new INITIATE decisions. Existing positions managed rule-based (no forced exit). Alert: Investment book in HALTED state. |
| Fundamental data source unavailable | HTTP error on screener.in | Use last cached data (MongoDB). Flag data as STALE. Do not re-score with stale data. |
| Thesis break condition ambiguous | Score unchanged but narrative shift | Route to human review. Log as `THESIS_REVIEW_REQUIRED`. |
| Position in loss but thesis intact | Normal | Do NOT exit. Hold. Document in HOLD record. |

---

## Interface Contract

```python
class InvestmentAlphaAgent:
    async def screen_universe(self) -> List[str]:
        """
        Apply minimum threshold filters to stock universe.
        Returns list of symbols passing all minimums.
        Pure computation — no Claude.
        """
    
    async def score_stock(self, symbol: str) -> StockScore:
        """
        Compute 4-factor composite score.
        Pure computation — no Claude.
        """
    
    async def generate_thesis(
        self,
        symbol: str,
        score: StockScore,
        portfolio_context: PortfolioState,
    ) -> InvestmentSignal:
        """
        Generate INITIATE signal with full Claude Sonnet thesis.
        Checks cache first. If hit: return cached. If miss: call Claude.
        Writes thesis to MongoDB signals collection.
        """
    
    async def review_open_positions(
        self,
        positions: List[Position],
    ) -> List[Tuple[Position, str]]:
        """
        Weekly review: batch Haiku call for all open investment positions.
        Returns (position, action) pairs: HOLD / FLAG_FOR_REVIEW / EXIT.
        """
    
    async def on_thesis_break(
        self,
        position: Position,
        break_condition: str,
    ) -> InvestmentSignal:
        """
        Generate EXIT signal. Thesis break overrides any price consideration.
        """
```

---

## Evaluation Metrics

| Metric | Target | How to Measure |
|---|---|---|
| **Thesis break detection accuracy** | > 80% of EXITs were correct thesis breaks | Postmortem: did fundamentals deteriorate as predicted? |
| **Margin of safety adherence** | 100% of INITIATEs have > 15% MOS | `investment_signals.margin_of_safety_pct >= 15` |
| **False INITIATE rate** | < 20% (underperform Nifty within 12 months) | Compare to NIFTY benchmark at 12m |
| **Portfolio concentration compliance** | 100% (no sector > 40%) | `portfolio_state.sector_exposure` check on every INITIATE |
| **Thesis cache hit rate** | > 80% (same week) | MongoDB ai_cache hit rate for investment theses |
| **Claude cost per INITIATE** | < ₹20 (≈ $0.02) | Token tracking per thesis generation |
