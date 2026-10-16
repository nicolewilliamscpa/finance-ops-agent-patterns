# Pattern 2 — Fail-Safe Guardrails

**Problem.** An unattended agent that runs real financial or operational work has
no human watching the moment it executes. The dangerous failure mode is not
"the agent errors out" — it's "the agent fills a gap with a plausible guess and
produces a confident, wrong deliverable." In accounting that means a workpaper
that ties out to fabricated numbers; in ops it means a report built on data that
never arrived.

**Solution.** Make the agent *refuse to proceed past uncertainty* and hand
control back, instead of improvising. A good unattended task is biased heavily
toward **stopping cleanly** over **finishing wrongly**.

## The core rules

**1. Stop, don't fabricate.** If a required input is missing, late, partial, or
doesn't look like what was expected, the agent must not invent, estimate, or
"fill in" the data. It stops and reports exactly what's missing and where it
looked.

> Do not guess or partially build. If any required input is not available,
> notify the owner listing exactly which inputs are missing, then stop.

**2. Never force a check to pass.** If a tie-out, reconciliation, or validation
doesn't balance, that is a *finding*, not an obstacle. The agent must never
nudge a figure, widen a tolerance, or hard-code a plug to make the check read
zero. It reports the specific discrepancy and stops.

> If the tie-outs don't match, report the discrepancy clearly rather than
> silently forcing a match.

**3. Partial input is not a green light.** Three of five files is "not ready,"
not "start on what's here." Building a partial deliverable as if it were final
is worse than building nothing, because it looks done. Treat partial as
not-ready, note what's missing, and re-check on the next run.

**4. Name the blocker precisely.** "Couldn't finish" is useless to the person
who has to unblock it. "The GL export is present but only covers the cost
accounts, not accumulated depreciation — re-export both and drop it in the
folder" is actionable. Always say *what's done, what's blocking, and what the
owner needs to do*.

**5. Keep manual steps manual.** Some actions should never be automated even
when the agent technically could — posting journal entries to the ledger,
sending external communications, anything irreversible or requiring sign-off.
Mark these explicitly as out of scope and leave them for a human.

> Do NOT post journal entries. Drafting them for review is in scope; posting
> stays a manual step for the preparer.

## Why this beats "try harder"

An agent optimizing to *complete the task* will, under pressure, do whatever
makes the task look complete — including papering over the exact problems you
most need to see. An agent optimizing to *either produce a correct deliverable
or a precise blocker* is one you can actually leave unattended, because its two
possible outcomes are both safe: right, or honestly stopped.

## Make the safe path the easy path

Write the prompt so stopping is low-friction and well-defined. Give the agent:

- A clear list of required inputs and how to recognize each one.
- An explicit "if missing → message X, then stop" instruction per input.
- The named checks that must equal zero before it's allowed to finish.
- A short, structured summary format for both success and blocked outcomes, so a
  stopped run is just as legible as a finished one.

## Prompt snippet

```
Guardrails:
- If any required input is missing/partial/unexpected: do not fabricate or
  estimate. List exactly what's missing and stop.
- If any tie-out/check does not equal zero: do not force it. Report the
  specific variance and stop.
- Never post to the ledger / send externally / take irreversible actions —
  draft for review only.
- Always finish with: what's done, what's blocking (if anything), and what the
  owner must do to unblock.
```

## Related patterns

- [Tie-out verification](05-tie-out-verification.md) — the checks that rule 2
  protects.
- [Idempotency & no-duplicate runs](04-idempotency-and-no-duplicate-runs.md).
