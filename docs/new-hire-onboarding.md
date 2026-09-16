# New Hire Onboarding Playbook

**Audience:** IT Operations
**Applies to:** All new employees and contractors (in-person or remote)
**Owner:** IT Operations Specialist

## Before Day 1 (T-3 business days)

1. Confirm start date, role, manager, and work location (in-office / remote / hybrid) with People Ops.
2. Create the employee record in the Asset & Onboarding console and instantiate the **Standard New Hire** checklist.
3. Order or pull a MacBook from stock (see [MDM Laptop Deployment](mdm-laptop-deployment.md) for model/spec guidance).
4. Pre-stage the device in **Mosyle** so it auto-enrolls on first boot (zero-touch / Automated Device Enrollment).
5. Create accounts:
   - SSO / identity provider account
   - Google Workspace or Microsoft 365 mailbox
   - Slack
   - Atlassian (Jira + Confluence + Bitbucket, scoped to the correct projects)
   - 1Password vault access (team vault relevant to their role)
6. Ship the device (remote hires) or stage it at the hire's desk (in-office hires).

## Day 1

1. Welcome message in the team Slack channel.
2. Walk the new hire through first boot: Mosyle enrollment profile, FileVault disk encryption confirmation, sign-in to SSO.
3. Confirm access to: email, Slack, Jira/Confluence/Bitbucket, 1Password.
4. Point them to this Knowledge Base and the IT support ticket process.
5. Set a 30-minute IT check-in for end of day 1 or start of day 2 to catch any access gaps.

## Week 1

1. Confirm the new hire can reach internal tools from both office Wi-Fi and remote/VPN (if applicable).
2. Verify MDM compliance status shows green (encryption on, OS up to date, agent checked in within 24h).
3. Close out the onboarding checklist in the console once every item is checked off.
4. Update the asset record to reflect the device is now **In Use**, assigned to the new hire.

## Standard New Hire Checklist (mirrors the in-app template)

- [ ] Mosyle enrollment complete
- [ ] SSO / identity account created
- [ ] Email / calendar provisioned
- [ ] Slack account created and added to team channels
- [ ] Jira / Confluence / Bitbucket access granted
- [ ] 1Password vault access granted
- [ ] Laptop shipped or handed off
- [ ] Day-1 IT check-in completed
- [ ] Asset record updated to "In Use"

## Notes

- Contractors follow the same flow but get a time-boxed offboarding date set in advance and a restricted 1Password vault.
- If a device isn't available in stock, flag procurement lead time to the hiring manager as soon as the req is approved — don't wait until T-3.
