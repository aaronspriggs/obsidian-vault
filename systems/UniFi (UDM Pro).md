---
status: active
category: network
ip: 192.168.1.1
url: https://192.168.1.1/login
last_verified: 2026-10-17
repo: https://github.com/aaronspriggs/spriggs-homelab/tree/main/unifi
notion_id: 2ff7ae76-22ba-8168-bc6d-da03f129328b
---

Router/firewall/UniFi controller + Protect (1 camera). Flat 192.168.1.0/24, no VLANs, one SSID. 10 adopted devices. Read-only API via unifi-api on the ClaudeCode VM; HA uses the UniFi Network integration (non-admin).

## Overview

Primary router, firewall, and UniFi network controller. ISP is CenturyLink. Flat network, no VLANs currently configured.

## Hardware

- **Model:** UniFi Dream Machine Pro (UDM Pro)
- **Role:** Router / Firewall / UniFi Controller
- **IP Address:** 192.168.1.1
- **Management URL:** [https://192.168.1.1/login](https://192.168.1.1/login)
- **Claude (read-only, since 2026-09-28):** local-only UniFi OS admin `claude-readonly`, Network = View Only, all other apps None. Credentials are in 1Password item **"Unifi read-only"** (vault `Homelab - Claude`, fields `username`/`password`); `unifi-api` reads them at run time via `homelab-secret`, with nothing on disk (corrected 2026-10-17: there is no `~/.config/homelab/unifi-readonly` file). Not shared with other consumers: Scrypted gets its own user (decided 2026-10-17). Verified 2026-09-28: permissions `network.management: readonly`; a no-op device rename returns 403 NoPermission; Protect API 403. Secrets it can't read: Wi-Fi passphrase, PPPoE, WireGuard keys, Cloudflare DDNS token (not returned by the API). It can read three settings fields: `magic_site_to_site_vpn.public_key` (public by design), `ips.utm_token` and `peer_to_peer.psk`; tooling must redact these and never store raw API dumps.
- **Uplink:** GbE to CenturyLink (ISP)
- **Home Assistant (UniFi Network integration, since 2026-01-30):** config entry "Default", site `default`, port 443, `verify_ssl: false`. Logs in as a **non-admin** UniFi user (`role_is_admin: false`), so HA can monitor but has no PoE/port or client-block controls. Which UniFi account and 1Password item it uses isn't recorded yet. Default options: every client is a `device_tracker` (47 on 2026-10-17, about 13 of them random-MAC `unifi_default_*`), plus state/CPU/memory/uptime sensors and `update.*` per device. Offline alerts come from Alert2 generator `homelab_unifi_offline` (repo `ha/alert2.yaml`) over `*_state` sensors labelled `homelab_watch`. **Gap (2026-10-17):** the two newly adopted Flex 2.5G switches (Basement, Aaron's Desk) aren't labelled, so they don't alert, and the Basement switch's sensor is `sensor.usw_flex_2_5g_8_poe_state_2`, which the generator's `_state$` match would skip even if labelled.

## UniFi Protect

Runs on this UDM Pro. One camera as of 2026-10-17: **G6 Instant** (`g6-instant`, MAC 90:41:b2:38:9a:10), on Wi-Fi "Ayo Rivah" (−65 dBm), DHCP 192.168.1.99 with no reservation. That's fine because consumers reach it through Protect, not directly. Consumers: Scrypted, running as an HA app on the HA VM (HomeKit/HKSV; logs in with its own local Protect user), and HA's UniFi Protect integration (API key only, no user); both are being set up in the [Scrypted project](<../projects/Scrypted — UniFi Camera HomeKit Bridge.md>). `claude-readonly` has no Protect access (403).

## Network

