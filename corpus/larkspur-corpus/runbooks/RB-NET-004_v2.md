---
doc_id: RB-NET-004
title: Firewall WAN failover check
doc_type: runbook
version: "2"
effective_date: 2024-06-17
owner: Tom Kessler
audience: internal
---

# RB-NET-004 Firewall WAN failover check

## Purpose / When to use

Use when:
- Beacon RMM or FortiGate alerts that a client firewall has **failed over** to its backup WAN (second ISP or LTE), or a WAN member's SLA has failed.
- During an internet outage (RB-NET-001), to confirm whether the site is running on backup.
- For the **quarterly WAN failover test** for clients with a backup WAN (every quarter, during an agreed maintenance window, with authorized contact approval).
- After an ISP modem or gateway swap, or any circuit change, on either WAN link.

Applies to Fortinet FortiGate firewalls configured with SD-WAN. Clients without a backup WAN skip this runbook.

## Prerequisites / access needed

- FortiCloud or FortiGate GUI/SSH (LockBox Vault). Tier 2 read-only; Tier 3 for changes and tests.
- Client Atlas Docs network page: WAN members (wan1 primary, wan2 or LTE backup), ISP contacts, performance SLA targets, which traffic is pinned to which link
- Beacon RMM network device monitoring

## Steps

### 1. Check current WAN state

1. GUI: **Network > SD-WAN**. The **SD-WAN Zones** tab shows member status and bandwidth; the **Performance SLAs** tab shows each member's latency, jitter, and packet loss against the probe targets and whether it is alive.
2. CLI:
   ```
   diagnose sys sdwan health-check
   diagnose sys sdwan member
   diagnose sys sdwan service
   get router info routing-table all
   ```
   - `health-check` shows each member alive/dead with latency, jitter, loss.
   - `routing-table all` shows which default route is active.
3. **Event log:** Log & Report > System Events > SD-WAN events. Note when the primary went dead and whether it has flapped (up/down repeatedly).
4. **Confirm the secondary WAN addressing still matches the ISP.** Compare the wan2/LTE interface settings (Network > Interfaces > wan2: addressing mode, IP/netmask, and the gateway in the SD-WAN member or static route) with what the backup ISP currently provides, as recorded on the client's Atlas Docs network page. ISPs change handoff details after a modem or gateway swap, a circuit move, or a plan change, and a backup link with a stale static IP or gateway will show "alive" on the interface but fail the health check, or fail the moment it is needed.
   ```
   get system interface physical wan2
   show system interface wan2
   show system sdwan
   execute ping-options source <wan2 IP>
   execute ping <wan2 gateway>
   ```
   If anything differs, Tier 3 updates the FortiGate and the Atlas Docs page. Ask the ISP to confirm the values if unsure.

### 2. If the site is on backup

5. Confirm users are working: ask the site contact; check Beacon agents are online.
6. Expect side effects of the backup link:
   - **Public IP changed**: scan-to-email via connector breaks (RB-PRT-002), IP-allowlisted vendor portals may block the client, inbound services (VPN on the primary IP) may not work.
   - **LTE backup**: limited bandwidth and possibly a data cap. Ask the site to pause large uploads and video calls where possible.
   - VoIP phones may need to re-register (RB-VOIP-001).
7. Open or update a ticket for the primary circuit and call the ISP (RB-NET-001, "Call the ISP").
8. When the primary returns, SD-WAN fails back automatically once the health check passes (per the configured fail-recovery threshold). Confirm in the SD-WAN view that traffic moved back and the backup is idle.

### 3. Primary is flapping

9. If the primary goes up and down repeatedly, users see drops every few minutes. Tier 3 may temporarily set the primary to standby (disable it in SD-WAN, or raise its priority/cost) so the site stays on backup while the ISP fixes the line. Note the change in the ticket and set a follow-up to revert.

### 4. Scheduled failover test (Tier 3)

10. Schedule with the authorized contact through Isaac Brennan or the vCIO calendar. Tests run after hours or at a low-traffic time the client picks.
11. Before: record current health-check output and active routes. Run the secondary WAN addressing check (step 4) first. Confirm someone on site (or a Beacon agent) can verify connectivity.
12. Simulate failure: administratively bring down wan1 (`config system interface`, `edit wan1`, `set status down`, `end`) or unplug the primary handoff with the site contact. Do not remove SD-WAN members.
13. Verify: backup member becomes active within the expected time (normally under 1 minute), browsing works, Beacon agents stay online, VoIP re-registers.
14. Restore wan1 (`set status up`), verify failback.
15. Record results in the ticket and in the client's Atlas Docs network page (test date, failover time, issues found). Jordan Pike includes failover test results in business reviews.

## Priority guidance

- Site failed over and working on backup: **P2** (key function degraded), until the primary is restored.
- Both WAN links down: **P1**, go to RB-NET-001.
- Backup link down while primary is fine (LTE modem offline, SLA failing on wan2): **P3**; the site has no redundancy until fixed.
- Scheduled failover test: **P4** scheduled change.

## Escalate if

- SD-WAN rules or health-check settings need changes: Tom Kessler.
- Failover did not happen when the primary died: Tom Kessler (configuration problem, P1 if site is down).
- LTE backup data cap is near its limit: account manager to talk with the client.
- ISP repeat outages (three or more in 30 days): Tom Kessler and the account manager; may lead to a circuit change recommendation by Jordan Pike.

## Ticket notes

- Time of failover and failback (from event log)
- Health-check output summary (latency/loss per member)
- Side effects observed and fixed (scan-to-email, VoIP, VPN)
- ISP ticket number
- For tests: approver, window, failover time, result

## Revision history

| Version | Date | Author | Change |
|---|---|---|---|
| 1 | 2021-02-22 | Tom Kessler | Initial WAN failover check. |
| 2 | 2024-06-17 | Tom Kessler | Updated for FortiOS SD-WAN GUI and CLI, added quarterly test procedure, secondary WAN addressing check (after an ISP modem swap left a backup link misconfigured), and side-effects checklist. |
