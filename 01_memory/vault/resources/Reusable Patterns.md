# Reusable Patterns

Tags: #resources #patterns #reusability

Artifacts worth extracting into shared AI_OS folders.

## Routing Table
| Artifact | Target |
|---|---|
| Reusable prompt templates | `D:\AI_OS\03_prompts\` |
| Claude agent definitions | `D:\AI_OS\06_agents\` |
| Code snippets and utilities | `D:\AI_OS\05_content\` (AI_SNIPP) |
| Project scaffolding | `D:\AI_OS\07_templates\` |
| MCP server configs | `D:\AI_OS\08_mcp\` |
| Architecture decisions | `D:\AI_OS\09_docs\` |
| Session context and memory | `D:\AI_OS\01_memory\` |

## Patterns Already Identified

### Zerodha WebSocket Client
Present in: OptionHABot, TradingBotA, TradingBotwithAIAnalyzer
Extract to: `D:\AI_OS\05_content\zerodha-ws-client\`

### LIMIT→MARKET Fallback
Present in: TradingBotA, TradingBotwithAIAnalyzer
Logic: LIMIT at LTP+2 → wait 10s → MARKET if slippage < 4pts else cancel
`market_protection=-1` required (SEBI compliance)

### Kill Switch / Daily Loss Limiter
Reference implementation: Quantara (most robust)
Pattern: 2/5 consecutive loss limits, daily/weekly drawdown gates (risk.yaml)

### Heikin Ashi Candle Builder
Present in: OptionHABot, TradingBotA, TradingBotwithAIAnalyzer

### 2-Lot Multi-Exit Risk Model
Present in: TradingBotA, TradingBotwithAIAnalyzer

### Design System (Frontend)
Reference: `D:\TradingBotwithAIAnalyzer\design_guidelines.json`
Promote to: `D:\AI_OS\07_templates\`

## Related
- [[Architecture Decisions]]
- [[Quantara]]