- **Domain:** [thespriggs.com](http://thespriggs.com/) (Cloudflare, free plan)
- **Topology:** Flat network, no VLANs
Verified via the read-only UniFi API 2026-09-28.
- **LAN** (network "LAN"): 192.168.1.0/24, gateway 192.168.1.1. **DHCP** on, pool 192.168.1.6–192.168.1.254, lease 24 h, DNS handed out = **1.1.1.1** (not the gateway), domain `localdomain`.
- **WireGuard VPN** clients: 192.168.7.0/24 (pool .2–.254).
- **Wi-Fi:** one SSID, **Ayo Rivah**, on all three U7 APs, 2.4/5/6 GHz, WPA2/WPA3 transition, PMF optional. Passphrase in 1Password (the read-only API doesn't return it).
- **DHCP reservations (fixed IPs):**

| IP | Name in UniFi | What |
| --- | --- | --- |
| 192.168.1.84 | hadashboard | Raspberry Pi wall panel |
| 192.168.1.106 | HDHomeRun Flex 4K | OTA tuner |
| 192.168.1.116 | Plex Virtual Machine | Plex VM |
| 192.168.1.156 | claudecode | ClaudeCode VM |
| 192.168.1.218 | Home Assistant | HA OS VM |
| 192.168.1.248 | truenas | Big Boi |

UniFi devices (switches, APs, UPS) take DHCP addresses managed by the controller and have no reservations; Hue, Lutron and Sonos also float.

## Network Topology (verified 2026-09-28; switches on ports 12, 13, 15 re-verified 2026-10-17)

```javascript
CenturyLink (PPPoE)
└── Dream Machine Pro (192.168.1.1) — WAN1 on port 9 (GbE)
    ├── port 2: Hue Bridge (192.168.1.73)
    ├── port 3: Lutron hub (192.168.1.46)
    ├── port 4: HDHomeRun Flex 4K (192.168.1.106)
    ├── port 8: UniFi UPS 2U (192.168.1.12)
    └── SFP+ 2 (port 11): USW Pro Max 16 PoE (192.168.1.250), 10 GbE
        ├── port 6: wall panel Pi (PoE)
        ├── ports 8, 9: Sonos
        ├── port 10: USW Flex [spare, offline by design]
        ├── port 12: USW Flex 2.5G 8 PoE - Basement (192.168.1.76, 1 GbE)
        ├── port 13: USW Flex 2.5G 5 - Aaron's Desk (192.168.1.6, 2.5 GbE)
        ├── port 14: U7-Pro-Wall-Front AP (2.5 GbE)
        ├── port 15: USW Flex 2.5G 8 PoE - Upstairs (2.5 GbE)
        │   └── port 3: U7 Pro - Upstairs AP (2.5 GbE)
        ├── port 16: U7-Pro-Wall-Back AP (2.5 GbE)
        └── SFP+ 2: Big Boi / TrueNAS br0 (10 GbE)
```
Per-port detail and PoE draw live on each switch's page.

## Connected UniFi Devices

Adopted devices from `unifi-api stat/device`, 2026-10-17 (10 including the UDM; none upgradable).

| Device | IP | Role | Status |
| --- | --- | --- | --- |
| USW Pro Max 16 PoE | 192.168.1.250 | Core switch | Up to date |
| USW Flex 2.5G 8 PoE - Upstairs | 192.168.1.24 | Secondary switch | Up to date |
| USW Flex 2.5G 8 PoE - Basement | 192.168.1.76 | Switch (adopted by 2026-10-17) | Up to date |
| USW Flex 2.5G 5 - Aaron's Desk | 192.168.1.6 | Desk switch (adopted by 2026-10-17) | Up to date |
| UPS 2U | 192.168.1.12 | Rack UPS (NUT server for Big Boi) | Up to date |
| USW Flex | 192.168.1.134 | Switch | Spare (offline by design; reserved for home theatre wiring) |
| U7 Pro - Upstairs | 192.168.1.219 | Access point | Up to date |
| U7-Pro-Wall-Front | 192.168.1.39 | Access point | Up to date |
| U7-Pro-Wall-Back | 192.168.1.230 | Access point | Up to date |

## Port Forwarding

| Name | WAN | External Port | Forward IP | Internal Port | Protocol |
| --- | --- | --- | --- | --- | --- |
| Plex Remote Access | WAN1 | 32400 | 192.168.1.116 | 32400 | TCP |

- Configured via Policy Engine → Policy Table → Port Forwarding (new UniFi UI location)
- Auto-generated firewall rule: "Allow Port Forward Plex Remote Access"

## WAN / ISP

- **ISP:** CenturyLink (PPPoE — UDM Pro authenticates directly, no CenturyLink router, no double NAT)
- **WAN interface:** WAN1 "Internet 1" (port 9, GbE, PPPoE). "Internet 2" (DHCP, failover-only) is configured but no port is assigned to it, so there's no failover in practice.
- **UniFi OS:** 5.1.33 | **Network:** 10.6.106 (re-checked 2026-10-17)
- **Public IP:** dynamic (changed at least once, found 2026-02-16).
- **CGNAT:** No — confirmed public/routable IP
- **DDNS:** Cloudflare, native on the UDM Pro: [vpn.thespriggs.com](http://vpn.thespriggs.com/), verified 2026-02-16. API token scoped to [thespriggs.com](http://thespriggs.com/) Zone.DNS:Edit only.
- **PPPoE credentials:** in 1Password, never on this page.

## VPN

- **WireGuard server** (since 2026-02-17): UniFi One-Click VPN on WAN1, port 51820, endpoint [vpn.thespriggs.com](http://vpn.thespriggs.com/). Split tunnel: clients' AllowedIPs = 192.168.1.0/24 only; clients get 192.168.7.x. See the Done project "Set up WireGuard VPN".

## Decisions

- **Local DNS host records:** explored and deferred; bookmarks are used instead.

## Open work

![[Projects.base#Open for this system]]

## Runbooks

![[Runbooks.base#For this system]]

## Recent changes

![[Changes.base#For this system]]
