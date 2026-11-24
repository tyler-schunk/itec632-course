---
doc_id: RB-PRT-001
title: Printer shows offline
doc_type: runbook
version: "2"
effective_date: 2024-08-19
owner: Andre Mitchell
audience: internal
---

# RB-PRT-001 Printer shows offline

## Purpose / When to use

Use when a user reports a printer shows **Offline** in Windows, jobs sit in the queue and never print, or "Error - Printing" won't clear. Applies to network HP and Brother printers/MFPs at client sites, printed to directly from Windows 10/11 PCs via a Standard TCP/IP port. If the printer is shared from a client print server, see the print server note in step 9.

Work the steps **in order**. Most "offline" printers are either a network/IP problem or a stuck spool, and clearing the spool before confirming the printer is reachable just wastes time.

## Prerequisites / access needed

- Beacon RMM remote session to the user's PC (run as admin for spooler steps)
- Client's Atlas Docs page: printer list with IP addresses, DHCP reservations, and printer web UI credentials (in LockBox Vault)
- UniFi or FortiGate access is helpful but not required (Tier 2/3)

## Steps

### 1. Check power and network first

1. Ask the user (or a coworker near the printer) to look at the printer:
   - Is it powered on and awake? Press a button to wake it from sleep.
   - Any error on the front panel (paper jam, toner, "door open", "IP conflict")? Clear physical errors first; jams and empty trays often show as "offline" or "error" in Windows.
   - Is the network cable plugged in with link lights? On Wi-Fi printers, is the Wi-Fi indicator solid?
2. **Find the printer's current IP** from its front panel (HP: Settings/Network or the network icon; Brother: Menu > Network > Wired LAN or WLAN > TCP/IP). Compare with the IP in the client's Atlas Docs printer list and the IP on the Windows port:
   - On the user's PC: Settings > Bluetooth & devices > Printers & scanners > the printer > **Printer properties** > **Ports** tab, note the checked port and its address (Configure Port).
3. From the user's PC, test reachability:
   ```powershell
   Test-Connection 10.20.1.45 -Count 4
   Test-NetConnection 10.20.1.45 -Port 9100
   ```
   Then open `http://<printer IP>` in a browser. If the web page loads, the printer is on the network.
4. **If the printer is not reachable at all:** check whether other PCs can print to it. If nobody can reach it, it is a printer or network problem, not a PC problem. Power-cycle the printer (off 30 seconds). Check the cable and switch port. If it still does not respond, escalate to Tier 2 or request onsite (see Escalate if).

### 2. Clear the stuck spool

5. With the printer confirmed reachable, clear the queue on the user's PC. The spool files must be deleted **while the Print Spooler service is stopped**, otherwise Windows holds them open.
   ```powershell
   Stop-Service -Name Spooler -Force
   Remove-Item -Path "C:\Windows\System32\spool\PRINTERS\*" -Force
   Start-Service -Name Spooler
   ```
   GUI equivalent: services.msc > Print Spooler > **Stop**; delete everything inside `C:\Windows\System32\spool\PRINTERS` (the files, not the folder); then Print Spooler > **Start**.
   Beacon RMM script library has this as **LR - Clear Print Spooler**.
6. **Start the spooler** (the script does this). Confirm the service is Running and set to Automatic.

### 3. Fix the port only if the IP changed

7. **Only if the printer's IP is different** from the IP on the Windows port: Printer properties > **Ports** > **Add Port** > Standard TCP/IP Port > enter the current IP > finish, then check the new port and Apply. Or update the existing port's address via **Configure Port**.
   - Then fix the root cause: ask Tier 2 to set a **DHCP reservation** (UniFi gateway or FortiGate DHCP server) or a static IP on the printer, and update the Atlas Docs printer list.
   - If the IP has not changed, do not touch the port or remove the printer.
8. While in Configure Port, uncheck **SNMP Status Enabled** if the printer keeps reporting offline even though it prints; some Brother and older HP models answer SNMP badly and Windows marks them offline.

### 4. Test and print server note

9. Print a Windows test page (Printer properties > General > **Print Test Page**). Have the user print their real document.
   - **Print server:** if the printer is shared from a client server (`\\SERVER\Printer`) and several users are affected, the spool to clear is on the print server, not the PCs. That is Tier 2: clearing the server spooler interrupts printing for everyone on that server, so tell the site contact first.
10. Remove and re-add the printer only as a last resort, after the steps above, if the driver itself is corrupt (errors referencing the driver, printer properties will not open). Use the current driver from the client's Atlas Docs page or the HP/Brother universal driver.

## Priority guidance

- One user cannot print, others can, or the user has another printer nearby: **P3**.
- A shared printer is down for a whole office or department, or it blocks a key function (front desk check-in/check-out at a clinic, shipping labels at a warehouse): **P2**.
- Printer needs hands-on work (hardware fault, fuser, network jack): request onsite through Isaac Brennan per RB-GEN-003.

## Escalate if

- Printer unreachable from all PCs after a power cycle: Tier 2 (network check, switch port, DHCP), then onsite via Isaac Brennan.
- Front panel shows a hardware error (fuser, scanner, formatter): onsite via Isaac Brennan; the client may have a separate copier lease vendor for MFPs (check client page) and should call them.
- IP conflicts or DHCP scope problems: Tom Kessler.
- Printer works but jobs from one application fail (EHR, practice management, label software): Tier 2.

## Ticket notes

- Printer name, model, IP (expected vs actual)
- Physical checks done and reachability result (ping / port 9100 / web UI)
- Spool cleared (stopped spooler, cleared folder, started spooler), number of stuck jobs
- Whether the port was changed and why
- Test page result and user confirmation

## Revision history

| Version | Date | Author | Change |
|---|---|---|---|
| 1 | 2022-11-07 | Andre Mitchell | Initial printer offline procedure. |
| 2 | 2024-08-19 | Andre Mitchell | Reordered: check power/network and IP first. Clear spool folder with spooler stopped, then start spooler. Re-add port only if IP changed. Remove/re-add printer is last resort. Added SNMP status note and print server note. |
