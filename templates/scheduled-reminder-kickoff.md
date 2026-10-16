# Template — Scheduled Reminder / Kickoff

For a process that can't run fully unattended because it needs a human to attach
inputs first. The task fires on the target business day, confirms it's the right
day, asks the owner for the specific inputs, and then *stops and waits* rather
than fabricating anything. Implements patterns 1 (gating) and 2 (guardrails).

Schedule it to fire daily across `{{WINDOW}}` so it always catches `{{BD_N}}`.

---

```
This is the kickoff for {{ORG}}'s {{PROCESS_NAME}}, for {{OWNER}}.

STEP 0 — BUSINESS-DAY GATE
This task fires daily across {{WINDOW}} so it can land on BD{{BD_N}}. Determine
today's date in {{TIMEZONE}} and compute the {{BD_N}}th business day of the month
(Mon–Fri from the 1st; skip weekends; {{HOLIDAY_RULE}}). If today is NOT that
date, do nothing further and end — do not message anyone, do not proceed.

IF TODAY IS BD{{BD_N}}:
1. If the `{{PROCESS_NAME}}` skill is available, load it and follow it. Otherwise
   consult {{SOP_FILE}} for the process, format, and conventions.
2. This session starts fresh with no files attached. Do NOT guess at data or
   fabricate a deliverable. Message {{OWNER}} explaining it's time for this
   period's {{PROCESS_NAME}}, and ask them to attach:
{{INPUTS}}
3. Stop and wait — do not attempt to build anything until those inputs are
   provided in this conversation. When they arrive, run the process per the
   skill/SOP, verify the tie-outs, and deliver.
```

---

**When to use this instead of the full close template:** when the inputs live
somewhere the agent can't reliably reach on its own (a system it isn't connected
to, a manual export), so a human has to hand them over. The kickoff makes the
hand-off punctual and specific instead of relying on memory.

**Fill-in checklist:** `{{ORG}}`, `{{PROCESS_NAME}}`, `{{OWNER}}`, `{{WINDOW}}`,
`{{BD_N}}`, `{{TIMEZONE}}`, `{{HOLIDAY_RULE}}`, `{{SOP_FILE}}`, `{{INPUTS}}`.
