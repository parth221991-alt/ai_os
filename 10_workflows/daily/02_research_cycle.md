# Workflow: Daily Research Cycle

**Owner:** Research Director  
**Trigger:** 8:30 AM (before market open)  
**Output:** `11_reports/archive/YYYY-MM-DD/research_brief.md`  
**Duration:** ~10 minutes to generate

---

## Purpose

Produce a daily research brief covering macro conditions, market regime, key news, and any developments relevant to Quantara's strategy. This is the intelligence feed that informs trading context — it does NOT override Quantara's internal regime detection.

---

## Inputs Required

| Input | Source | How to get it |
|---|---|---|
| Market conditions (describe current regime) | Founder provides / news scan | Describe verbally or paste headlines |
| NIFTY status (range, trend, key levels) | Trading terminal | Paste current levels |
| Key economic events today | Economic calendar | NSE / Zerodha calendar |
| Relevant news (macro, geopolitical, sector) | News sources | Paste top 3–5 headlines |
| Quantara paper trading status | Quantara logs | Check `D:\quantara` health |

---

## Process

Claude (acting as Research Director) will:

1. Synthesize provided inputs into a market regime assessment
2. Identify the day type (trending, ranging, event-driven, risk-off)
3. Flag any developments relevant to Quantara's active strategies
4. Note any sectors or stocks to watch for TradeCopilot signal ideas
5. Surface one research question worth investigating this week
6. Write the brief

---

## Output Format

```
# Research Brief — [DATE]

## Market Regime
[Day type + rationale in 2–3 lines]

## Key Levels (NIFTY)
Support: | Resistance: | Trend:

## Today's Watchlist
- [Item 1: why it matters]
- [Item 2: why it matters]

## Quantara Relevance
[How today's conditions affect active Quantara strategies]

## Research Thread
[One question worth investigating this week]

## Macro Calendar
[Today's scheduled events that could move the market]
```

---

## What This Is NOT

- This does NOT replace Quantara's internal regime agent (which runs at 9:00 AM using live data)
- This does NOT generate trading signals
- This is company-level intelligence, not execution-level intelligence
