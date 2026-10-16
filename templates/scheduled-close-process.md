# Template — Scheduled Close / Workpaper Process

A full period-end deliverable built from inputs, run unattended on a target
business day. Implements patterns 1 (gating), 2 (guardrails), 3 (SOP-driven),
4 (idempotency), and 5 (tie-out verification).

Schedule it to fire daily across `{{WINDOW}}` so it always catches `{{BD_N}}`.

---

```
You are running {{ORG}}'s {{PROCESS_NAME}} for the period that just closed.
This is a fresh session with no memory of prior runs — start from scratch and
rely only on durable state (the files, the workbook, the checklist).

STEP 0 — BUSINESS-DAY GATE (do this before anything else)
Determine today's date in {{TIMEZONE}}. Compute the {{BD_N}}th business day of
the current month (Mon–Fri counted from the 1st; skip weekends; {{HOLIDAY_RULE}}).
If today is NOT that date, stop immediately — do not open any files, message
anyone, or produce output. Just end. Only if today IS BD{{BD_N}}, continue.

STEP 1 — SCOPE
The period being processed is {{PERIOD_RULE}} (e.g. the calendar quarter that
just closed; the prior calendar month). All of that period's activity should be
final in the source system by now.

STEP 2 — DUPLICATE / GAP CHECK
- If this period's deliverable already exists in {{OUTPUT_FOLDER}} (the output
  file for this period is present, or the workbook already includes this period),
  stop and report "already completed" — do not re-do it.
- If the last completed period is more than one period behind this one, stop and
  report the gap rather than catching up silently.

STEP 3 — GATHER INPUTS
Work in {{INPUT_FOLDER}}. Required inputs:
{{INPUTS}}
If any required input is missing, partial, or doesn't look like what's expected,
do NOT guess, estimate, or partially build. Notify {{OWNER}} listing exactly
which inputs are missing and what you found, then stop.

STEP 4 — RUN THE PROCESS
1. Invoke the `{{PROCESS_NAME}}` skill and follow it end to end.
2. Read its detailed reference "{{SOP_FILE}}" in {{INPUT_FOLDER}} before starting.
3. Locate every block by its label, not a fixed row number — rows shift each
   period. Pay active attention to the fragilities the SOP flags (year-hardcoded
   helper columns, formula ranges that must be explicitly rewritten when rows are
   inserted, etc.).

STEP 5 — VERIFY (hard precondition for success)
Before declaring done, confirm every one of these equals zero (within rounding):
{{CHECKS}}
Also confirm there are no #REF!/#N/A errors anywhere in the output. If any check
fails, do NOT force it to zero — stop and report the specific cell and variance.

STEP 6 — SAVE (never overwrite the source)
Save the result as a NEW period-stamped file in {{OUTPUT_FOLDER}}
(e.g. "{{OUTPUT_NAME_PATTERN}}"). Do not overwrite the file you started from.

STEP 7 — MANUAL STEPS STAY MANUAL
Do NOT {{MANUAL_STEPS}} (e.g. post journal entries, send externally). Draft/flag
these for {{OWNER}} to do; never take the irreversible action yourself.

STEP 8 — SUMMARIZE
Finish with a short, structured summary: which period was processed, the result
of each tie-out (call out any variance and likely cause), the exact output
filename(s), and anything needing {{OWNER}}'s manual follow-up. If you were
blocked, say clearly what's done, what's blocking, and what {{OWNER}} must do to
unblock it. Round currency to 2 decimals unless a figure genuinely needs more
precision (flag it if so).
```

---

**Fill-in checklist:** `{{ORG}}`, `{{PROCESS_NAME}}`, `{{WINDOW}}`, `{{BD_N}}`,
`{{TIMEZONE}}`, `{{HOLIDAY_RULE}}`, `{{PERIOD_RULE}}`, `{{INPUT_FOLDER}}`,
`{{OUTPUT_FOLDER}}`, `{{INPUTS}}`, `{{SOP_FILE}}`, `{{CHECKS}}`,
`{{OUTPUT_NAME_PATTERN}}`, `{{MANUAL_STEPS}}`, `{{OWNER}}`.
