# Larkspur Ridge IT - Data Dictionary

Structured operational data for the fictional MSP **Larkspur Ridge IT** (ITEC 632 corpus).
Data extracted from Harbor PSA on
**Monday 2026-11-02 08:00 CT**; tickets cover **2025-01-07 to 2026-10-30** (created_at).

Files: `larkspur.db` (SQLite; same six tables), one CSV per table, `tickets_sample_100.jsonl`.

**The `tickets` table is a sample.** It is a representative sample of about 1,500 client tickets exported from Harbor PSA
for the course, not every ticket Larkspur worked in the period. Dashboard totals quoted in meeting notes and other
documents (ticket volumes, CSAT, P1 counts) come from the full Harbor PSA and will not match counts computed from this sample.

## Conventions

* **Timestamps** are US Central local time, naive (no offset), minute resolution: `YYYY-MM-DD HH:MM`. Dates are `YYYY-MM-DD`.
* **Booleans** are integers `1`/`0` in SQLite and CSV (`true`/`false` in the JSONL sample).
* **NULL** is an empty field in CSV.
* **Business hours:** Monday-Friday 07:00-18:00 CT, closed on company holidays. Christmas Eve is a half day (07:00-12:00).
  Holidays used: 2025-01-01, 2025-05-26, 2025-07-04, 2025-09-01, 2025-11-27, 2025-11-28, 2025-12-24 (half), 2025-12-25,
  2026-01-01, 2026-05-25, 2026-07-03 (Independence Day observed), 2026-09-07, 2026-11-26, 2026-11-27, 2026-12-24 (half), 2026-12-25.
* A **business day** is 660 business minutes (11 hours).

## Simplifications

* `sla_response_met` and `after_hours` are computed with the **2026 business hours (07:00-18:00)** and the **2026 SLA table**
  for the whole date range, even though business hours in 2025 were 08:00-17:00 (they changed on 2026-01-01). This is a
  known simplification; students may notice that some 2025 tickets would be flagged differently under the 2025 hours.

## Table `clients` (40 rows)

| Column | Type | Description |
|---|---|---|
| code | TEXT PK | 3-letter client code (e.g. `EMS`). Used in asset tags and hostnames. |
| name | TEXT | Client legal/trade name. |
| industry | TEXT | The client's industry. |
| city, state | TEXT | Location (KS or MO). |
| users | INTEGER | Managed users (total 1,287). |
| tier | TEXT | `Essentials`, `Professional`, `Premier`. |
| client_since | INTEGER | Year the client signed. |
| primary_contact_id | TEXT FK contacts | Day-to-day contact (usually the office manager). |
| authorized_contact_id | TEXT FK contacts | Person who approves MFA resets, access changes, purchases. May equal the primary contact. |
| email_domain | TEXT | Client email domain (`*.example`). |
| main_phone | TEXT | Main office number (fictional 555-01xx range). |
| backup_included | INTEGER | 1 if VaultLine backup is managed (always for Professional/Premier; Essentials only with the $6/user add-on). |
| has_voip | INTEGER | 1 if the client has Yealink desk phones managed by Larkspur. |
| sites | INTEGER | Number of physical locations. |

## Table `contacts` (164 rows)

Key client-side people who submit and approve tickets (3-6 per client, scaled by size). Not every employee:
descriptions often mention other staff by first name who are not in this table.

| Column | Type | Description |
|---|---|---|
| contact_id | TEXT PK | `C-<CODE>-NN`. |
| client_code | TEXT FK clients | |
| first_name, last_name, title | TEXT | Fictional people. |
| email | TEXT | `<local>@<client domain>`; local-part pattern varies by client. |
| phone | TEXT | Client main number plus extension (this is the "number on file" used for callback verification). |
| is_authorized_contact | INTEGER | 1 for the client's authorized contact. |
| is_vip | INTEGER | 1 for owners/executives (a fully blocked VIP is P2 per the priority definitions). |

## Table `technicians` (17 rows)

