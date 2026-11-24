---
doc_id: RB-GEN-003
title: Onsite visit procedure
doc_type: runbook
version: "4"
effective_date: 2026-01-05
owner: Brian Novak
audience: internal
---

# RB-GEN-003 Onsite visit procedure

## Purpose / When to use

Use this runbook when a ticket cannot be resolved remotely and someone needs to go to the client site: dead hardware, cabling, network gear that is offline, a printer that needs hands, a new workstation install, or a client who explicitly requests an onsite visit. It covers how to request a dispatch, how onsite time is covered by tier, and what the field tech does on arrival and before leaving.

All onsite work is scheduled by **Isaac Brennan** (Dispatcher / Service Coordinator, ext. 224). Field techs are **Olivia Grant** and **Derek Simmons**, with **Brian Novak** as field/onsite lead. Tier 2 and Tier 3 techs go onsite when the work needs them, but Isaac still books it.

## Prerequisites / access needed

- Harbor PSA ticket with remote troubleshooting documented
- Client site details on the client's Atlas Docs page (address, parking, door codes, site contact, network diagram)
- Field kit (see step 7)
- Harbor PSA mobile app for time and mileage entry

## Coverage by tier

| Tier | Onsite coverage (metro) |
|---|---|
| Essentials | Billable at the out-of-scope rate ($165/hour business hours, 15-minute increments) plus a $75 trip charge |
| Professional | **4 hours per month included**, then billable at the out-of-scope rate plus $75 trip charge per billable visit |
| Premier | Unlimited onsite, included; no trip charge in the metro |

- "Metro" means the Kansas City metro service area, roughly within 40 miles of our Lenexa office. Visits outside the metro are quoted; Isaac will get a quote approved through the account manager before booking.
- After-hours onsite (outside 7:00 AM - 6:00 PM CT Monday-Friday, weekends, holidays) is billed at $247.50/hour with a 1-hour minimum unless the tier covers it (Premier, or a Professional P1).
- Check the Professional onsite balance on the client's Contract tab in Harbor PSA (**Onsite Hours - Month to Date**). The 4 hours reset on the 1st of each month; unused hours do not roll over.
- Project work (workstation rollouts, migrations) is quoted separately at the project rate and does not consume the Professional onsite bucket.

## Steps

### Requesting a dispatch (any technician)

1. **Exhaust remote options first.** Use Beacon RMM, remote session, and the relevant runbook. Document what you tried. Exceptions: physical damage, no power, cabling, and anything the client cannot safely do themselves.
2. **Check coverage.** Look up the tier and, for Professional, the remaining onsite hours this month.
3. **Get approval if billable.** For Essentials, for Professional clients past their 4 hours, or for anything out of scope, an **authorized contact** must approve the estimated cost before booking. Record the approver's name and the time in the ticket. Professional includes unlimited onsite visits, so dispatch for those clients does not normally need cost approval.
4. **Request the dispatch** in Harbor PSA: set the ticket status to **Needs Dispatch** and fill the Dispatch Request form (site, on-site contact, access notes, parts needed, estimated duration, priority, preferred window). Isaac will not schedule from a chat message alone.
5. **Isaac schedules** based on priority and field tech availability:
   - P1: same-day, next available tech, Isaac calls the client with an ETA.
   - P2: same day if requested before 12:00 PM CT, otherwise next business morning.
   - P3: within 2 business days.
   - P4: scheduled at a time agreed with the client.
   Isaac confirms the appointment with the client by email from Harbor PSA and assigns the tech.

### On the day (field tech)

6. **Review the ticket** before leaving. Check parts, the client page in Atlas Docs, and any LockBox Vault credentials you will need (local admin, switch, firewall, printer web UI).
7. **Field kit check:** laptop with charger, USB-C/Thunderbolt dock for testing, spare patch cables (Cat6, various lengths), cable tester/toner, USB boot drive with Windows 11 install and Dell diagnostics, spare power strip, label maker, asset tags (`LR-<CLIENT>-####`), PoE injector, screwdrivers, flashlight.
8. **Travel status:** set the ticket to **En Route** in the mobile app. Log mileage in Harbor PSA (reimbursed at the current IRS standard rate).
9. **Arrival:** check in with the site contact, set status **On Site**. Onsite time counts from arrival to departure, not from when you leave the office. Travel time is not billed for metro visits; the $75 trip charge applies only to billable visits (never to Premier metro visits).
10. **Do the work** following the relevant runbook. Keep the client informed. If the scope grows (for example, a 20-minute printer fix turns into rewiring a closet), stop and call Isaac so he can get approval for the additional time before you continue.
11. **Before leaving:**
    - Confirm the fix with the user or site contact.
    - Tidy up: cables labeled, closet doors closed, ceiling tiles back.
    - Take a photo of any rack or closet you changed and attach it to the ticket.
    - Update asset records in Harbor PSA for any hardware installed, removed, or swapped.
12. **Departure:** set status **Complete - Onsite**, enter time with work type **Onsite**. Harbor deducts Professional time from the monthly onsite bucket automatically when the time entry is marked Onsite.

### Parts and RMAs

- Dell warranty parts are ordered through Dell TechDirect by the field lead (Brian Novak). Dell ProSupport often sends its own tech; if Dell is sending a tech, tell Isaac so we do not double-book.
- Do not leave client hardware in your car overnight. Bring it to the office and log it in the hardware shelf sheet.

## Priority guidance

- Onsite is never a reason to lower priority. A P1 internet outage that needs onsite still has a 4-hour resolution target.
- If a P1 or P2 needs a tech onsite and none is available within 2 hours, Isaac escalates to Brian Novak, who may pull a Tier 2 tech off the desk.

## Escalate if

- No field tech is available for a P1 within the same day: Brian Novak, then Marcus Oyelaran.
- The client disputes onsite charges or the remaining Professional hours: account manager (Alicia Brandt or Kevin Duong).
- You find a safety hazard (exposed wiring, overheating closet, water near equipment): stop, tell the site contact, photograph it, and call Brian Novak.
- The fix needs Tier 3 (firewall, server, switch configuration): call Tom Kessler from site.

## Ticket notes

Per RB-GEN-004, plus:
- Arrival and departure times
- Approver name and time for billable visits
- Parts used (with serial numbers) and asset tags updated
- Photos of closet/rack changes
- Remaining Professional onsite hours after this visit (check the Contract tab)

## Revision history

| Version | Date | Author | Change |
|---|---|---|---|
| 1 | 2019-05-13 | Brian Novak | Initial onsite checklist. |
| 2 | 2021-09-20 | Brian Novak | Added dispatch request form and Isaac Brennan as scheduler. |
| 3 | 2024-01-08 | Brian Novak | Added field kit list, mileage logging, photo requirement. |
| 4 | 2026-01-05 | Brian Novak | Updated rates for 2026 price sheet ($165/$247.50, $75 trip charge). Professional onsite bucket (4 hours/month) tracked on Contract tab. |
