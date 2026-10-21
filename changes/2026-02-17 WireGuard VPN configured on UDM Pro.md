---
date: 2026-02-17
type: install
system:
- '[[UniFi (UDM Pro)]]'
notion_id: 31b7ae76-22ba-817a-9e8a-fb43e24cad7b
---

# WireGuard VPN configured on UDM Pro

Configured WireGuard VPN server on UDM Pro for remote homelab access. Server: One-Click VPN, port 51820, WAN1, endpoint [vpn.thespriggs.com](http://vpn.thespriggs.com/). Mode: split tunnel, AllowedIPs 192.168.1.0/24 only. DNS field left blank on all clients (auto-generated 192.168.7.1 removed). Clients added: aaron-mac, aaron-iphone, aaron-ipad. Tested successfully over iPhone cellular hotspot. Gotcha for future clients: after importing config, always clear DNS field and change AllowedIPs from 0.0.0.0/0 to 192.168.1.0/24.
