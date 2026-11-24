---
doc_id: OPS-ONCALL-2026
title: On-Call Rotation and Expectations (2026)
doc_type: policy
version: "2026.2"
effective_date: 2026-09-14
owner: Marcus Oyelaran
audience: internal
---

# On-Call Rotation and Expectations - 2026

**Owner:** Marcus Oyelaran, Director of Service Delivery
**Applies to:** Tier 2 and Tier 3 engineers on the after-hours rotation
**Related:** RB-GEN-002 (After-hours on-call and escalation), RB-GEN-001 (Ticket triage and priority assignment), RB-GEN-004 (Ticket notes and closure standards), POL-HR-HANDBOOK-2026 Section 12 (pay and stipend)
**Revision 2026.2 (2026-09-14):** added Q4 2026 calendar; added note on WAN failover checks after the EMS post-mortem.

This doc covers who is on call, when, what is expected, and how you get paid for it. The step-by-step procedure for handling a page lives in RB-GEN-002. If this doc and the runbook ever disagree on a procedural step, follow the runbook and tell Marcus so we can fix one of them.

## 1. Why We Have On-Call

- **Professional** clients get 24x7 coverage for **P1** incidents. P1 response target: **30 minutes, 24x7**.
- **Premier** clients get 24x7 coverage for **all priorities**. P1 response target: **15 minutes, 24x7**; P2: 1 hour, 24x7.
- **Essentials** clients get business-hours help desk only. After-hours work for Essentials (and for non-P1 Professional issues) is billable at the after-hours rate of **$247.50/hour, 1-hour minimum**, and only if the client's authorized contact approves it on the call.

Missed P1 response targets cost us a 5% SLA credit per miss on that client's monthly managed-services fee (capped at 20%). On-call is where most of that risk lives.

## 2. Coverage Window

- **After hours** = any time outside business hours (**Mon-Fri 7:00 AM - 6:00 PM CT**), plus all day on weekends and company holidays.
- On-call weeks run **Monday 7:00 AM CT to the following Monday 7:00 AM CT**.
- During business hours the live service desk handles everything. The on-call engineer works their normal shift.

## 3. How Pages Reach You

1. Client calls the support line (913) 555-0111 after hours, or calls PagerLine directly at **(913) 555-0142**. After-hours calls to the support line roll to PagerLine.
2. PagerLine takes the caller's name, client, callback number, and a short description, then **pages the on-call engineer from the weekly rotation** (push + SMS + phone call).
3. Beacon RMM critical alerts for Professional and Premier clients (server down, firewall offline, VaultLine job failure on a server marked critical) also page through PagerLine.

### Escalation order

| Step | Who | When |
|---|---|---|
| 1 | On-call engineer (weekly rotation) | Immediately |
| 2 | **Tom Kessler**, Senior Systems Engineer | If no answer in **15 minutes** |
| 3 | **Marcus Oyelaran**, Director of Service Delivery | If Tom does not answer |

When Tom himself is the on-call engineer, PagerLine skips step 2 and goes straight to Marcus.

Do not hand out personal cell numbers to clients. Everything goes through PagerLine so it is logged.

## 4. The Rotation

Rotation members (2026):

| Engineer | Role | Ext. |
|---|---|---|
| Tom Kessler | Senior Systems Engineer (Tier 3) | 204 |
| Renee Castillo | Systems Engineer (Tier 3) | 205 |
| Lena Fischer | Tier 2 Technician | 211 |
| Andre Mitchell | Tier 2 Technician | 212 |
| Grace Liu | Tier 2 Technician | 213 |
| Brian Novak | Tier 2 Technician / Field Lead | 214 |

Rotation order repeats every six weeks: Andre Mitchell, Grace Liu, Brian Novak, Renee Castillo, Tom Kessler, Lena Fischer.

New Tier 2 hires join the rotation after their 90-day introductory period and after shadowing two on-call weeks. Tier 1 technicians are not on the rotation.

## 5. Expectations While On Call

**Acknowledge every page within 15 minutes.** After 15 minutes PagerLine escalates to Tom, and that counts as a missed page.

Beyond that:

