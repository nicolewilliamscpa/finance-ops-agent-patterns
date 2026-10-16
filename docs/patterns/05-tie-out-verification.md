# Pattern 5 — Tie-Out Verification

**Problem.** The output of a financial process *looks* right very easily — a
workbook full of numbers is convincing whether or not it's correct. Without a
built-in check, neither the agent nor the reviewer can tell a clean close from a
subtly broken one until someone catches it downstream.

**Solution.** Bake **reconciliation checks that must equal zero** into the
deliverable itself, and make "every check is zero" a hard precondition for the
agent to declare success. The checks are part of the work product, not an
afterthought.

## What a tie-out is

A tie-out is a computed difference between two things that *must* agree, designed
so the correct answer is always `0.00`:

- Subledger total − GL balance = 0
- Beginning balance + additions − disposals − ending balance = 0
- Sum of allocated pieces − control total = 0
- Recomputed figure − source figure = 0

Because the target is always zero, a non-zero result is an unambiguous signal
that something is wrong — no judgment required to notice it.

## Design rules

**1. Make checks live, not hard-coded.** A check cell should be a formula that
recomputes from the data (`=subledger_total - gl_balance`), so it stays honest
when the data changes. A hard-coded `0` proves nothing.

**2. One check per thing that must agree.** Don't rely on a single grand-total
check — it can net to zero while two offsetting errors hide inside it. Check
each account, each month, each section that has its own control.

**3. Zero is a gate, not a goal.** This is the hinge between this pattern and
[fail-safe guardrails](02-failsafe-guardrails.md): the agent must treat a
non-zero check as a *reason to stop and report*, never as something to adjust
away. "Make it zero" is the one thing it must not do; "verify it's already zero"
is the job.

**4. Verify before declaring done.** The last step before the agent writes its
success summary is to confirm every named check equals zero (within rounding).
If any doesn't, the run is *blocked*, not *finished*, and it reports which check
failed and by how much.

## Rounding and tolerance

Decide the tolerance explicitly. Most tie-outs should be exactly zero; some carry
a sub-cent rounding tolerance (e.g. `abs(diff) < 0.01`). State which, and round
displayed figures consistently (two decimals is a sensible default for currency;
flag anything that genuinely needs more precision rather than silently changing
it). Don't let a rounding convention hide a real variance — a tolerance of "a few
cents" is fine; a tolerance of "a few dollars" is a bug smuggled in as a setting.

## Build the check list into the prompt

Name the specific checks the agent must confirm, so "verify" has a concrete
meaning:

> Before finishing, confirm: (a) the subledger-to-GL diff is 0.00 for every
> account, (b) the roll-forward check (begin + activity − end) is 0.00 for every
> month, (c) no `#REF!`/`#N/A` errors anywhere in the workbook. If any fails, do
> not deliver — report the specific cell and variance.

## Reference implementation

See [`scripts/tie_out.py`](../../scripts/tie_out.py) for a tiny,
dependency-free verification helper: define named checks as (actual, expected)
or (left, right) pairs, run them all, and get back a structured pass/fail report
with the exact variances — the shape of output an agent should produce before
claiming success.

## Related patterns

- [Fail-safe guardrails](02-failsafe-guardrails.md) — never force a check.
- [SOP-driven skills](03-sop-driven-skills.md) — where the specific checks for a
  given process are documented.
