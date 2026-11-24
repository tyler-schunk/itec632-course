---
doc_id: RB-SW-001
title: Software install requests
doc_type: runbook
version: "3"
effective_date: 2025-06-23
owner: Lena Fischer
audience: internal
---

# RB-SW-001 Software install requests

## Purpose / When to use

Use when a user asks for software to be installed on their managed Windows PC, asks for local admin rights to install something themselves, or a client asks to roll an application out to several users. Users on managed devices do not have local admin rights; installs go through us.

## Prerequisites / access needed

- Intune admin center (Apps) via GDAP, Intune Administrator, for packaged apps and Company Portal
- Beacon RMM (scripted installs, software inventory, remote session with elevation)
- Client Atlas Docs page: **Approved software list** and who can approve new software

## Approval rules

| Request type | Approval needed |
|---|---|
| App already on the client's approved list (Adobe Acrobat Reader, Zoom, 7-Zip, Chrome, client LOB apps) | None. Install it. |
| Free app not on the list | Tier 2 checks it is legitimate and safe (vendor site, not a bundled downloader). If fine, install and add to the approved list with a note. |
| Paid app or subscription | **Authorized contact** approves the purchase. Licensing is bought by the client or through the account manager. |
| Browser extensions | Allowed per the client's Edge/Chrome policy; most clients allow from the official stores only. |
| Remote access tools (TeamViewer, AnyDesk), personal VPNs, torrent clients, crypto miners, "PC optimizers" | **Not installed.** Explain politely; escalate if the client insists. |
| Local admin rights | Not granted by default. Requires authorized contact request and Renee Castillo approval; documented in Atlas Docs. |

## Steps

1. **Confirm the request:** app name, version or edition, which user and device (asset tag), business reason. If the request came from a coworker on behalf of someone else, confirm with that user.
2. **Check the approved list** on the client's Atlas Docs page and the approval table above. Get approval if needed and record it.
3. **Check if it is already available in Company Portal.** Many apps are published as **Available** in Intune. Walk the user through: Start > **Company Portal** > Apps > select the app > **Install**. This is the preferred route.
4. If not in Company Portal, choose the install method:
   - **Intune (preferred for anything more than one user):** add the app as a Microsoft Store app (new) / WinGet-sourced app, or package as a Win32 app (.intunewin) and assign it to the user's group as Required or Available. Tier 2 does packaging.
   - **Beacon RMM (single user, quick):** run the install from the Beacon script library (**LR - Install via WinGet**, takes the WinGet package ID) or a silent installer pushed from Beacon. Example WinGet IDs: `Adobe.Acrobat.Reader.64-bit`, `Zoom.Zoom`, `7zip.7zip`, `Google.Chrome`.
     ```powershell
     winget install --id Zoom.Zoom --silent --accept-package-agreements --accept-source-agreements --scope machine
     ```
   - **Remote session with elevation (last resort):** for installers that need interactive choices. Use the LockBox Vault local admin credential (LAPS where deployed: Intune > Devices > device > **Local admin password**). Do not leave the user logged in as admin.
5. **License activation:** sign in with the user's account (Microsoft, Adobe) or enter the license key the client provided. Store license keys in LockBox Vault under the client, not in the ticket.
6. **Test** with the user: app launches, signs in, opens a file.
7. **Update the approved list** in Atlas Docs if this was a new approval.

## Line-of-business applications

Industry apps (dental imaging and practice management at Foxhaven Dental, dealer management at Kaw Valley Auto Group, tax software at Hollis Lane CPAs, design suites at Silo & Grain Architecture) usually have vendor-specific installers, database connections, or license servers. Check the client page for the vendor support contact. Major LOB upgrades (version jumps, server components) are project work: hand to Rachel Kim for a quote.

## Priority guidance

- Single install request: **P4** (1 business day response, 5 business days resolution).
- User blocked from doing their job without the app (needed for a client meeting today, LOB app missing after a device replacement): **P3**.
- Rollout to many users: **P4** scheduled change, or a project if it needs packaging and testing beyond an hour or two.

## Escalate if

- Local admin rights requested: Renee Castillo.
- App packaging for Intune fails or the app needs a custom detection rule: Lena Fischer.
- Unknown or suspicious software already found installed on a device: Tier 2, and Renee Castillo if it looks malicious.
- Licensing purchases or disputes: account manager (Alicia Brandt or Kevin Duong).

## Ticket notes

- App name and version, user, device asset tag
- Approval (who, when) or "on approved list"
- Install method (Company Portal, Intune assignment, Beacon WinGet, manual)
- License location (LockBox Vault entry name, never the key itself)
- Test result and user confirmation

## Revision history

| Version | Date | Author | Change |
|---|---|---|---|
| 1 | 2020-06-01 | Lena Fischer | Initial software request procedure. |
| 2 | 2022-08-15 | Lena Fischer | Added Company Portal and approval table. |
| 3 | 2025-06-23 | Lena Fischer | Added WinGet installs via Beacon RMM, LAPS for elevation, blocked software categories. |
