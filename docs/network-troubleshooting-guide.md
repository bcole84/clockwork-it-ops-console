# Network Troubleshooting Guide (macOS)

**Audience:** IT Operations
**Applies to:** Office Wi-Fi/wired connectivity issues and remote employee connectivity support
**Owner:** IT Operations Specialist

## First questions to ask

1. Wired or Wi-Fi? Office or remote?
2. Is it just this person, a section of the office, or everyone?
3. Did anything change recently (moved desks, new device, router/AP reboot, ISP maintenance window)?

## Quick checks on the user's Mac

- **Wi-Fi status:** hold Option and click the Wi-Fi icon in the menu bar for signal strength, channel, and PHY mode without opening System Settings.
- **Confirm the right network:** System Settings → Wi-Fi — check for a similarly-named rogue/guest SSID the device may have auto-joined.
- **Renew DHCP lease:** System Settings → Network → Wi-Fi → Details → TCP/IP → Renew DHCP Lease.
- **Flush DNS cache:** `sudo dscacheutil -flushcache; sudo killall -HUP mDNSResponder`
- **Basic reachability test:** `ping -c 5 8.8.8.8` (tests raw connectivity) vs `ping -c 5 google.com` (tests DNS resolution) — if the IP ping works but the hostname ping doesn't, it's a DNS problem, not a connectivity problem.
- **Check for a stuck VPN/proxy config:** System Settings → Network → VPN, and check `networksetup -getwebproxy Wi-Fi` for an unexpected proxy.
- **Forget and rejoin the network:** System Settings → Wi-Fi → Details (i) → Forget This Network, then rejoin — clears a corrupted stored network profile.

## Office network checks

1. Check the access point / switch dashboard for the affected area — look for a flapping or offline AP.
2. Confirm the uplink to the ISP modem/router is up before assuming an internal issue.
3. If a specific AP is overloaded (many devices, one AP), that shows up as slow-but-connected rather than fully down — consider load or channel congestion, not just an outage.
4. Reboot the specific AP/switch first before rebooting the whole stack — narrows the blast radius and downtime.

## Remote employee checks

1. Have them run a speed test and share results (rules out "my internet is just slow").
2. Confirm they can reach the general internet but not just internal tools — that isolates whether it's their ISP or a company-side (VPN, SSO, specific SaaS outage) issue.
3. If VPN is required for a specific tool, confirm the VPN client is actually connected, not just installed.

## When to escalate to the ISP or a vendor

- Office-wide outage that a modem/router power cycle doesn't resolve within 10-15 minutes.
- Consistent packet loss or high latency reproducible from multiple devices/locations.
- Always log the ISP case number on the related ticket so downtime and resolution are tracked.

## After resolving

Log what the actual root cause was on the ticket. If it's a recurring pattern (same AP, same time of day, same remote employee's ISP), note it — a pattern worth watching is worth writing down once rather than re-diagnosing from scratch next time.
