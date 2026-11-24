---
doc_id: RB-NET-001
title: Internet outage triage
doc_type: runbook
version: "4"
effective_date: 2026-09-29
owner: Tom Kessler
audience: internal
---

# RB-NET-001 Internet outage triage

## Purpose / When to use

Use when a client site has lost internet: users report "no internet", Teams and email are down for everyone at a site, or Beacon RMM shows a **Site offline** alert (most or all agents at one site dropped at the same time). Internet down for a site is a **P1** by definition.

## Prerequisites / access needed

- Beacon RMM (site view, last check-in times)
- FortiGate access: FortiCloud portal or direct GUI/SSH via the backup WAN where present (credentials in LockBox Vault)
- UniFi Site Manager (unifi.ui.com) for clients with UniFi gateways
- Client's Atlas Docs network page: ISP, circuit ID, ISP support number, modem location, whether a backup WAN exists
- RB-NET-004 (Firewall WAN failover check)
- A site contact on the phone

## Steps

### 1. Confirm scope (first 5 minutes)

1. Open the P1 ticket per RB-GEN-001 and post it in the Service Desk channel. Call the site contact.
   - In Beacon RMM, check the site: are all agents offline at the same time? Are agents at the client's other sites online (multi-site clients like Sunbeam Child Care Centers, Timberhaus Furniture, Arbor Mill Storage)?
   - Ask the site contact: Is power on in the building? Are lights on the network equipment? Is it everyone, or only Wi-Fi users (Wi-Fi only: RB-NET-002)? Can they browse from a phone on cellular (rules out a broader outage such as Microsoft 365, see https://status.cloud.microsoft)?
   - Check whether other Larkspur clients on the same ISP are affected. Two or more clients down at once suggests an ISP or regional outage; tell Tom Kessler right away.

### 2. Run the WAN failover check (RB-NET-004)

2. **If the site has a backup WAN** (LTE or second ISP), go to **RB-NET-004** now and run its "Check current WAN state" steps, including the secondary WAN addressing check. Do this before anyone power-cycles anything.
   - Failed over and users working: the site is degraded, not down. Downgrade to **P2** with a note, handle the backup-link side effects listed in RB-NET-004 (public IP change, scan-to-email, VoIP re-registration), and continue below to get the primary fixed.
   - Backup WAN should have taken over but did not (dead, misaddressed after an ISP modem swap, or failing its health check): that is a Tier 3 problem on top of the outage. Page Tom Kessler and keep going with step 3 in parallel.
   - No backup WAN on the client page: continue to step 3.

### 3. Check the firewall

3. If you can reach the FortiGate (FortiCloud, or the backup WAN), check the primary WAN interface: **Network > Interfaces** (link status, IP). From the CLI:
   ```
   get system interface physical wan1
   execute ping-options source <wan1 IP>
   execute ping 8.8.8.8
   diagnose sys sdwan health-check
   ```
   - WAN link down: physical (modem, cable, ISP handoff).
   - WAN up with an IP but no ping: ISP routing problem or upstream outage.
   - WAN has no IP (DHCP circuits): modem or ISP problem.
4. If the FortiGate itself is unreachable and has no backup WAN, you cannot check it remotely. Proceed with the site contact.

### 4. Have the site contact check the hardware

5. Walk them to the network closet (Atlas Docs has a photo and location). Check:
   - **ISP modem/ONT**: power and status lights. Note which are red, off, or blinking.
   - **FortiGate**: power light, status light. A FortiGate with no lights or a red alarm light likely needs onsite.
   - Cable from modem to FortiGate WAN port seated.
6. **Power-cycle in order:** unplug the modem/ONT 60 seconds, plug back in, wait for it to fully sync (3-5 minutes, sometimes longer for fiber ONTs). Reboot the FortiGate only if it has not recovered 5 minutes after the modem is back. Do not have users power-cycle core switches.
7. If a UPS is in the closet, check whether it is on battery or tripped.

### 5. Call the ISP

8. If the modem shows no sync, or the WAN is up but nothing passes, call the ISP using the number and circuit ID from Atlas Docs. Most business ISPs need the account holder's authorization; our client pages note whether Larkspur is an authorized agent. If not, conference in the client's authorized contact.
9. Get a ticket number and ETA from the ISP. Put both in the Harbor PSA ticket. Ask the ISP to call our support line with updates.
10. If the ISP swapped or replaced a modem or gateway as part of the fix, re-run the RB-NET-004 addressing check afterward; handoff IPs and gateways sometimes change.

### 6. Communicate and track

11. Update the client every 30 minutes (P1 cadence) even if the update is "waiting on ISP".
12. If no backup WAN exists and the ISP ETA is long, offer workarounds: staff use phone hotspots for critical tasks, work from home, temporary LTE router (Tier 3 can drop one off via Isaac Brennan).
13. When service returns: confirm Beacon agents reconnect, users can browse, VPN tunnels and VoIP phones re-register (RB-VOIP-001), traffic has failed back to the primary (RB-NET-004), and scan-to-email works if the public IP changed (RB-PRT-002).

## Onsite

Dispatch through Isaac Brennan (ext. 224) per RB-GEN-003 if the FortiGate appears dead, cabling is damaged, or the site contact cannot safely check equipment. Premier clients' onsite is included; Professional uses monthly onsite hours (4 hours/month); Essentials is billable.

## Priority guidance

- Site internet down, no failover: **P1**. Response targets: Essentials 1 hour (business hours only), Professional 30 minutes (24x7), Premier 15 minutes (24x7). Resolution target 4 hours (often dependent on the ISP; document ISP delays).
- Failed over to backup WAN and users working: downgrade to **P2** with a note; keep the ticket open until the primary is back and traffic fails back.
- After hours: Premier and Professional P1s are worked per RB-GEN-002 (included). Essentials after-hours work is billable at $247.50/hour (1-hour minimum) with authorized contact approval.

## Escalate if

- Not resolved or no clear ISP ETA within 30 minutes: Tom Kessler.
- Backup WAN present but did not take over: Tom Kessler immediately.
- FortiGate shows hardware failure, config loss, or boot loop: Tom Kessler, and onsite via Isaac Brennan.
- Multiple clients down: Tom Kessler and Marcus Oyelaran.
- Signs of attack (FortiGate CPU pegged, unusual traffic, firewall policies changed): Tom Kessler immediately.

## Ticket notes

- Time outage started (from Beacon) and time reported
- Scope: site(s), users affected, failover status and RB-NET-004 result
- What the site contact saw (modem lights, firewall lights)
- Power-cycle actions and results
- ISP name, ticket number, ETA, and updates
- Time restored and verification steps

## Revision history

| Version | Date | Author | Change |
|---|---|---|---|
| 1 | 2019-08-05 | Tom Kessler | Initial outage triage. |
| 2 | 2022-06-27 | Tom Kessler | Added Beacon RMM site offline check and FortiGate CLI commands. |
| 3 | 2025-07-14 | Tom Kessler | Added SD-WAN failover checks, ISP authorization note, post-restore checks for VoIP and scan-to-email. |
| 4 | 2026-09-29 | Tom Kessler | Moved WAN failover check to step 2 after EMS outage review. |
