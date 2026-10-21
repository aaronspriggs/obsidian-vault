---
date: 2026-09-28
type: doc
system:
- '[[UniFi (UDM Pro)]]'
- '[[USW Pro Max 16 PoE]]'
- '[[USW Flex 2.5G 8 PoE]]'
- '[[U7 Pro]]'
- '[[U7-Pro-Wall-Front]]'
- '[[U7-Pro-Wall-Back]]'
- '[[ClaudeCode (VM)]]'
project:
- '[[Document UniFi network config (subnet-DHCP, reservations, SSIDs, switch ports, PoE)]]'
commit: https://github.com/aaronspriggs/spriggs-homelab/commit/80f0250
notion_id: 3e97ae76-22ba-81e4-ae5b-fd5b0796d2c2
---

# Added unifi-api read-only client; documented UniFi network from live data

New repo tool unifi/unifi-api (GET only, redacts secret fields, one login per run). Used it to fill the UDM, switch and AP pages; corrected DHCP DNS (1.1.1.1, not the gateway).

## What

- **Repo:** [`unifi/unifi-api`](https://github.com/aaronspriggs/spriggs-homelab/tree/main/unifi) (commits [9173a49](https://github.com/aaronspriggs/spriggs-homelab/commit/9173a49), [80f0250](https://github.com/aaronspriggs/spriggs-homelab/commit/80f0250)), deployed to `~/.local/bin/unifi-api`, added to `deployed.tsv`, `make check` clean. GET only; redacts `x_*`, pass, secret, token, psk, private and `*_key` fields; takes several paths per run.
- **Docs from live data:** UDM Pro (LAN/DHCP, reservations, WireGuard subnet, SSID, topology by port, WAN2 unassigned, versions), USW Pro Max and USW Flex 2.5G (per-port link, PoE, what's connected), the three U7 APs (SSID, widths, auto channels, firmware), UPS 2U uplink, Big Boi's switch port. `Last Verified` 2026-09-28 on all of them.
- **Corrected:** DHCP hands out DNS **1.1.1.1**, not 192.168.1.1 as written earlier the same day.

## Gotcha

The UDM rate-limits logins: about six logins in a minute got HTTP 429 for a couple of minutes. The client now logs in once per run; batch paths.

## Verify

`~/.local/bin/unifi-api stat/sysinfo` prints versions; `unifi-api rest/setting | grep -c redacted` > 0.
