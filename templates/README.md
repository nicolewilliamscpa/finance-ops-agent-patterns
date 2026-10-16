# Prompt Templates

Fully genericized, copy-pasteable prompts for scheduled agent tasks. Every
company-specific detail is a `{{PLACEHOLDER}}` — fill them in for your own
process. Each template implements one or more of the
[design patterns](../docs/patterns).

| Template | Use it for | Patterns |
|----------|-----------|----------|
| [scheduled-close-process.md](scheduled-close-process.md) | A full period-end workpaper/reconciliation built from inputs | 1, 2, 3, 4, 5 |
| [scheduled-reminder-kickoff.md](scheduled-reminder-kickoff.md) | A task that kicks off a process and waits for a human to attach inputs | 1, 2 |
| [monthly-append-update.md](monthly-append-update.md) | A roll-forward that appends a new period's rows to a workbook | 1, 2, 4, 5 |
| [daily-briefing.md](daily-briefing.md) | A morning briefing or end-of-day reminder from multiple sources | 2, 4, 6 |
| [skill-and-sop-structure.md](skill-and-sop-structure.md) | How to split the procedure into a skill + SOP the task invokes | 3, 5 |

## Placeholder conventions

- `{{TIMEZONE}}` — e.g. `America/New_York`
- `{{BD_N}}` — target business day number, e.g. `2` or `6`
- `{{WINDOW}}` — the calendar-day wake-up window, e.g. `1st–5th`
- `{{OWNER}}` — who to notify (name / email / chat handle)
- `{{PROCESS_NAME}}` — the skill/process name
- `{{SOP_FILE}}` — the detailed SOP document's filename
- `{{INPUT_FOLDER}}` / `{{OUTPUT_FOLDER}}` — where inputs live / outputs go
- `{{INPUTS}}` — the list of required input files and how to recognize each
- `{{CHECKS}}` — the named tie-outs that must equal zero
- `{{MANUAL_STEPS}}` — actions that must stay manual (e.g. posting entries)

> **Before using any of these on real data:** confirm you're allowed to automate
> the process, and never commit real inputs, outputs, names, account numbers, or
> credentials to a repository. These templates describe *structure*, not your
> data.
