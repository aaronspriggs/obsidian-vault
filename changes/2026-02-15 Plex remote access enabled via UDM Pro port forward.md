---
date: 2026-02-15
type: config
system:
- '[[Plex Media Server]]'
- '[[UniFi (UDM Pro)]]'
notion_id: 3087ae76-22ba-812a-9078-f40f60df41ed
---

# Plex remote access enabled via UDM Pro port forward

Created port forward rule on UDM Pro: TCP 32400 → 192.168.1.116:32400 (WAN1). Configured via Policy Engine → Policy Table → Port Forwarding. Enabled manual port 32400 in Plex Remote Access settings. Validated with 5G cellular playback test — fully working.
