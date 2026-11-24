---
doc_id: STD-HW-2024
title: Hardware Standard 2024
doc_type: standard
version: "2024"
effective_date: 2024-01-15
owner: Rachel Kim
audience: internal
---

# Hardware Standard 2024

**Applies to:** Larkspur staff equipment and the default hardware we quote to clients for new and replacement endpoints.
**Owner:** Rachel Kim, Projects Engineer
**Approved by:** Marcus Oyelaran, Director of Service Delivery

## 1. Purpose

Standardizing on a short list of models keeps imaging, driver management, spare parts, and warranty claims simple. Techs learn one set of quirks instead of twenty. Clients get predictable performance and predictable pricing.

When a client asks "what should we buy?", quote from this list unless an approved exception applies (Section 7).

## 2. Standard Laptop

| Item | Specification |
|---|---|
| Model | **Dell Latitude 5440** (14") |
| Processor | Intel Core i5-1345U (13th gen, vPro) |
| Memory | **16 GB** DDR4 |
| Storage | 512 GB NVMe SSD |
| Display | 14" FHD (1920x1080), anti-glare |
| Operating system | Windows 11 Pro |
| Warranty | 3-year Dell ProSupport, next business day onsite |
| Extras | Backlit keyboard, fingerprint reader, USB-C charging |

Notes:
- 16 GB is the minimum for anyone running Teams, Outlook, and a browser all day. Do not quote 8 GB configurations.
- Power users (CAD, video, large Excel models) go through the exception process in Section 7 for a Precision workstation.

## 3. Standard Desktop

| Item | Specification |
|---|---|
| Model | **Dell OptiPlex Micro 7010** |
| Processor | Intel Core i5-13500T |
| Memory | 16 GB |
| Storage | 512 GB NVMe SSD |
| Operating system | Windows 11 Pro |
| Warranty | 3-year Dell ProSupport, next business day onsite |
| Mounting | VESA mount kit behind monitor where desk space is tight |

Use desktops for fixed workstations: front desks, reception, shop floor stations, shared check-in kiosks, and exam rooms.

## 4. Monitors

| Use | Model |
|---|---|
| Standard | Dell P2423D 24" (QHD 2560x1440) |
| Value / reception | Dell E2423H 24" (FHD) |
| Large / design | Dell P2723QE 27" 4K USB-C hub monitor |

Standard staff setup is two 24" monitors. Design-heavy clients (architecture, engineering, animation) may get 27" monitors as an approved exception.

## 5. Docking Stations and Peripherals

| Item | Model |
|---|---|
| Dock | Dell WD19S (USB-C, 130 W) |
| Keyboard / mouse | Dell KM5221W wireless combo |
| Headset | Jabra Evolve2 30 (wired USB-C) for service desk and call-heavy users |
| Webcam | Built-in laptop camera; Logitech C920 for desktops that need video |

Docks: always confirm the client's monitor cables. The WD19S has two DisplayPort and one HDMI output. Keep a spare WD19S at the office for swap testing.

## 6. Replacement Cycle

| Device | Replacement cycle |
|---|---|
| Laptops | **4 years** |
| Desktops | 5 years |
| Monitors | Replace on failure |
| Docks | Replace on failure |

- Warranty is 3 years. For year 4 on laptops, the client may buy a 1-year warranty extension or accept out-of-warranty risk. Note the client's choice in the asset record.
- Jordan Pike flags devices reaching end of cycle in each client's business review so replacement can be budgeted.
- Beacon RMM hardware inventory report is the source of truth for purchase dates.

## 7. Approved Exceptions Process

Some users genuinely need something different. To request an exception:

1. Open a P4 ticket in Harbor PSA with category "Hardware - Exception Request".
2. Include the user, client, business reason, and the proposed model and price.
3. Rachel Kim reviews for supportability (drivers, warranty, dock compatibility).
4. Marcus Oyelaran approves or declines. For client purchases, the client's authorized contact must also approve the quote.
5. Approved exceptions are recorded in the client's Atlas Docs page under "Hardware Exceptions".

Common approved exceptions:
- Dell Precision mobile workstations for CAD/BIM users (Granite Peak Engineering, Silo & Grain Architecture) and animation staff (Zenith Arc Animation).
- Rugged or semi-rugged laptops for field staff where a client requests them.
- Apple Mac devices for creative staff, supported on a best-effort basis.

Not approved: consumer-grade laptops, devices purchased at retail stores without business warranties, and any device that cannot run Windows 11 Pro (for Windows users).

## 8. Asset Tagging

Every device we deploy gets an asset tag in the format `LR-<CLIENTCODE>-<4 digits>` (for example, `LR-EMS-0142`) and is recorded in Beacon RMM and the client's Atlas Docs asset list. Deployment follows RB-HW-002.

## 9. Review

This standard is reviewed annually by the Projects Engineer.
