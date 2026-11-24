---
doc_id: RB-BAK-002
title: VaultLine backup job failure
doc_type: runbook
version: "2"
effective_date: 2025-05-05
owner: Tom Kessler
audience: internal
---

# RB-BAK-002 VaultLine backup job failure

## Purpose / When to use

Use when VaultLine Backup reports a failed or warning job (the alert creates a Harbor PSA ticket through the VaultLine integration), when the daily backup report shows a protected item with no successful backup in 24 hours, or when a client's backup appliance or agent shows offline.

## Background

- VaultLine protects M365 tenants (Exchange, OneDrive, SharePoint, Teams), servers (image-level and file-level), and selected workstations.
- Most jobs run nightly between 9:00 PM and 5:00 AM CT. M365 backups run several times a day.
- The service desk reviews the **VaultLine daily report** at 7:30 AM each business day. Tier 2 owns the review; failures become tickets.

## Prerequisites / access needed

- VaultLine console (LockBox Vault: "VaultLine - MSP console")
- Beacon RMM remote session to the protected server or workstation
- Server credentials (LockBox Vault) for Tier 2/3

## Steps

1. **Open the job details** in the VaultLine console: client > protected item > job history. Note the error message, how many consecutive failures, and the last successful backup time.
2. **Retry once** if it looks transient (network timeout, "target busy"). Many failures clear on a manual retry. If the retry succeeds, document and close.
3. **Common causes and fixes:**
   - **Agent offline / cannot contact agent:** check the device in Beacon RMM. Is it powered on? Restart the VaultLine agent service (`Get-Service VaultLine*` then `Restart-Service`). Servers that were shut down by the client will fail; ask why.
   - **VSS errors** (snapshot failed, writer timeout): on the server, run `vssadmin list writers` in an elevated prompt. Writers in a **Failed** state (SQL, Exchange, Hyper-V, System Writer) usually recover after restarting their service or a reboot in the maintenance window. Check `vssadmin list shadowstorage` for shadow storage limits.
   - **Low disk space** on the source volume (VSS needs free space) or on a local backup appliance: see RB-SRV-001.
   - **Credentials expired:** M365 backups use an app registration/consent; if VaultLine shows "unauthorized" for a tenant, the consent may have been revoked or a secret expired. Escalate to Tom Kessler or Renee Castillo.
   - **Files locked or changed during backup:** warnings on a few open files are usually acceptable for file-level jobs; image jobs should be clean.
   - **Network/offsite upload slow:** offsite copy behind schedule after a large data change. Check the client's internet (RB-NET-001), and check whether a large file dump happened.
4. **After a fix, run a manual backup** and confirm it completes successfully.
5. **Check retention health:** confirm the recovery point chain is intact (no broken chain warnings) and the retention matches the client's tier: Essentials add-on 14 days daily; Professional 30 daily + 12 monthly; Premier 30 daily + 12 monthly + 7 yearly.

## Thresholds

| Situation | Action |
|---|---|
| 1 failure, retry succeeds | Document, close |
| 2 consecutive failures on the same item | Tier 2 works it as **P3**; tell Tom Kessler in the ticket |
| No successful backup for 48 hours on a server | **P2**, Tom Kessler |
| No successful backup for 72 hours on anything, or backup appliance offline | **P2**, Tom Kessler, and inform the client's account manager |
| Backup failures plus signs of ransomware (encryption, mass renames, VSS deleted) | **P1**, Tom Kessler immediately |

## Priority guidance

- Backup failures do not usually affect users, so they are internally driven tickets. Response is about protecting the client before they need a restore.
- Do not wait for users to notice. A missed backup only matters the day someone needs a restore.
- After hours: backup failures are worked next business morning unless the protected item is a Premier client server with 48+ hours of failures, or there are signs of ransomware.

## Escalate if

- Repeated VSS failures that a service restart does not fix: Tom Kessler.
- M365 backup authorization errors: Renee Castillo.
- Backup appliance hardware failure, storage full, or offsite replication broken for more than 24 hours: Tom Kessler.
- A client's protected item has been removed or excluded without a ticket explaining why: Tom Kessler and the account manager.

## Ticket notes

- Protected item, job name, error text, consecutive failure count
- Last successful backup time before and after the fix
- Steps taken (retry, agent restart, VSS writer fixes)
- Manual backup result
- Any follow-up scheduled (reboot in maintenance window, disk expansion)

## Revision history

| Version | Date | Author | Change |
|---|---|---|---|
| 1 | 2021-11-15 | Tom Kessler | Initial VaultLine failure procedure. |
| 2 | 2025-05-05 | Tom Kessler | Added threshold table, daily report review at 7:30 AM, M365 authorization errors. |
