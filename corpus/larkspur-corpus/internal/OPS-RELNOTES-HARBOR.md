---
doc_id: OPS-RELNOTES-HARBOR
title: Internal Tools Release and Change Log (Harbor PSA, Beacon RMM, Atlas Docs, PagerLine)
doc_type: release_notes
version: "2026-10"
effective_date: 2026-10-19
owner: Marcus Oyelaran
audience: internal
---

# Internal Tools Release and Change Log

Running log of configuration changes, automation rules, and fixes to our internal tools. Newest entries at the bottom. Add an entry for any change that affects how techs work, how SLA timers behave, or what clients see.

**Tools covered:** Harbor PSA (ticketing, time, billing), Beacon RMM (monitoring, patching, alerts), Atlas Docs (runbooks and KB), PagerLine (after-hours paging).

**Entry format:** ID | date | tool | change | why | who | impact on techs.

Change approvals: Marcus Oyelaran approves anything touching SLA timers, billing, or escalation. Priya Raman approves ticket categories and Harbor automation rules. Tom Kessler owns Beacon RMM and PagerLine configuration.

---

## 2025

### REL-2501 | 2025-01-15 | Harbor PSA
**Change:** Added required field **"Verification method"** to tickets in categories "Account - Password Reset" and "Account - MFA Reset". Options: "Callback to number on file" and "Callback to number on file + authorized contact confirmed (MFA)".
**Why:** Goes with RB-ACC-001 v3 (effective 2025-01-15). Identity verification is now by callback to the phone number on file in Harbor, plus authorized-contact confirmation for MFA resets.
**Who:** Priya Raman (config), Renee Castillo (runbook).
**Impact:** Ticket cannot be closed without the field filled in. Date of birth and employee ID are no longer options.

### REL-2502 | 2025-02-10 | Beacon RMM
**Change:** Split patch policy into two rings: **Pilot** (Larkspur internal devices plus 2-3 volunteer devices per client) installs Windows cumulative updates on Patch Tuesday + 2 days; **Broad** installs on Patch Tuesday + 7 days.
**Why:** Two bad updates in late 2024 hit all clients at once.
**Who:** Tom Kessler.
**Impact:** If a client reports an update problem, check whether the device is in Pilot first. See RB-SW-002 for Windows Update failures.

### REL-2503 | 2025-02-24 | Harbor PSA
**Change:** Automation rule: CSAT survey responses of 1 or 2 stars create a follow-up task assigned to Priya Raman, due in 1 business day.
**Why:** Low scores were sitting unread for a week or more.
**Who:** Priya Raman.
**Impact:** None for techs directly. Expect Priya to ask about the ticket.

### REL-2504 | 2025-03-03 | Harbor PSA / Atlas Docs
**Change:** RB-ACC-002 v2 published in Atlas Docs. Harbor "MFA Enrollment" checklist updated: method is **Microsoft Authenticator push with number matching**. "SMS code" removed from the method picklist.
**Why:** SMS codes are no longer allowed for new enrollments.
**Who:** Renee Castillo.
**Impact:** Use Authenticator only for new enrollments. If a user has no smartphone, escalate to Renee.

### REL-2505 | 2025-03-24 | Harbor PSA
**Change:** New categories: "Security - Phishing Report" (default P3) and "Security - Lost/Stolen Device" (default P2). Linked to RB-SEC-001 and RB-SEC-002.
**Why:** These were getting filed under "Email - Other" and "Hardware - Other", which hid them in reports.
**Who:** Priya Raman.
**Impact:** Use the new categories. Default priority can still be changed per RB-GEN-001.

### REL-2506 | 2025-04-14 | Atlas Docs
**Change:** Runbook pages now show a header banner with **version number and effective date** pulled from page metadata.
**Why:** Techs were opening runbooks without knowing which version they had.
**Who:** Marcus Oyelaran.
**Impact:** Check the banner. Older versions of a runbook can still be opened from the page history and, for some runbooks, still exist as separate pages. Always confirm you are on the newest effective date.

### REL-2507 | 2025-05-30 | Harbor PSA / PagerLine / Atlas Docs
**Change:** Greg Halvorsen (former Service Desk Lead) accounts disabled in Harbor PSA, Beacon RMM, Atlas Docs, and the old after-hours phone tree following his departure in May 2025. His open tickets reassigned to Priya Raman.
**Why:** Offboarding.
**Who:** Tom Kessler, Priya Raman.
**Impact:** Do not route anything to Greg. After-hours escalation moves to PagerLine on 2025-06-02 (REL-2508).

