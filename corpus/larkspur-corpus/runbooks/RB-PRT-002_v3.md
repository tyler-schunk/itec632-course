---
doc_id: RB-PRT-002
title: Scan-to-email failures
doc_type: runbook
version: "3"
effective_date: 2025-05-12
owner: Andre Mitchell
audience: internal
---

# RB-PRT-002 Scan-to-email failures

## Purpose / When to use

Use when an MFP (HP, Brother, or a leased copier) can no longer scan to email: the device shows "Send failed", "Authentication error", "Cannot connect to SMTP server", or scans never arrive. Scan-to-email usually breaks after a password change on the scanning account, an M365 security change, a printer firmware update, or an IP/network change.

## Background: how our clients send scans

Check the client's Atlas Docs printer page to see which method the device uses. There are three:

| Method | Server / port | Auth | Notes |
|---|---|---|---|
| **SMTP relay via connector** (Larkspur standard for new setups) | `<tenant>.mail.protection.outlook.com`, port 25 | None; an inbound connector in Exchange Online trusts the client's static public IP | Works for internal and external recipients. Needs a static public IP. |
| **Direct send** | `<tenant>.mail.protection.outlook.com`, port 25 | None | Internal recipients only. Being phased out at our clients. |
| **SMTP AUTH client submission** (older setups) | `smtp.office365.com`, port 587, STARTTLS | Username/password of a licensed scanning mailbox | Microsoft is retiring Basic authentication for SMTP AUTH. Move these devices to the connector method when they break. |

## Prerequisites / access needed

- Printer web UI credentials (LockBox Vault, client printer entry)
- Exchange admin center via GDAP (Exchange Administrator) for message trace and connectors
- Client's public IP (FortiGate dashboard or client Atlas Docs page)
- Remote session to a PC on the same network as the MFP

## Steps

1. **Get the exact error** from the device panel or its job log (web UI > Scan/Send log). Note it word for word.
2. **Basic checks:**
   - Can the device reach the network? Ping its IP from a PC on site; open its web UI.
   - DNS: in the device's network settings, confirm DNS servers are set (usually the FortiGate or UniFi gateway IP). Scan-to-email fails silently with bad DNS.
   - Time: wrong date/time on the device breaks TLS. Set NTP if available.
3. **Run a message trace:** EAC > **Mail flow > Message trace** > start a trace for the last few hours, sender = the scanner address. If messages show as **Delivered**, the problem is the recipient's mailbox or junk folder. If **Failed** or no record, the device never got the message to M365.
4. **By method:**

   **SMTP relay via connector**
   - Confirm the site's current public IP matches the connector: EAC > **Mail flow > Connectors** > the inbound connector from "Your organization's email server" > IP addresses. An ISP change or failover to a backup WAN (RB-NET-004) changes the public IP and breaks relay.
   - Check the device uses port 25, no authentication, TLS enabled if supported, and the "From" address is in an accepted domain.
   - Some ISPs block outbound port 25 on business circuits. Test from a PC on site: `Test-NetConnection <tenant>.mail.protection.outlook.com -Port 25`.

   **Direct send**
   - Only works to internal recipients. If the user is trying to scan to an outside address, that is the cause. Move to the connector method.

   **SMTP AUTH (587)**
   - Error **535 5.7.139 Authentication unsuccessful** usually means SMTP AUTH is disabled for the mailbox or tenant, or security defaults/Conditional Access blocks it.
   - Check: `Get-CASMailbox scanner@client.example | fl SmtpClientAuthenticationDisabled`
   - If the password was changed, update it in the device's SMTP settings.
   - Do not re-enable SMTP AUTH tenant-wide. Plan the move to the connector method instead; if the device needs to work today, Tier 2 can enable SMTP AUTH on just that mailbox as a temporary fix with Renee Castillo's approval:
     `Set-CASMailbox scanner@client.example -SmtpClientAuthenticationDisabled $false`
5. **Firmware:** if the device's firmware is several years old it may not support TLS 1.2, which M365 requires. Update firmware from the HP/Brother site, or have the copier lease vendor do it.
6. **Test:** scan a one-page document to the user and to an outside address (if allowed). Confirm delivery in message trace.
7. **Scan to folder** as a workaround: if scan-to-email cannot be fixed today and the device is configured for scan-to-SMB folder or scan-to-SharePoint, point the user there.

## Converting a device to the connector method (Tier 2)

1. Confirm the site has a static public IP.
2. Create or update the inbound connector: EAC > Mail flow > Connectors > Add > From **Your organization's email server** to **Office 365** > identify by IP address > add the public IP.
3. Device SMTP settings: server `<tenant>.mail.protection.outlook.com` (MX record value from the client's DNS), port 25, no auth, TLS on.
4. Add the public IP to the SPF record if scans go to outside recipients.
5. Update the Atlas Docs printer page.

## Priority guidance

- One device failing, other scanning options available: **P3**.
- The only MFP at a site cannot scan and the business depends on it (title company closing documents, medical intake forms, mortgage files): **P2**.
- Several devices at several sites failing at once after a Microsoft change: **P2**, tell Renee Castillo.

## Escalate if

- SMTP AUTH needs enabling on a mailbox, or Conditional Access is blocking it: Renee Castillo.
- Connector, SPF, or public IP changes: Tier 2, then Tom Kessler for FortiGate/ISP questions.
- Leased copier with vendor-managed settings: tell the client to contact their copier vendor, give them the settings we need, and keep the ticket in Waiting on Vendor.
- Device hardware or panel failure: onsite via Isaac Brennan (RB-GEN-003).

## Ticket notes

- Device model, IP, method used (connector / direct send / SMTP AUTH)
- Exact error message
- Message trace result
- What was changed (password, IP on connector, firmware, method conversion)
- Test results to internal and external addresses

## Revision history

| Version | Date | Author | Change |
|---|---|---|---|
| 1 | 2021-03-01 | Andre Mitchell | Initial scan-to-email troubleshooting. |
| 2 | 2023-02-13 | Andre Mitchell | Added message trace steps and direct send limitations. |
| 3 | 2025-05-12 | Andre Mitchell | Connector method is now the standard; added SMTP AUTH retirement guidance and 5.7.139 error. |
