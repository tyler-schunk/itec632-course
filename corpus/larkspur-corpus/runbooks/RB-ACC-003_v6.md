---
doc_id: RB-ACC-003
title: New user onboarding
doc_type: runbook
version: "6"
effective_date: 2026-01-12
owner: Renee Castillo
audience: internal
---

# RB-ACC-003 New user onboarding

## Purpose / When to use

Use for every new employee at a client: account creation, licensing, groups and shared resources, MFA, device, and first-day support. Also use for rehires (check for a disabled or deleted account first, see step 5). Contractors and temporary accounts follow the same steps with an expiration date set.

Onboarding is a P4 request by definition, but it has a hard date attached (the start date). Late onboarding is one of the most visible failures we can have with a client, so treat the start date like a deadline.

## Notice requirement

- Clients must request new users **at least 5 business days before the start date.** This is in the 2026 service catalog and the client onboarding form.
- If a request arrives with less than 5 business days of notice: accept it, set P4, tell the requester we will do our best but cannot guarantee everything (especially hardware) will be ready, and flag the account manager (Alicia Brandt or Kevin Duong) in an internal note. Do not refuse the request.
- Hardware that must be ordered (Dell build-to-order) typically takes 5-10 business days. If the client wants a new laptop and gives short notice, offer a loaner from the client's spare pool if they have one (check their Atlas Docs page).

## Prerequisites / access needed

- Harbor PSA: the client's **New User Request** form submitted through the portal, or an email from an authorized contact
- M365 admin center / Entra admin center via GDAP: User Administrator and License Administrator at minimum; Exchange Administrator for mailbox and distribution group work
- Intune admin center (for Autopilot and device assignment)
- For hybrid clients: Beacon RMM session to a DC or RSAT workstation; domain admin credential from LockBox Vault
- Client's Atlas Docs page: naming convention, license type, standard groups, shared mailboxes, line-of-business apps, printers, and the **onboarding template** for that client
- RB-ACC-002 (MFA) and RB-HW-002 (workstation deployment)

## Information we need from the client

The New User Request form collects these. If anything is missing, ask the requester before you start (one consolidated email, not five).

- Legal first and last name, preferred name if different
- Start date and start time, work location (which site for multi-site clients like Sunbeam Child Care Centers or Arbor Mill Storage)
- Job title, department, manager
- Personal mobile number for the Harbor PSA contact record (used for callbacks per RB-ACC-001)
- "Same access as" another user, or an explicit list of groups, shared mailboxes, Teams, SharePoint sites, and apps
- Device: new laptop/desktop, reuse existing (asset tag), or bring their own (BYOD needs client approval and app protection only)
- License: Business Standard or Business Premium (default per client page)
- Phone extension needed (Yealink desk phone) yes/no
- Approval from an authorized contact (form submitted by an authorized contact counts)

## Steps

### 1. Validate the request

1. Confirm the requester is an **authorized contact** in Harbor PSA. If not, forward the request to the authorized contact for approval and set the ticket to Waiting on Client.
2. Check the start date against the 5-business-day notice requirement and flag short notice as above.
3. Set priority **P4**, runbook_ref **RB-ACC-003**, and due date = the business day before the start date.
4. Create the user's **Harbor PSA contact record** now (name, title, mobile, email to be). This is the "number on file" for future password and MFA callbacks, so get it right.

### 2. Check for an existing account

5. Search Entra ID and (for hybrid) AD for the name. Rehires may have a disabled account or a deleted one. Deleted Entra users can be restored for 30 days (Entra admin center > **Identity > Users > Deleted users**). If the old account is restorable and the client wants the same address, restore it rather than creating a duplicate.

### 3. Create the account

**Cloud-only tenant:**

