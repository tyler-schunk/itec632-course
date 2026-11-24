---
doc_id: STD-HW-2026
title: Hardware Standard 2026
doc_type: standard
version: "2026"
effective_date: 2026-01-05
owner: Rachel Kim
audience: internal
---

# Hardware Standard 2026

**Applies to:** Larkspur staff equipment and the default hardware we quote to clients for new and replacement endpoints.
**Owner:** Rachel Kim, Projects Engineer
**Approved by:** Marcus Oyelaran, Director of Service Delivery
**Effective:** January 5, 2026. Applies to all quotes issued on or after this date. Quotes issued before this date may be honored as written.

## 1. Purpose

A short list of standard models keeps imaging, drivers, spares, and warranty claims simple, and gives clients predictable performance and pricing. When a client asks "what should we buy?", quote from this list unless an approved exception applies (Section 8).

## 2. What Changed for 2026

- Standard laptop moves to the **Dell Latitude 5550** with Intel Core Ultra 5 and **32 GB RAM**. Teams, browser-heavy line-of-business apps, and Copilot-era Office features were pushing 16 GB machines into heavy paging by year 3. 32 GB gives the 4-year cycle real headroom.
- Standard desktop moves to the **Dell OptiPlex Micro 7020**. The OptiPlex Micro 7020 has been quoted since mid-2025 after the 7010 reached end of sale; this standard formalizes it.
- New standard dock (Dell Universal Dock UD22) replaces the WD19S.
- Standard monitor moves to the Dell P2425H family.
- Tickets in the "Hardware - Exception Request" category now auto-assign to Rachel Kim (Harbor automation rule added 2025-11, see OPS-RELNOTES-HARBOR).

## 3. Standard Laptop

| Item | Specification |
|---|---|
| Model | **Dell Latitude 5550** (15.6") |
| Processor | **Intel Core Ultra 5** (vPro) |
| Memory | **32 GB** |
| Storage | 512 GB NVMe SSD |
| Display | 15.6" FHD (1920x1080), anti-glare |
| Operating system | Windows 11 Pro |
| Warranty | **3-year Dell ProSupport**, next business day onsite |
| Extras | Backlit keyboard, fingerprint reader, IR camera for Windows Hello, USB-C charging |

Notes:
- Do not quote 16 GB configurations of the standard laptop. If budget is the issue, talk to Jordan Pike or the account manager about spreading the purchase across two quarters rather than downgrading RAM.
- 1 TB SSD upgrade is allowed without an exception for users with large local OneDrive sync sets (design, engineering, media clients).
- Users who need a 14" form factor can be quoted the Latitude 5450 with the same CPU/RAM/SSD/warranty without a formal exception. Note it in the ticket.

## 4. Standard Desktop

| Item | Specification |
|---|---|
| Model | **Dell OptiPlex Micro 7020** |
| Processor | Intel Core i5 (14th gen, T-series) |
| Memory | **16 GB** |
| Storage | 512 GB NVMe SSD |
| Operating system | Windows 11 Pro |
| Warranty | 3-year Dell ProSupport, next business day onsite |
| Mounting | VESA mount kit behind monitor where desk space is tight |

Use desktops for fixed workstations: reception, front desks, shop floor stations, exam rooms, and shared kiosks. 16 GB is sufficient for these single-purpose stations.

## 5. Monitors

| Use | Model |
|---|---|
| Standard | Dell P2425H 24" (FHD, 100 Hz, height-adjustable) |
| Standard with USB-C | Dell P2425HE 24" (USB-C hub, for single-cable desks) |
| Large / design | Dell P2725QE 27" 4K USB-C hub monitor |

Standard staff setup is two 24" monitors. 27" 4K monitors are approved without an exception for design and engineering roles at clients such as Granite Peak Engineering, Silo & Grain Architecture, Zenith Arc Animation, and Tallgrass Marketing Studio.

## 6. Docking Stations and Peripherals

| Item | Model |
|---|---|
| Dock | **Dell Universal Dock UD22** (USB-C, 96 W power delivery) |
| Keyboard / mouse | Dell KM5221W wireless combo |
| Headset | Jabra Evolve2 30 (wired USB-C) for service desk and call-heavy users |
| Webcam | Built-in laptop camera; Logitech C920 for desktops that need video |

Notes:
- The UD22 supports up to four displays. Check the client's monitor cables before the visit; bring DisplayPort and HDMI cables.
- Existing WD19S docks stay in service until they fail. They work with the 5550.
- Dock and monitor troubleshooting: RB-HW-003.

## 7. Replacement Cycle

| Device | Replacement cycle |
|---|---|
| Laptops | **4 years** |
| Desktops | 5 years |
| Monitors | Replace on failure |
| Docks | Replace on failure |

- Warranty is 3 years. For year 4 on laptops, the client may buy a 1-year ProSupport extension or accept out-of-warranty risk. Record the client's choice in the asset record in Beacon RMM.
- Jordan Pike reviews devices reaching end of cycle in each client's business review so replacements can be budgeted ahead of time.
- The Beacon RMM hardware inventory report is the source of truth for purchase and warranty dates.
- Staff laptops follow the same 4-year cycle. Hannah Moreau tracks staff device assignments.

## 8. Approved Exceptions Process

To request a device outside this standard:

1. Open a P4 ticket in Harbor PSA with category **"Hardware - Exception Request"**.
2. Include the user, client, business reason, proposed model, and quoted price.
3. Rachel Kim reviews for supportability (drivers, warranty, dock compatibility, imaging).
4. Marcus Oyelaran approves or declines within 3 business days. For client purchases, the client's authorized contact must also approve the quote in writing.
5. Approved exceptions are recorded on the client's Atlas Docs page under "Hardware Exceptions" with the ticket number.

Common approved exceptions:
- Dell Precision mobile workstations for CAD/BIM users and animation staff.
- Rugged or semi-rugged laptops for field staff at construction and electrical clients where requested.
- Apple Mac devices for creative staff, supported on a best-effort basis.

Not approved: consumer-grade laptops, retail-purchased devices without business warranties, and any Windows device that cannot run Windows 11 Pro.

## 9. Asset Tagging and Deployment

Every device we deploy gets an asset tag in the format `LR-<CLIENTCODE>-<4 digits>` (for example, `LR-EMS-0142`) and is recorded in Beacon RMM and the client's Atlas Docs asset list before it leaves the office. Deployment follows RB-HW-002 (New workstation deployment).

## 10. Review

This standard is reviewed annually by the Projects Engineer, normally in December, with changes effective in January.
