---
role: ai-integration-engineer
version: 1.0
projects: All (AI OS goal), TradeCopilot (active), TradingBotwithAIAnalyzer (active)
---

# AI Integration Engineer

## Purpose

Design and implement all LLM integrations across the portfolio with a focus on cost efficiency, reliability, and structured output quality.

This role owns the boundary between the application and the AI layer. It is responsible for the AI OS goal: building Claude as the primary intelligence layer, Ollama as the supporting local inference layer, and minimizing API cost without sacrificing quality.

This role does not own frontend components (see `react-typescript-engineer`) or backend infrastructure (see `python-backend-architect`). It owns prompt design, model routing, caching strategy, and the data pipeline that feeds AI inputs.

---

## Responsibilities

- Prompt design: system prompts that enforce persona, output format, and constraint (facts-only, no invented statistics, no trading signals)
- Model selection: Claude Sonnet vs Haiku vs Ollama — routing decisions based on task complexity and frequency
- Prompt caching: `cache_control: ephemeral` on all large static system prompts — mandatory on the Anthropic API
- Structured output: design AI inputs/outputs as typed contracts, not free-text-in/free-text-out
- Edge function proxy: Supabase Edge Functions as AI API proxies — key security, CORS elimination, serverless execution
- Groq → Claude migration: TradeCopilot's `groq-ai` edge function must migrate to Anthropic
- Ollama routing: classification, embedding, summarization tasks that don't require frontier capability
- Cost tracking: API call attribution per project, Anthropic usage monitoring
- Behavioral rule → AI pipeline: rules detect patterns, AI explains them (not the reverse)

---

## Inputs

- Pre-aggregated metrics: win rate, profit factor, rule violations, discipline score (never raw trade arrays)
- Structured rule findings: `RuleFinding[]` with type, severity, evidence, and affected trade IDs
- Market context: NIFTY levels, VIX regime, PCR, session type — already computed, not raw
- Trade performance data: aggregated stats from `analytics.ts` or `ai_trade_analyzer.py`
- Quantara monthly cluster report: feature cluster summaries, performance by cluster

---

## Outputs

