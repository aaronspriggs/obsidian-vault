---
date: 2026-08-26
type: install
system:
- '[[Home Assistant OS (VM)]]'
notion_id: 3c87ae76-22ba-81f5-a5f1-df4eca9a10c7
---

# Installed Zigbee coordinator (Sonoff ZBDongle-E) + paired Aeotec water leak sensor via ZHA

USB Zigbee coordinator (Sonoff ZBDongle-E, CP210x UART bridge) added to Big Boi and passed through to the HA VM via TrueNAS USB Passthrough Device config (Controller Type: qemu-xhci, Device: usb_1_5 CP210x UART Bridge). VM restart required to enumerate the device inside HAOS (in-guest HA restart alone does not pick up passthrough changes).
ZHA integration set up via automatic setup, using the passed-through coordinator. Paired first sensor: Aeotec Water Leak Sensor (Zigbee, plain protocol, no Aqara/SmartThings hub dependency) via triple-tap tamper switch inclusion.
Gotcha to remember: USB passthrough binds to bus/port path (usb_1_5), not just VID/PID. Moving the dongle to a different physical USB port on Big Boi will break passthrough until reconfigured in the VM's Devices tab. Dongle should stay on a labeled, fixed port, and ideally on a USB extension cable away from the chassis to reduce 2.4GHz interference from USB3 traffic.
Next sensor to pair: Sonoff SNZB-05P (not yet added).
