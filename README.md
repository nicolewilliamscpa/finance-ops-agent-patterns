# Patterns for Reliable Finance & Ops Agents

A field-tested toolkit for building **scheduled AI agents that run real finance
and operations work unattended** — month-end closes, reconciliations,
roll-forwards, access reviews, and daily briefings — without fabricating data,
double-running, or producing confident-but-wrong deliverables.

It is deliberately *not* a framework. It's a set of **design patterns**, a
library of **copy-pasteable prompt templates**, and a few **runnable example
scripts** that capture the techniques that make unattended agents trustworthy.
Everything is model-agnostic and tool-agnostic: the ideas work with any agent
runtime and any scheduler.

## Why this exists

Scheduling an AI agent to "run the monthly close" is easy. Scheduling one you can
actually *leave alone* is not. The hard parts aren't the accounting — they're:

- firing on the right **business day**, which drifts against the calendar;
- **refusing to improvise** when an input is missing instead of inventing it;
- not **double-processing** a period when a task wakes up several times;
- proving the output is right with **tie-outs that must equal zero**;
- keeping long procedures **maintainable** instead of a wall of prompt text.

These patterns come from running a dozen production accounting automations
through full monthly and quarterly close cycles. The specifics have been
genericized; the structure is exactly what works.

## Repo map

```
docs/patterns/     the six design patterns (start here)
templates/         genericized, fill-in-the-blanks prompt templates
scripts/           runnable example code + dummy sample data
```

### The patterns

| # | Pattern | In one line |
|---|---------|-------------|
| 1 | [Business-day gating](docs/patterns/01-business-day-gating.md) | Wake on a calendar window; act only on the real BD-N. |
| 2 | [Fail-safe guardrails](docs/patterns/02-failsafe-guardrails.md) | Stop and report; never fabricate or force a result. |
| 3 | [SOP-driven skills](docs/patterns/03-sop-driven-skills.md) | Split *when* (task) from *how* (skill) from *exactly how* (SOP). |
| 4 | [Idempotency & no-duplicate runs](docs/patterns/04-idempotency-and-no-duplicate-runs.md) | Check "already done?" before doing anything; write new files. |
| 5 | [Tie-out verification](docs/patterns/05-tie-out-verification.md) | Bake in checks that must equal zero; zero is a gate, not a goal. |
| 6 | [Multi-source briefing](docs/patterns/06-multi-source-briefing.md) | One filtered, cross-referenced, phone-friendly digest. |

### The templates

Fill-in-the-blank prompts for the common task shapes — full close process,
reminder/kickoff, monthly append/roll-forward, daily briefing, and the skill+SOP
split. See [`templates/`](templates/README.md).

### The scripts

| Script | Shows |
|--------|-------|
| [`business_days.py`](scripts/business_days.py) | A dependency-free business-day calculator + the `is_target_business_day()` gate, with weekend-only and US-federal-holiday modes. |
| [`tie_out.py`](scripts/tie_out.py) | A tiny verification harness: named checks, exact variances, pass/fail report. |
| [`make_census_pivot.py`](scripts/make_census_pivot.py) | Building an `.xlsx` with **genuine, refreshable Excel PivotTables** via the LibreOffice UNO bridge — the reliable way, after the hand-authored-XML way fails. |

See [`scripts/README.md`](scripts/README.md) for a quickstart.

## How the pieces fit together

A single scheduled task usually combines several patterns:

```
wake up (calendar window)
   └─ Pattern 1: is today the target business day?  ── no ─▶ exit silently
                      │ yes
   └─ Pattern 4: already done this period / is there a gap? ── yes ─▶ stop + report
                      │ no
   └─ Pattern 2: are all inputs present & valid? ── no ─▶ notify owner + stop
                      │ yes
   └─ Pattern 3: invoke the skill; follow the SOP
   └─ Pattern 5: every tie-out == 0?  ── no ─▶ report variance + stop
                      │ yes
   └─ write a NEW period-stamped file; summarize; leave manual steps for a human
```

The [close-process template](templates/scheduled-close-process.md) is that whole
flow, ready to fill in.

## A word on data & confidentiality

This repo contains **patterns and structure only**. It ships no real data. If you
adapt these for your own organization:

- Never commit real inputs, outputs, account numbers, employee data, folder
  paths, channel IDs, or credentials.
- Confirm you're permitted to automate the process before you do.
- Keep the repo private until you've reviewed every file and have any sign-off
  your organization requires.

The `.gitignore` here blocks the obvious offenders, but it is not a substitute
for reading your diffs.

## License

[MIT](LICENSE). Use it, adapt it, ship it.
