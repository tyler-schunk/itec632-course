---
doc_id: RB-GEN-001
title: Ticket triage and priority assignment
doc_type: runbook
version: "5"
effective_date: 2026-01-05
owner: Priya Raman
audience: internal
---

# RB-GEN-001 Ticket triage and priority assignment

## Purpose / When to use

Use this runbook every time a new ticket lands in the Harbor PSA **Service Desk - New** board, whether it came in by phone (support line (913) 555-0111), email (help@larkspurridge.example), the client portal (portal.larkspurridge.example), or a Beacon RMM alert. Triage is the first touch. The goal is simple: right client, right contact, right priority, right queue, and a first human response inside the SLA.

Triage is done by whoever is on the triage seat (Tier 1 rotation, posted weekly by Priya in the Service Desk channel). Everyone on the desk is expected to triage when the New board has anything older than 10 minutes.

This version reflects the 2026 SLA exhibit (effective Jan 1, 2026).

## Prerequisites / access needed

- Harbor PSA technician login with Service Desk board access
- Beacon RMM read access (to check device and site status)
- Atlas Docs (client pages and runbooks)
- Client tier and authorized contacts are on the client record in Harbor PSA (Company > Contract and Company > Authorized Contacts tabs)

## Business hours and SLA clocks

- Business hours: **Monday-Friday, 7:00 AM - 6:00 PM CT**, excluding company holidays (New Year's Day, Memorial Day, Independence Day, Labor Day, Thanksgiving Day and the Friday after, Christmas Eve after 12:00 PM, Christmas Day).
- "Response" means first human response (a call, or a personal email/portal reply). The auto-acknowledgment email from Harbor does **not** count.
- Business-hours clocks pause outside business hours unless the client's tier includes 24x7 for that priority. Harbor PSA calculates this from the contract, but check the SLA due time on the ticket header before you move on.

## Priority definitions

| Priority | Definition | Typical examples |
|---|---|---|
| **P1 Critical** | Business down or most users unable to work | Internet outage at a site, server down, email down company-wide, all phones down, ransomware-type behavior across machines |
| **P2 High** | Multiple users affected or a key function degraded; or a single VIP/executive fully blocked | Shared printer down for a whole office, line-of-business app failing for a department, VPN down for all remote staff, owner locked out of email |
| **P3 Normal** | Single user affected, workaround may exist | One user's Outlook crashing, one laptop slow, single user printer offline, one user can't sync OneDrive |
| **P4 Low** | Requests, questions, scheduled changes, new user setups | New user onboarding, software install requests, permission changes, "how do I" questions, quote requests |

## SLA targets (2026)

| Priority | Essentials response | Professional response | Premier response | Resolution target (all tiers) |
|---|---|---|---|---|
| P1 | 1 hour (business hours only) | 30 minutes (24x7) | 15 minutes (24x7) | 4 hours |
| P2 | 2 business hours | 1 business hour | 1 hour (24x7) | 8 business hours |
| P3 | 4 business hours | 4 business hours | 2 business hours | 2 business days |
| P4 | 1 business day | 1 business day | 1 business day | 5 business days |

Missed P1 **response** targets cost us an SLA credit of 5% of that client's monthly managed-services fee per miss (capped at 20% per month). Resolution targets are goals and are not credited, but they are reported in every business review. Treat P1 response time as non-negotiable.

## Steps

1. **Pick the oldest ticket first** on the New board, except that any ticket with "down", "outage", "can't work", "everyone", or a Beacon "Site offline" alert in the subject gets looked at immediately.
2. **Confirm the client and contact.**
   - Match the ticket to the correct company. Watch for similar names (Brightlane Realty vs. Bluffline Logistics; Willowshade Senior Living vs. Westfork Credit Advisors). Email domain is the best tie-breaker.
   - Make sure the contact exists in Harbor. If not, create the contact, but do not grant anything that needs authorization (new accounts, access, purchases) until an authorized contact approves.
   - Check the contact record for the **VIP** flag. VIPs are set by the client during onboarding and reviewed in business reviews.
3. **Check the tier** on the Contract tab (Essentials, Professional, Premier). Tier drives SLA, after-hours handling, onsite coverage, and what is billable. If the company shows no active contract or shows "Hold", stop and message the account manager (Alicia Brandt or Kevin Duong) before doing work beyond a basic response.
4. **Look for duplicates and related tickets.** Search the client's open tickets. If three or more tickets from the same site describe the same symptom, you probably have a P1 or P2 parent. Create or pick a parent ticket, link the others as children, and work the parent.
5. **Check Beacon RMM.** For anything that sounds like connectivity or device health, open the client site in Beacon:
   - Many agents at one site went offline at the same time: likely internet or power, go to RB-NET-001.
   - Server agent offline or critical alerts: RB-SRV-002.
   - Single device offline: may just be powered off.
6. **Assign priority** using the definitions above. Rules of thumb:
   - Count people affected, not how loud the caller is. Upgrade one step if it blocks a key business function (front desk check-in at a clinic, dispatch at Bluffline, payroll day at any client).
   - A single VIP fully blocked is P2. A single VIP inconvenienced (one app slow, workaround exists) stays P3.
   - Security-flavored tickets: a single user reporting a phishing email is P3 (RB-SEC-001). A user who entered their password into a phishing page is P2. Lost or stolen device is P2 (RB-SEC-002).
   - New user setups are P4 regardless of urgency claims; if the start date does not give us **5 business days** notice, still accept it, set P4, and flag the account manager (see RB-ACC-003).
   - Same-day offboarding requests received before 3:00 PM CT are P2 so they get done the same business day (RB-ACC-004). After 3:00 PM, P3 for the next business morning unless the client says the termination is hostile, in which case call Renee Castillo.
   - When in doubt between two priorities, pick the higher one and note why. It is easier to downgrade than to explain a missed SLA.
7. **Set ticket type and board.**
   - Tier 1 board: password resets, MFA resets, single-user Outlook/Teams/OneDrive issues, printer offline, basic hardware, software installs, phishing reports.
   - Tier 2 board: anything Tier 1 has worked for 45 minutes without progress, multi-user issues, scan-to-email, Wi-Fi, VPN, docking problems needing hardware swaps, workstation deployments.
   - Tier 3 / Engineering: servers, firewalls, WAN, backups, tenant-wide M365 configuration, anything P1.
   - Projects (Rachel Kim): migrations, multi-machine rollouts, anything that should be quoted.
   - Dispatch (Isaac Brennan): anything needing an onsite visit; see RB-GEN-003.
8. **Set the runbook reference.** Fill `runbook_ref` with the Atlas Docs runbook ID you expect to apply (for example `RB-PRT-001`). If none applies, leave it blank and say so in the internal note. Priya reviews blank runbook_ref tickets weekly to find gaps.
9. **Make the first human response.**
   - P1/P2: call the contact. If no answer, leave a voicemail and send a portal reply. Then work the problem.
   - P3/P4: a personal reply is fine. Give the ticket number (TCK-1xxxxx), what happens next, and when.
   - Do not promise resolution times. Promise the next update.
10. **For P1 tickets**, in addition to the above:
    - Post in the Service Desk channel: client code, symptom, ticket number.
    - Notify Priya Raman (business hours) and assign to Tier 3 (Tom Kessler for network/server, Renee Castillo for M365/Entra).
    - Update the client every 30 minutes until resolved, even if the update is "still working on it".
    - After hours, follow RB-GEN-002.
11. **Hand off or start work.** If the ticket is yours (Tier 1 scope), start the runbook. Otherwise assign it with a short internal note so the next tech does not have to re-ask the user anything.

## After-hours tickets

Tickets that arrive outside business hours are triaged by the on-call engineer per RB-GEN-002. At 7:00 AM the triage seat sweeps anything left on the New board from overnight first, oldest first, P1/P2 before P3/P4.

Quick tier reference for after-hours work:

| Tier | After-hours coverage |
|---|---|
| Essentials | Not covered. Work is billable at the after-hours rate ($247.50/hour, 1-hour minimum) and only with authorized contact approval. Otherwise queued for 7:00 AM. |
| Professional | P1 covered 24x7 (30-minute response). P2-P4 after hours are billable or wait until business hours. |
| Premier | 24x7 for all priorities, included. |

## Priority guidance examples

- Foxhaven Dental (Professional) front desk printer offline, other printers fine, they can print from the back office: **P3**, Tier 1, RB-PRT-001. If the front desk cannot print and it is blocking patient check-out, P2 is reasonable; note why.
- Emberline Metalworks (Professional) whole plant has no internet: **P1**, RB-NET-001, Tier 3.
- Dunmore & Pace Attorneys (Premier) managing partner cannot sign in to anything: **P2** (VIP fully blocked), RB-ACC-001.
- Cask & Kettle Brewing (Essentials) asks for a new hire next Monday, request sent Thursday: **P4**, RB-ACC-003, flag short notice to account manager.
- Willowshade Senior Living (Premier) nurse station Wi-Fi dropping for one wing at 9:00 PM: **P2**, after-hours on-call, RB-NET-002.

## Escalate if

- You cannot determine the client or the contact cannot be verified: Priya Raman.
- The request is out of scope or would need a quote (new projects, hardware purchases, work for a client on Hold): account manager (Alicia Brandt or Kevin Duong).
- A P1 is not acknowledged by Tier 3 within 15 minutes during business hours: Marcus Oyelaran.
- The client disputes the priority or asks for an SLA exception: Priya Raman, then Marcus Oyelaran.
- More than one client reports the same problem at once (possible upstream provider issue or a Larkspur tooling problem): Tom Kessler and Marcus Oyelaran.

## Ticket notes

Follow RB-GEN-004. At triage, record at minimum:

- Who reported it, callback number, and how it came in
- What is affected (user, device asset tag `LR-<CLIENT>-####`, site) and how many people
- Priority and a one-line reason ("P2 - whole billing dept cannot print")
- Board/assignee and runbook_ref
- Time of first human response and method (call/voicemail/portal)

## Revision history

| Version | Date | Author | Change |
|---|---|---|---|
| 1 | 2019-03-04 | Marcus Oyelaran | Initial triage checklist. |
| 2 | 2021-06-14 | Greg Halvorsen | Added priority examples and duplicate-ticket parent/child steps. |
| 3 | 2023-08-07 | Greg Halvorsen | Added runbook_ref requirement and Beacon RMM site-offline check. |
| 4 | 2025-02-10 | Priya Raman | Ownership moved to Service Desk Manager. Added security-ticket priority rules. |
| 5 | 2026-01-05 | Priya Raman | Updated SLA table and after-hours rate for 2026 SLA exhibit and price sheet. Business hours 7:00 AM - 6:00 PM CT. Clarified onboarding notice (5 business days) and offboarding cutoff. |
