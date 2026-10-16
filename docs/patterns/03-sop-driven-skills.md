# Pattern 3 — SOP-Driven Skills

**Problem.** Real recurring processes are long. A full month-end reconciliation
might have twenty steps, a dozen column-level mechanics, and a handful of
fragilities that only matter in certain months. If you cram all of that into the
scheduled task's prompt, the prompt becomes unmaintainable, and every small
process change means editing a wall of text. If you leave it out, the agent
improvises the details and gets them subtly wrong.

**Solution.** Separate the three concerns into three layers:

```
┌─────────────────────────────────────────────────────────────┐
│  SCHEDULED TASK PROMPT  (the trigger)                        │
│  - when to run, the business-day gate                        │
│  - where the inputs/outputs live                             │
│  - which skill to invoke                                     │
│  - guardrails + summary format                               │
│  → short, stable, rarely edited                              │
└──────────────────────────┬──────────────────────────────────┘
                           │ invokes
┌──────────────────────────▼──────────────────────────────────┐
│  SKILL  (the procedure)                                      │
│  - the ordered steps of the process                          │
│  - what "done" and "tied out" mean                           │
│  → the reusable recipe, versioned with the process           │
└──────────────────────────┬──────────────────────────────────┘
                           │ references
┌──────────────────────────▼──────────────────────────────────┐
│  SOP DOCUMENT  (the ground truth)                            │
│  - exact tab/column mechanics, formulas, constants           │
│  - known fragilities and the month they bite                 │
│  → deep detail, updated when the workbook changes            │
└─────────────────────────────────────────────────────────────┘
```

**The task says *when and whether*. The skill says *how*. The SOP says *exactly
how, down to the cell*.**

## Why three layers instead of one

- **The task prompt stays short and stable.** It's about scheduling and safety,
  not procedure, so it almost never changes. That keeps your scheduled tasks
  readable and easy to audit.
- **The skill is reusable.** The same skill can be invoked by a schedule, by a
  person on demand, or by another agent. It carries the procedure once.
- **The SOP is the ground truth, and it's diff-able.** When the underlying
  workbook or system changes, you update one document. Crucially, an SOP that
  was *verified against real artifacts* (e.g. by diffing last quarter's actual
  output) can be trusted by the agent directly instead of re-derived each run.

## Anchor to labels, not positions

The single most important instruction to put in an SOP for spreadsheet work:
**locate blocks by their labels, not by fixed row/column numbers.** Rows shift
every period as data is added. A procedure that says "the total is in row 47"
breaks the first month a row is inserted above it; one that says "find the row
labeled `Total` in column A" survives. This one habit prevents a large share of
silent automation failures.

## Write the fragilities down

Every mature process has a few load-bearing quirks that aren't obvious:

- A helper column that hard-codes a year and must be bumped when the fiscal year
  rolls over.
- A library that doesn't auto-adjust formula ranges when you insert rows, so
  every affected `SUM`/check formula must be *explicitly rewritten* to the new
  last row.
- A file format that looks like one thing and is actually another (e.g. an HTML
  table saved with a spreadsheet extension).

These belong in the SOP as named, standing warnings — "check this every run" —
not as tribal knowledge in someone's head. The agent can only be careful about
fragilities you've told it exist.

## Keep the SOP honest

An SOP is only trustworthy if it reflects reality. The highest-value SOPs are
the ones built or verified by comparing against *actual past outputs* rather than
memory. When you change the process, change the SOP in the same commit. A stale
SOP is worse than none, because the agent will follow it confidently.

## Prompt snippet

```
1. Invoke the `<process-name>` skill and follow it end to end.
2. Its detailed reference — exact tab/column mechanics, formulas, and known
   fragilities — is "<SOP filename>" in the project folder. Read that too
   before starting.
3. Locate every block by its label, not a fixed row number; rows shift each
   period. Pay active attention to the fragilities the SOP flags.
```

## Related patterns

- [Business-day gating](01-business-day-gating.md) — lives in the task layer.
- [Tie-out verification](05-tie-out-verification.md) — lives in the skill/SOP
  layers.
