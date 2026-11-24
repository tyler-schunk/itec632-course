---
doc_id: RB-SEC-002
title: Lost or stolen device
doc_type: runbook
version: "2"
effective_date: 2025-04-07
owner: Renee Castillo
audience: internal
---

# RB-SEC-002 Lost or stolen device

## Purpose / When to use

Use when a user reports a lost or stolen company laptop, company phone, or a personal phone that has company email/Teams on it. Also use when a departing employee does not return a device and the client asks us to lock it (RB-ACC-004). The goal is to protect company data quickly and get the user working again.

Treat every lost or stolen device report as **P2**.

## Prerequisites / access needed

- Intune admin center and Entra admin center via GDAP (Intune Administrator, User Administrator)
- Beacon RMM (last check-in, last known public IP)
- Harbor PSA asset record (asset tag `LR-<CLIENT>-####`, service tag, assigned user)
- Authorized contact for the client (required before a full wipe)

## Steps

### 1. Gather facts (5 minutes)

1. Verify the caller: callback at the number on file in Harbor PSA (RB-ACC-001). If the user's phone is the lost device, call the authorized contact at their number on file instead and have them confirm.
2. Ask:
   - Which device (laptop or phone; company or personal)? Asset tag if they know it.
   - When and where was it last seen? Lost or stolen?
   - Was it powered on, asleep, or locked? (Our laptops have BitLocker; data at rest is encrypted.)
   - Were any passwords written down with it or saved in a browser that is not protected?
3. Look up the device in Harbor PSA and Beacon RMM: last check-in time and last public IP.

### 2. Protect the account (do these right away)

4. **Revoke sessions** and reset the password (RB-ACC-001):
   ```powershell
   Revoke-MgUserSignInSession -UserId user@client.example
   ```
5. If the lost device is the user's MFA phone: remove its Microsoft Authenticator registration (Entra > user > Authentication methods) and plan re-enrollment on the replacement per RB-ACC-002 (authorized contact confirmation required for the MFA reset).

### 3. Protect the device

**Company Windows laptop (Intune-managed):**

6. Intune admin center > **Devices > Windows** > select device:
   - Confirm **BitLocker** is enabled (Device > Encryption report or Recovery keys present).
   - **Lost or stolen with low risk** (left in a cab, likely to be found): disable the device in Entra (Devices > All devices > select > **Disable**) so it cannot get tokens, and wait 24 hours if the user expects it back.
   - **Stolen, or not recovered within 24 hours**: with the authorized contact's approval, issue **Wipe**. The wipe runs the next time the device comes online. Note: a wipe removes the chance to locate or recover data from it.
7. Beacon RMM: tag the device **Lost/Stolen** so alerts about it going offline do not generate noise, and watch for check-ins (we will see the public IP if it comes online).

**Company phone (Intune-enrolled):**

8. Intune > Devices > iOS/iPadOS or Android > select device: **Remote lock**; for supervised iOS, enable **Lost Mode** with a message and phone number (support line (913) 555-0111). Wipe after authorized contact approval if not recovered.

**Personal phone with company apps (app protection / BYOD):**

9. We do not wipe personal devices. Use **Apps > App protection > Wipe requests** (selective wipe) to remove company data from Outlook, Teams, and OneDrive on that device, and remove the device from the user's Exchange mobile devices list.

### 4. Paperwork and replacement

10. For stolen devices, recommend the user files a police report; some clients' insurers require one. Note the report number if the client shares it. The serial/service tag is in Harbor PSA.
11. Update the asset record in Harbor PSA: status **Lost** or **Stolen**, date, ticket number.
12. Replacement laptop: P4 child ticket per RB-HW-002, with purchase approval from the authorized contact through the account manager. Offer a loaner meanwhile. User files are in OneDrive (Known Folder Move), so the replacement is mostly provisioning time.
13. If the device turns up: confirm with the user, re-enable in Entra, run a full scan, and decide with Renee Castillo whether to reimage (always reimage if it was stolen and recovered).

## Priority guidance

- All lost or stolen device reports: **P2** (Professional 1 business hour response, Premier 1 hour 24x7, Essentials 2 business hours).
- After hours: Premier is worked by on-call (RB-GEN-002). For Professional and Essentials, the on-call engineer offers billable after-hours account lockdown (session revoke, password reset) with authorized contact approval; otherwise it is first in the queue at 7:00 AM.

## Escalate if

- The device held regulated data and was not encrypted, or BitLocker status is unknown: Renee Castillo immediately (the client may have reporting obligations; Jordan Pike and the account manager will help the client with next steps).
- Sign-in logs show activity from the device after it was lost: Renee Castillo.
- The device is a server, a backup drive, or removable media with client data: Tom Kessler and Renee Castillo.
- The client wants us to track down or recover the device physically: not our job; the client works with police.

## Ticket notes

- Device type, asset tag, service tag, owner (company/personal)
- Last seen time/place, lost vs stolen, police report number if provided
- Encryption status confirmed (BitLocker / device encryption)
- Actions with times: sessions revoked, password reset, MFA method removed, device disabled, lock/wipe issued (and approver), selective wipe
- Replacement ticket number and loaner asset tag

## Revision history

| Version | Date | Author | Change |
|---|---|---|---|
| 1 | 2022-07-11 | Renee Castillo | Initial lost device procedure. |
| 2 | 2025-04-07 | Renee Castillo | Added Entra device disable, iOS Lost Mode, app protection selective wipe for personal phones, authorized contact approval for full wipe. |
