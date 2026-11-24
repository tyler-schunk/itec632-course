---
doc_id: RB-SW-002
title: Windows Update failures
doc_type: runbook
version: "2"
effective_date: 2025-02-10
owner: Lena Fischer
audience: internal
---

# RB-SW-002 Windows Update failures

## Purpose / When to use

Use when Beacon RMM reports a device failing patch installation repeatedly, a device is behind on cumulative updates, a user sees "Some update files are missing or have problems" or "We couldn't complete the updates, undoing changes", or a device is stuck in a patch reboot loop.

## Background

- Beacon RMM manages patching for all managed workstations and servers. Workstations patch in rings: **Pilot** (Larkspur internal and a few client volunteers) on Patch Tuesday + 2 days, **Broad** the following week. Install window is overnight with a reboot; users get a deferral prompt.
- Servers patch in the client's agreed maintenance window (see client page), managed by Tier 3.
- A device that fails the same update **twice** generates a Beacon ticket automatically.

## Prerequisites / access needed

- Beacon RMM (patch status, script library, remote shell)
- Remote session with admin rights (LAPS / LockBox Vault)

## Steps

1. **Read the failure in Beacon:** device > Patch Management > history. Note the KB number and the error code. Common codes:
   - `0x800f0922`: often low space on the System Reserved/recovery partition, or .NET/servicing issues.
   - `0x80070002` / `0x80070003`: missing files in the update store.
   - `0x800f081f` / `0x800f0831`: component store corruption.
   - `0x80070070`: not enough disk space.
   - `0x8024402c` / `0x80072efd`: cannot reach update source (network/proxy).
2. **Check disk space.** Cumulative updates need several GB free. Under 10 GB free on C: run Disk Cleanup (`cleanmgr /sageset` and `/sagerun`, or Settings > System > Storage > Temporary files) and clear `C:\Windows\SoftwareDistribution\Download` as part of step 4.
3. **Check pending reboot.** If the device has not rebooted in weeks, reboot first and retry the patch from Beacon. Many failures clear here.
4. **Reset Windows Update components** (Beacon script **LR - Reset Windows Update**, or manually from an elevated prompt):
   ```
   net stop wuauserv
   net stop bits
   net stop cryptsvc
   ren C:\Windows\SoftwareDistribution SoftwareDistribution.old
   ren C:\Windows\System32\catroot2 catroot2.old
   net start cryptsvc
   net start bits
   net start wuauserv
   ```
5. **Repair the component store and system files:**
   ```
   DISM /Online /Cleanup-Image /RestoreHealth
   sfc /scannow
   ```
   DISM can take 15-30 minutes. Reboot afterward and retry the update from Beacon.
6. **Manual install:** download the specific KB from the Microsoft Update Catalog (https://www.catalog.update.microsoft.com) and install the .msu with `wusa.exe <file>.msu /quiet /norestart`, then reboot.
7. **Stuck in "undoing changes" loop:** boot to Windows RE > Troubleshoot > Advanced options > **Uninstall Updates** > latest quality update. Then hide the KB in Beacon for that device and escalate (see below). See RB-HW-001 if it will not boot at all.
8. **Feature updates (for example 23H2 to 24H2):** failures here often come from old drivers or apps. Run Dell Command | Update first. Check `C:\$WINDOWS.~BT\Sources\Panther\setuperr.log` for the blocking item. Feature updates are scheduled by Lena Fischer per client; do not force one on a user without checking the client's schedule.
9. **Verify:** Beacon shows the device compliant after its next scan, Settings > Windows Update shows up to date.

## Priority guidance

- One device behind on updates, working normally: **P4** (or P3 if it is more than 2 months behind; it falls out of compliance).
- Device unusable after an update (boot loop, broken app): **P3** single user, **P2** VIP.
- Same update breaking many devices: **P1/P2**. Pause the ring in Beacon RMM immediately and escalate.

## Escalate if

- An update causes widespread issues (several devices or clients): Lena Fischer and Tom Kessler immediately; pause the ring.
- Server patch failures: Tom Kessler (servers are Tier 3).
- DISM cannot repair the component store (source files not found): Tier 2; in-place repair upgrade or reimage may be needed (RB-HW-002), with user data confirmed in OneDrive first.
- Recovery partition too small for an update (common `0x800f0922` with WinRE updates): Tier 2; resizing partitions is a Tier 2 task.

## Ticket notes

- KB number and error code
- Disk space before/after, last reboot
- Steps done (reset components, DISM/SFC results, manual install)
- Whether the KB was hidden or the ring paused, and who approved
- Final compliance status in Beacon

## Revision history

| Version | Date | Author | Change |
|---|---|---|---|
| 1 | 2021-05-10 | Lena Fischer | Initial Windows Update troubleshooting. |
| 2 | 2025-02-10 | Lena Fischer | Added Beacon patch rings, error code table, feature update log location, Update Catalog manual install. |
