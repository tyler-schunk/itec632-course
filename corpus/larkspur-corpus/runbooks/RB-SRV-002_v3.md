---
doc_id: RB-SRV-002
title: Server unresponsive
doc_type: runbook
version: "3"
effective_date: 2025-08-25
owner: Tom Kessler
audience: internal
---

# RB-SRV-002 Server unresponsive

## Purpose / When to use

Use when a client server stops responding: Beacon RMM shows the server agent offline, users cannot reach file shares or a line-of-business app hosted on it, RDP fails, or the server is hung at a black screen. Covers physical Dell PowerEdge servers and Hyper-V virtual machines at client sites. A server that most users depend on being down is a **P1**.

## Prerequisites / access needed

- Beacon RMM (agent status, last check-in, recent alerts, patch history)
- LockBox Vault: server admin, Hyper-V host, and **iDRAC** credentials
- Remote access to the site (another online device via Beacon, or FortiGate VPN) to reach the iDRAC or host
- Client Atlas Docs server page: server roles, host/VM layout, iDRAC IP, UPS, maintenance window
- Tier 2 does initial checks; **Tier 3 (Tom Kessler) owns server recovery**. Do not hard-reset a server without Tier 3 approval unless this runbook says so.

## Steps

### 1. Confirm it is the server (first 10 minutes)

1. Open or update the ticket. If users are blocked, set **P1** per RB-GEN-001, post in the Service Desk channel, and assign Tom Kessler.
2. Check whether the **whole site** is offline in Beacon. If every agent at the site dropped, it is an internet or power problem: go to RB-NET-001.
3. From another device at the site (Beacon remote shell on a workstation):
   ```powershell
   Test-Connection SERVER01 -Count 4
   Test-NetConnection SERVER01 -Port 445    # file shares
   Test-NetConnection SERVER01 -Port 3389   # RDP
   ```
   - Ping fails: server is off, hung, or network-isolated.
   - Ping works but services fail: the OS is up but a service or the app is stuck. Try RDP or Beacon remote shell to the server.
4. Check Beacon alerts for the last 24 hours: low disk (RB-SRV-001), high CPU/memory, patch reboot pending, VaultLine job running.

### 2. OS up, services stuck

5. RDP or Beacon shell in. Check:
   - Task Manager / `Get-Process | Sort CPU -Descending | Select -First 10` for a runaway process.
   - Services for the role (Server service/LanmanServer for shares, SQL Server, the LOB app's services). Restart the specific stuck service rather than the whole server.
   - Event Viewer > System and Application for errors around the time it started.
   - Disk space on all volumes.
6. If a reboot is clearly needed (Windows Update half-applied, memory exhausted), **Tier 3 approves** and the client's site contact is told first: everyone using the server will be disconnected.

### 3. Server not responding at all

7. **Physical server:** log in to the **iDRAC** web interface (IP from the client page). Check:
   - Power state and the virtual console (is it at a blue screen, hung at boot, or showing a login screen?).
   - **Lifecycle Log / System Event Log** for hardware faults (memory, PSU, disk/RAID controller).
   - Storage: virtual disk state (degraded or failed RAID).
8. **Virtual machine:** connect to the Hyper-V host (Beacon or RDP). In Hyper-V Manager, check the VM state (Running, Paused, Saved) and the host's own health. A VM that shows **Paused-Critical** usually means the host volume holding its VHDX is full: free space on the host (Tier 3), then resume.
9. **Restart decision (Tier 3):** if the console shows a hung OS or blue screen and there is no hardware fault, Tom may approve a graceful shutdown via iDRAC or Hyper-V (**Shut Down**), then a power reset only if that fails. Record the time.
10. **No iDRAC access and no one onsite:** dispatch through Isaac Brennan per RB-GEN-003. For P1s, Isaac sends the next available field tech same day.

### 4. After recovery

11. Confirm services are up and users can work (have the site contact test the shares or app).
12. Check VaultLine: did backups run? If the server was down overnight, run a manual backup once it is stable (RB-BAK-002).
13. Find the cause: event logs (unexpected shutdown event 6008, bugcheck 1001), iDRAC log, patch history. Hardware faults on servers under warranty go to Dell ProSupport via Tom Kessler.

## Priority guidance

- Server down and most users blocked (file server, LOB app server, DC with no backup DC): **P1**. Response targets: Essentials 1 hour business hours only, Professional 30 minutes 24x7, Premier 15 minutes 24x7. Resolution target 4 hours.
- Server degraded or a secondary server down with limited impact: **P2**.
- After hours: P1 is worked for Premier and Professional (included). For Essentials, after-hours work is billable with authorized contact approval (RB-GEN-002).

## Escalate if

- Any P1 server outage: Tom Kessler from the start.
- Hardware fault in the iDRAC log or degraded RAID: Tom Kessler; Dell ProSupport case.
- Signs of ransomware (encrypted files, ransom notes, VSS deleted): Tom Kessler immediately, then Marcus Oyelaran. Do not reboot or restore until Tom says so.
- Server not under a server management agreement: still stabilize a P1, then tell the account manager.

## Ticket notes

- Time down (Beacon last check-in), time reported, time restored
- Ping/port test results, console state, iDRAC or Hyper-V findings
- Who approved any restart, and exact time
- Root cause if found, follow-up tickets (hardware case, capacity)
- Backup status after recovery

## Revision history

| Version | Date | Author | Change |
|---|---|---|---|
| 1 | 2019-10-14 | Tom Kessler | Initial server down checklist. |
| 2 | 2022-04-04 | Tom Kessler | Added iDRAC checks and Hyper-V Paused-Critical guidance. |
| 3 | 2025-08-25 | Tom Kessler | Tier 3 approval for restarts, post-recovery backup check, ransomware stop rule. |
