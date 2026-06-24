# AI Agent Philosophy

Tags: #context #claude #cost #architecture

## Use Claude For
- Strategy logic reasoning, edge cases, architectural tradeoffs
- Code generation requiring codebase contextual understanding
- Signal logic review and architecture decisions
- Writing prompts, templates, agent definitions
- Analyzing trade performance, surfacing non-obvious patterns
- Any task requiring judgment, not pattern matching

## Do NOT Use Claude For
- Pattern classification where local model suffices
- Embedding generation (use Ollama)
- Batch offline operations that don't need real-time reasoning
- High-frequency repeated prompts (cache aggressively)

## Use Ollama For
- Embedding generation (nomic-embed-text, mxbai-embed-large)
- Candle regime / volatility state / day-type classification
- Summarizing long trade logs before passing to Claude
- Background jobs: overnight reports, weekly clustering
- Any task running >10x/minute in production

## Decision Rule
If the task does NOT require world knowledge, nuanced reasoning, or frontier capability — run it locally with Ollama.

## Cost Optimization Rules
1. Prompt cache all static context (`cache_control: ephemeral` on system prompt blocks)
2. Preprocess with Ollama before Claude — summarize 500 lines → 50 lines locally
3. Batch non-urgent Claude calls via Anthropic Batch API
4. Gate Claude calls behind local pre-filters (hard gates first)
5. Cache Claude responses where output is deterministic
6. Haiku for high-frequency, Sonnet for reasoning — never swap
7. Tag API calls with project identifier for cost attribution

## Groq Note
TradeCopilot uses Groq (tech debt). New AI features in TradeCopilot → Anthropic. Migration is medium-priority backlog.

## Related
- [[Canonical Tech Stack]]
- [[AI_OS Overview]]
