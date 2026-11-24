---
doc_id: RB-GEN-002
title: After-hours on-call and escalation
doc_type: runbook
version: "4"
effective_date: 2025-06-02
owner: Marcus Oyelaran
audience: internal
---

# RB-GEN-002 After-hours on-call and escalation

## Purpose / When to use

Use this runbook when you are the on-call engineer, or when you are anyone at Larkspur who needs to escalate something outside business hours (Monday-Friday 7:00 AM - 6:00 PM CT, plus company holidays). It covers how after-hours calls reach us, what tier gets what, how to escalate, and how to bill.

## How after-hours contact works

- After hours, the support line (913) 555-0111 rolls to **PagerLine**, our on-call routing service. Clients can also call PagerLine directly at **(913) 555-0142**.
- PagerLine takes the caller's name, company, callback number, and a short description, then pages the **on-call engineer from the weekly rotation**.
- Beacon RMM critical alerts (server offline, site offline, backup appliance offline) for Professional and Premier clients also page the on-call engineer through PagerLine.
- The rotation runs Monday 7:00 AM to the following Monday 7:00 AM, among **Andre Mitchell, Grace Liu, Brian Novak, Renee Castillo, Tom Kessler, and Lena Fischer**. The schedule is published in Atlas Docs (On-Call Calendar) and loaded into PagerLine by Tom Kessler. Swaps need Marcus Oyelaran's approval; once approved, update PagerLine yourself before the swap starts and post the swap in the Service Desk channel.

## Prerequisites / access needed

- PagerLine app installed and logged in on your phone, notifications allowed through Do Not Disturb
- Laptop with VPN to Larkspur, Harbor PSA, Beacon RMM, LockBox Vault, M365 partner admin access
- Be within 30 minutes of a reliable internet connection for the whole rotation

## Steps for the on-call engineer

1. **Acknowledge the page in PagerLine right away.** If there is no acknowledgment in 15 minutes, the escalation chain starts (see below).
2. **Call the client back.** Get the full story. Confirm the caller is a contact on the client record in Harbor PSA.
3. **Create or update a Harbor PSA ticket** right away, even before troubleshooting. Set priority per RB-GEN-001. Response SLA clocks for 24x7 tiers are running.
4. **Check the client's tier and decide coverage:**

| Tier | After-hours handling |
|---|---|
| **Premier** | 24x7 for all priorities, included. Work it. P1 response target 15 minutes; P2 1 hour. P3/P4 may be scheduled for the next business day if the client agrees; note the agreement. |
| **Professional** | P1 is covered 24x7 and included (30-minute response). P2-P4 after hours are **billable** at the after-hours rate, 1-hour minimum, and only if an authorized contact approves. Otherwise tell them it is queued for 7:00 AM. |
| **Essentials** | Not covered after hours. Any after-hours work, including P1, is **billable** at the after-hours rate with a 1-hour minimum and requires authorized contact approval. Otherwise queue for 7:00 AM. |

   Rates are on the current price sheet in Atlas Docs. Do not quote a number from memory; read it from the sheet.
5. **Get approval for billable work** before starting. The approver must be listed under Authorized Contacts in Harbor PSA. Record their name and the time of approval in the ticket.
6. **Work the issue** using the matching runbook. For P1s, update the client at least every 30 minutes.
7. **Hand off** anything not finished by 7:00 AM: leave a clear internal note and assign to the right board. Tell the 7:00 AM triage seat in the Service Desk channel.

## Escalation chain (current)

Use this chain when the on-call engineer needs help, when a page is not acknowledged, or when anyone at Larkspur needs to reach the on-call engineer.

1. **Call PagerLine (913) 555-0142.** It pages the on-call engineer from the weekly rotation.
2. **If no acknowledgment in 15 minutes, page Tom Kessler** (Senior Systems Engineer) through PagerLine using the "Escalate - Tier 3" option.
3. **If Tom does not answer in 15 minutes, page Marcus Oyelaran** (Director of Service Delivery) through PagerLine using the "Escalate - Director" option.

**If Tom Kessler is the on-call engineer that week, skip step 2 and go straight to Marcus Oyelaran.**

Do not call personal cell numbers listed in old documents or email signatures. PagerLine logs every page and acknowledgment, and that log is what we use for SLA reporting.

Escalate to Tier 3 by subject:
- Network, firewall, WAN, servers, backups: Tom Kessler
- M365, Entra ID, Intune, tenant-wide email issues: Renee Castillo (if she is not on call, page via PagerLine "Escalate - Tier 3"; PagerLine routes to Tom first, who will pull in Renee)

## When to wake someone up

Escalate up the chain immediately (do not wait 15 minutes) if:
- A P1 affects a Premier client and you cannot make progress in 30 minutes.
- Two or more clients report outages at the same time.
- You see signs of ransomware or mass account compromise (many files renamed, many users locked out, mass outbound spam).
- A client asks for an executive or threatens to cancel.

## Priority guidance

- P1 after hours for Premier and Professional: work immediately, included.
- P1 for Essentials: offer billable work; if declined, document and queue as first ticket at 7:00 AM.
- P2 for Premier: work it, included. For others: billable with approval or queue.
- P3/P4: almost never worked after hours except for Premier when the client asks.

## Billing

- In Harbor PSA, enter time with work type **After Hours**. Billable vs. included is set by the contract, but double-check: Professional P1 = included, Professional non-P1 = billable, Essentials = billable, Premier = included.
- Billable after-hours time has a 1-hour minimum. Enter actual time; Harbor applies the minimum on invoicing.
- Hourly staff: after-hours time is paid at 1.5x. The on-call stipend is $300 per week on call.

## Escalate if

- No acknowledgment within 15 minutes at any step: go to the next step in the chain.
- The client disputes billing: do the minimum to stabilize if it is a P1, note the dispute, and leave it for the account manager in the morning.
- You are sick or cannot cover your shift: arrange a swap, or tell Marcus Oyelaran as soon as you know.

## Ticket notes

Per RB-GEN-004, plus:
- PagerLine page time, acknowledgment time, callback time
- Coverage decision (included vs. billable) and why
- Name of authorized contact who approved billable work, and time
- Anyone you escalated to and when

## Revision history

| Version | Date | Author | Change |
|---|---|---|---|
| 1 | 2018-01-08 | Marcus Oyelaran | Initial after-hours procedure. |
| 2 | 2021-10-04 | Marcus Oyelaran | Added after-hours phone tree routing. |
| 3 | 2024-02-12 | Marcus Oyelaran | Updated escalation contacts and tier coverage table. |
| 4 | 2025-06-02 | Marcus Oyelaran | Escalation now runs through PagerLine weekly rotation, then Tom Kessler, then Marcus Oyelaran. Removed individual cell numbers. Added billing section. |
