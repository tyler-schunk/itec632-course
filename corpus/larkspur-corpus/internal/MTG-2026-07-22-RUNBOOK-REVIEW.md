---
doc_id: MTG-2026-07-22-RUNBOOK-REVIEW
title: Annual Runbook Review Meeting - 2026-07-22
doc_type: meeting_notes
version: "1"
effective_date: 2026-07-22
owner: Marcus Oyelaran
audience: internal
---

# Annual Runbook Review - Wednesday, July 22, 2026

**Time:** 1:00 - 2:40 PM CT, conference room + Teams
**Facilitator:** Marcus Oyelaran
**Notes:** Priya Raman
**Attendees:** Marcus Oyelaran, Priya Raman, Tom Kessler, Renee Castillo, Lena Fischer, Andre Mitchell, Grace Liu, Brian Novak, Rachel Kim
**Optional / joined for part:** Isaac Brennan (onsite items only)

## Purpose

Yearly pass over every runbook in the Atlas Docs catalog (RB-GEN-001 through RB-SEC-002, 31 runbooks). Each owner confirms their runbook is accurate or lists the changes needed. Second goal: decide what to do about superseded runbook versions that are still sitting in Atlas Docs.

## 1. Runbook usage numbers (Priya)

From the new Runbook ref picklist data (only clean since the picklist goes live next week, so this is from the free-text field with typos cleaned up by hand):

| Runbook | Times referenced, Jan-Jun 2026 |
|---|---|
| RB-ACC-001 Password reset and account unlock | 612 |
| RB-PRT-001 Printer shows offline | 288 |
| RB-M365-005 OneDrive / SharePoint sync errors | 241 |
| RB-M365-003 Outlook profile rebuild | 219 |
| RB-ACC-002 MFA enrollment and reset | 204 |
| RB-SW-001 Software install requests | 187 |
| RB-ACC-003 New user onboarding | 164 |
| RB-SEC-001 User-reported phishing email | 151 |
| Everything else | under 150 each |

Priya noted that with the free-text field there is no way to tell which **version** a tech had open. The picklist will not fix that either; it records the ID only.

## 2. Owner check-ins

**Priya Raman**
- RB-GEN-001 (triage): accurate. Will add an example for "single VIP fully blocked = P2".
- RB-GEN-004 (notes and closure): accurate. Add a pointer to the auto-close rule (REL-2511).

**Marcus Oyelaran**
- RB-GEN-002 (after-hours on-call and escalation): v4 accurate. PagerLine repeat-call change (REL-2604) to be mentioned in a note.

