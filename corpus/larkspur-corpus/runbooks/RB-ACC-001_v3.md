---
doc_id: RB-ACC-001
title: Password reset and account unlock
doc_type: runbook
version: "3"
effective_date: 2025-01-15
owner: Renee Castillo
audience: internal
---

# RB-ACC-001 Password reset and account unlock

## Purpose / When to use

Use when a user is locked out, has forgotten their password, or their password has expired and self-service did not work. Covers cloud-only Microsoft 365 / Entra ID accounts and hybrid accounts (on-prem Active Directory synced with Entra Connect). For MFA problems ("I got a new phone", "Authenticator isn't prompting"), use RB-ACC-002 instead.

## Prerequisites / access needed

- Harbor PSA (contact record with phone number on file)
- M365 admin center / Entra admin center via partner (GDAP) access, at minimum Password Administrator or User Administrator role for the client tenant
- For hybrid clients: remote session to a domain controller or a management workstation with RSAT, via Beacon RMM; domain admin credential from LockBox Vault
- The client's Atlas Docs page tells you whether the tenant is cloud-only or hybrid and whether password writeback is enabled

## Identity verification (required, every time)

**Never reset a password based on the incoming call or email alone.**

1. Look up the user's contact record in Harbor PSA.
2. **Call the user back at the phone number on file in Harbor PSA.** Not the number they called from, not a number in their email signature, not a number they give you on the call.
3. If there is no phone number on file, or the number on file does not reach the user, verify through the client's **designated authorized contact** (listed under Authorized Contacts in Harbor PSA): call the authorized contact at their number on file and have them confirm the request.
4. **Never verify identity using date of birth, SSN, employee ID, or "security questions".** We do not collect or store those for verification.
5. If the request came by email or portal, the callback is still required.

Note in the ticket how you verified (see Ticket notes).

## Steps

### A. Cloud-only account (Entra ID)

1. Complete identity verification above.
2. Check sign-in status: Entra admin center > **Identity > Users > All users** > select user > **Sign-in logs**. Look for error 50053 (account locked, smart lockout) or 50126 (bad password), and note whether failures come from an unexpected location.
3. If the account shows **Block sign-in**, find out why before unblocking. A blocked account may be an offboarding or a security hold. Check open tickets for the client. Do not unblock without confirming with the authorized contact.
4. Reset the password: M365 admin center > **Users > Active users** > select user > **Reset password**. Select "Automatically create a password" or set one that meets the client's policy, and leave **Require this user to change their password when they first sign in** checked.
5. Give the temporary password to the user **on the verified callback only**. Never email it, never put it in a portal reply, never put it in the ticket.
6. Smart lockout clears on its own after the lockout period. If the user is still locked out after a correct reset, wait 5 minutes and have them try again in a private browser window at https://www.office.com.
7. Have the user sign in, set a new password, and confirm Outlook, Teams, and OneDrive reconnect. Outlook may prompt once more; that is expected.

PowerShell alternative (Microsoft Graph):

```powershell
Connect-MgGraph -Scopes "User.ReadWrite.All" -TenantId <tenant>
$pw = @{ Password = "<temp>"; ForceChangePasswordNextSignIn = $true }
Update-MgUser -UserId user@client.example -PasswordProfile $pw
```

### B. Hybrid account (on-prem AD synced to Entra)

1. Complete identity verification.
2. On a DC or RSAT workstation, check lockout:
   ```powershell
   Get-ADUser jdoe -Properties LockedOut, PasswordExpired, PasswordLastSet, BadLogonCount
   ```
3. Unlock only (password known, just locked):
   ```powershell
   Unlock-ADAccount -Identity jdoe
   ```
4. Reset:
   ```powershell
   Set-ADAccountPassword -Identity jdoe -Reset -NewPassword (Read-Host -AsSecureString "Temp password")
   Set-ADUser -Identity jdoe -ChangePasswordAtLogon $true
   ```
   Or in Active Directory Users and Computers: right-click user > **Reset Password**, check **User must change password at next logon** and **Unlock the user's account**.
5. Password changes reach Entra on the next Entra Connect sync cycle (about every 30 minutes). Password hash sync usually lands in a couple of minutes. If the user needs M365 access right away, force a sync from the Entra Connect server:
   ```powershell
   Start-ADSyncSyncCycle -PolicyType Delta
   ```
6. If the user is remote (not on the office network or VPN), "change at next logon" can trap them: Windows cannot change the cached password without reaching a DC. For remote users, either keep them on VPN while they change it (RB-NET-003), or set a password without forcing a change and walk them through changing it once they are connected.
7. Repeated lockouts with no user error usually mean an old password saved somewhere (phone mail app, mapped drive credentials, a second PC). Check the DC Security log for event **4740** to find the caller computer.

### C. Self-service password reset (SSPR)

Where SSPR is enabled (see client Atlas Docs page), walk the user through https://aka.ms/sspr first if they are already registered. That is faster and avoids a reset by us. Identity verification still applies if we end up resetting it ourselves.

## Priority guidance

- Single user locked out: **P3**.
- Single VIP/executive locked out and fully blocked: **P2**.
- Several users at one client locked out at once: **P2**, and suspect a policy or sync issue; escalate to Renee Castillo.
- After hours: Premier clients any priority; Professional only if P1 (a single-user lockout is not P1), otherwise billable with authorized contact approval per RB-GEN-002.

## Escalate if

- You cannot verify the user through the number on file or the authorized contact: stop, do not reset, and escalate to Priya Raman.
- Sign-in logs show successful sign-ins from unexpected countries or impossible travel: treat as possible compromise, revoke sessions (`Revoke-MgUserSignInSession -UserId user@client.example`), and escalate to Renee Castillo the same hour. See RB-SEC-001.
- Many users locked out at once, or Entra Connect sync errors: Renee Castillo (M365/Entra) or Tom Kessler (on-prem AD/DC health).
- The account belongs to an admin or service account: Tier 3 only.

## Ticket notes

- Verification: "Called back at number on file (913-xxx-xxxx) and spoke to user" or "Verified via authorized contact <name>, called at number on file, <time>"
- Account type (cloud-only / hybrid), lockout cause if found
- Actions: unlock, reset, forced change, sync forced
- Confirmation user signed in successfully
- Never record the temporary password

## Revision history

| Version | Date | Author | Change |
|---|---|---|---|
| 1 | 2020-07-06 | Renee Castillo | Initial password reset procedure. |
| 2 | 2023-04-10 | Renee Castillo | Added hybrid AD steps and verification section. |
| 3 | 2025-01-15 | Renee Castillo | Identity verification changed to callback at phone number on file in Harbor PSA, with authorized contact fallback. DOB and employee ID no longer used. Added Graph PowerShell, sign-in log checks, remote user note. |