| Column | Type | Description |
|---|---|---|
| tech_id | TEXT PK | `TECH-NN`. |
| name | TEXT | Larkspur staff member. |
| role | TEXT | Job title. |
| tier_level | INTEGER | 1 = Tier 1, 2 = Tier 2 / field / desk lead / manager, 3 = engineers (systems, projects). |
| hire_date | TEXT | |
| termination_date | TEXT | Only Greg Halvorsen (2025-05-16). |
| active | INTEGER | 0 for Greg Halvorsen. |

Staffing rules visible in tickets: Greg Halvorsen appears only on tickets created on/before 2025-05-16; Emily Sandoval
only from 2026-02-02; Noah Whitaker only from 2026-06-08. After-hours tickets go to the on-call engineer: before
2025-06-02 Greg Halvorsen (then Tom Kessler after Greg left); from 2025-06-02 the weekly PagerLine rotation
(Monday 07:00 to Monday 07:00) Andre Mitchell -> Grace Liu -> Brian Novak -> Renee Castillo -> Tom Kessler -> Lena Fischer
(Andre holds the week starting 2026-08-31). Onsite work is usually reassigned to a field technician.

## Table `assets` (2386 rows)

| Column | Type | Description |
|---|---|---|
| asset_tag | TEXT PK | `LR-<CODE>-####`, numbered per client in purchase order (one exception: the EMS primary firewall is `LR-EMS-0007`). |
| client_code | TEXT FK clients | |
| hostname | TEXT | `<CODE>-LT###` laptops, `<CODE>-DT###` desktops, `<CODE>-SHOP##` shop-floor PCs, `<CODE>-FS01`/`DC01`/`APP01`... servers, `-FW`, `-SW`, `-AP`, `-PRN`, `-NAS`. NULL for desk phones. |
| type | TEXT | laptop, desktop, server, firewall, switch, access_point, printer, phone, nas. |
| make, model | TEXT | Dell Latitude/OptiPlex/Precision/PowerEdge, Apple MacBook Pro (design clients), Fortinet FortiGate, Ubiquiti UniFi, HP/Brother, Yealink, Synology. |
| ram_gb | INTEGER | Computers and servers only. |
| os | TEXT | Windows 11 Pro / Windows 10 Pro 22H2 / macOS / Windows Server / FortiOS / UniFi / DSM / Yealink firmware. NULL for printers. |
| assigned_contact_id | TEXT FK contacts | Primary user if that user is a listed contact; otherwise NULL. |
| purchase_date, warranty_end | TEXT | Computers 3-year ProSupport; servers 5 years; network/printers/phones vendor default. |
| status | TEXT | active, retired, in_repair. |
| last_seen | TEXT | Last Beacon RMM check-in (<= 2026-11-02). For retired assets, the retirement date. |
| notes | TEXT | Free text: Windows 10 retirement/replacement, straggler exceptions, repair status, server role. |

