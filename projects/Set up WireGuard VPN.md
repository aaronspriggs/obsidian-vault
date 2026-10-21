---
type: project
status: done
priority: high
system:
- '[[UniFi (UDM Pro)]]'
completed: 2026-02-17
notion_id: 3087ae76-22ba-81f2-8c12-cebf14cded69
---

Complete. WireGuard server configured on UDM Pro (One-Click VPN, port 51820, WAN1). DDNS endpoint: [vpn.thespriggs.com](http://vpn.thespriggs.com/). Split tunnel — AllowedIPs 192.168.1.0/24 only. DNS left blank on all clients (192.168.7.1 removed). Clients configured: aaron-mac, aaron-iphone, aaron-ipad. Tested successfully over iPhone hotspot. Runbook: clear DNS field and set AllowedIPs to 192.168.1.0/24 on every new client config after import.

## Outcome

Done 2026-02-17; details in Notes, current config on the [UniFi (UDM Pro)](<../systems/UniFi (UDM Pro).md>) page. For every new client: after importing the config, clear the DNS field and change AllowedIPs from `0.0.0.0/0` to `192.168.1.0/24`.

## Links

Original note (merged here 2026-09-29, now deprecated): "WireGuard VPN configured on UDM Pro", a subpage of this page.
[DEPRECATED] WireGuard VPN configured on UDM Pro
