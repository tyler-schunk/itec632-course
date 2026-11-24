---
doc_id: RB-ACC-001
title: Password reset and account unlock
doc_type: runbook
version: "2"
effective_date: 2023-04-10
owner: Renee Castillo
audience: internal
---

# RB-ACC-001 Password reset and account unlock

## Purpose / When to use

Use when a user is locked out, forgot their password, or has an expired password. Covers Microsoft 365 cloud accounts and hybrid accounts synced from on-prem Active Directory. MFA issues go to RB-ACC-002.

## Prerequisites / access needed

- Harbor PSA (user contact record)
- M365 admin center access for the client tenant (Password Administrator or User Administrator)
- For hybrid clients: Beacon RMM remote session to a domain controller or management workstation; domain admin credential from LockBox Vault

## Identity verification

Verify the caller before any reset:

1. Ask the user for their **date of birth** and **employee ID**.
2. Compare against the client's HR roster in the client's Atlas Docs page or the user's contact record in Harbor PSA.
3. Both must match. If either does not match, or the client has not provided a roster, contact the client's authorized contact before proceeding.

Record in the ticket that the user was verified.

## Steps

### A. Cloud-only account

1. Verify identity as above.
2. M365 admin center > **Users > Active users** > select user > **Reset password**.
3. Choose "Automatically create a password" and keep **Require this user to change their password when they first sign in** checked.
4. Read the temporary password to the user over the phone. Do not email it.
5. Have the user sign in at https://www.office.com and set a new password.
6. Confirm Outlook, Teams, and OneDrive reconnect.

If the account shows **Sign-in blocked**, check with the client before unblocking.

### B. Hybrid account

1. Verify identity.
2. Check the account on a DC:
   ```powershell
   Get-ADUser jdoe -Properties LockedOut, PasswordExpired, PasswordLastSet
   ```
3. Unlock:
   ```powershell
   Unlock-ADAccount -Identity jdoe
   ```
4. Reset if needed, in Active Directory Users and Computers: right-click > **Reset Password**, check **User must change password at next logon** and **Unlock the user's account**.
5. Force a sync if the user needs M365 access right away:
   ```powershell
   Start-ADSyncSyncCycle -PolicyType Delta
   ```
6. Remote users must be on VPN to change a forced password. If they are not, set a password without forcing a change.
7. For repeated lockouts, check event ID 4740 on the DC to find the source computer.

## Priority guidance

- Single user locked out: P3.
- Executive fully blocked: P2.
- Several users at once: P2, escalate.

## Escalate if

- The user cannot pass verification and the authorized contact cannot be reached: escalate to Greg Halvorsen (Service Desk Lead).
- Sign-ins from unexpected locations: escalate to Renee Castillo.
- Multiple users locked out, or sync errors: Renee Castillo or Tom Kessler.
- Admin or service accounts: Tier 3 only.

## Ticket notes

- Verified with DOB and employee ID (do not record the actual values)
- Account type and actions taken
- User confirmed sign-in
- Never record the temporary password

## Revision history

| Version | Date | Author | Change |
|---|---|---|---|
| 1 | 2020-07-06 | Renee Castillo | Initial password reset procedure. |
| 2 | 2023-04-10 | Renee Castillo | Added hybrid AD steps and verification section. |
