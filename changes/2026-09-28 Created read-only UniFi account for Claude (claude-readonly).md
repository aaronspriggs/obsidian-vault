---
date: 2026-09-28
type: config
system:
- '[[UniFi (UDM Pro)]]'
- '[[ClaudeCode (VM)]]'
project:
- '[[Document UniFi network config (subnet-DHCP, reservations, SSIDs, switch ports, PoE)]]'
notion_id: 3e97ae76-22ba-8104-b51b-d42196ee36cd
---

# Created read-only UniFi account for Claude (claude-readonly)

Aaron created local-only UniFi OS admin claude-readonly (Network View Only, other apps None); creds on ClaudeCode VM ~/.config/homelab/unifi-readonly (600). Verified read-only (403 on write, Protect 403); secret exposure tested.

## What

Local-only UniFi OS admin `claude-readonly` on the UDM Pro: Network = View Only, other apps None. Password in 1Password "UniFi - Claude read-only"; written by Aaron to `~/.config/homelab/unifi-readonly` (600) on the ClaudeCode VM.

## Why

Lets Claude document the UniFi network live (subnet/DHCP, reservations, SSIDs, ports, PoE) and set `Last Verified`, instead of Aaron relaying screenshots.

## Verify (2026-09-28)

- Login OK; `/api/users/self` permissions = `network.management: readonly`; site role `readonly`.
- Write test: same-name PUT on a device → 403 `api.err.NoPermission`. Protect API → 403.
- Secrets: the API does **not** return the Wi-Fi passphrase, PPPoE, WireGuard or Cloudflare DDNS secrets. It **does** return `ips.utm_token`, `peer_to_peer.psk` and `magic_site_to_site_vpn.public_key` (public). Test output printed field names only, never values.
- UPS 2U: the Network API shows 8 outlets (all on, unnamed) but no battery, load or runtime data.

## Roll back

Delete the `claude-readonly` user in UniFi OS → Admins & Users, and `rm ~/.config/homelab/unifi-readonly`.
