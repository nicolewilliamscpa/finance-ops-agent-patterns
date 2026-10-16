# Template — Monthly Append / Roll-Forward Update

For a workbook that grows each period by appending the new period's rows and
extending its formulas (subscription roll-forwards, schedules, registers).
The append shape makes duplicate rows the main risk, so idempotency is central.
Implements patterns 1 (gating), 2 (guardrails), 4 (idempotency), 5 (tie-outs).

---

```
You are running the periodic update of {{ORG}}'s "{{WORKBOOK}}" roll-forward.
This affects {{WHAT_IT_AFFECTS}} (e.g. revenue recognition) — be precise and do
not guess past what's specified. If something doesn't match the description
below, STOP before making changes and flag it rather than proceeding.

STEP 1 — TARGET PERIOD
Target period = {{PERIOD_RULE}} (e.g. the calendar month immediately before this
run's current month).

STEP 2 — FIND THE SOURCE FILE
In {{INPUT_FOLDER}}, find the source file for the target period following the
naming pattern "{{SOURCE_PATTERN}}". If it doesn't exist, STOP and report that
the source for that period wasn't found — do not substitute a different period.

STEP 3 — FIND THE CURRENT WORKBOOK (and duplicate/gap check)
In {{OUTPUT_FOLDER}}, find the most recently modified "{{WORKBOOK_PATTERN}}"
(exclude any test/scratch copies). Then:
- Confirm it does NOT already include the target period (check the last populated
  period column/row). If it already does, STOP — possible duplicate run.
- If it is more than one period behind the target, STOP and report the gap
  instead of catching up multiple periods silently.

STEP 4 — MAP AND APPEND
Per the mapping in {{SOP_FILE}}: filter the source to the rows in scope, map each
field to its destination column, and append new rows under the correct section —
copying formula/value patterns from the preceding row so the pattern stays
consistent. Do NOT touch rows/sections outside the mapping. Preserve all existing
formatting and formulas elsewhere exactly.

STEP 5 — EXTEND FORMULAS EXPLICITLY
Update every total / ending-balance / summary / check formula so its range
includes the newly added rows. Do NOT rely on auto-adjustment — rewrite the
ranges to the new last row explicitly (this is a known fragility of row
insertion in most libraries).

STEP 6 — TIE-OUT CHECK (before finalizing)
Compare the total of new rows against the corresponding source summary for the
target period, and confirm each new row's check column nets to zero:
{{CHECKS}}
If anything doesn't tie, report the discrepancy clearly rather than forcing it.

STEP 7 — SAVE AS A NEW FILE
Save as a NEW period-stamped file in {{OUTPUT_FOLDER}} ("{{OUTPUT_PATTERN}}").
Never overwrite the file you started from.

STEP 8 — FLAG MANUAL STEPS
Leave {{MANUAL_STEPS}} (e.g. posting JEs, entering the GL balance from the source
system) for {{OWNER}}; leave those cells blank and call them out — do not attempt
them.

STEP 9 — SUMMARIZE
Rows added per section with counts and amounts, the tie-out result, the new
filename, and the flagged manual steps. Round currency to 2 decimals unless a
figure needs more precision.
```

---

**Fill-in checklist:** `{{ORG}}`, `{{WORKBOOK}}`, `{{WHAT_IT_AFFECTS}}`,
`{{PERIOD_RULE}}`, `{{INPUT_FOLDER}}`, `{{OUTPUT_FOLDER}}`, `{{SOURCE_PATTERN}}`,
`{{WORKBOOK_PATTERN}}`, `{{SOP_FILE}}`, `{{CHECKS}}`, `{{OUTPUT_PATTERN}}`,
`{{MANUAL_STEPS}}`, `{{OWNER}}`.