Hardware standards reflected: laptops bought in 2024-2025 are mostly **Latitude 5440, 16 GB** (2024 standard);
laptops bought in 2026 are mostly **Latitude 5550, 32 GB** (2026 standard), with some Latitude 5450 (the 14" option, also 32 GB);
desktops bought from mid-2025 on are OptiPlex Micro 7020, 16 GB (earlier ones are OptiPlex Micro 7010).
Windows 10 machines (bought 2019-2020) were mostly retired and replaced, the majority in **Aug-Oct 2025** before the
2025-10-14 end of support. 12 Windows 10 machines are still active or in repair (stragglers, flagged in `notes`).
Servers exist only where the client has on-prem infrastructure; many clients have none.

## Table `sla_targets` (12 rows)

Exactly the target table in the current SLA exhibit (`client-docs/SLA-EXH-2026.md`, Section 3), applied to the whole ticket range.

| tier | priority | response_minutes | response_clock | resolution_business_minutes | resolution_clock |
|---|---|---|---|---|---|
| Essentials | P1 | 60 | business | 240 | business |
| Essentials | P2 | 120 | business | 480 | business |
| Essentials | P3 | 240 | business | 1320 | business |
| Essentials | P4 | 660 | business | 3300 | business |
| Professional | P1 | 30 | 24x7 | 240 | 24x7 |
| Professional | P2 | 60 | business | 480 | business |
| Professional | P3 | 240 | business | 1320 | business |
| Professional | P4 | 660 | business | 3300 | business |
| Premier | P1 | 15 | 24x7 | 240 | 24x7 |
| Premier | P2 | 60 | 24x7 | 480 | business |
| Premier | P3 | 120 | business | 1320 | business |
| Premier | P4 | 660 | business | 3300 | business |

`response_clock = business` means the clock only runs during business hours; `24x7` means wall-clock minutes.
"1 business day" = 660, "2 business days" = 1320, "5 business days" = 3300, "8 business hours" = 480.
P1 resolution is "4 hours" for every tier; it uses the same clock as that tier's P1 response.

## Table `tickets` (1502 rows)

| Column | Type | Description |
|---|---|---|
| ticket_id | TEXT PK | `TCK-1xxxxx`. Harbor PSA numbers all Larkspur work (internal, projects, other queues), so client ticket IDs are **not contiguous**; they increase with created_at across TCK-100001..TCK-120000. |
| created_at | TEXT | When the ticket was created (CT). |
| client_code | TEXT FK clients | |
| contact_id | TEXT FK contacts | Requester. **NULL for `rmm_alert` tickets** (machine-generated). |
| channel | TEXT | phone, email, portal, rmm_alert. |
| subject | TEXT | As submitted (can be vague, e.g. "help!!"). RMM/VaultLine subjects are machine-formatted. |
| description | TEXT | Requester's own words (phone tickets are the caller's words as typed at intake). Includes typos, forwarded fragments, sign-offs. |
| category | TEXT | One of the 12 categories below. |
| subcategory | TEXT | Snake-case subcategory (see below). |
| priority | TEXT | P1-P4 as defined in `client-docs/SLA-EXH-2026.md` (Section 2). |
| status | TEXT | closed, open, in_progress, waiting_on_client (non-closed only near the extract date). |
| assigned_tech_id | TEXT FK technicians | |
| first_response_at | TEXT | First human response. |
| resolved_at | TEXT | NULL if not closed. |
| resolution_notes | TEXT | Technician's closing notes (style varies by technician). NULL for non-closed tickets (and see quirks). |
| runbook_ref | TEXT | Atlas Docs runbook ID used (see `runbooks/`), nullable. |
| billable | INTEGER | Work billed outside the flat fee (rules below). |
| after_hours | INTEGER | 1 if the ticket was created **and** first responded to outside business hours (i.e. after-hours work happened). |
| sla_response_met | INTEGER | 1 if first response met the tier/priority target using that target's clock. |
| csat | INTEGER | 1-5 survey score, NULL if no response (~35% of closed human tickets respond). |
| onsite | INTEGER | 1 if a technician visited the client site. |
| labor_minutes | INTEGER | Time logged (includes travel for onsite tickets). |
| asset_tag | TEXT FK assets | Device involved, when known (RMM alerts, hardware tickets, Windows 10 replacements). |

**Priority mix:** P1 32 (2.1%), P2 167 (11.1%), P3 840 (55.9%), P4 463 (30.8%).

**Categories and subcategories (ticket counts):**

| Category | Tickets | Subcategories |
|---|---|---|
| Account/Access | 275 | account_locked, folder_permissions, login_issue, mfa_reenrollment, mfa_reset, password_reset |
| Email/M365 | 215 | email_delivery, email_signature, mailbox_full, onedrive_sharepoint, outlook_issue, shared_mailbox_calendar, spam_quarantine, teams_issue |
| Hardware | 216 | dock_monitor, laptop_damage, new_workstation, peripheral, slow_computer, wont_boot, workstation_replacement |
| Printing/Scanning | 109 | print_quality_jam, printer_offline, printer_setup, scan_to_email |
| Network/Internet | 87 | internet_outage, network_other, slow_network, vpn, wan_down_alert, wifi |
| Software | 185 | app_error, license_request, lob_app_issue, software_install, windows_update |
| Backup/Restore | 44 | backup_failure, email_restore, file_restore |
| Onboarding/Offboarding | 161 | new_user, offboarding, user_change |
| Phone/VoIP | 44 | call_quality, phone_not_registering, voicemail_forwarding |
| Security Report | 60 | av_alert, lost_device, phishing_report, suspicious_activity |
| Server/Infrastructure | 27 | server_hw_alert, server_low_disk, server_request, server_unresponsive |
| General Request | 79 | how_to_question, office_move_project, purchase_quote, report_request, vendor_coordination |

