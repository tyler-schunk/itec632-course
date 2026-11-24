---
doc_id: RB-ACC-004
title: User offboarding
doc_type: runbook
version: "3"
effective_date: 2025-11-03
owner: Renee Castillo
audience: internal
---

# RB-ACC-004 User offboarding

## Purpose / When to use

Use when a client tells us an employee is leaving or has left. Covers blocking access, preserving data, handling the mailbox and OneDrive, recovering the device, and cleaning up licenses. For a terminated employee who may be hostile, do the "Immediate cutoff" steps first and call Renee Castillo.

## Timing commitment

- Offboarding requested **before 3:00 PM CT** on a business day is completed **the same business day**.
- Requests after 3:00 PM CT are completed the next business morning, unless the client says the separation is hostile or urgent; then do the immediate cutoff right away and finish the rest the next morning.
- Clients can schedule an offboarding in advance (for example, "disable at 5:00 PM Friday"). Set a scheduled task in Harbor PSA for the exact time.

## Prerequisites / access needed

- Request from an **authorized contact** (portal Offboarding form or email). We never offboard on the word of the departing user or a coworker who is not an authorized contact.
- Entra/M365 admin via GDAP: User Administrator, Exchange Administrator, License Administrator
- Intune admin center
- Hybrid clients: Beacon RMM session to a DC; domain admin credential from LockBox Vault

## Information to collect

The Offboarding form asks for these. Defaults are in brackets if the client does not say.

- Last day and time access should end
- Mailbox: forward to someone, convert to shared mailbox and grant access, or auto-reply only [convert to shared, grant manager Full Access]
- Auto-reply text [none]
- OneDrive: who gets access [manager]
- Devices to recover (asset tags), and whether the user has a company phone
- Anything else: shared passwords the user knew, line-of-business accounts, building access (client handles)

## Steps

### 1. Immediate cutoff (do these first, in this order)

1. **Block sign-in:** M365 admin center > **Users > Active users** > user > **Block sign-in**. For hybrid, also disable in AD (`Disable-ADAccount -Identity jdoe`) and force a delta sync, or the block will be overwritten on the next sync.
2. **Reset the password** to a random value (do not record it). This kills any saved credential use on-prem.
3. **Revoke sessions:** user > **Sign out of all sessions** in the admin center, or:
   ```powershell
   Revoke-MgUserSignInSession -UserId jdoe@client.example
   ```
4. **Remove MFA methods** (Entra > user > Authentication methods > delete each method) so a stale phone cannot be used to re-register.
5. **Mobile devices:** in Intune, retire or selectively wipe company data from the user's phone (Devices > select device > **Retire**). Exchange admin center > user > Mobile devices: remove any ActiveSync devices.

### 2. Mailbox

6. Set the auto-reply if requested (Exchange admin center > **Recipients > Mailboxes** > user > **Manage automatic replies**).
7. **Convert to shared mailbox** (default): Exchange admin center > user > **Others > Convert to shared mailbox**. Shared mailboxes under 50 GB do not need a license. If the mailbox is over 50 GB or has an archive or litigation hold, keep a license or ask Renee Castillo.
   ```powershell
   Set-Mailbox -Identity jdoe@client.example -Type Shared
   Add-MailboxPermission -Identity jdoe@client.example -User manager@client.example -AccessRights FullAccess -AutoMapping $true
   ```
8. If forwarding is requested instead, set it on the mailbox (Mail flow settings > Email forwarding) and note that forwarding stops when the license is removed unless the mailbox is shared.
9. Hide from the global address list if the client asks (most do after 30 days).

### 3. Data

10. **OneDrive:** M365 admin center > user > **OneDrive** tab > **Create link to files** to give the manager access. Tell the manager they have the retention period to copy what they need. The tenant's OneDrive retention setting for deleted users is on the client page (Microsoft default is 30 days, we set most clients to 90).
11. Do not delete the user until the client confirms data has been copied or the retention window is agreed. VaultLine Backup protects M365 data for clients with backup coverage (Professional, Premier, and Essentials with the backup add-on); confirm the user is still in the backup scope until deletion.

### 4. Groups and licenses

12. Remove the user from groups, Teams ownership (assign a new owner first if they were the only owner), and distribution lists.
13. **Remove licenses** once the mailbox is converted and OneDrive access is granted. Tell the authorized contact the license is now free (they may want it for a new hire, or to reduce their count; seat changes go to the account manager).

### 5. Devices

14. Coordinate device return with the client. When the laptop is back:
    - If it will be reused: **Autopilot Reset** or **Wipe** from Intune, then hold for the next user (RB-HW-002).
    - If it is being retired: wipe, remove from Intune and Autopilot, update asset status in Harbor PSA, and arrange disposal.
15. If a device is not returned and the user has left, treat it under RB-SEC-002 (lost device) at the client's request.
16. Remove the user from Beacon RMM device assignment and from the client's VaultLine endpoint backup if applicable.

### 6. Wrap up

17. Update the Harbor PSA contact to **Inactive** (do not delete; ticket history matters).
18. Rotate any shared credentials the user knew if the client asks (Wi-Fi PSK, shared mailbox passwords, alarm codes are the client's job). Shared credentials we manage live in LockBox Vault; update them there.
19. Send the authorized contact a completion summary from the ticket.

## Priority guidance

- Before 3:00 PM CT same-day request: **P2** so it is finished the same business day.
- After 3:00 PM or scheduled in advance: **P3**, due next business morning or at the scheduled time.
- Hostile termination: **P2** immediately regardless of time of day; after hours, follow RB-GEN-002 (Premier included; Professional and Essentials billable with authorized contact approval unless the client treats it as P1, which is rare).

## Escalate if

- The departing user is an admin, owner of the tenant, or has access to finance systems: Renee Castillo.
- Litigation hold, legal, or HR investigation is mentioned: Renee Castillo before deleting or converting anything.
- The client wants the account deleted immediately with no data retention: confirm in writing with the authorized contact and loop in Renee Castillo.
- The user is still signing in after the block (sync overwrite, cached sessions): Renee Castillo.

## Ticket notes

- Requester (authorized contact), time of request, requested cutoff time
- Exact time sign-in was blocked and sessions revoked
- Mailbox disposition and who has access
- OneDrive access granted to whom, retention period communicated
- Licenses removed, devices recovered (asset tags), contact set Inactive

## Revision history

| Version | Date | Author | Change |
|---|---|---|---|
| 1 | 2019-02-18 | Renee Castillo | Initial offboarding checklist. |
| 2 | 2022-05-09 | Renee Castillo | Added same-day commitment for requests before 3:00 PM CT, shared mailbox conversion default. |
| 3 | 2025-11-03 | Renee Castillo | Reordered immediate cutoff steps, added MFA method removal and Intune retire, Graph session revocation. |
