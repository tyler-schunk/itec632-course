---
doc_id: RB-NET-002
title: Wi-Fi connectivity problems (UniFi)
doc_type: runbook
version: "2"
effective_date: 2024-12-02
owner: Tom Kessler
audience: internal
---

# RB-NET-002 Wi-Fi connectivity problems (UniFi)

## Purpose / When to use

Use when users at a client site report Wi-Fi problems on a Ubiquiti UniFi network: can't connect, connected but no internet, slow, or dropping. For a site where wired users are also down, use RB-NET-001 instead.

## Prerequisites / access needed

- UniFi Site Manager (https://unifi.ui.com) with Larkspur's admin account (LockBox Vault: "UniFi - Larkspur MSP"), or the client's self-hosted UniFi Network application URL from their Atlas Docs page
- Beacon RMM remote session to an affected laptop if available
- Client's Atlas Docs network page: SSIDs, VLANs, AP locations map

## Steps

### 1. Scope it

1. One user or many? One device or all of that user's devices? One area of the building or everywhere? Corporate SSID only or guest too?
2. In UniFi Network > **Devices**: are all APs **Online**? An AP showing **Disconnected** or **Adopting** in the area with complaints is the likely cause.
3. **Client Devices** list: find the user's device (by hostname or MAC). Note the AP it is connected to, signal (dBm), channel, band, and experience/satisfaction score.

### 2. Single user / single device

4. Signal weaker than about -70 dBm: user is too far from the AP or behind obstacles. Move closer to test. Recurring complaint from one spot is a coverage issue: note it for Tom Kessler.
5. On the Windows laptop:
   - Forget the network and reconnect: Settings > Network & internet > Wi-Fi > **Manage known networks** > select SSID > **Forget**.
   - Check the IP: `ipconfig /all`. A 169.254.x.x address means DHCP failed (see step 9).
   - Reset the stack if needed (admin):
     ```
     netsh winsock reset
     netsh int ip reset
     ipconfig /flushdns
     ```
     Reboot after.
   - Update the Wi-Fi driver with **Dell Command | Update** (Intel Wi-Fi driver updates fix many drop issues on Latitudes).
   - Power management: Device Manager > Network adapters > Wi-Fi adapter > Power Management > uncheck "Allow the computer to turn off this device to save power".
6. Phones: forget network and rejoin; turn off "private/random MAC" for the corporate SSID only if the client's network uses MAC filtering (rare).
7. Password recently changed? If the client rotated the Wi-Fi PSK, every device needs the new key. The current PSK is in LockBox Vault for that client.
8. Older devices that cannot join a **WPA3** or WPA2/WPA3 transition SSID: check the SSID's security setting in UniFi > Settings > WiFi. Do not lower security without Tom Kessler's approval.

### 3. Many users / one area

9. **DHCP exhaustion:** many users "connected, no internet" with 169.254 addresses. Check the DHCP scope on the gateway (UniFi gateway: Settings > Networks > the network > DHCP range; FortiGate: Network > Interfaces > the VLAN > DHCP Server, and Dashboard > DHCP monitor). Guest networks with long lease times fill up. Tier 3 can shorten lease time or expand the scope.
10. **AP offline:** in UniFi Devices, an offline AP usually means lost PoE. Check the switch port in UniFi (Ports view) and whether the switch or PoE injector is up. **Restart** the AP from UniFi (Device > Settings/Manage > Restart). If it stays offline, power-cycle the PoE port from the switch (Port > Power Cycle) if it is a UniFi switch.
11. **Interference / channel:** UniFi Network > **Insights** or the AP's RF environment view. Many APs on the same 2.4 GHz channel or a busy 5 GHz channel cause slowness. Don't change channel plans during business hours without Tom Kessler; schedule an RF scan.
12. **Firmware:** an AP update can cause brief drops. Check the device's update history. UniFi auto-updates are scheduled after hours at our clients.

### 4. Everyone on Wi-Fi, wired fine

13. Check the gateway and switch uplink to the APs. If all APs are offline at once, the PoE switch or its uplink is down: escalate to Tier 3 and consider onsite.
14. Check the UniFi Network application itself is reachable; if the site is managed through a cloud key that died, the APs keep working with their last config but you cannot manage them.

## Priority guidance

- One user, others fine: **P3**.
- Multiple users or an area of the building (a clinic wing, a classroom block at Chalkboard Hollow Montessori, a nursing station at Willowshade Senior Living): **P2**.
- All Wi-Fi down and the business runs on Wi-Fi (many laptops, no wired drops): **P1**.

## Escalate if

- APs offline that will not come back after restart and PoE cycle: Tier 3 (Tom Kessler), possibly onsite via Isaac Brennan.
- DHCP scope or VLAN changes needed: Tom Kessler.
- Coverage gaps needing new APs: Tom Kessler, then account manager for a quote.
- Suspected rogue AP or unknown devices on the corporate SSID: Tom Kessler.

## Ticket notes

- Scope (users, area, SSID), AP name and status
- Client device details from UniFi: AP, signal, band, IP
- Actions taken (forget/rejoin, driver update, AP restart, PoE cycle)
- Any coverage or capacity issues for Tom's follow-up
- User confirmation

## Revision history

| Version | Date | Author | Change |
|---|---|---|---|
| 1 | 2020-09-14 | Tom Kessler | Initial UniFi Wi-Fi troubleshooting. |
| 2 | 2024-12-02 | Tom Kessler | Moved to UniFi Site Manager, added DHCP exhaustion, WPA3 compatibility, PoE port power cycle. |
