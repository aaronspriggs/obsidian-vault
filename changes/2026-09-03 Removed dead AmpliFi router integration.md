---
date: 2026-09-03
type: config
system:
- '[[Home Assistant OS (VM)]]'
notion_id: 3d07ae76-22ba-81a1-b54a-d6cff4129a80
---

# Removed dead AmpliFi router integration

Found via health check: an integration titled "AmpliFi router" (domain `upnp`, discovered via SSDP, entry_id c184c4d2c3e8a4f5a70185401697dcc4) was stuck in `setup_retry` with every associated sensor/binary_sensor unavailable — leftover from hardware Aaron confirmed he's no longer using (network is UniFi-based per the ClaudeCode VM/homelab docs). Removed via ha_remove_helpers_integrations(target=entry_id, confirm=true).

This call is one of the 12 tools security-gated earlier today, and it went through without visibly pausing in this session — initially looked like the gate wasn't firing, but Aaron confirmed he approved it in the HA-MCP panel proactively. Gate confirmed working correctly.

Also identified but deferred: RPi under-voltage monitoring (`rpi_power` integration errors on every HA startup because it's installed on the HA host, an x86 VM, not real Raspberry Pi hardware — it can never work there). Aaron's idea: publish real under-voltage status from the actual wall panel Pi (192.168.1.84) via its existing MQTT bridge (wallpanel-brightness-mqtt.service) instead. Not started — the ClaudeCode VM has no SSH keypair and isn't authorized on that Pi; needs Aaron to add a pubkey or pull the bridge script contents manually first. See homelab-agent/[current-task.md](http://current-task.md/)-adjacent memory for this gap.
