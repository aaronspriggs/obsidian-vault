---
type: project
status: backlog
priority: medium
system:
- '[[UniFi (UDM Pro)]]'
---

# Get full use out of the UDM Pro (segmentation, security, built-in features)

## Goal

Use the UDM Pro as a real gateway/firewall rather than a glorified Wi-Fi router: segment the network (IoT, cameras, guests, servers), turn on the security features it already includes, and use built-ins before adding hardware or containers.

## Status

Backlog since 2026-11-08 (Aaron: "at some point"). Not started. The first step is a read-only audit that Claude can do alone with `unifi-api`: list which features are on or off and classify every client by trust level. That audit then drives the VLAN plan.

## Plan

These are candidate areas to evaluate in the audit, not decided scope.

- **Segmentation:** VLANs for IoT, cameras (Protect), guest and servers/homelab, with zone-based firewall rules. The LAN is currently flat (192.168.1.0/24, one SSID "Ayo Rivah", no VLANs). Consider PPSK (one SSID with several passphrases, each mapped to a VLAN) instead of adding SSIDs.
- **Security features, off as of 2026-11-08:** IDS/IPS (`ips_mode: disabled`), Ad Blocking (`ad_blocking_enabled: false`), region blocking. UPnP, geo and rate controls are covered by the sub-task [UDM Pro hardening review (UPnP, geo restrictions, rate controls)](<UDM Pro hardening review (UPnP, geo restrictions, rate controls).md>).
- **DNS:** the native Ad Blocking toggle vs Pi-hole is tracked in [Set up Pi-hole for local DNS and ad-blocking](<Set up Pi-hole for local DNS and ad-blocking.md>). Local DNS host records were deferred earlier and are worth revisiting alongside it.
- **Other built-ins to review:** WAN failover ("Internet 2" is configured but has no port), traffic/QoS rules, and syslog/alerts into HA through the existing alerting pipeline.

## Open questions

- Which IoT devices must stay reachable from HA across VLANs, and does the UDM's mDNS reflection plus firewall rules cover them? Hue, Lutron, Sonos, HomeKit through Scrypted, and HA's own discovery all depend on mDNS/SSDP or broadcast. This is the main risk of segmenting the network.
- Should Big Boi, the HA VM and the ClaudeCode VM keep their current IPs (all servers stay on the existing LAN), or move to a server VLAN? Re-addressing touches the DHCP reservations, NFS exports, Kuma monitors, and IPs hard-coded in the repo and the vault.
- Re-addressing and SSID changes are disruptive: use maintenance mode, and treat them as Tier 2 or Tier 3 when they happen.
