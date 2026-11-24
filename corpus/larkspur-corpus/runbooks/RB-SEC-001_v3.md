---
doc_id: RB-SEC-001
title: User-reported phishing email
doc_type: runbook
version: "3"
effective_date: 2025-10-20
owner: Renee Castillo
audience: internal
---

# RB-SEC-001 User-reported phishing email

## Purpose / When to use

Use when a user forwards or reports a suspicious email ("Is this real?"), uses the **Report** button in Outlook, or admits to clicking a link or opening an attachment in a suspicious email. This is a routine help-desk task. Most reports are spam or harmless; the goal is to answer the user quickly, remove the message if it is malicious, and catch the few cases where someone entered their password.

## Prerequisites / access needed

- Exchange admin center and Microsoft Defender portal (https://security.microsoft.com) via GDAP: Security Reader to look, Security Administrator or Exchange Administrator to act
- Harbor PSA
- RB-ACC-001 (password reset) for compromised accounts

## Steps

### 1. Talk to the user first (2 minutes)

1. Thank them for reporting. Never make users feel foolish for reporting; we want more reports, not fewer.
2. Ask: **Did you click anything, open an attachment, or enter your password or MFA approval?**
   - **No:** continue with step 3. Priority P3.
   - **Clicked a link but did not enter anything:** P3; continue, and check the device in Beacon (step 7).
   - **Entered password, approved an MFA prompt, or opened an attachment and enabled content:** **P2**. Jump to Section 3 now, then come back.
3. Ask the user not to forward the email to coworkers, and to delete it after we confirm we have it. If they have not used the Report button, have them use **Report > Report phishing** in Outlook (classic, new Outlook, or web). That sends it to Microsoft and the tenant's submissions list.

### 2. Look at the message

4. Defender portal > **Actions & submissions > Submissions > User reported** to see the reported message. Or find it in **Email & collaboration > Explorer** (Business Premium tenants) or a message trace (EAC > **Mail flow > Message trace**) by sender and time.
5. Quick judgment:
   - Sender address vs display name mismatch, lookalike domains (`larkspurridqe.example`), urgent payment/gift card requests, unexpected "shared document" links, voicemail or invoice attachments (.html, .htm, .svg, .zip) are typical phish.
   - A real vendor email that looks odd: verify with the sender through a known phone number, not by replying.
6. **How many people got it?** In Explorer or message trace, search by sender or subject across the tenant.

### 3. If credentials were entered or the user approved an MFA prompt

7. **Reset the user's password** per RB-ACC-001 (callback verification still applies).
8. **Revoke sessions:**
   ```powershell
   Revoke-MgUserSignInSession -UserId user@client.example
   ```
   And require MFA re-registration if the user approved a prompt they did not start (RB-ACC-002 Section B, with authorized contact confirmation).
9. **Check for attacker persistence** (Exchange Online PowerShell):
   ```powershell
   Get-InboxRule -Mailbox user@client.example | fl Name,Enabled,From,SubjectContainsWords,MoveToFolder,DeleteMessage,ForwardTo,RedirectTo
   Get-Mailbox user@client.example | fl ForwardingSmtpAddress,DeliverToMailboxAndForward
   ```
   Rules that delete, move to RSS Feeds/Archive, or forward externally are red flags. Disable them and note what you found.
10. **Check sign-in logs** in Entra for the user: successful sign-ins from unfamiliar locations or IPs after the click time.
11. If the device opened an attachment: run a full scan via Beacon RMM / Defender for Business and check for alerts.
12. Tell Renee Castillo the same hour if you found suspicious rules, foreign sign-ins, or outbound spam.

### 4. Clean up

13. **Remove the message** from all mailboxes that received it if it is malicious:
    - Business Premium (Defender for Office 365): Explorer > select messages > **Take action > Move to mailbox > Soft delete** (or Hard delete).
    - Other tenants: Tier 2 uses Purview content search and `New-ComplianceSearchAction -SearchName "<search>" -Purge -PurgeType SoftDelete`.
14. **Block the sender or domain**: Defender portal > **Policies & rules > Threat policies > Tenant Allow/Block Lists** > Domains & addresses > Block. Block URLs there too if the link domain is clearly malicious.
15. Reply to the user: what it was, what we did, and thanks.

## Priority guidance

- Single user report, no click: **P3**.
- Clicked, nothing entered: **P3**.
- Password entered / MFA approved / attachment opened with content enabled: **P2**.
- Many users received and several clicked, or the account is sending spam: **P2**, Renee Castillo immediately; P1 if mail flow for the company is affected (for example, tenant blocked from sending).
- After hours: a compromised account at a Premier client is worked by on-call (RB-GEN-002). Professional and Essentials: on-call can do the password reset and session revoke as a billable after-hours task with authorized contact approval, or first thing at 7:00 AM.

## Escalate if

- Suspicious inbox rules, external forwarding, foreign sign-ins, or outbound spam: Renee Castillo.
- Payment fraud involved (vendor bank details changed, wire sent): Renee Castillo and the client's authorized contact immediately; the client contacts their bank.
- Malware alerts on the device: Renee Castillo; isolate the device from Defender if available.
- The same campaign hits several Larkspur clients: Renee Castillo and Marcus Oyelaran.

## Ticket notes

- Sender, subject, received time, number of recipients
- What the user did (no click / clicked / entered credentials / opened attachment)
- Actions: password reset, sessions revoked, rules found/removed, message purged, sender blocked
- Sign-in log findings
- User notified of outcome

## Revision history

| Version | Date | Author | Change |
|---|---|---|---|
| 1 | 2021-02-08 | Renee Castillo | Initial phishing report procedure. |
| 2 | 2023-10-30 | Renee Castillo | Added Report Message add-in, inbox rule checks. |
| 3 | 2025-10-20 | Renee Castillo | Moved to built-in Report button, Defender portal submissions and Explorer, Tenant Allow/Block List, MFA fatigue handling. |
