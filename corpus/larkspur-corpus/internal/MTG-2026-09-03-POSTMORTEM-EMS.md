---
doc_id: MTG-2026-09-03-POSTMORTEM-EMS
title: Post-Mortem - P1 Internet Outage at Emberline Metalworks (2026-09-01)
doc_type: meeting_notes
version: "1"
effective_date: 2026-09-03
owner: Marcus Oyelaran
audience: internal
---

# Post-Mortem: P1 Internet Outage at Emberline Metalworks (EMS)

**Incident date:** Tuesday, September 1, 2026
**Post-mortem meeting:** Thursday, September 3, 2026, 2:00 - 3:00 PM CT, conference room + Teams
**Facilitator:** Marcus Oyelaran
**Notes:** Priya Raman
**Attendees:** Marcus Oyelaran, Priya Raman, Tom Kessler, Andre Mitchell, Brian Novak, Jordan Pike, Isaac Brennan
**Ticket:** TCK-118742 (P1, category Network - Internet Outage)
**Client:** Emberline Metalworks (EMS), Lenexa, KS - Professional tier, 88 users
**Runbooks involved:** RB-NET-001 (Internet outage triage), RB-NET-004 (Firewall WAN failover check), RB-GEN-002 (After-hours on-call and escalation)

This is a blameless review. The goal is to fix the system, not find someone to blame.

## 1. Summary

At about 5:35 AM CT on Tuesday 9/1, a road construction crew cut the fiber line serving Emberline's building. EMS has a secondary cable internet connection configured for automatic failover on their FortiGate firewall (asset LR-EMS-0007). **Failover did not work.** The secondary WAN link was physically up, but its gateway setting was wrong after the cable provider swapped the modem in late July, so the FortiGate health check on that link had been failing for about five weeks without anyone noticing.

The whole site was offline: shop floor terminals, the cloud ERP, Microsoft 365, and Yealink phones. First shift starts at 6:00 AM. Service was restored over the secondary link at **7:21 AM** after Tom corrected the configuration onsite. The fiber was repaired and the primary link came back at **12:04 PM**.

- **P1 response SLA (Professional, 30 minutes, 24x7): met.** First human response at 5:58 AM, 17 minutes after the ticket was created.
- **P1 resolution target (4 hours): met.** Service restored 1 hour 40 minutes after ticket creation.
- **SLA credit:** none owed.
- **Client impact:** roughly 80 minutes of lost production time on first shift; about 60 of EMS's 88 users were on site during the outage. Phones down until about 7:45 AM.

## 2. Timeline (all times CT, Tuesday 2026-09-01)

| Time | Event |
|---|---|
| ~5:35 AM | Fiber cut by construction crew on the road east of EMS (per ISP, confirmed later). |
| 5:38 AM | EMS FortiGate primary WAN (wan1) goes down. SD-WAN tries to move traffic to wan2 (cable). wan2 health check fails, so no traffic passes. Site is fully offline. |
| 5:41 AM | Beacon RMM raises "EMS-FW01 offline" (no check-in from the firewall). Critical alert pages through PagerLine. Harbor auto-creates **TCK-118742**, After-Hours source flag set. |
| 5:47 AM | Andre Mitchell (on-call engineer, week of 8/31) acknowledges the page. |
| 5:52 AM | EMS plant supervisor calls PagerLine: "Nothing on the floor can reach the ERP and phones are dead." PagerLine adds caller info to the page. |
| 5:58 AM | Andre calls the supervisor back. **First human response (17 minutes).** Andre confirms site-wide impact, sets **P1**. Starts RB-NET-001. |
| 6:03 AM | Andre checks ISP status page: outage reported in the area. Opens ISP ticket by phone. ISP says a crew is being dispatched, no ETR. |
| 6:05 - 6:20 AM | Andre waits on ISP hold for an estimated time to repair and tries to reach the FortiGate remotely through both WAN IPs. No response on either. Beacon dashboard shows wan2 interface "up" from its last check-in before the firewall went dark. |
| 6:20 AM | Andre posts in #oncall that EMS is down and the firewall is unreachable on both WANs. |
| 6:24 AM | Andre calls Tom Kessler for help (not a PagerLine escalation; voluntary escalation per OPS-ONCALL-2026, "escalate if stuck"). |
| 6:31 AM | Tom on the call. Agrees failover should have worked and that the issue is likely wan2 itself. Decides to go onsite; EMS is about 10 minutes from Tom's home. |
| 6:35 AM | Andre updates the EMS supervisor: engineer en route, ETA 7:00 AM. Jordan Pike texted to give a heads-up to EMS's operations manager. |
| 6:58 AM | Tom arrives onsite, badges in, wears required safety footwear. |
| 7:05 AM | Tom on the FortiGate console. wan2 link up, but SD-WAN health check for wan2 shows **failed** (ping to health check target timing out). wan2 configured with a **static IP and gateway** from the old cable modem. |
| 7:10 AM | EMS facilities manager confirms the cable company replaced the modem "sometime in July" after a service call EMS made directly. Larkspur was not told. New modem hands out a different address range. |
| 7:18 AM | Tom changes wan2 to DHCP from the new modem, following RB-NET-004 (confirm the secondary WAN addressing matches what the provider hands out). Health check passes within 30 seconds. |
| 7:21 AM | SD-WAN moves traffic to wan2. **Site back online over secondary.** Tom confirms ERP access from a shop floor terminal with the supervisor. Ticket status: Service Restored - Degraded (secondary WAN, reduced bandwidth). |
| 7:25 AM | Tom posts restoration in #oncall. Marcus notified. |
| 7:30 AM | Ticket handed to the business-hours queue; Tom stays on it as owner. |
| 7:45 AM | Remaining Yealink phones re-register after a PoE switch port bounce (RB-VOIP-001). Phones confirmed working. |
| 8:15 AM | Jordan calls EMS operations manager with a summary and confirms post-mortem will follow. |
| 11:50 AM | ISP reports fiber splice complete. |
| 12:04 PM | wan1 back up. SD-WAN returns traffic to primary per rules. Tom verifies both health checks green. |
| 1:00 PM | Ticket resolved after confirmation with EMS facilities manager. |

