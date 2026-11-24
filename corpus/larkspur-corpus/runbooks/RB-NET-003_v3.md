---
doc_id: RB-NET-003
title: Remote access VPN client issues (FortiClient)
doc_type: runbook
version: "3"
effective_date: 2025-09-02
owner: Tom Kessler
audience: internal
---

# RB-NET-003 Remote access VPN client issues (FortiClient)

## Purpose / When to use

Use when a remote user cannot connect to the client's FortiGate VPN with FortiClient, connects but cannot reach internal resources (file server, mapped drives, line-of-business app), or gets disconnected repeatedly. Only some clients use a VPN (those with on-prem servers or apps); the client's Atlas Docs page says whether they do and which type.

## Background

- Most of our VPN clients use the free **FortiClient VPN** app on Windows, connecting to the FortiGate.
- Older setups use **SSL VPN** (port 443 or 10443). Fortinet has removed SSL VPN tunnel mode from newer FortiOS releases, so we are moving clients to **IPsec VPN (IKEv2)** as their firewalls are upgraded. The client page lists the current type.
- Our standard is **split tunnel**: only traffic for the client's internal subnets goes over the VPN. Teams, M365, and web traffic go direct.
- Authentication is either local FortiGate users, LDAP to the client's AD, or SAML with Entra ID (Authenticator push with number matching). The client page says which.

## Prerequisites / access needed

- Beacon RMM remote session to the user's laptop
- FortiGate GUI access (LockBox Vault) for Tier 2/3; read-only VPN monitor for Tier 1 where set up
- Client Atlas Docs page: VPN type, gateway address, port, user group, auth method

## Steps

### 1. Basic checks

1. Is the user's own internet working? Have them open a web page. Public Wi-Fi (hotels, coffee shops) sometimes blocks VPN ports.
2. Is it just this user? If several remote users cannot connect, check the FortiGate is up (RB-NET-001) and look at **Dashboard > Network > IPsec / SSL-VPN** for active tunnels. Several users failing at once is **P2**.
3. Confirm the FortiClient connection profile matches the client page (remote gateway, port, VPN type). Users sometimes edit or delete profiles.
4. Check FortiClient version against the version noted on the client page. Very old or very new versions can mismatch the FortiGate; Beacon RMM can push the approved version.

### 2. Common errors

5. **"Credential or ssl vpn configuration is wrong (-7200)"** or "Permission denied": wrong username/password, account locked, or user not in the VPN user group.
   - LDAP/AD auth: check the AD account (RB-ACC-001) and group membership.
   - SAML/Entra: confirm the user can sign in at https://myapps.microsoft.com and completes MFA.
   - Local users: Tier 2 checks the user in **User & Authentication > User Definition**.
6. **"Unable to establish the VPN connection. The VPN server may be unreachable (-14)"**: gateway address or port wrong, the user's network blocks the port, or the FortiGate is down. Test from the laptop: `Test-NetConnection vpn.client.example -Port 443` (or the configured port). For IPsec, UDP 500/4500 must be allowed; try a phone hotspot to rule out the local network.
7. **Connects, then drops at 98% or after a few seconds**: often an MTU or DNS issue, or a stale FortiClient virtual adapter. Reboot, then repair FortiClient (Settings > Apps > FortiClient VPN > Modify > Repair) or reinstall the approved version via Beacon RMM.
8. **Connected but cannot reach file server / mapped drives**:
   - Ping the server by IP. Works by IP but not by name: DNS. Check `ipconfig /all` shows the client's internal DNS servers on the FortiClient adapter, and that the DNS suffix is set.
   - Nothing reachable by IP: the user's home network may use the **same subnet** as the office (for example both 192.168.1.0/24). That conflicts with split tunnel routes. Tier 3 fix; short-term the user can try a hotspot.
   - Mapped drives disconnected: remap after VPN connects, or check the drive mapping script/GPO on the client page.
9. **Password expired** on AD-backed VPN: remote users cannot change an expired password over a VPN that requires a valid password. Reset per RB-ACC-001 with no forced change, then have them change it once connected.

### 3. Logs (Tier 2/3)

10. FortiGate GUI: **Log & Report > System Events > VPN Events** (or Events > VPN). Filter by the user. Look for auth failures, IKE negotiation failures, or tunnel down reasons.
11. CLI for SSL VPN:
    ```
    diagnose debug application sslvpn -1
    diagnose debug enable
    ```
    For IPsec:
    ```
    diagnose vpn ike log-filter rem-addr4 <user public IP>
    diagnose debug application ike -1
    diagnose debug enable
    ```
    Always run `diagnose debug disable` and `diagnose debug reset` when finished.

## Priority guidance

- Single user cannot connect, can work some other way (web apps, OneDrive): **P3**.
- Single user fully blocked from their only work system (practice management server at Hollis Lane CPAs during tax season, for example): **P3**, or **P2** if a VIP.
- All remote users unable to connect: **P2**. If the business depends on remote access to operate, treat as **P1** and call Tom Kessler.

## Escalate if

- FortiGate config changes (user groups, IPsec phase settings, address objects, routes): Tom Kessler.
- Subnet conflicts with home networks: Tom Kessler.
- SAML/Entra sign-in errors on the FortiGate app: Renee Castillo.
- Client asking for a new VPN user or VPN for a new site: P4, Tier 2 with authorized contact approval.

## Ticket notes

- VPN type, FortiClient version, gateway/port
- Exact error message and code
- Network the user was on (home, hotel, hotspot) and test results
- Changes made (profile fixed, reinstall, group added)
- Confirmation user reached internal resources

## Revision history

| Version | Date | Author | Change |
|---|---|---|---|
| 1 | 2020-04-06 | Tom Kessler | Initial FortiClient SSL VPN steps (written for the remote work surge). |
| 2 | 2022-12-12 | Tom Kessler | Added SAML/Entra authentication and error codes. |
| 3 | 2025-09-02 | Tom Kessler | Added IPsec IKEv2 migration notes, split tunnel standard, subnet conflict check, IKE debug commands. |