**Brian Novak**
- RB-GEN-003 (onsite visit): mostly fine. Brian has not done a full line-by-line read against the 2026 service catalog yet. Carry to next review.
- RB-HW-001 (won't boot) and RB-HW-003 (dock/monitor): update RB-HW-003 for the UD22 dock in STD-HW-2026. WD19S content stays since those docks are still in the field.

**Renee Castillo**
- RB-ACC-001 v3 (password reset): accurate. Callback to the number on file in Harbor; no DOB or SSN.
- RB-ACC-002 v2 (MFA): accurate. Authenticator push with number matching only.
- RB-ACC-003 (onboarding): updated in January for 5 business days notice. Accurate.
- RB-ACC-004 (offboarding): accurate. Same business day if requested before 3:00 PM CT.
- RB-M365-001, RB-M365-002: accurate.
- RB-SEC-001, RB-SEC-002: accurate. Keep them simple.

**Lena Fischer**
- RB-M365-003: accurate. Adding screenshots for the new Outlook.
- RB-SW-001, RB-SW-002: accurate. RB-SW-002 already describes the Beacon patch rings (Pilot/Broad).

**Grace Liu**
- RB-M365-004 (Teams): add the Teams Rooms reset steps used at Granite Peak.
- RB-M365-005 (OneDrive sync): accurate.

**Andre Mitchell**
- RB-PRT-001 v2 (printer offline): accurate. Order is check power/network and IP, stop spooler, clear the spool folder, start spooler, re-add port only if IP changed.
- RB-PRT-002 (scan-to-email): needs an update for the M365 SMTP relay connector changes. Andre to draft.
- RB-VOIP-001 (Yealink): accurate.

**Tom Kessler**
- RB-NET-001, RB-NET-002, RB-NET-003: accurate.
- RB-NET-004 (firewall WAN failover check): procedure is accurate, but Tom flagged that the quarterly failover test it describes **is not actually being done** for most clients with a secondary WAN. Beacon only shows interface link state. Tom wants a proper health-check monitor. Discussed briefly; no owner or date set. **Parked for Q4 planning.**
- RB-BAK-001, RB-BAK-002, RB-SRV-002: accurate. RB-SRV-001: Tom to double-check the wording against the 15%/10% disk thresholds (REL-2512).

**Rachel Kim**
- RB-HW-002 (new workstation deployment): accurate. Already references the Latitude 5550 / OptiPlex Micro 7020 and the 32 GB standard.

## 3. Old runbook versions still in Atlas Docs

Background: when a runbook gets a new major version, the habit has been to create a new page rather than edit the existing one, so the old page stays. Most of these have a version banner (REL-2506) but they still show in search and still get opened. Atlas Docs has had an "Archived" status since 6/29 (REL-2606) that hides a page from search and the index while keeping it readable by direct link.

Grace raised the same issue at the April all-hands. Andre said a newer tech followed an old printer runbook in June and skipped clearing the spool folder; the ticket got reopened the next day.

**Cleanup list (agreed today):**

| Page in Atlas Docs | Current version | Action | Owner |
|---|---|---|---|
| RB-ACC-001 **v2** (effective 2023-04-10) | v3 (2025-01-15) | Archive | Marcus Oyelaran (with Renee) |
| RB-PRT-001 **v1** (effective 2022-11-07) | v2 (2024-08-19) | Archive | Marcus Oyelaran (with Andre) |
| Any other superseded runbook pages found during the sweep | - | List, confirm with owner, archive | Marcus Oyelaran |

Discussion:
- Tom asked whether we should just delete them. Marcus: no. Archive, not delete. We sometimes need to show a client what procedure was in effect on a given date.
- Renee: until they are archived, any tech who lands on an old page should check the effective date banner against the runbook index.
- Priya will remind the service desk at huddle to turn on "Show current versions only" in Atlas Docs search.
- Marcus to do a full sweep of Atlas Docs for other superseded pages and bring the list to the next service delivery weekly.

**Decision:** Archive RB-ACC-001 v2 and RB-PRT-001 v1, plus anything else found in the sweep. Target: **August 14, 2026**.

## 4. Process changes going forward

- New major versions of a runbook: **edit the existing page and let page history keep the old text**, instead of creating a new page. Owners who must create a new page archive the old one the same day.
- Every runbook gets a "Last reviewed" date in its header. Marcus to add the field.
- Next annual review: July 2027. Owners still expected to fix problems as they find them.

## Action items

| # | Action | Owner | Due | Status |
|---|---|---|---|---|
| 1 | Archive RB-ACC-001 v2 and RB-PRT-001 v1 in Atlas Docs | Marcus Oyelaran | 2026-08-14 | Open |
| 2 | Sweep Atlas Docs for other superseded runbook pages; bring list to SD weekly | Marcus Oyelaran | 2026-08-14 | Open |
| 3 | Huddle reminder: "Show current versions only" toggle and effective date banner | Priya Raman | 2026-07-23 | Done 7/23 |
| 4 | RB-HW-003 update for UD22 dock | Brian Novak | 2026-08-31 | Open |
| 5 | RB-PRT-002 SMTP relay update | Andre Mitchell | 2026-08-31 | Open |
| 6 | RB-M365-004 Teams Rooms steps | Grace Liu | 2026-08-31 | Open |
| 7 | RB-GEN-003 full read-through against 2026 service catalog | Brian Novak | Next review | Open |
| 8 | Add "Last reviewed" header field to runbook template | Marcus Oyelaran | 2026-08-14 | Open |
| 9 | Scope a WAN health-check monitor for clients with secondary WAN | Tom Kessler | Q4 planning | Parked |

---

**Follow-up note (2026-08-19, Marcus):** Items 1, 2, and 8 not done. Hollis Lane server migration ate the first half of August. New target 2026-09-11.

**Follow-up note (2026-09-14, Marcus):** Item 9 pulled forward and completed after the Emberline outage (REL-2609, MTG-2026-09-03-POSTMORTEM-EMS). Items 1 and 2 still open; the archive sweep has not started. RB-ACC-001 v2 and RB-PRT-001 v1 are still live pages in Atlas Docs. Moving to the Q4 backlog.

**Follow-up note (2026-10-06, Priya):** Item 6 (RB-M365-004 Teams Rooms steps) in progress. Items 1 and 2 still open, no new date.
