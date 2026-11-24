---
doc_id: OPS-QUALITY-2025
title: Service Desk Quality Guide
doc_type: guide
version: "2025"
effective_date: 2025-03-03
owner: Priya Raman
audience: internal
---

# Service Desk Quality Guide (2025)

**Owner:** Priya Raman, Service Desk Manager
**Applies to:** Tier 1, Tier 2, and Field Technicians; anyone who touches a client ticket
**Related runbooks:** RB-GEN-001 (Ticket triage and priority assignment), RB-GEN-004 (Ticket notes and closure standards)

This guide is the "how we do the work well" companion to the runbooks. The runbooks tell you what steps to take. This tells you what good looks like, how we measure it, and how often we look at the numbers.

## 1. The Short Version

- Every interaction gets a ticket. No exceptions, including "quick questions" in the hallway at a client site.
- Pick the right priority (RB-GEN-001) and the right category. Bad categories wreck our reporting.
- Write notes the next tech can pick up without calling you.
- Tell the client what happens next and when.
- Close tickets with a resolution the client can understand.
- Targets: **CSAT 4.6 / 5 or better**, **first-contact resolution 65% or better**, zero missed P1 response targets.

## 2. Ticket Hygiene

### 2.1 Creating the ticket

Every ticket in Harbor PSA needs:

