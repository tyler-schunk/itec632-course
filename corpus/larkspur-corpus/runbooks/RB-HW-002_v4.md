---
doc_id: RB-HW-002
title: New workstation deployment
doc_type: runbook
version: "4"
effective_date: 2026-01-12
owner: Rachel Kim
audience: internal
---

# RB-HW-002 New workstation deployment

## Purpose / When to use

Use when deploying a new or reimaged Windows 11 laptop or desktop to a client user: new hire (from RB-ACC-003), replacement for a failed or aging device, or a reused device for a different user. Five or more devices at once is a project: hand it to Rachel Kim for a quote at the project rate.

## Hardware standard (2026)

| Type | Model | Spec |
|---|---|---|
| Standard laptop | Dell Latitude 5550 | Intel Core Ultra 5, **32 GB RAM**, 512 GB SSD, 3-year ProSupport warranty |
| Standard desktop | Dell OptiPlex Micro 7020 | 16 GB RAM |

Non-standard requests (CAD workstations for Granite Peak Engineering or Silo & Grain Architecture, animation workstations for Zenith Arc Animation, rugged laptops for field staff) are quoted individually by the account manager. Do not order non-standard hardware without an approved quote.

## Prerequisites / access needed

- Approved hardware order (authorized contact approval and account manager quote) and Dell order number
- Intune admin center (Autopilot) via GDAP, Intune Administrator
- Beacon RMM (agent deployment is part of the Intune app set)
- Harbor PSA asset records
- Asset tag labels (`LR-<CLIENT>-####`)
- Client Atlas Docs page: Autopilot profile name, required apps, printers, any non-Intune exceptions

## Steps

### 1. Order and receive

1. Order through the Dell Premier account with **Autopilot registration** selected for the client's tenant so the device hash is uploaded by Dell. Ship to the Larkspur office unless the client asked for direct ship.
2. On arrival, open the box, check the model and spec match the order, and apply the asset tag.
3. Create the asset in Harbor PSA: asset tag, service tag, model, warranty end date (3 years from ship date for ProSupport), client, assigned user.

### 2. Autopilot registration check

4. Intune admin center > **Devices > Windows > Windows enrollment > Devices** (Windows Autopilot devices). Search for the service tag / serial. Confirm it shows the correct **group tag** and **profile status: Assigned**.
5. If the device is missing (Dell did not register it, or it is a reused device), collect the hardware hash: boot to OOBE, press **Shift+F10**, and run:
   ```powershell
   PowerShell.exe -ExecutionPolicy Bypass
   Install-Script -Name Get-WindowsAutopilotInfo -Force
   Get-WindowsAutopilotInfo -Online -GroupTag <ClientTag>
   ```
   Sign in with a GDAP admin account when prompted. Wait for the profile to assign (15 minutes to an hour).
6. **Assign the user** to the Autopilot device record so the device greets them by name.

### 3. Provision

7. Connect the device to wired network if possible (faster and avoids Wi-Fi password entry in OOBE). Power on.
8. At OOBE, the Autopilot profile takes over. For **user-driven** mode, the user signs in (or we sign in with the user during a scheduled session). For **pre-provisioning** (technician flow), press the Windows key 5 times at the first OOBE screen and select **Pre-provision with Windows Autopilot** so apps install before the user gets it. We pre-provision at the office whenever we have time; it shortens day one.
9. The **Enrollment Status Page** installs required apps: Microsoft 365 Apps, Beacon RMM agent, endpoint protection, FortiClient VPN (if the client uses VPN), and client line-of-business apps packaged in Intune. If ESP fails, note the app that failed, then check Intune > Apps > the app > Device install status.
10. After provisioning, confirm:
    - Device shows in Beacon RMM under the right client and site.
    - Device is compliant in Intune (BitLocker on, Defender on, OS version current).
    - BitLocker recovery key escrowed (Entra > Devices > device > BitLocker keys).
    - Windows Update has run (Settings > Windows Update) and Dell Command | Update has applied BIOS/drivers.
11. For a reused device: before handing over, run **Autopilot Reset** or **Wipe** from Intune so no old user data remains (RB-ACC-004 step 14).

### 4. User handoff

12. User signs in (Windows Hello for Business setup prompts for a PIN; face/fingerprint if the device supports it), completes MFA with Authenticator (RB-ACC-002).
13. Confirm OneDrive Known Folder Move, Outlook, Teams, printers, mapped drives or SharePoint shortcuts, VPN profile if applicable.
14. For a replacement device: confirm with the user that their files are present via OneDrive before collecting the old device. Old device goes to wipe and retire (or redeploy) per RB-ACC-004 step 14.
15. Onsite delivery and setup goes through Isaac Brennan (RB-GEN-003). Premier includes onsite; Professional uses monthly onsite hours (4 hours/month included); Essentials is billable. Remote handoff by phone is fine for users comfortable with it.

## Priority guidance

- New hire device: **P4** tied to the onboarding start date (RB-ACC-003).
- Replacement for a failed device: matches the failure ticket (usually **P3**), but the deployment itself is a P4 child ticket.
- Not worked after hours unless Premier asks.

## Escalate if

- Autopilot profile will not assign, or device registered to the wrong tenant: Renee Castillo.
- ESP failures for multiple devices or a required app failing to install: Renee Castillo (Intune) or Lena Fischer (app packaging, RB-SW-001).
- Hardware arrives damaged or wrong spec: Rachel Kim (Dell order) and the account manager.
- Five or more devices, or any site-wide refresh: Rachel Kim (project).

## Ticket notes

- Dell order number, service tag, asset tag
- Autopilot registration method (Dell vs manual hash), group tag, profile
- Provisioning mode (pre-provision vs user-driven), ESP result
- Compliance and BitLocker escrow confirmed
- User handoff date, old device disposition

## Revision history

| Version | Date | Author | Change |
|---|---|---|---|
| 1 | 2020-10-05 | Rachel Kim | Initial deployment checklist (imaging). |
| 2 | 2022-03-21 | Rachel Kim | Moved to Windows Autopilot and Intune. |
| 3 | 2024-02-05 | Rachel Kim | Added pre-provisioning, Dell Autopilot registration at order, 2024 hardware standard. |
| 4 | 2026-01-12 | Rachel Kim | 2026 hardware standard: Latitude 5550 (Core Ultra 5, 32 GB, 512 GB, 3-year ProSupport) and OptiPlex Micro 7020 (16 GB). Updated onsite coverage wording. |