- Keep your company laptop, charger, and a working internet connection (hotspot counts) with you. You should be able to start remote work within 15 minutes of acknowledging.
- Stay fit to work. No alcohol or anything else that would impair you.
- Stay within reasonable driving distance of the metro (roughly 60 minutes) unless you have arranged otherwise with Marcus. Most issues are remote, but some P1s need hands on the equipment.
- Call the client back. A page acknowledgment is not a response; the SLA response clock stops at the first human response to the client.
- Assign priority per RB-GEN-001. If the caller says "everything is down", verify. If it is one user, it is not a P1.
- Open or update a Harbor PSA ticket for every page, even ones that turn out to be nothing. Use the "After-Hours" source flag so time bills and reports correctly.
- For anything P1, post a short note in the #oncall Teams channel when you start and when service is restored.
- If you are stuck after 30 minutes on a P1, escalate. Tom for infrastructure (servers, firewalls, networking); Renee for M365/Entra/Intune. Asking for help early is expected, not a failure.

### Internet outage and WAN failover (added 2026-09)

After the Emberline Metalworks outage on 2026-09-01 (see MTG-2026-09-03-POSTMORTEM-EMS), for any site-down call:

1. Work RB-NET-001 (Internet outage triage) first.
2. If the client has a secondary WAN, run RB-NET-004 (Firewall WAN failover check) **before** waiting on the ISP. Do not assume failover worked because the firewall shows the secondary interface "up".

## 6. Handoff

- Handoff happens **Monday at 7:00 AM CT**.
- The outgoing engineer posts a handoff note in #oncall by 7:00 AM: open after-hours tickets, anything still being watched, and any client who was told "we will check again in the morning".
- The incoming engineer confirms in the thread and checks that PagerLine shows them as primary.
- Open after-hours tickets go back to the normal queue at 7:00 AM unless the outgoing engineer is actively working them.

## 7. Swaps, PTO, and Holidays

- Swap a week or individual days with another rotation member. Get Marcus's approval and **update PagerLine before the swap starts**. Until PagerLine shows the change, the original engineer is still on the hook.
- PTO requests that overlap your on-call week are not approved until you have a swap (handbook Section 9.4).
- Holidays are after-hours all day. Holiday weeks are spread across the rotation year to year; Marcus keeps a running tally.

## 8. Pay

- **Stipend: $300 per week** on call. Partial weeks from swaps are prorated by day.
- **Hourly staff: after-hours time worked is paid at 1.5x**, in 15-minute increments with a 15-minute minimum per incident. Log it in the timekeeping system and in Harbor PSA.
- The stipend is paid in addition to after-hours pay, not instead of it.
- Exempt engineers (Tom, Renee) receive the stipend.
- On-call engineers receive the cell phone allowance stated in their role memo.

Full terms are in POL-HR-HANDBOOK-2026 Section 12.

## 9. What Counts as a Missed Page

A page that escalates to step 2 because the on-call engineer did not acknowledge within 15 minutes. Marcus reviews every missed page. One miss gets a conversation. A pattern gets handled under the handbook's discipline section. Phone died, slept through it, no signal: tell Marcus the same morning; it is much better coming from you.

## 10. Q4 2026 Rotation Calendar

Each week runs Monday 7:00 AM CT to the following Monday 7:00 AM CT. Escalation for every week: Tom Kessler, then Marcus Oyelaran (Marcus only when Tom is primary).

| Week starting (Mon) | On-call engineer | Holidays / notes |
|---|---|---|
| 2026-09-28 | Tom Kessler | Covers Oct 1 (start of Q4) |
| 2026-10-05 | Lena Fischer | |
| 2026-10-12 | Andre Mitchell | |
| 2026-10-19 | Grace Liu | |
| 2026-10-26 | Brian Novak | Approved swap: Grace Liu covers Fri 10/30 - Sun 11/1 |
| 2026-11-02 | Renee Castillo | |
| 2026-11-09 | Tom Kessler | |
| 2026-11-16 | Lena Fischer | |
| 2026-11-23 | Andre Mitchell | Thanksgiving (Thu 11/26) and Fri 11/27 are holidays, after-hours all day |
| 2026-11-30 | Grace Liu | |
| 2026-12-07 | Brian Novak | |
| 2026-12-14 | Renee Castillo | |
| 2026-12-21 | Tom Kessler | Christmas Eve (Thu 12/24) after-hours from 12:00 PM; Christmas Day (Fri 12/25) holiday |
| 2026-12-28 | Lena Fischer | New Year's Day (Fri 1/1/2027) holiday; runs to Mon 1/4/2027 7:00 AM |

Swaps after publication go in PagerLine first, then in this table. PagerLine is the source of truth if they disagree.

## 11. Quick Reference

- PagerLine: **(913) 555-0142**
- Support line: (913) 555-0111
- Main line: (913) 555-0100
- Teams channel: #oncall
- Procedure: RB-GEN-002
- Escalation: on-call engineer, then Tom Kessler after 15 minutes, then Marcus Oyelaran
