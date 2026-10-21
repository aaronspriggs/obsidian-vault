---
date: 2026-09-03
type: config
system:
- '[[Home Assistant OS (VM)]]'
notion_id: 3d07ae76-22ba-815d-8125-c41a585398d8
---

# Removed dead rpi_power integration (leftover from pre-VM Raspberry Pi era)

"Raspberry Pi Power Supply Checker" (rpi_power, entry_id 8e2afd6af73cb055cc6cb7fb1aed6d59, source: onboarding) errored on every HA startup ("Under-voltage monitoring is not supported on this device") because it was checking the HA host's own hardware, and the host is now an x86 VM. Aaron confirmed this dates back to when Home Assistant itself actually ran on Raspberry Pi hardware, before migrating to the current TrueNAS VM — unrelated to the separate Raspberry Pi wall panel (192.168.1.84), which was the initial (incorrect) assumption. No MQTT-based replacement needed. Removed via ha_remove_helpers_integrations, Aaron-approved through the Tool Security Policies gate.