| Field | What good looks like |
|---|---|
| Client | Correct client code (EMS, DPA, etc.). Do not file under "Larkspur Internal" because you could not find the client. |
| Contact | The actual person who reported it, with the callback number confirmed. |
| Summary | Specific. "Outlook keeps asking for password - J. Ruiz" not "Email issue". |
| Priority | Per RB-GEN-001. Priority is about business impact, not how loud the caller is. |
| Category / subcategory | The closest match. If nothing fits, use "Other" and tell Priya so we can add a category. |
| Asset | Link the device (LR-XXX-#### tag) when the issue is device-specific. |
| Runbook ref | The runbook you followed, e.g. RB-PRT-001. Leave blank only if no runbook applies. |

### 2.2 While you work it

- **Time entries:** enter time against the ticket the same day, in the ticket, not in a spreadsheet. Billing depends on this.
- **Status:** keep it honest. "Waiting on Client" only when we actually asked the client for something and are waiting. "Waiting on Vendor" only with a vendor case number in the notes.
- **Internal vs. external notes:** internal notes for tech detail and anything we would not say to the client. External notes are visible in the portal and emailed to the contact. Proofread external notes.
- **No passwords in tickets.** Ever. Credentials live in LockBox Vault. If a client emails a password, redact it from the ticket and ask them to change it.
- **Touch rule:** an open ticket with no update in 2 business days shows on the stale ticket report. If you are waiting on something, say so in a note.

### 2.3 Closing the ticket

Follow RB-GEN-004. At minimum the resolution note has:

1. What the problem actually was (cause, if known).
2. What we did to fix it.
3. How we confirmed it was fixed (and with whom).
4. Anything the client needs to do or watch for.

Bad: "Fixed."
Good: "Print queue was stuck on a 400-page job. Stopped spooler, cleared the queue, restarted spooler per RB-PRT-001. Printed a test page with Karen at the front desk. No further action needed."

Do not close a ticket the client has not confirmed unless we have made three contact attempts over at least 3 business days (the 3-touch rule in RB-GEN-004). Note each attempt.

## 3. Tone With Clients

Our tagline is "IT that answers the phone." Clients stay with us because talking to us is easy. That is a skill, and we coach it like any other technical skill.

### 3.1 On the phone

- Answer: "Thank you for calling Larkspur Ridge IT, this is [name]. How can I help?"
- Let them finish describing the problem before you start troubleshooting.
- Restate the problem in one sentence so they know you heard it.
- Explain what you are doing in plain language when you are on their screen. Do not go silent for two minutes.
- Never blame the user, even when it is the user. "Let's get this sorted out" beats "You shouldn't have clicked that."
- If you need to put them on hold, ask first and check back at least every two minutes.
- End with what happens next: "I've reset it, and you should get a confirmation email in a few minutes. If you don't, call us back and reference ticket TCK-1xxxxx."

### 3.2 In writing

- Lead with the answer or the status, then the detail.
- No jargon the client did not use first. "Your computer could not reach the printer" instead of "DNS resolution failure on the print server".
- No all caps, no exclamation-point stacks, no sarcasm.
- Sign with your name. Clients like knowing who helped them.

### 3.3 Frustrated clients

- Acknowledge the frustration specifically ("I know payroll is due today and this is the worst timing").
- Do not argue about whether it is a P1. Escalate the conversation to Priya or the Tier 2 lead on shift if the priority is disputed.
- If a client is abusive, you may end the call politely and tell your manager. See the handbook on harassment.

### 3.4 Healthcare and legal clients

Many of our clients handle patient or legal records. Do not read anything on screen you do not need to read. Do not repeat what you saw. If a client starts sharing patient details that you do not need, politely stop them.

## 4. Metrics and Targets

| Metric | Target | Source |
|---|---|---|
| CSAT (customer satisfaction) | **4.6 / 5** average or better, rolling 30 days | Harbor PSA closure survey (1-5 stars) |
| First-contact resolution (FCR) | **65%** or better | Harbor PSA: tickets resolved on first interaction with no reopen within 5 business days |
| P1 response | 100% within SLA | Harbor PSA SLA dashboard |
| P2-P4 response | 95% within SLA | Harbor PSA SLA dashboard |
| Resolution | 90% within target | Harbor PSA SLA dashboard |
| Stale tickets | Fewer than 10 open tickets with no update in 2 business days | Stale ticket report |
| Reopen rate | Under 5% | Harbor PSA |

### 4.1 CSAT

- Every closed ticket triggers a one-question survey (1 to 5 stars, optional comment).
- Any 1 or 2 star response creates a follow-up task for Priya. Priya or the tech's lead calls the client within 1 business day.
- Good comments get read out in the weekly service delivery meeting. Name the tech.
- Do not ask clients to give you 5 stars. Just do good work.

### 4.2 First-contact resolution

FCR counts tickets solved during the first interaction (call, chat, or walk-up) without a hand-off and without the client coming back about the same issue within 5 business days.

Things that help FCR:
- Tier 1 handles password resets, MFA re-registration, printer offline, Outlook profile rebuilds, and basic OneDrive sync on the first call, following the runbooks.
- Know when not to chase FCR. A P1 or anything needing Tier 3 should be escalated right away. Escalating correctly is better than a long, failed first attempt.

Things that do not count as FCR: tickets created by Beacon RMM alerts, P4 scheduled work (new users, offboarding, projects), and onsite dispatches.

### 4.3 SLA targets

Current SLA response and resolution targets by tier and priority are in the client SLA exhibit and RB-GEN-001. The Harbor PSA SLA timers are configured to match. If a timer looks wrong, report it to Priya rather than working around it.

## 5. SLA Dashboard Review Cadence

| When | Who | What |
|---|---|---|
| **Start of each shift** | Shift Tier 2 lead | Harbor PSA SLA dashboard: anything at risk (yellow) or breached (red). Reassign as needed. |
| **Daily at 11:30 AM and 3:30 PM** | Priya Raman (or delegate) | Midday and late-day sweep of the at-risk list and unassigned queue. |
| **Weekly, Tuesday** service delivery meeting | Marcus Oyelaran, Priya Raman, Tier 2/3 leads, Isaac Brennan | Prior week: SLA response/resolution by priority, CSAT, FCR, stale ticket count, any missed P1. Every missed P1 gets a short review. |
| **Monthly, first week** | Marcus Oyelaran, Priya Raman, Jordan Pike | Month-end SLA report by client. Feeds SLA credit calculation (Samuel Ortiz) and business review talking points (Jordan Pike). |
| **Quarterly** | Leadership | Trend review at the quarterly all-hands; targets revisited. |

Missed P1 response targets trigger the SLA credit in the client agreement (5% of the monthly managed-services fee per miss, capped at 20%). Priya notifies Samuel Ortiz of each one by the 3rd business day of the following month.

## 6. Ticket Quality Reviews

Each month Priya pulls **5 random closed tickets per technician** and scores them:

| Item | Points |
|---|---|
| Correct client, contact, and asset | 1 |
| Correct priority and category | 2 |
| Runbook referenced where one applies | 1 |
| Notes clear enough for another tech to follow | 2 |
| Client informed of next steps | 1 |
| Resolution note meets RB-GEN-004 | 2 |
| Time entered same day | 1 |
| **Total** | **10** |

Target is an average of 8 or better. Scores are shared one-on-one, not posted. They feed the annual review along with CSAT and FCR, but they are one input among several.

## 7. Coaching

- New technicians shadow a Tier 2 for their first two weeks and have their first 20 tickets reviewed by Priya or a Tier 2 before closing.
- Monthly one-on-ones include a look at the tech's CSAT comments and quality review scores.
- When a runbook is unclear or wrong, tell the runbook owner (listed in Atlas Docs). Fixing the runbook helps everyone.

## 8. Changes to This Guide

Suggestions go to Priya. The guide is reviewed annually, with target changes announced at the quarterly all-hands.
