# Pattern 4 — Idempotency & No-Duplicate Runs

**Problem.** The business-day gating pattern deliberately wakes a task up on
several calendar days so it can catch the right business day. But that, plus
manual re-runs, retries, and overlapping schedules, means a task *will*
sometimes run more than once for the same period. If the work isn't idempotent,
you get doubled rows, a workbook processed twice, two Slack posts of the same
briefing, or a reconciliation re-run on a month that's already closed.

**Solution.** Every run should be able to answer "has this period already been
done?" *before* it does anything, and exit cleanly if so. Design the work so
that running it twice produces the same result as running it once.

## Three complementary guards

**1. Completion check (preferred).** Look for evidence that this period's output
already exists, and if it does, stop. The evidence is usually a file, a tab, a
row, or a checklist mark:

- Does the target folder already contain the deliverable named for this period?
- Does the workbook's last populated column already include this month?
- Is the checklist row for this task already dated as prepared?

> Before building, check whether this period's output already exists. If the
> target month's file is already present (or the workbook already includes this
> month), stop and report a possible duplicate run rather than re-doing it.

**2. Gap check.** The opposite failure: if the last completed period is more than
one period behind the target, something was *skipped*. Don't silently try to
catch up several periods at once — that compounds risk. Stop and report the gap
so a human decides how to backfill.

**3. De-dupe on output.** For messages and posts, check recent history before
sending. If an identical message (same header/period) went out in the last few
minutes, don't send again. Compose once, send with exactly one call, and on an
unclear result re-read history before retrying rather than blindly re-posting.

## Write to new files; never overwrite the source

A strong, simple safety habit: each run writes a **new, period-stamped output
file** and never overwrites the file it started from.

- `... thru Q3.xlsx` → new file `... thru Q4.xlsx`, prior file untouched.
- The prior period's deliverable stays as an audit trail and a fallback.
- A bad run can't destroy good prior work.

Pair this with reading the *most recent* matching file as the starting point, so
the chain advances cleanly period over period.

## Idempotency for append-style updates

When a run adds rows (new subscriptions, new assets, new entries), the duplicate
risk is doubled rows. Guard it by checking, before appending, whether the period
being added is already represented in the data. If the target month's rows are
already there, stop — don't append a second copy.

## Why this matters more for agents than for humans

A human running a monthly process remembers they already did it. An unattended
agent starts fresh every run with no memory of prior runs, so the *only* thing
standing between you and a double-processed close is an explicit check against
durable state (the files, the workbook, the checklist, the message history).
Make that check the first real step after the business-day gate.

## Prompt snippet

```
Before doing any work (after the business-day gate):
- Completion check: if this period's deliverable already exists in the target
  location (file present / workbook already includes this period / checklist
  row already dated), stop and report "already completed".
- Gap check: if the last completed period is more than one period behind the
  target, stop and report the gap instead of catching up silently.
- Write output to a NEW period-stamped file; never overwrite the source.
- For messages: read recent history first; if today's was already posted, do
  not send again.
```

## Related patterns

- [Business-day gating](01-business-day-gating.md) — the reason multiple runs
  happen in the first place.
- [Fail-safe guardrails](02-failsafe-guardrails.md) — the gap check is a "stop,
  don't improvise" decision.
