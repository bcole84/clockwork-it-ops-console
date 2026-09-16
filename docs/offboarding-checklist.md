# Offboarding Checklist

**Audience:** IT Operations
**Applies to:** Any departing employee or contractor
**Owner:** IT Operations Specialist

## As soon as the departure date is known

1. Instantiate the **Standard Offboarding** checklist in the console with the last day of work.
2. Confirm the exact time access should be cut with the manager and People Ops (immediate vs. end-of-day).
3. Note whether the device ships back or is collected in person.

## On the last day (or the agreed cutoff time)

1. Disable SSO / identity provider account (this cascades to most downstream SaaS access).
2. Remove from Slack; export/transfer ownership of any channels they solely own.
3. Revoke Atlassian access (Jira, Confluence, Bitbucket) — reassign any Bitbucket repo admin rights first.
4. Revoke 1Password vault access; rotate any shared credentials they had standing access to.
5. Set up email auto-reply / forwarding per manager's instructions, then suspend the mailbox.
6. Remote-lock or remote-wipe the device via Mosyle if it isn't being returned same-day.

## Device return

1. Provide a prepaid shipping label (remote) or collect the device directly (in-office).
2. On receipt: wipe via Mosyle (or Erase All Content and Settings if Mosyle wipe isn't confirmed), remove from MDM enrollment, then re-image for the next hire.
3. Update the asset record: status → **In Repair** (pending wipe) → **In Stock** once wiped and verified clean.
4. Inspect for physical damage; log any issues on the asset record.

## Standard Offboarding Checklist (mirrors the in-app template)

- [ ] SSO / identity account disabled
- [ ] Slack account removed
- [ ] Atlassian access revoked
- [ ] 1Password vault access revoked
- [ ] Email suspended / forwarded per manager
- [ ] Device remote-locked (if not same-day return)
- [ ] Device returned and inspected
- [ ] Device wiped via Mosyle and re-enrolled as spare
- [ ] Asset record updated to "In Stock" or "Retired"

## Notes

- For involuntary departures, coordinate timing tightly with People Ops/legal — access should be cut at or before the notification meeting, not after.
- Retired devices older than the refresh cycle should be marked **Retired** rather than returned to stock, and queued for secure data wipe + recycling/donation per the asset disposal policy.