### Derived-field rules

* **sla_response_met** = elapsed(created_at, first_response_at) <= `sla_targets.response_minutes` for the client's tier and the
  ticket's (labeled) priority. Elapsed is business minutes when `response_clock = business`, wall-clock minutes when `24x7`.
* **after_hours** = created_at outside business hours AND first_response_at outside business hours.
* **billable** = 1 when any applies (per the current service catalog, `client-docs/SVC-CAT-2026.md` Sections 2, 5 and 8):
  * subcategory is quoted project work (`office_move_project`, `workstation_replacement`) - every tier;
  * after_hours and tier = Essentials;
  * after_hours and tier = Professional and priority != P1;
  * onsite and tier = Essentials;
  * onsite and tier = Professional and the client's onsite `labor_minutes` for that calendar month (by created_at, in ticket order)
    exceed the 240 included minutes - the ticket that crosses 240 and later onsite tickets that month are billable.
  * Premier after-hours and onsite work is included (not billable). Tickets closed as duplicates/related are never billable.
  * Exception: Tom Kessler's onsite visit on the EMS outage (TCK-118742) is not counted against EMS's included onsite
    minutes (per the post-mortem) and is not billable (P1 after-hours work is included for Professional).

### Events and patterns in the data

* **Mar-Apr 2025** MFA re-enrollment wave after the 2025-03-03 switch to Authenticator push with number matching (SMS retired).
* **Aug-Oct 2025** Windows 10 end-of-life replacements (Hardware / `workstation_replacement`, linked to replacement assets).
* **January and June** onboarding bursts (summer staff at the school and child-care clients).
* **Tuesday 2026-09-01** Emberline Metalworks (EMS) P1 internet outage: fiber cut ~05:35, **TCK-118742** (RMM alert, 05:41,
  first response 05:58 by on-call Andre Mitchell, escalated to Tom Kessler, who went onsite and owns the ticket), traffic restored over secondary WAN 07:21,
  primary 12:04; related user tickets that morning closed as related; RCA request the next day.
* Hollis Lane CPAs volume rises in tax season (Jan-Apr); the Montessori school is quiet in July.
* Most tickets meet SLA; misses cluster on Mondays and on business days next to holidays.
* Notes follow procedures in effect at the time (e.g. password resets before 2025-01-15 verified identity by employee ID/DOB
  under RB-ACC-001 v2; from 2025-01-15, callback to the number on file; MFA notes mention number matching only from 2025-03-03;
  after-hours notes mention PagerLine only from 2025-06-02).

## Known data-quality issues (planted on purpose)

Real PSA data is messy. These are deliberate; finding and handling them is part of the exercises.

1. **Wrong category labels (~3%, 45 tickets).** The description and notes clearly describe one kind of
   issue but `category`/`subcategory` name another (a technician picked the wrong dropdown).
2. **Priority mislabels (~2%, 30 tickets).** E.g. a single-user request marked P1/P2, or a multi-user outage marked P4.
   SLA fields were computed by Harbor from the labeled priority, as they would be in the real system.
3. **Duplicate submissions (~1%, 15 tickets).** Same requester, same issue, minutes apart (often a
   different channel); the later one is closed with a note pointing to the original.
4. **Missing resolution notes (7 closed tickets)** have NULL `resolution_notes`.
5. **Low-quality notes (~40 tickets)** such as "fixed" or "done" that do not meet the RB-GEN-004 closure standard.
6. **Inconsistent email capitalization (6 contacts)** e.g. upper-case local parts or a
   capitalized domain. Email matching should be case-insensitive.
7. Tickets closed after three unanswered contact attempts ("closing per 3-strike policy") have no confirmation from the user.
8. `rmm_alert` tickets have no contact and no CSAT.