### REL-2508 | 2025-06-02 | PagerLine / Harbor PSA
**Change:** **PagerLine go-live** for after-hours calls. Number: **(913) 555-0142**. After-hours calls to the support line roll to PagerLine. PagerLine pages the on-call engineer from the **weekly rotation**; if no acknowledgment in **15 minutes**, pages **Tom Kessler**, then **Marcus Oyelaran**. Harbor PSA gained an **"After-Hours" ticket source flag** so after-hours tickets bill and report separately.
**Why:** Replaces the personal-cell escalation chain. Goes with RB-GEN-002 v4 (effective 2025-06-02).
**Who:** Tom Kessler (PagerLine), Marcus Oyelaran (RB-GEN-002 v4), Priya Raman (Harbor flag).
**Impact:** All after-hours work goes through PagerLine. Set the After-Hours source flag on any ticket worked outside business hours.

### REL-2509 | 2025-06-23 | Beacon RMM / PagerLine
**Change:** Beacon critical alerts for Professional and Premier clients now page through PagerLine after hours: server offline, firewall offline, and VaultLine backup job failure on servers tagged "critical".
**Why:** Alerts were only emailing the service desk inbox after hours.
**Who:** Tom Kessler.
**Impact:** On-call engineers will get alert pages, not just client calls. Alert pages open a Harbor ticket automatically.

### REL-2510 | 2025-07-14 | Harbor PSA
**Change:** **SLA timer fix.** Business-hours SLA timers were not applying the company holiday calendar, so the clocks kept running on Independence Day (Friday 2025-07-04). Holiday calendar re-linked to all SLA policies; response and resolution times recalculated for tickets opened 2025-07-03 through 2025-07-07.
**Why:** 11 tickets showed false SLA breaches on the June/July dashboard, including 2 that were about to be counted toward SLA credits.
**Who:** Priya Raman (found), Marcus Oyelaran (approved recalculation).
**Impact:** July SLA report re-run. If an SLA timer looks wrong, report it to Priya, do not edit timestamps by hand.

### REL-2511 | 2025-08-18 | Harbor PSA
**Change:** Automation rule: tickets in **"Resolved - Pending Confirmation"** auto-close after 3 business days if the ticket has three logged contact attempts. Without three attempts, the ticket goes to the stale report instead.
**Why:** Matches the closure standard in OPS-QUALITY-2025 and RB-GEN-004.
**Who:** Priya Raman.
**Impact:** Log your contact attempts as separate notes so the rule can see them.

### REL-2512 | 2025-09-08 | Beacon RMM
**Change:** Warning-level (15% free) server disk alerts now auto-create Harbor tickets; previously only critical (10% free) alerts did.
**Why:** Earlier warning gives time to clean up during business hours instead of after-hours pages.
**Who:** Tom Kessler.
**Impact:** Expect more warning-level tickets, fewer critical pages. Follow RB-SRV-001.

### REL-2513 | 2025-11-10 | Harbor PSA
**Change:** Automation rule: tickets in category "Hardware - Exception Request" auto-assign to Rachel Kim and add Marcus Oyelaran as a watcher.
**Why:** Exception requests were sitting in the general queue.
**Who:** Priya Raman, Rachel Kim.
**Impact:** File exception requests in that category and they route automatically. See STD-HW-2026.

### REL-2514 | 2025-12-15 | Harbor PSA (billing)
**Change:** 2026 rate cards loaded, effective for service dates on or after 2026-01-01: Essentials $95, Professional $145, Premier $199 per user per month; out-of-scope labor $165/hour; after-hours $247.50/hour (1-hour minimum); project work $150/hour; onsite trip charge $75 (metro); server management $175/server/month; network device management $25/device/month. 2024-2025 rate cards set to end-dated 2025-12-31.
**Why:** 2026 price change.
**Who:** Samuel Ortiz, Alicia Brandt.
**Impact:** Time entered on 2025 dates bills at 2025 rates. Do not back-date time.

## 2026

### REL-2601 | 2026-01-02 | Harbor PSA
**Change:** Business-hours calendar for all SLA policies changed to **Monday-Friday 7:00 AM - 6:00 PM CT** (was 8:00 AM - 5:00 PM), and the 2026 holiday calendar loaded (including Christmas Eve half day closing at 12:00 PM). New-user request form in the client portal now requires a start date at least **5 business days** out; shorter requests are flagged for Priya to review.
**Why:** 2026 SLA exhibit and service catalog.
**Who:** Priya Raman, Marcus Oyelaran.
**Impact:** Business-hours SLA clocks now run 7:00 AM - 6:00 PM, and 2026 holidays pause them. Portal requests under 5 business days will show a warning to the client.

