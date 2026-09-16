# Ticket Triage SOP

**Audience:** IT Operations
**Applies to:** All incoming IT support tickets
**Owner:** IT Operations Specialist

## Priority definitions

| Priority | Definition | Target first response | Target resolution |
|---|---|---|---|
| Critical | Company-wide outage or security incident (e.g. office network down, all-hands tool inaccessible) | 15 minutes | Same business day |
| High | Single employee fully blocked from working (device won't boot, no network access, locked out of SSO) | 1 hour | Same business day |
| Medium | Degraded but workable (slow Wi-Fi, one app misbehaving, non-blocking hardware issue) | 4 business hours | 2 business days |
| Low | Requests, questions, non-urgent access changes | 1 business day | 5 business days |

## Triage steps (for every new ticket)

1. Read the ticket; if the category/priority the requester picked looks wrong, correct it.
2. Check whether this is a known, already-in-progress issue (e.g. an ongoing outage) — if so, link it and notify the requester rather than duplicating work.
3. Set status to **In Progress** once you start working it; leave as **New** only while it's in the queue.
4. If you need info from the requester, set status to **Waiting** and note exactly what you're waiting on.
5. Resolve and set status to **Resolved** with a one-line summary of the fix — this becomes searchable history for the next similar ticket.

## Common categories and first moves

- **Account / access** (locked out, needs new permission): verify identity first, then check SSO/1Password/Atlassian admin console for the actual state before making changes.
- **Hardware**: check the asset record for warranty/AppleCare status and device age before deciding repair vs. replace.
- **Network**: see the [Network Troubleshooting Guide](network-troubleshooting-guide.md).
- **Software**: confirm whether it's a single user or spreading — a spike in the same software complaint across multiple tickets usually means a vendor-side incident, not N separate local issues.

## Escalation

- Anything Critical, or anything touching security/data exposure, gets flagged to IT leadership immediately regardless of time of day.
- If a fix requires a vendor (Apple, Atlassian, ISP), open the vendor case and note the case number on the ticket so anyone can pick it up.

## Closing the loop

Every resolved ticket should leave a trail someone else could follow. If you solved something non-obvious, add or update a Knowledge Base playbook rather than only closing the ticket — that's the difference between fixing it once and fixing it every time.