6. M365 admin center > **Users > Active users > Add a user**.
   - First/last name, display name per client convention (most clients: "First Last")
   - Username per client convention (most clients: first.last@domain or firstinitiallast@domain; check the client page)
   - Auto-generate password, require change at first sign-in. Do not email the password.
   - Location: United States
   - Assign license: Microsoft 365 Business Standard or Business Premium per request. If no license is available, see step 8.
   - Profile info: job title, department, manager, office (these feed the global address list and some clients' email signatures)
7. PowerShell alternative for bulk or templated creates:
   ```powershell
   Connect-MgGraph -Scopes "User.ReadWrite.All","Group.ReadWrite.All" -TenantId <tenant>
   $pw = @{ Password = "<temp>"; ForceChangePasswordNextSignIn = $true }
   New-MgUser -DisplayName "Jane Doe" -GivenName Jane -Surname Doe `
     -UserPrincipalName jane.doe@client.example -MailNickname jane.doe `
     -AccountEnabled -PasswordProfile $pw -UsageLocation US `
     -JobTitle "Office Manager" -Department "Front Office"
   ```

**Hybrid tenant:**

- Create the user in AD in the correct OU (the OU must be in Entra Connect sync scope; the client page lists it). Copying the "same as" user in ADUC copies group memberships, which is usually what the client wants, but review the groups.
- Set the UPN suffix to the client's email domain, not .local.
- Run `Start-ADSyncSyncCycle -PolicyType Delta` on the Entra Connect server, wait for the user to appear in Entra, then assign the license in the M365 admin center.

8. **Licensing:** if the tenant has no spare license, do not buy one on your own. Larkspur bills licenses through the client's agreement, so the account manager or the authorized contact must approve the purchase. Note the approval, then add the license through our distributor portal (Projects team or Renee if you do not have access). Business Premium is required for clients using Intune device management and Defender for Business; do not assign Standard to a user at a Premium-managed client without asking.

### 4. Groups, mailboxes, and access

9. Add security groups and Microsoft 365 groups per the "same as" user or the explicit list. Check Teams membership and SharePoint site access, not just groups.
10. Add distribution lists in Exchange admin center > **Recipients > Groups**.
11. Shared mailboxes and calendars: follow RB-M365-002. Full Access with automapping is the usual default.
12. Line-of-business apps (dental imaging, practice management, dealer management, accounting packages): most are not ours to administer. Note in the ticket which apps need accounts and tell the client who owns that system. If our client page says we create accounts in that app, do it and document it.
13. Printers: add the user's printers per the client page; most are deployed by Intune or by GPO and will appear automatically.
14. Phone: if a Yealink extension is needed, the client's VoIP provider usually provisions the extension. Open a child ticket for the phone and coordinate with the provider; Larkspur handles placing and connecting the phone (RB-VOIP-001).

### 5. Device

15. Follow **RB-HW-002 New workstation deployment**. Standard laptop (2026 hardware standard): Dell Latitude 5550, Intel Core Ultra 5, 32 GB RAM, 512 GB SSD, 3-year ProSupport. Standard desktop: Dell OptiPlex Micro 7020, 16 GB.
16. For Autopilot devices, assign the device to the user in Intune so the user sees their name at first sign-in (Intune admin center > **Devices > Windows > Windows enrollment > Devices**, select device > **Assign user**).
17. Reused devices: wipe and re-provision (Intune **Autopilot Reset** or **Wipe**). Do not hand a new user a device with the previous user's profile on it.
18. Record the asset tag (`LR-<CLIENT>-####`) against the user's contact in Harbor PSA.

### 6. MFA and first sign-in

19. Schedule the first-day sign-in with the new user (call at start time, or field tech onsite if the client asked for onsite setup). Use **RB-ACC-002**: Microsoft Authenticator push with number matching only, Temporary Access Pass read over the phone. No SMS.
20. Walk the user through: Windows sign-in, Outlook, Teams, OneDrive Known Folder Move confirmation, Company Portal (if used), printers.
21. Confirm the user's mobile apps (Outlook, Teams, Authenticator) if the client allows mobile email.

### 7. Before the start date

22. Send the authorized contact a **ready email** from Harbor PSA by the business day before the start date: username, device status, what the user should expect on day one, and who to call ((913) 555-0111). Never include the password; we give the temporary password or TAP to the user directly on the day-one call.
23. If anything will not be ready on time (hardware delayed, license not approved), tell the authorized contact as soon as you know.

### 8. Day one and close-out

24. Day-one call at the agreed time. Complete MFA, sign-in, and app checks.
25. Keep the ticket open until the user has successfully signed in and the requester confirms access looks right. Then close per RB-GEN-004.

## Onsite onboarding

Some clients want a tech onsite on day one. That goes through Isaac Brennan per RB-GEN-003. Premier includes it. For Professional it uses the client's monthly onsite hours (4 hours/month included), and for Essentials it is billable with a trip charge. Tell the requester before booking if it will be billable.

## Priority guidance

- Always **P4** (1 business day response, 5 business day resolution target), but the real deadline is the start date.
- If a new user is starting today and has nothing, the request is still P4 by definition; handle it as fast as the queue allows and tell Priya Raman so she can assign someone.
- Onboarding requests are not worked after hours unless the client is Premier and asks for it.

## Escalate if

- The request is not from an authorized contact and you cannot reach one: Priya Raman.
- License purchase or hardware purchase approval is needed: account manager (Alicia Brandt or Kevin Duong).
- Entra Connect sync errors, duplicate attribute conflicts, or the user never appears in Entra: Renee Castillo.
- Five or more new users in a week at one client: hand to Rachel Kim (Projects) to coordinate; it may need a quote for device deployment.
- Client asks for admin rights for the new user: Renee Castillo (we do not grant local admin by default).

## Ticket notes

Per RB-GEN-004, plus:
- Requester and authorized contact approval (name, time)
- Notice given (business days) and whether the short-notice flag was raised
- UPN created, license assigned, groups/mailboxes/Teams added (list them)
- Device asset tag and deployment ticket number
- MFA enrollment method and date
- Day-one confirmation and who confirmed

## Revision history

| Version | Date | Author | Change |
|---|---|---|---|
| 1 | 2019-03-04 | Renee Castillo | Initial onboarding checklist. |
| 2 | 2020-03-16 | Renee Castillo | Added hybrid AD steps and license checks. |
| 3 | 2021-11-08 | Renee Castillo | Added Autopilot device assignment. |
| 4 | 2023-06-05 | Renee Castillo | Added New User Request portal form and "ready email". |
| 5 | 2025-03-10 | Renee Castillo | MFA enrollment aligned with RB-ACC-002 v2 (Authenticator push with number matching, TAP). |
| 6 | 2026-01-12 | Renee Castillo | Notice requirement is now 5 business days (2026 service catalog). Updated standard hardware to 2026 standard. Added short-notice handling and Harbor PSA contact record step. |
