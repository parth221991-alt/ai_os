# Specs — AI_OS Self-Fixing Loop

Specs written by `/spec` live here. `/build` reads them. `/review` grades against them.

## Directory layout

```
specs/
├── Quantara/          ← Quantara feature specs
├── TradeCopilot/      ← TradeCopilot feature specs
├── OptionHABot/       ← OptionHABot feature specs
├── TradingBotA/       ← TradingBotA feature specs
├── CareerPilot/       ← CareerPilot feature specs
├── AI_SNIPP/          ← AI_SNIPP content specs
└── AI_OS/             ← Infrastructure / dashboard specs
```

## Naming convention

`<kebab-case-feature-name>.md`

Examples:
- `quantara-frontend-dashboard.md`
- `careerpilot-naukri-apply-worker.md`
- `tradecopilot-claude-haiku-migration.md`

## Workflow

```
/spec          → interview → specs/<project>/<name>.md
/build         → reads spec → builds → coverage report
/review        → grades build vs spec → PASS or FAIL list
loop /build /review → runs until clean
```

## Spec status values

| Status | Meaning |
|---|---|
| Draft | Interview in progress |
| Ready | Spec complete, ready to build |
| In Build | /build is working against this |
| In Review | /review is checking the build |
| Done | /review passed clean |
