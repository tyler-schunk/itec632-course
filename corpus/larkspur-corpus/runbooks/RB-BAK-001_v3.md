---
doc_id: RB-BAK-001
title: File and folder restore requests
doc_type: runbook
version: "3"
effective_date: 2026-01-05
owner: Tom Kessler
audience: internal
---

# RB-BAK-001 File and folder restore requests

## Purpose / When to use

Use when a user or client asks to recover deleted, overwritten, or corrupted files or folders: from OneDrive, SharePoint, Exchange mailboxes, a file server, or a workstation. Check the native Microsoft 365 options first (they are fast and free), then VaultLine Backup.

## Backup coverage by tier (2026 service catalog)

| Tier | VaultLine Backup | Retention |
|---|---|---|
| Essentials | Only with the backup add-on ($6/user/month) | 14 days daily (if add-on) |
| Professional | Included | 30 daily + 12 monthly |
| Premier | Included | 30 daily + 12 monthly + 7 yearly |

Essentials clients **without** the add-on have only native Microsoft 365 recovery (recycle bins, version history, mailbox recoverable items) and whatever local backups they run themselves. Check the client's Contract tab in Harbor PSA for the add-on before promising anything. Server backups are covered where the client pays for server management.

## Prerequisites / access needed

- Request from the file owner, or for someone else's data, an **authorized contact**
- SharePoint/OneDrive admin and Exchange admin via GDAP
- VaultLine Backup console (credentials in LockBox Vault: "VaultLine - MSP console")
- Beacon RMM for server/workstation access

## Steps

### 1. Get the details

1. What was lost (file/folder names, path or site/library), where it lived, roughly when it was last good, and when it was noticed. "Last good" date decides which recovery point to use and whether it is still within retention.
2. Authorization: users can request their own files. Restores of another user's data, a whole shared library, or a mailbox need an authorized contact.

### 2. Native Microsoft 365 recovery (try first)

3. **OneDrive/SharePoint recycle bin:** the user (or a site owner) can restore from the site's **Recycle bin**; items there remain for 93 days total (first-stage plus second-stage). Admins can restore from the **Second-stage recycle bin** at the bottom of the recycle bin page.
4. **Version history:** for overwritten or corrupted files, right-click the file in OneDrive/SharePoint > **Version history** > restore an earlier version.
5. **Restore your OneDrive / Restore this library:** for mass deletion or encryption within the last 30 days, OneDrive Settings > **Restore your OneDrive** (or the library settings **Restore this library**) rolls the whole location back to a point in time. This overwrites later changes; confirm with the requester first.
6. **Mailbox items:** Outlook > Deleted Items > **Recover items recently removed from this folder** (Recoverable Items, 14 days default; 30 if the client page says the tenant was extended). Admin option: EAC or `Get-RecoverableItems` / `Restore-RecoverableItems` in Exchange Online PowerShell.

### 3. VaultLine restore

7. If native options do not cover it (older than the recycle bin, a file server, permanently purged items, a whole mailbox), confirm VaultLine coverage for the client and check the requested date is within retention.
8. VaultLine console > client > protected item (M365 tenant, server, or workstation) > **Restore** > pick the recovery point closest to (but before) the problem.
9. Restore options:
   - **Restore to original location, keep both** (default): restored items get a suffix so nothing current is overwritten.
   - **Restore to alternate location**: for large restores or when the user wants to compare. For M365, restore to a folder named `Restored-YYYYMMDD` in the user's OneDrive or the library.
   - **Overwrite**: only with explicit approval from the requester and authorized contact.
10. Monitor the restore job to completion. Large restores (tens of GB) can take hours; give the user an estimate.
11. Verify with the user that the right files and versions are back and they open.

### 4. File server and workstation restores

12. File server restores: same VaultLine process, protected item = the server. Restore to an alternate folder on the server (`D:\Restores\TCK-xxxxxx\`) and let the user copy what they need, or restore in place with keep-both. Check NTFS permissions on the restored data match the original.
13. Workstations: we back up workstations only where the client page says so. OneDrive Known Folder Move is the standard protection for user files.

## Priority guidance

- Single file or folder, user can wait: **P3** (P4 if it is "nice to have").
- Critical business data missing for a team or a whole shared library: **P2**.
- Mass deletion, encryption, or files renamed with strange extensions across many locations: possible ransomware. **P1**, stop and call Tom Kessler immediately. Do not start restores until Tom confirms the source of the problem is contained.

## Escalate if

- Possible ransomware or mass changes: Tom Kessler (immediately).
- Requested date is outside retention or VaultLine shows no recovery point: Tom Kessler; tell the requester honestly what is and is not recoverable.
- Requester is not authorized for the data requested: Priya Raman.
- Restore of a full server or a database (SQL, QuickBooks, LOB app data): Tom Kessler.
- Client without backup coverage asks for VaultLine-level recovery: account manager (they may want to add the backup add-on going forward).

## Ticket notes

- What, where, last good date, requester and authorization
- Recovery method (recycle bin, version history, Restore your OneDrive, VaultLine) and recovery point date
- Restore location and option (keep both / alternate / overwrite with approver)
- Size and duration of restore, user verification

## Revision history

| Version | Date | Author | Change |
|---|---|---|---|
| 1 | 2020-08-17 | Tom Kessler | Initial restore procedure. |
| 2 | 2023-09-11 | Tom Kessler | Added native M365 recovery steps before VaultLine. |
| 3 | 2026-01-05 | Tom Kessler | Updated retention table for 2026 service catalog. Added ransomware stop rule and Restore your OneDrive guidance. |