### REL-2602 | 2026-02-09 | Atlas Docs
**Change:** Search results now show the version banner (version and effective date) in each result snippet. New toggle **"Show current versions only"**, off by default.
**Why:** Searches like "printer offline" were returning several versions of the same runbook with no way to tell them apart from the results list.
**Who:** Marcus Oyelaran.
**Impact:** Turn on the toggle, or check the effective date in the snippet. Old versions still appear in search unless archived.

### REL-2603 | 2026-03-16 | Beacon RMM
**Change:** Beacon agent updated to 7.2 across all managed endpoints. FortiGate WAN interface status now collected by SNMP for clients with network device management.
**Why:** Vendor end of support for agent 6.x; better visibility into firewall WAN links.
**Who:** Tom Kessler.
**Impact:** WAN interface up/down shows on the client's network dashboard. Note: this reports interface link state only, not whether traffic actually passes. (See REL-2609.)

### REL-2604 | 2026-04-20 | PagerLine
**Change:** Unacknowledged pages now repeat as a voice call every 5 minutes until acknowledged or escalated at 15 minutes. SMS fallback added if push delivery fails.
**Why:** Two near-misses in Q1 where the push notification did not wake the on-call engineer.
**Who:** Tom Kessler.
**Impact:** Expect up to three voice calls before escalation. Keep the PagerLine app's critical alert permission turned on.

### REL-2605 | 2026-05-18 | Harbor PSA
**Change:** Field technician mileage entry moved onto the dispatch record: start location, destination, miles, and auto-filled IRS standard rate for the trip date.
**Why:** Mileage was being entered in three different places.
**Who:** Isaac Brennan, Samuel Ortiz.
**Impact:** Field techs log every trip on the dispatch in Harbor PSA. The monthly mileage spreadsheet is retired for field techs.

### REL-2606 | 2026-06-29 | Atlas Docs
**Change:** New page status **"Archived"**. Archived pages are hidden from search and from the runbook index but remain readable by direct link and in history.
**Why:** Needed a way to retire superseded runbook versions without deleting them.
**Who:** Marcus Oyelaran.
**Impact:** None until pages are actually archived. The archive sweep is a separate project (see MTG-2026-07-22-RUNBOOK-REVIEW).

### REL-2607 | 2026-07-27 | Harbor PSA
**Change:** "Runbook ref" field now offers a picklist of runbook IDs (RB-GEN-001 through RB-SEC-002) instead of free text.
**Why:** Free text had typos ("RB-PRT-01", "RBNET001") that broke runbook usage reporting.
**Who:** Priya Raman.
**Impact:** Pick the runbook from the list. The picklist shows IDs only, not versions.

### REL-2608 | 2026-08-24 | PagerLine
**Change:** Holiday override schedule added so holiday coverage can be assigned independently of the weekly rotation.
**Why:** Needed for Thanksgiving and Christmas planning.
**Who:** Tom Kessler.
**Impact:** Holiday assignments appear as overrides in the PagerLine schedule.

### REL-2609 | 2026-09-10 | Beacon RMM / Harbor PSA
**Change:** New Beacon monitor for FortiGate SD-WAN **health check status** (not just link state) on every client with a secondary WAN. Alerts when the secondary WAN health check has failed for more than 10 minutes, even if the primary is up. New Harbor category "Network - WAN Failover" (default P3 when primary is up; P1 when the site is down) linked to RB-NET-004.
**Why:** Action item from the Emberline Metalworks P1 post-mortem (MTG-2026-09-03-POSTMORTEM-EMS). The secondary WAN at EMS showed "up" while its health check had been failing for weeks.
**Who:** Tom Kessler, Priya Raman.
**Impact:** Expect a batch of initial alerts as existing silent failures surface. Work them per RB-NET-004 during business hours.

### REL-2610 | 2026-10-05 | PagerLine
**Change:** Q4 2026 rotation and holiday overrides loaded (Thanksgiving, Christmas Eve, Christmas Day, New Year's Day). Matches OPS-ONCALL-2026 Section 10.
**Why:** Quarterly schedule load.
**Who:** Tom Kessler.
**Impact:** Check your weeks. Swaps go into PagerLine first.

### REL-2611 | 2026-10-19 | Harbor PSA
**Change:** SLA dashboard "at risk" (yellow) threshold changed from 90% to **75%** of the response target elapsed.
**Why:** At 90% there was not enough time to react on 15-minute and 30-minute P1 targets.
**Who:** Priya Raman, approved by Marcus Oyelaran.
**Impact:** More tickets will show yellow. That is intended; grab them sooner.
