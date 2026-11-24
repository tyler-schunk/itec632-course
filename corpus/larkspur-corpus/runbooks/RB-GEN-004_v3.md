---
doc_id: RB-GEN-004
title: Ticket notes and closure standards
doc_type: runbook
version: "3"
effective_date: 2025-09-15
owner: Priya Raman
audience: internal
---

# RB-GEN-004 Ticket notes and closure standards

## Purpose / When to use

Every ticket, every time. These standards exist so that anyone can pick up a ticket cold, so the client sees what we did, so billing is accurate, and so business reviews have real data. Priya Raman audits a sample of closed tickets every week against this runbook.

## Prerequisites / access needed

- Harbor PSA technician login
- Familiarity with RB-GEN-001 (priorities) and the runbook catalog in Atlas Docs

## Note types in Harbor PSA

- **Internal note:** technician-only. Troubleshooting detail, credentials references (never the credential itself), escalation chatter.
- **Discussion (client-visible):** what the client sees in the portal and in emails. Plain language, no jargon dumps, no blame.
- **Resolution:** required at closure. Client-visible.

## Steps

### While working the ticket

1. **First note within the response SLA.** The first human response (call, voicemail, or personal reply) is logged as a Discussion note with the method used, for example "Called Jane at 9:12 AM, left voicemail, sent portal reply."
2. **Use the standard internal note format** for each work session:
   ```
   Symptom: what the user reports, in their words where useful
   Scope: who/what is affected (user, asset tag LR-XXX-####, site, # users)
   Steps taken: numbered, specific (commands run, settings changed, results)
   Result: fixed / partially fixed / not fixed
   Next step: what happens next and who owns it
   ```
3. **Be specific.** "Fixed printer" fails audit. "Stopped spooler, cleared C:\Windows\System32\spool\PRINTERS, started spooler, test page OK" passes.
4. **Never paste passwords, MFA codes, recovery keys, or Temporary Access Passes** into any note. Write "credential stored in LockBox Vault entry <name>" or "TAP issued by phone."
5. **Record identity verification** for any password, MFA, or access change: method and who confirmed (see RB-ACC-001 and RB-ACC-002).
6. **Record approvals** for anything billable or anything needing authorization (approver name, role, time).
7. **Keep runbook_ref accurate.** If you ended up using a different runbook than triage expected, update the field.
8. **Update the client** at the cadence for the priority: P1 every 30 minutes, P2 at least every 2 hours, P3 at least once per business day while active, P4 when status changes.

### Time entry

9. Enter time **against the ticket**, not at end of day from memory. Increments are 15 minutes for business-hours work.
10. Choose the correct **work type**: Remote, Onsite, After Hours, or Project. Work type drives billing and the Professional onsite bucket.
11. After-hours billable work has a 1-hour minimum; enter actual time and Harbor applies the minimum on the invoice.
12. If you believe the work is out of scope (not covered by the client's tier), mark the entry **Billable - Review**. The account manager reviews before invoicing. Do not argue billing with the user.

### Closure

13. **Confirm with the user** that the issue is resolved before closing. A call or a reply saying "it's working" is ideal.
14. If the user does not respond, use the **3-touch rule**: three contact attempts over at least 3 business days (for example, call + email on day 1, email on day 2, final email on day 3 stating the ticket will close). Then close with status **Closed - No Response**. The user can reply to reopen within 7 days.
15. **Write the Resolution note** (client-visible): one to three sentences, plain language. What was wrong, what we did, anything the user should do.
16. **Set the closure fields:** root cause category, runbook_ref, and whether a knowledge gap was found ("Runbook update needed" checkbox). Checking the box sends the ticket to the runbook owner listed in Atlas Docs.
17. **Do not close parent tickets** until all child tickets are resolved and the client has a summary.

## Priority guidance

- Do not change priority silently. If you change it, add an internal note with the reason.
- Closing a P1 requires a short internal summary: start time, resolution time, cause, and whether the 4-hour resolution target was met. Priya or Marcus reviews every P1 within 2 business days.

## Escalate if

- A user refuses to confirm closure but the issue is clearly fixed: Priya Raman.
- You find you have been entering time to the wrong ticket or client: tell Samuel Ortiz (billing) before month-end invoicing.
- A client complains about note quality or what they see in the portal: Priya Raman.

## Ticket notes example (passes audit)

> Symptom: User (front desk, Foxhaven Dental) reports printer "offline" in Windows. Scope: 1 user, LR-FHD-0217, other PCs print fine. Steps: 1) Pinged printer 10.20.1.45 OK, web UI loads. 2) Stopped Spooler, cleared spool folder (3 stuck jobs), started Spooler. 3) Test page printed. Result: fixed. Next step: none. Verified with user by phone 10:42 AM. runbook_ref RB-PRT-001.

## Revision history

| Version | Date | Author | Change |
|---|---|---|---|
| 1 | 2020-02-03 | Greg Halvorsen | Initial notes standard. |
| 2 | 2023-05-22 | Greg Halvorsen | Added 3-touch closure rule and work types. |
| 3 | 2025-09-15 | Priya Raman | Ownership to Priya Raman. Added standard note format, credential rule, runbook update checkbox, P1 closure summary. |
