# Python Trading Bot — Project Scaffold

Copy this structure to `D:\AI_OS\04_projects\{{ProjectName}}`.

## Directory Structure

```
{{ProjectName}}/
├── config/
│   ├── strategy.yaml       # All strategy thresholds (no hardcoding)
│   ├── risk.yaml           # Kill switch levels, daily/weekly loss limits
│   └── broker.yaml         # Zerodha connection params (not secrets)
├── src/
│   ├── bot.py              # Main FSM loop (IDLE → WATCHING → SIGNAL → IN_TRADE → EXITED)
│   ├── strategy.py         # Signal logic — reads from config/strategy.yaml
│   ├── risk.py             # Kill switch, loss limiter (port from Quantara)
│   ├── broker.py           # Zerodha Kite Connect wrapper
│   ├── candles.py          # Heikin Ashi / raw OHLC builder
│   ├── orders.py           # LIMIT→MARKET fallback logic
│   └── logger.py           # Append-only JSONL logger
├── api/
│   ├── main.py             # FastAPI app (health, status, manual controls)
│   └── routes/
├── tests/
│   ├── test_strategy.py
│   ├── test_risk.py
│   └── test_candles.py
├── .env.example            # All required keys listed, no real values
├── requirements.txt
└── README.md
```

## Required Config Keys (strategy.yaml)

```yaml
# strategy.yaml — ALL thresholds live here
entry:
  body_pct_threshold: 0.6      # C1 body as % of LTP
  confirmation_lookback: 1     # bars to look back for C2

exit:
  lot1_target_pts: 30
  lot1_stop_pts: 15
  lot2_target_pts: 15

timeframe_minutes: 1
instrument: "NIFTY"
```

## Required Config Keys (risk.yaml)

```yaml
# risk.yaml — matches Quantara kill switch pattern
kill_switch:
  consecutive_loss_limit: 2     # Level 1: pause
  consecutive_loss_hard: 5      # Level 2: halt session
  daily_loss_limit_pct: 2.0     # % of capital
  weekly_loss_limit_pct: 5.0

paper_mode: true               # MUST be true until paper gate passes
paper_weeks_required: 8
```

## Non-Negotiable Requirements

- `market_protection=-1` on all MARKET orders (SEBI compliance)
- Kill switch checked before every entry
- No intrabar entries — candle close only
- JSONL append-only trade log
- `paper_mode: true` default until paper gate passes (8 weeks)
