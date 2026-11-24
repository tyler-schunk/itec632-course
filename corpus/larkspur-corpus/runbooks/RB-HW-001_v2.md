---
doc_id: RB-HW-001
title: Laptop/desktop won't boot
doc_type: runbook
version: "2"
effective_date: 2024-09-09
owner: Brian Novak
audience: internal
---

# RB-HW-001 Laptop/desktop won't boot

## Purpose / When to use

Use when a user's Dell laptop or desktop will not power on, powers on but shows nothing, stops at a BitLocker recovery screen, loops on "Preparing Automatic Repair", or shows a blue screen at startup. Most of our fleet is Dell Latitude and OptiPlex with Windows 11 and 3-year ProSupport, so Dell diagnostics and warranty dispatch are central here.

## Prerequisites / access needed

- Phone contact with the user (the device is probably offline in Beacon RMM)
- Beacon RMM (last check-in, last reboot, recent patches)
- Entra admin center / Intune (BitLocker recovery keys)
- Device asset tag (`LR-<CLIENT>-####`) and Dell service tag (in Harbor PSA asset record)
- Dell TechDirect access for warranty dispatch (Brian Novak or field techs)

## Steps

### 1. No power at all

1. Confirm the power source: laptop charger plugged into a known-good outlet, charger LED on (Dell barrel chargers have a light ring), USB-C charger fully seated. Desktop: power strip on, cable seated at both ends.
2. Laptop: **remove from dock** and connect the charger directly. Docks are a common culprit (see RB-HW-003).
3. **Power drain / flea power reset:** unplug everything, hold the power button 30 seconds, then plug in only the charger and power on. Many Latitudes recover from this.
4. Watch the **battery/power LED**. Dell laptops blink amber/white codes for hardware faults (for example, blinking amber 2 times then white 3 times). Have the user count the pattern and look it up on Dell's support site for that model's LED code table. Record the code.
5. Desktop OptiPlex: the power button LED pattern means the same thing; solid amber or blinking amber usually indicates power supply or board issues.

### 2. Powers on, black screen

6. Is there fan noise, keyboard backlight, Caps Lock light toggling? Then it may be a display issue: connect an external monitor (laptop) or try another cable/port (desktop). Press **Win+Ctrl+Shift+B** to reset the graphics driver.
7. If the Dell logo appears and stops, run **Dell ePSA/SupportAssist diagnostics**: power on and tap **F12**, select **Diagnostics**. Record any error code and validation code. A failed diagnostic on a ProSupport device goes straight to warranty dispatch.

### 3. BitLocker recovery screen

8. Common after BIOS updates, dock changes, or TPM resets. It is not a failure.
9. **Verify the user's identity** before giving out a key (callback to the number on file in Harbor PSA, as in RB-ACC-001).
10. Get the key: Entra admin center > **Devices > All devices** > select device > **BitLocker keys** (or Intune admin center > Devices > select device > **Recovery keys**). Match the **Key ID** shown on the user's screen (first 8 characters).
11. Read the 48-digit key to the user. Do not email it or put it in the ticket. After boot, have Beacon RMM or Intune rotate the key if the device is Intune-managed (Devices > select device > ... > **BitLocker key rotation**).
12. If no key is found, stop and escalate: the drive cannot be unlocked without it.

### 4. Automatic Repair loop / boot errors

13. From the recovery environment (it appears after two failed boots, or boot from the field tech's USB): **Troubleshoot > Advanced options**:
    - **Uninstall Updates**: remove the latest quality update if the problem started after patch night. Check Beacon RMM patch history for the date.
    - **Startup Repair**.
    - **System Restore** if restore points exist.
14. Command Prompt (Tier 2):
    ```
    chkdsk C: /f
    sfc /scannow /offbootdir=C:\ /offwindir=C:\Windows
    bcdboot C:\Windows
    ```
    You may need the BitLocker key to unlock C: first (`manage-bde -unlock C: -RecoveryPassword <key>`).
15. If Windows will not recover and the user's data is in OneDrive (Known Folder Move is standard), the fastest path is usually **reset or reimage** (Intune Autopilot Reset if it boots far enough, or USB reinstall and Autopilot) rather than long repair attempts. Confirm OneDrive was synced (check the last-sync time in the M365 admin center or with the user) before wiping.

### 5. Get the user working

16. If the device will be down more than an hour or two, offer a loaner (client spare pool or Larkspur loaner shelf) and set up via RB-HW-002 or web access to M365.

### 6. Warranty dispatch

17. Brian Novak or a field tech opens the Dell TechDirect case with the service tag, LED code or ePSA codes. Dell ProSupport usually sends parts and often a Dell technician next business day. Tell Isaac Brennan so he can coordinate with the client and avoid double-booking our tech.
18. Out-of-warranty devices: get repair-vs-replace guidance from the account manager; the client approves any purchase.

## Priority guidance

- Single user device down, loaner or other device available: **P3**.
- Single user device down, no workaround: **P3**; VIP with no workaround: **P2**.
- Multiple devices failing to boot after the same patch night: **P1** or **P2** depending on scale; escalate immediately (Lena Fischer for patch issues, see RB-SW-002).

## Escalate if

- No BitLocker key found: Renee Castillo.
- Several devices failing after the same update: Lena Fischer and Tom Kessler right away; pause the patch ring in Beacon RMM.
- Physical damage (liquid, drop, swollen battery): stop using the device; swollen batteries are a fire risk; onsite via Isaac Brennan. Accidental damage may not be covered by ProSupport; account manager handles the quote.
- Hardware fault confirmed: Brian Novak for warranty dispatch.

## Ticket notes

- Device asset tag, service tag, model
- Symptoms, LED codes, ePSA error and validation codes
- BitLocker key provided (yes/no, Key ID only), identity verification method
- Repair steps and result, or warranty case number
- Loaner provided (asset tag)

## Revision history

| Version | Date | Author | Change |
|---|---|---|---|
| 1 | 2020-05-18 | Brian Novak | Initial no-boot checklist. |
| 2 | 2024-09-09 | Brian Novak | Added BitLocker key retrieval from Entra/Intune, key rotation, reimage-over-repair guidance with OneDrive KFM. |
