---
doc_id: RB-GEN-002
title: After-hours on-call and escalation
doc_type: runbook
version: "3"
effective_date: 2024-02-12
owner: Marcus Oyelaran
audience: internal
---

# RB-GEN-002 After-hours on-call and escalation

## Purpose / When to use

Use this runbook when you are the on-call technician or when you need to escalate an issue outside business hours. It covers how after-hours calls reach the on-call tech, coverage by tier, and who to call when you need help.

## How after-hours contact works

- After hours, calls to the support line (913) 555-0111 roll to the on-call phone through the after-hours phone tree.
- The on-call technician carries the on-call phone for the week (Monday morning to Monday morning). The schedule is in Atlas Docs.
- Beacon RMM alerts go to the service desk inbox by email. Check the inbox during your on-call week.

## Prerequisites / access needed

- The on-call phone, charged and with you
- Laptop with Harbor PSA, Beacon RMM, LockBox Vault, and M365 admin access
- Stay within 30 minutes of an internet connection during your on-call week

## Steps for the on-call technician

1. Answer the on-call phone, or pick up the voicemail if you missed the call.
2. Call the client back and confirm they are a contact in Harbor PSA.
3. Open a Harbor PSA ticket and set priority per RB-GEN-001.
4. Check the client tier:
   - **Premier:** all priorities covered after hours. Work it.
   - **Professional:** P1 covered after hours. Other priorities are billable with authorized contact approval, or wait for the next business day.
   - **Essentials:** not covered after hours. Billable with authorized contact approval, or wait for the next business day.
5. Record approval for any billable work (name and time).
6. Work the issue using the matching runbook. Update the client every 30 minutes on P1s.
7. Leave a handoff note for the morning triage seat on anything still open.

## Escalation contacts

If you are stuck, the issue is bigger than one client, or you need a second set of hands:

1. **Call Greg Halvorsen's cell (913) 555-0177.** Greg is the Service Desk Lead and the first after-hours escalation contact.
2. **If Greg does not answer, call Tom Kessler** (Senior Systems Engineer) for networking, firewall, server, and backup issues.

For M365 or Entra ID issues that Greg cannot resolve, Greg will bring in Renee Castillo.

Leave a voicemail and send a text with the client name and ticket number when you call. Give each contact about 15 minutes before moving to the next.

## When to escalate right away

- A P1 for a Premier client with no progress after 30 minutes
- Two or more clients down at the same time
- Signs of ransomware or many accounts compromised
- A client asking for a manager

## Billing

- Enter time in Harbor PSA with work type After Hours.
- Professional P1 is included; Professional non-P1 is billable; Essentials is billable; Premier is included.
- Billable after-hours work has a 1-hour minimum.

## Escalate if

- You cannot reach Greg or Tom: keep calling, and email Marcus Oyelaran with the ticket number.
- The client disputes after-hours billing: stabilize P1s, note the dispute, and leave it for the account manager.

## Ticket notes

- Call time and callback time
- Tier coverage decision (included or billable)
- Who approved billable work and when
- Who you escalated to and when

## Revision history

| Version | Date | Author | Change |
|---|---|---|---|
| 1 | 2018-01-08 | Marcus Oyelaran | Initial after-hours procedure. |
| 2 | 2021-10-04 | Marcus Oyelaran | Added after-hours phone tree routing. |
| 3 | 2024-02-12 | Marcus Oyelaran | Updated escalation contacts and tier coverage table. |
