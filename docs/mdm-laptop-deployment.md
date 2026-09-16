# MDM Laptop Deployment (Mosyle)

**Audience:** IT Operations
**Applies to:** All company-owned Mac laptops
**Owner:** IT Operations Specialist

## Standard hardware

- **Default:** MacBook Air (M-series), 16GB unified memory, 512GB storage — covers the large majority of roles.
- **Upgrade to MacBook Pro** for engineering, design, video, or other compute/graphics-heavy roles.
- Keep 3-5 units of current-generation stock on hand for new-hire lead time.

## Zero-touch enrollment flow

1. Record the device serial number in the asset console the moment it's received (status: **In Stock**).
2. Add the serial to Apple Business Manager (ABM) and assign it to the Mosyle MDM server, if not already synced automatically.
3. In Mosyle, confirm the device is assigned the correct enrollment profile (standard employee vs. contractor vs. shared/kiosk).
4. When the device ships or is handed to the new hire, update the asset record to **In Use** and link it to the employee.
5. On first boot, the employee signs in with their Apple ID (or skips, per policy) and the Mosyle profile installs automatically — no manual IT touch required for a properly ABM-enrolled device.

## Baseline configuration pushed via Mosyle

- FileVault disk encryption enforced, recovery key escrowed
- Automatic OS updates within a defined grace window
- Required apps: Slack, 1Password, Google Chrome, Zoom/Teams, the standard EDR/security agent
- Gatekeeper and firewall enabled by default
- Passcode/password complexity policy enforced
- Screen lock timeout enforced

## Troubleshooting enrollment issues

- **Device doesn't pick up the MDM profile on first boot:** confirm it's actually present in ABM and correctly assigned to the Mosyle server (a device bought outside the organization's Apple Business Manager account won't auto-enroll).
- **Profile installs but required apps don't push:** check the device's Mosyle compliance/last-check-in timestamp — it needs an internet connection and to check in at least once before policies fully apply.
- **User can't complete FileVault enrollment:** confirm they're logged in with a local admin or standard account that has escrow permissions; retry after a reboot.

## Retiring a device

See [Offboarding Checklist](offboarding-checklist.md) for the wipe/re-enroll/inspect flow. Devices older than the refresh cycle (typically 3-4 years) should be marked **Retired**, removed from Mosyle and ABM, and queued for secure wipe and recycling/donation.
