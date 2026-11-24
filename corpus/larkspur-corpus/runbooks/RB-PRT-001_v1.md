---
doc_id: RB-PRT-001
title: Printer shows offline
doc_type: runbook
version: "1"
effective_date: 2022-11-07
owner: Andre Mitchell
audience: internal
---

# RB-PRT-001 Printer shows offline

## Purpose / When to use

Use when a user says their printer shows **Offline** in Windows or jobs are stuck in the queue. Applies to network HP and Brother printers at client sites.

## Prerequisites / access needed

- Beacon RMM remote session to the user's PC with admin rights
- Client's Atlas Docs page with the printer list and drivers

## Steps

1. Ask the user to check that the printer is on and has paper and no jam showing on the screen.
2. Ask whether other people can print to it. If nobody can, power-cycle the printer and wait 2 minutes.
3. **Restart the Print Spooler** on the user's PC:
   ```powershell
   Restart-Service -Name Spooler -Force
   ```
   Or services.msc > Print Spooler > **Restart**.
4. Try printing a test page (Printer properties > General > Print Test Page).
5. If it still shows offline, **remove the printer**: Settings > Bluetooth & devices (Windows 11) or Devices > Printers & scanners (Windows 10) > select the printer > **Remove**.
6. **Re-add the printer**: Printers & scanners > **Add device**. If it does not appear, choose **Add manually** > **Add a printer using an IP address or hostname** > enter the printer's IP from the client page > select the driver (HP Universal Print Driver or Brother driver from the client page).
7. Print a test page and have the user print their document.
8. If the printer is offline for everyone, check the network cable at the printer and power-cycle again before escalating.

## Priority guidance

- One user unable to print: P3.
- Whole office unable to print: P2.

## Escalate if

- The printer does not respond for anyone after a power cycle: Tier 2.
- Hardware errors on the printer: request an onsite visit through Isaac Brennan.
- Driver install fails: Tier 2.

## Ticket notes

- Printer name and IP
- Spooler restarted, printer removed and re-added
- Test page result

## Revision history

| Version | Date | Author | Change |
|---|---|---|---|
| 1 | 2022-11-07 | Andre Mitchell | Initial printer offline procedure. |
