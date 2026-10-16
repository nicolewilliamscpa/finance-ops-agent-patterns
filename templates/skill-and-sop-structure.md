# Template — Skill + SOP Structure

The [SOP-driven skills pattern](../docs/patterns/03-sop-driven-skills.md) splits
a process into three layers. The scheduled-task prompt (the other templates in
this folder) is the top layer. This file gives a starting shape for the lower
two: the **skill** (the recipe) and the **SOP** (the ground truth).

---

## Skill — `{{PROCESS_NAME}}` (the recipe)

A skill is a reusable procedure an agent can invoke from a schedule, on demand,
or from another agent. Keep it to the ordered steps and what "done" means; push
cell-level mechanics down into the SOP.

```markdown
---
name: {{process-name}}
description: >
  Run {{ORG}}'s {{PROCESS_NAME}} for a given period — {{ONE_LINE_WHAT}}.
  Use when {{WHEN_TO_USE}}. The deliverable is {{DELIVERABLE}}; {{MANUAL_STEPS}}
  stay manual.
---

# {{PROCESS_NAME}}

## Inputs
{{INPUTS}}  (and how to recognize each)

## Procedure
1. Confirm scope (which period) and that inputs are complete; if not, stop and
   report what's missing (see guardrails).
2. {{STEP}} …
3. {{STEP}} …
   - Locate blocks by label, not fixed row number.
   - Watch the fragilities listed in the SOP.
4. Build the deliverable.

## Verification (must pass before declaring done)
Confirm each of these equals zero (within rounding); if any fails, stop and
report the cell + variance, never force it:
{{CHECKS}}
No #REF!/#N/A anywhere in the output.

## Output
Save as a new period-stamped file: "{{OUTPUT_PATTERN}}". Never overwrite the
source. Leave {{MANUAL_STEPS}} for a human.

## Reference
Full mechanics and known fragilities: {{SOP_FILE}}.
```

---

## SOP — `{{SOP_FILE}}` (the ground truth)

The deep document. This is where cell-level detail and hard-won lessons live.
Update it in the same change as any process change.

```markdown
# SOP — {{PROCESS_NAME}}

## Purpose & cadence
What this produces, for whom, and when ({{BD_N}}/period).

## Source of truth
This SOP was verified by {{HOW_VERIFIED}} (e.g. diffing the actual Q1 and Q2
workbooks), so its formulas and mechanics can be trusted directly — not
re-derived each run.

## Tab-by-tab / section-by-section mechanics
For each tab/section: what it contains, the exact columns, the formulas and
their patterns, and how new rows are added.

## Known fragilities (check every run)
- {{FRAGILITY}} — e.g. helper columns Z/AB hard-code the year; bump them when the
  fiscal year rolls over.
- {{FRAGILITY}} — the library does not auto-rewrite formula ranges when rows are
  inserted; every affected SUM/check/diff formula must be explicitly rewritten to
  the new last row.
- {{FRAGILITY}} — the raw export looks like one format but is actually another.

## Tie-outs
The named checks that must equal zero, and where each lives.

## Change log
Date — what changed in the process and in this SOP.
```

---

**Why keep them separate from the task prompt:** the task prompt is about *when
and whether to run* and changes almost never; the skill is the reusable *how*;
the SOP is the deep *exactly how* that changes when the workbook does. Three
layers, three rates of change, one source of truth each.

**Fill-in checklist:** `{{PROCESS_NAME}}`, `{{ORG}}`, `{{ONE_LINE_WHAT}}`,
`{{WHEN_TO_USE}}`, `{{DELIVERABLE}}`, `{{INPUTS}}`, `{{CHECKS}}`,
`{{OUTPUT_PATTERN}}`, `{{MANUAL_STEPS}}`, `{{SOP_FILE}}`, `{{BD_N}}`,
`{{HOW_VERIFIED}}`.
