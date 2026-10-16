# Pattern 6 — Multi-Source Briefing

**Problem.** The information a person needs to start (or end) their day is
scattered across calendar, email, chat, a task tracker, and a process schedule.
Checking all of them is a daily chore, and the useful signal is buried in noise —
newsletters, group-alias traffic, already-handled threads, the agent's own prior
messages.

**Solution.** A scheduled agent that pulls from each source, applies **explicit
relevance filters**, cross-references the sources against each other, and posts
**one** tightly formatted digest to where the person already looks (usually a
chat DM on their phone).

## The shape of a good briefing agent

**1. Read-only by default.** A briefing observes; it does not act. State this
flatly: do not send, reply to, label, or delete email; do not change calendar
events; do not edit shared files. Read, compose, post one message. This makes
the agent safe to run unattended every day.

**2. Explicit relevance filters per source.** "Everything in my inbox" is noise.
Encode what *actually* needs the person:

- **Email:** only threads they're actively part of (have sent/replied in) or that
  are addressed directly to them. Exclude group aliases and distribution lists
  unless they've already engaged. Skip newsletters and automated notices unless
  it's a system/finance alert addressed to them that needs action.
- **Chat:** mentions and DMs from the lookback window that they *haven't replied
  to yet*. Explicitly ignore the agent's own prior posts.
- **Calendar:** today's events with times and attendee counts; call out
  back-to-backs and long open blocks.
- **Schedule/tasks:** what's due today, what's overdue, what's coming in the next
  few days — with status, not just titles.

**3. Cross-reference, don't just concatenate.** The value multiplies when sources
corroborate each other. A resolved ticket means the file arrived, so say "files
received, report still to complete" — not "waiting on helpdesk." A post in the
right channel means the request went out. Always cite the *original* source and
its real timestamp, and never treat the agent's own earlier briefing as evidence
that something happened.

**4. Status must be grounded, never assumed.** Pull completion from the system of
record (the checklist, the tracker), not from vibes. A date in the "prepared"
column means done; a note like "in progress" or a dependency name does *not* mean
done. Never mark something complete without the hard evidence.

## Format for the screen it's read on

A briefing read on a phone has to be built for a narrow screen, or it's useless:

- Lead each line with the key fact (time, sender, item), then a short status.
- One idea per bullet; no nested bullets; ~60 characters per line.
- A fixed section order every day so the eye knows where to look.
- Put the most urgent item first in each section.
- If a section is empty, say so in one line rather than omitting it silently.
- Match the chat platform's actual markup (they differ — some use `*bold*`,
  others `**bold**`; the wrong one renders as literal asterisks).
- Keep the whole thing short enough to read in one glance.

## Compose once, send once

Build the complete message first, then post with exactly one send call. Before
sending, check recent history: if today's digest already went out, don't double-
post. On an unclear send result, re-read history before trying again. (This is
the [idempotency](04-idempotency-and-no-duplicate-runs.md) pattern applied to
messages.)

## Two flavors worth having

- **Morning briefing** — forward-looking: today's calendar, what needs a reply,
  what's due, a preview of tomorrow.
- **End-of-day reminder** — a tighter "what's due today and still open" nudge
  that catches anything before it slips.

Same machinery, different lookback and framing.

## Related patterns

- [Idempotency & no-duplicate runs](04-idempotency-and-no-duplicate-runs.md) —
  one-message-per-day discipline.
- [Fail-safe guardrails](02-failsafe-guardrails.md) — read-only is a guardrail.
