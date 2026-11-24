---
doc_id: RB-VOIP-001
title: Yealink desk phone not registering
doc_type: runbook
version: "2"
effective_date: 2024-07-22
owner: Andre Mitchell
audience: internal
---

# RB-VOIP-001 Yealink desk phone not registering

## Purpose / When to use

Use when a Yealink VoIP desk phone (T3x, T4x, T5x series) shows "No Service", "Registration failed", "Network unavailable", an account line icon that is not green/registered, or the phone has no dial tone. Larkspur supports the phones and the network they sit on. The phone **service** (extensions, call routing, numbers) belongs to the client's hosted VoIP provider, listed on the client's Atlas Docs page with their support contact.

## Prerequisites / access needed

- Client Atlas Docs page: VoIP provider and support number, voice VLAN ID, phone admin password (LockBox Vault), provisioning method
- UniFi or FortiGate access for Tier 2/3 (switch ports, VLANs, firewall settings)
- A site contact or the user at the phone

## Steps

### 1. One phone or many?

1. **Many phones at a site** not registering at once: internet (RB-NET-001), the switch, or the provider. Check the provider's status page (on the client page). Many phones down = **P1** if the business runs on phones (clinics, dispatch at Bluffline Logistics, auto dealership sales floor).
2. **One phone:** continue below.

### 2. Physical and network

3. Is the phone powered? Most of our clients' phones run on **PoE**. No display at all: check the cable in the **LAN/Internet** port (not the PC port), try another cable and wall jack. If the switch port has no PoE, use a Yealink power adapter as a test.
4. If a PC is daisy-chained through the phone's PC port and the PC also has no network, the cable or switch port is the issue.
5. On the phone, check its IP: **Menu > Status** (or press the **OK** key on many models). Note the IP.
   - **No IP or 169.254.x.x**: DHCP failed. Check the switch port is on the correct **voice VLAN** (UniFi port profile or FortiSwitch port), and that the voice VLAN DHCP scope has free leases.
   - IP in the **data** subnet instead of the voice subnet: VLAN tagging or LLDP/DHCP option not applied on that port. Tier 2 checks the port profile.
6. **Reboot the phone:** Menu > Advanced settings (password from LockBox Vault) > Reboot, or unplug PoE for 10 seconds. Re-registration takes 1-3 minutes.

### 3. Registration

7. Log in to the phone's web UI at `http://<phone IP>` (admin credentials in LockBox Vault). **Status** page shows each account's register status. **Account > Register** shows the SIP server, username, and register status.
8. **Registration failed (403/401)**: credentials wrong or the extension was changed at the provider. Do not retype SIP credentials by hand unless the client page says we manage them. Most providers auto-provision phones: trigger a re-provision (Settings > Auto Provision > **Autoprovision Now**) or ask the provider to push the config.
9. **Registered but one-way audio or calls drop at about 30 seconds**: classic **SIP ALG** symptom on the firewall. Escalate to Tier 3. On FortiGate, Tom Kessler handles this (`config system settings` / `set default-voip-alg-mode kernel-helper-based`, and removing the SIP session helper if the provider requires it).
10. **Phone was moved** to another desk or site: confirm the new port is on the voice VLAN; some providers lock registration to a site.
11. **Factory reset** (last resort, only if the provider auto-provisions): Menu > Advanced settings > Reset to factory, or hold **OK** for about 10 seconds on many models. The phone then needs to pull its config from the provider; confirm with the provider before resetting.

### 4. Provider ticket

12. If the phone has a valid voice VLAN IP, the network is fine, and registration still fails, open a ticket with the VoIP provider (number on client page). Give them the phone's MAC address (on the label underneath and on the Status page), model, extension, and the error. Many providers require the client's authorized contact to open tickets; if so, conference them in.
13. Put the provider ticket number in our Harbor PSA ticket and set status to **Waiting on Vendor**.

## Priority guidance

- Single phone, user can use a softphone, cell, or a nearby phone: **P3**.
- Key phone down (front desk/reception, main line, dispatch): **P2**.
- All phones at a site down: **P1**.
- Onsite needed (new jack, dead phone, wiring): through Isaac Brennan per RB-GEN-003.

## Escalate if

- Multiple phones, SIP ALG, voice VLAN, or QoS issues: Tom Kessler.
- Provider issue confirmed: provider ticket, and keep the client updated.
- Dead phone hardware: replacement ordered through the account manager or provider (client page says which), installed onsite or shipped.

## Ticket notes

- Phone model, MAC, extension, location
- IP and VLAN observed, PoE status
- Register status and error from the web UI
- Steps taken (reboot, re-provision, port change)
- Provider ticket number if opened

## Revision history

| Version | Date | Author | Change |
|---|---|---|---|
| 1 | 2021-01-25 | Andre Mitchell | Initial Yealink troubleshooting. |
| 2 | 2024-07-22 | Andre Mitchell | Added voice VLAN checks, SIP ALG escalation, auto-provision steps, provider ticket requirements. |
