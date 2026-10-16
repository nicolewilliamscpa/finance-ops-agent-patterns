# Pattern 1 — Business-Day Gating

**Problem.** A lot of recurring finance and ops work is due on the *Nth business
day* of a period ("book accruals on BD2", "deliver the tie-out on BD6"), but
schedulers (cron, most task systems) only understand calendar days. Business-day
number drifts against the calendar every month because of weekends and holidays,
so a fixed calendar-day schedule either fires on the wrong day or misses the
target entirely.

**Solution.** Decouple *when the task wakes up* from *when it does work*.

1. Schedule the task to wake up on a **window of calendar days** that is
   guaranteed to contain the target business day (e.g. the 1st–5th of the month
   for BD2, the 6th–10th for BD6).
2. On every wake-up, the first thing the agent does is **compute the real target
   business day** and compare it to today. If today is not the target, the run
   **no-ops immediately** — no files opened, no messages sent, nothing.
3. Only on the one day that matches does the agent proceed to the actual work.

This turns an unreliable "fire once on a guessed date" into a reliable "wake up
a few times, act exactly once."

## Why a window instead of a single calendar day

If you hard-code a single calendar day you have to guess how weekends/holidays
will fall, and you will be wrong some months. A window a few days wide costs you
nothing — the extra wake-ups no-op in well under a second — and it is robust to
every month's layout. Size the window so it always covers the target:

| Target      | Safe calendar window | Why |
|-------------|----------------------|-----|
| BD1         | 1st–5th              | A long holiday weekend can push BD1 to the 5th (e.g. Jan 1 + weekend). |
| BD2         | 1st–5th              | Same reasoning, +1 day of slack. |
| BD6         | 6th–10th             | Six business days can land as late as the 9th–10th. |

## The gate goes first, and it is cheap

The no-op path must be the fastest, safest path in the whole task. Put the gate
at the very top, before any file access, API call, or message. A run on a
non-target day should read today's date, do the arithmetic, and exit. This is
what makes the "wake up several times" approach free.

## Holidays: decide your precision explicitly

You have three honest options; pick one per task and say which in the prompt:

- **Weekends only** (skip Sat/Sun, ignore holidays). Simplest. Good when being a
  day early on a holiday month is harmless.
- **Weekends + a fixed holiday list** (e.g. US federal holidays). More accurate,
  needs a maintained list.
- **Weekends + a holiday library.** Most accurate, adds a dependency.

The mistake is leaving it ambiguous. An agent that silently assumes one thing
while you assumed another will fire on the wrong day a few times a year.

## Reference implementation

See [`scripts/business_days.py`](../../scripts/business_days.py) for a
dependency-free business-day calculator with all three holiday modes, plus a
`is_target_business_day()` helper that is exactly what the gate should call.

## Prompt snippet

```
Step 0 — GATE (do this before anything else):
Determine today's date in <TIMEZONE>. Compute the <N>th business day of the
current month (Mon–Fri counted from the 1st; skip weekends; <holiday rule>).
If today is NOT that date, stop immediately — do not open any files, message
anyone, or produce output. Just end. Only if today IS BD<N>, continue.
```

## Related patterns

- [Idempotency & no-duplicate runs](04-idempotency-and-no-duplicate-runs.md) —
  the second guard, for when the target day fires but the work is already done.
- [Fail-safe guardrails](02-failsafe-guardrails.md) — what to do when inputs
  aren't ready on the target day.