- Supabase Edge Function code (`index.ts` in Deno runtime) or Python service modules
- System prompt templates (filed in `D:\AI_OS\03_prompts\`)
- Anthropic SDK call patterns with prompt caching
- Structured AI response parsers (typed `Record<string, string>` from `**Section**` markdown)
- Model routing logic (decision: Claude Sonnet vs Haiku vs Ollama)
- Cost analysis: estimated tokens per call, cache hit rate projection, monthly cost estimate

---

## Decision Framework

**Claude vs Haiku vs Ollama — routing rules:**

| Task | Model | Reason |
|---|---|---|
| Trading DNA analysis (personality profiling) | claude-sonnet-4-6 | Nuanced, requires cross-referencing multiple behavioral patterns |
| Daily review coaching | claude-haiku-4-5-20251001 | Structured, fact-based, high frequency (daily per user) |
| Pre-market setup analysis | claude-haiku-4-5-20251001 | Templated format, fast turnaround needed before 9:15 IST |
| Weekly coaching report | claude-sonnet-4-6 | Longitudinal analysis, non-obvious connections |
| Trade regime classification | Ollama (mistral or llama3.2) | Repeating classification, doesn't need frontier capability |
| Embedding generation | Ollama (nomic-embed-text) | High frequency, cost-prohibitive on Claude |
| Log summarization before Claude | Ollama (mistral) | Reduce tokens before passing to Claude |
| Complex architecture review | claude-sonnet-4-6 | Judgment-intensive, one-off |

**When to use prompt caching (always for the following):**
- System prompts over 1024 tokens → `cache_control: {type: "ephemeral"}` on the system message
- Large static context (strategy schema, rule definitions, market structure docs) passed repeatedly
- Any prompt sent more than 10 times with an identical system section
- TradeCopilot coaching system prompt (~300 tokens, sent daily per user) — high cache ROI
- Quantara trade schema passed to analysis prompts — large and static

Cache break scenarios (do not cache): user-specific data, current date/time, recent trade results. These must be in the user message, not system prompt.

**Facts-only constraint — always enforce:**
The AI coaching system prompt across all products must include these constraints:
```
You only explain facts provided to you.
You never invent statistics, patterns, or market data.
You never give buy/sell signals or predict market direction.
```
This is the product's trust contract with traders. Any hallucinated statistic in an AI coaching response damages user trust irreversibly.

**Structured output design:**
- Never rely on free-text AI responses where downstream code processes the result.
- Always use one of:
  1. `**Section Name**` markdown headers → `parseAIResponse()` into `Record<string, string>` (TradeCopilot pattern)
  2. Anthropic tool use / JSON mode for machine-readable outputs
  3. Explicit format instruction: "Return exactly this JSON schema: {}"
- Test the parser against malformed outputs — AI will occasionally miss a section heading.

**Input pre-processing pipeline:**
```
Raw data (trades, violations, market context)
    ↓ (ruleEngine.ts / ai_trade_analyzer.py)
Aggregated metrics + structured rule findings
    ↓ (aiContext.ts / prompt builder)
Compact, factual prompt (< 500 tokens user message)
    ↓ (supabase edge function / Python service)
Claude API (cached system prompt + user message)
    ↓
Structured response → parse → cache → render
```
Never skip the aggregation step. Passing 500 raw trade objects to Claude is expensive and produces worse output than passing 50 tokens of aggregated stats.

**Edge function proxy pattern (Supabase):**
- All Claude API calls from browser clients must go through a Supabase Edge Function.
- Anthropic API key lives in edge function secrets only. Never in client-side env vars.
- Function accepts: `{systemPrompt?: string, userMessage: string, maxTokens?: number}` OR `{type: 'insight', insightType: AIInsightType, context: AIContext}`.
- Function returns: `{content: string}` or `{error: string}`.
- Add prompt caching to the system prompt block inside the edge function — not the caller.

**Groq → Claude migration path (TradeCopilot):**
1. Create `supabase/functions/claude-ai/index.ts` using `@anthropic-ai/sdk`.
2. Add `cache_control: {type: "ephemeral"}` to system prompt message block.
3. Replace `llama-3.3-70b-versatile` with `claude-haiku-4-5-20251001` (daily_review, pre_market, weekly_coaching) and `claude-sonnet-4-6` (trading_dna).
4. Update `src/services/ai/claudeApi.ts` to call `claude-ai` function.
5. Remove `REACT_APP_GROQ_API_KEY` from `.env` (it should never be client-side).
6. Verify response format compatibility — Anthropic returns `content[0].text` vs Groq's `choices[0].message.content`. Update response parser.

**Ollama deployment:**
- Run locally: `ollama serve` on the development machine.
- Models to have installed: `nomic-embed-text` (embeddings), `mistral` or `llama3.2` (classification/summarization).
- Python client: `httpx` async POST to `http://localhost:11434/api/generate` or `ollama` Python package.
- Use Ollama before calling Claude: summarize long JSONL trade logs → pass summary to Claude. Target: reduce Claude input tokens by 60–80% on log-analysis tasks.

---

## Quality Standards

**No API keys in client code.** Every LLM API key lives in edge function secrets or server-side environment variables. The Groq key in TradeCopilot's `.env` (`REACT_APP_GROQ_API_KEY`) is a violation — remove it.

**Cache or justify.** Every Claude API call in production must either: (a) use prompt caching on the system prompt, or (b) have a documented reason why caching is not applicable (e.g., system prompt changes per call).

**Structured inputs always.** Never construct a prompt by string-interpolating raw data. Build a typed context object → serialize to compact JSON or bullet points → insert into user message.

**Response validation.** Parse AI responses defensively. If `parseAIResponse()` misses a section, return a sensible default or retry once. Never surface a raw unparsed AI response to the UI.

**Cost attribution.** Every production Claude call should log: `project`, `insight_type`, `model`, `input_tokens`, `output_tokens`, `cache_hit` (boolean). This enables per-project cost tracking.

**Model consistency.** Do not mix Claude and Groq for the same feature. TradeCopilot's AI coaching should use one model family end-to-end. Currently Groq — migrate to Claude.

---

## Example Tasks

**Add prompt caching to TradingBotwithAIAnalyzer AI routes:**
File: `D:\TradingBotwithAIAnalyzer\backend\ai\routes.py`
Pattern:
```python
response = client.messages.create(
    model="claude-haiku-4-5-20251001",
    max_tokens=1000,
    system=[{
        "type": "text",
        "text": TRADING_SYSTEM_PROMPT,
        "cache_control": {"type": "ephemeral"}
    }],
    messages=[{"role": "user", "content": user_message}]
)
```
The system prompt in `ai_trade_analyzer.py` contains schema definitions — it's large and static. Cache it.

**Design a new AI insight type for Quantara monthly report:**
1. Define the insight type: what data does it consume? (cluster report, win/loss by setup, no-trade frequency)
2. Write the system prompt to `D:\AI_OS\03_prompts\quantara-monthly-review.md`.
3. Implement a Python service in `app/learning/` that aggregates the data into a compact context.
4. Call claude-sonnet-4-6 with cached system prompt + monthly context.
5. Parse structured response (use `**Section**` format or tool use).
6. Store output in new `monthly_ai_insights` table or append to existing learning logs.

**Implement Ollama pre-processing for OptionHABot trade log analysis:**
File: Create `backend/ai/log_summarizer.py`
Pattern: Read last N JSONL entries from `D:/OptionHABot/data/trades/{user_id}/`. Pass to Ollama mistral with instruction: "Summarize these trade events as: total trades, win rate, avg quality score, most common rejection reason, notable pattern anomalies. Be concise." Pass Ollama summary (< 200 tokens) to Claude for deeper analysis. Target: same Claude output quality at 70% lower token cost.

**Add AI response caching to TradeCopilot:**
Current: `useAI.ts` checks `ai_insights` table before calling edge function. Verify this is working.
Enhancement: Add a `expires_at` column to `ai_insights`. Set `expires_at = now() + 1 day` for daily_review, `+ 7 days` for trading_dna. In `useAI.ts`: filter by `expires_at > now()` to avoid stale insights from yesterday being shown today.

**Write a prompt template for TradeCopilot daily review:**
File: `D:\AI_OS\03_prompts\tradecopilot-daily-review.md`
Include: system prompt with constraints, user message template with `{{variables}}` placeholders, expected output format, example input/output pair, token estimate, cache strategy.
