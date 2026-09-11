---
description: Run the skill-library health check
---

Run the validator and report results:

```bash
python3 scripts/validate.py
```

If anything fails, list each failure with its file path and what to fix. If it
passes, note any `UNVERIFIED` blocks or stale verification dates still
outstanding — those are tracked, not blocking, but they're the backlog.
