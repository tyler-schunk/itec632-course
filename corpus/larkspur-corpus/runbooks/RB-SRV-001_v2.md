---
doc_id: RB-SRV-001
title: Server low disk space alert
doc_type: runbook
version: "2"
effective_date: 2024-11-11
owner: Tom Kessler
audience: internal
---

# RB-SRV-001 Server low disk space alert

## Purpose / When to use

Use when Beacon RMM raises a low disk space alert on a client Windows Server (file server, domain controller, application/database server, Hyper-V host) or a VaultLine backup job fails for lack of space. Applies to servers covered under server management (the server management add-on). If the server is not under management, tell the account manager before doing more than a quick look.

## Alert thresholds (Beacon RMM)

| Level | Threshold | Ticket priority |
|---|---|---|
| **Warning** | 15% free | P3 |
| **Critical** | 10% free | P2 |
| C: (system volume) under 5 GB free, or any volume nearly full and services failing | | P1 if users are affected (server effectively down), otherwise P2 |

Beacon creates the Harbor PSA ticket automatically and attaches the volume and free space at alert time.

## Prerequisites / access needed

- Beacon RMM (remote session, remote shell, disk history graph)
- Server admin credential from LockBox Vault
- Client Atlas Docs server page: server roles, what lives on each volume, maintenance window
- Tier 2 can do the safe cleanup below; anything involving databases, Exchange, deleting user data, or resizing volumes is Tier 3

## Steps

1. **Look at the trend** in Beacon's disk history graph. A slow climb over months is a capacity issue (plan expansion). A sudden jump in hours or days means something specific: a runaway log, a user dumping data, a failed backup leaving files, shadow copies growing.
2. **Find what is using the space.** Remote session, run TreeSize Free or WizTree (portable versions in the Beacon tool library), or PowerShell:
   ```powershell
   Get-ChildItem D:\ -Directory | ForEach-Object {
     $s = (Get-ChildItem $_.FullName -Recurse -File -ErrorAction SilentlyContinue | Measure-Object Length -Sum).Sum
     [pscustomobject]@{Folder=$_.FullName; GB=[math]::Round($s/1GB,2)}
   } | Sort-Object GB -Descending | Select-Object -First 15
   ```
3. **Safe cleanup on C: (Tier 2 OK):**
   - Windows component store:
     ```
     Dism.exe /Online /Cleanup-Image /StartComponentCleanup
     ```
   - Windows Update download cache: stop `wuauserv`, clear `C:\Windows\SoftwareDistribution\Download`, start `wuauserv`.
   - Temp folders: `C:\Windows\Temp` and `C:\Users\*\AppData\Local\Temp` (files older than 7 days).
   - Old IIS logs (`C:\inetpub\logs\LogFiles`) older than 30 days, if IIS is installed and the client page does not say logs must be kept.
   - Old memory dumps: `C:\Windows\MEMORY.DMP` and `C:\Windows\Minidump` (note it in the ticket in case a crash investigation needs them).
   - Do **not** delete anything from `C:\Windows\WinSxS` by hand, `C:\Windows\Installer`, or `System Volume Information`.
4. **Shadow copies:** check how much space Volume Shadow Copy is using:
   ```
   vssadmin list shadowstorage
   ```
   If shadow storage is unbounded or very large, Tier 3 can cap it (`vssadmin resize shadowstorage /for=D: /on=D: /maxsize=10%`). Previous Versions on file shares depend on these; ask before shrinking.
5. **Data volumes (file servers):** look for obvious large items: duplicate copies of folders, ISO files, personal media, old backups someone made by hand ("Copy of Accounting 2019"). **Do not delete user data.** Send the client's authorized contact a list of the largest folders and ask what can be removed or archived.
6. **Application and database servers:** SQL logs (`.ldf`) growing usually means a database in Full recovery model without log backups. **Do not shrink or delete database files.** Escalate to Tom Kessler.
7. **Hyper-V hosts:** check for leftover checkpoint files (`.avhdx`) and old VHDX files of retired VMs. Merging or deleting checkpoints is Tier 3 only.
8. **Confirm the alert clears** in Beacon (free space back above 15%). If cleanup cannot get it above 15%, open a P4 follow-up for capacity: Tom Kessler sizes a volume expansion (virtual disk expansion for VMs, new drives for physical servers); hardware needs a quote through the account manager.

## Priority guidance

- Warning (15% free): **P3**, work it within the normal SLA.
- Critical (10% free): **P2**.
- Volume full and services failing (file shares read-only, Exchange/SQL/LOB app stopped, DC replication problems): **P1**, server effectively down; use RB-SRV-002 alongside this runbook.
- After hours: critical alerts on Premier servers are worked by on-call per RB-GEN-002. Professional only if it is a P1 (server down). Warnings wait for business hours.

## Escalate if

- Database or log files are the cause: Tom Kessler.
- C: on a domain controller is under 10% free: Tom Kessler (a full system volume can break AD).
- The space is consumed faster than you can clean (runaway process, ransomware encrypting and duplicating files): Tom Kessler immediately.
- Volume expansion or new storage is needed: Tom Kessler, then account manager for any hardware quote.

## Ticket notes

- Server name, volume, free space at alert and after cleanup
- What was using the space (top folders/files)
- Cleanup actions taken and space recovered by each
- Anything sent to the client for decision (list of large folders)
- Follow-up ticket number for capacity planning if opened

## Revision history

| Version | Date | Author | Change |
|---|---|---|---|
| 1 | 2020-12-07 | Tom Kessler | Initial low disk space procedure. |
| 2 | 2024-11-11 | Tom Kessler | Beacon RMM thresholds set to 15% free (warning) and 10% free (critical). Added shadow storage, Hyper-V checkpoint, and SQL log cautions. |
