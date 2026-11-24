---
doc_id: RB-HW-003
title: Docking station and monitor issues
doc_type: runbook
version: "2"
effective_date: 2025-03-17
owner: Brian Novak
audience: internal
---

# RB-HW-003 Docking station and monitor issues

## Purpose / When to use

Use when a user's external monitors are black, flickering, at the wrong resolution, or in the wrong order; the dock's USB devices (keyboard, mouse, headset, wired network) stop working; or the laptop will not charge on the dock. Our standard docks are Dell USB-C / Thunderbolt docks (WD19S, WD22TB4, and the newer Dell Pro Dock series) paired with Latitude laptops.

## Prerequisites / access needed

- Beacon RMM remote session (works only if the laptop has network; if the dock's Ethernet is what is broken, ask the user to switch to Wi-Fi)
- Dock model and asset tag if tagged (`LR-<CLIENT>-####`)
- Dell Command | Update available on the laptop (installed by Intune on all managed devices)

## Steps

### 1. Basics (with the user)

1. **Reseat the USB-C/Thunderbolt cable** at the laptop. Use the correct port: Latitude laptops have Thunderbolt/USB-C ports marked with a lightning bolt or DisplayPort symbol. A plain USB-C port may charge but will not drive monitors.
2. Check the dock's power brick is plugged in and the dock's power LED is on.
3. Check monitor power, input source (menu button on the monitor: DisplayPort vs HDMI), and cables at both ends.
4. **Dock power reset:** unplug the laptop from the dock, unplug the dock's power for 30 seconds, plug power back in, wait for the LED, then reconnect the laptop. This fixes most "dock stopped working" calls.
5. Reboot the laptop while connected to the dock.

### 2. Display settings

6. Windows: **Settings > System > Display**. Click **Detect** under Multiple displays. Use **Identify** to show numbers; drag monitors to match the physical layout. Set "Extend these displays".
7. Set each monitor to its native resolution (marked "Recommended") and the scale the user likes.
8. **Win+P** cycles projection modes if the user accidentally switched to "PC screen only".
9. Flicker or one monitor dropping: try another cable (DisplayPort cables fail often), then another port on the dock. Daisy-chaining (DisplayPort MST) through monitors is unreliable on some models; prefer direct cables from the dock.

### 3. Firmware and drivers

10. Run **Dell Command | Update** with the laptop connected to the dock. It updates BIOS, Thunderbolt firmware, graphics drivers, and dock firmware for supported Dell docks. Reboot when prompted. BIOS updates can trigger BitLocker recovery if BitLocker is not suspended; Dell Command | Update suspends it automatically, but have the recovery key process ready (RB-HW-001 step 8).
11. For docks not covered by Dell Command | Update, download the dock firmware utility from Dell support for that dock model.
12. Device Manager: check **Display adapters** and **Universal Serial Bus controllers** for errors. Update the Intel graphics driver through Dell Command | Update rather than Windows Update where possible.

### 4. Charging and USB

13. "Slow charger" or not charging: older docks may supply less wattage than the laptop wants. Check the dock wattage against the laptop's charger. Not charging at all with power on the dock suggests a cable or dock fault.
14. USB devices dead but displays fine: dock power reset, then try devices directly in the laptop. If they work direct, the dock's USB controller or firmware is the issue.
15. Dock Ethernet not working: check the dock network adapter in Network Connections, check the cable and wall jack (try the cable directly in the laptop with a USB-C adapter if available). Wall jack issues: RB-NET-002 / Tier 2 for switch port checks.

### 5. Swap test

16. If you can, swap in a known-good dock (client spare, or have a field tech bring one). If the problem follows the dock, the dock is faulty.
17. Docks purchased with the laptop under ProSupport may be covered; Brian Novak handles Dell TechDirect cases. Otherwise the client approves a replacement purchase through the account manager.

## Priority guidance

- Single user, can work on the laptop screen: **P3**.
- Several users at one site after a recent update (BIOS, graphics driver): **P2**; pause the update in Beacon RMM and tell Lena Fischer.
- New setups or moving monitors: **P4**.

## Escalate if

- Firmware update fails or leaves the dock unresponsive: Tier 2, then Brian Novak.
- Hardware fault confirmed and swap needed onsite: request through Isaac Brennan (RB-GEN-003).
- Many docks of one model failing: Brian Novak and Rachel Kim (may affect the hardware standard).

## Ticket notes

- Dock model, laptop model, which port used
- Steps tried (reseat, power reset, display detect, cable swap)
- Firmware/driver versions before and after Dell Command | Update
- Result of swap test, warranty case number if any

## Revision history

| Version | Date | Author | Change |
|---|---|---|---|
| 1 | 2021-07-19 | Brian Novak | Initial dock troubleshooting. |
| 2 | 2025-03-17 | Brian Novak | Added Dell Command | Update as primary firmware tool, BitLocker caution, WD22TB4 and Pro Dock models. |