## 3. Root cause

1. **Direct cause:** The secondary WAN (wan2) had a static IP and gateway from the previous cable modem. After the cable provider replaced the modem (late July), wan2 could not route traffic. The link still showed "up".
2. **Why nobody noticed:** Beacon RMM monitored FortiGate WAN **interface link state** only (since REL-2603 in March). It did not monitor the SD-WAN health check. The FortiGate logged the wan2 health check failure starting **2026-07-28** but those logs were not alerting anywhere.
3. **Why the quarterly check did not catch it:** RB-NET-004 describes a quarterly failover check for every client with a secondary WAN. That check was not being done for most clients. Tom raised this at the 7/22 runbook review; it was parked for Q4.
4. **Why the client change was invisible to us:** EMS called the cable provider directly about a slow connection in July and the provider swapped the modem. There is no step in our client communications asking clients to tell us about ISP equipment changes.

## 4. What went well

- PagerLine paged within 3 minutes of the firewall going dark, and Andre acknowledged in 6 minutes.
- Response SLA met with room to spare.
- Andre escalated to Tom on his own before the 30-minute "stuck" point.
- Tom's proximity got hands on the firewall fast. Field safety requirements followed.
- Client communication was steady: supervisor updated at 5:58, 6:35, and 7:21; Jordan kept EMS management informed.

## 5. What did not go well

- About 15 minutes spent waiting on ISP hold for an ETR before focusing on why failover had not worked. RB-NET-001 sends you to the ISP early, and RB-NET-004 is only linked at the end of RB-NET-001.
- With both WANs down, there was no remote path to the firewall. Only option was a drive.
- The Beacon dashboard "wan2 up" status was misleading; it reflected link state from the last check-in.
- Quarterly WAN failover checks not happening.
- Yealink phones needed a manual PoE bounce after the internet came back; that should be in our notes for EMS.

## 6. Action items

| # | Action | Owner | Due |
|---|---|---|---|
| 1 | Beacon monitor for FortiGate SD-WAN health check status on every client with a secondary WAN; alert after 10 minutes failed | Tom Kessler | 2026-09-11 |
| 2 | New Harbor category "Network - WAN Failover" linked to RB-NET-004 | Priya Raman | 2026-09-11 |
| 3 | RB-NET-001: move the pointer to RB-NET-004 up to the first steps ("if client has secondary WAN, check failover before waiting on ISP") | Tom Kessler | 2026-09-30 |
| 4 | Add WAN failover note to OPS-ONCALL-2026 | Marcus Oyelaran | 2026-09-14 |
| 5 | Schedule quarterly WAN failover tests for all clients with a secondary WAN; first round in Q4 | Tom Kessler, Isaac Brennan | Schedule by 2026-09-30 |
| 6 | Ask clients in business reviews to tell us before any ISP equipment change; add to QBR template | Jordan Pike | Next QBR cycle |
| 7 | Quote out-of-band management (LTE) for EMS firewall | Alicia Brandt (Tom to spec) | 2026-09-18 |
| 8 | EMS Atlas Docs page: add "Yealink phones may need PoE port bounce after WAN outage" | Andre Mitchell | 2026-09-08 |
| 9 | Audit all clients with secondary WAN for static addressing on the secondary link | Tom Kessler | 2026-10-15 |

## 7. Billing

- P1 after-hours work for a Professional client is included. No charge to EMS for Tom's onsite visit or Andre's after-hours time. Onsite time logged but not counted against EMS's 4 included onsite hours for September, per Marcus.
- Andre's after-hours time (5:47 - 7:00 AM) paid at 1.5x per handbook.

## 8. Follow-up status (added later)

- 2026-09-10: Items 1 and 2 done (REL-2609). First run surfaced 3 other clients with failing secondary WAN health checks; tickets opened.
- 2026-09-14: Item 4 done (OPS-ONCALL-2026 rev 2026.2). Item 8 done 9/4.
- 2026-09-29: Item 3 done. Item 5: first round of failover tests scheduled for October-November.
- 2026-10-15: Item 9 done; 5 clients corrected. Item 7: EMS reviewing quote.
