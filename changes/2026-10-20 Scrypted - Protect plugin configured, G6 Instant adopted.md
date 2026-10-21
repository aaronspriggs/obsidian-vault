---
date: 2026-10-20
type: config
system:
- '[[Home Assistant OS (VM)]]'
- '[[UniFi (UDM Pro)]]'
project:
- '[[Scrypted — UniFi Camera HomeKit Bridge]]'
commit: https://github.com/aaronspriggs/spriggs-homelab/commit/c782956
notion_id: 3ff7ae76-22ba-81c5-9cb4-eb6c561ca371
---

# Scrypted: Protect plugin configured, G6 Instant adopted, HomeKit standalone accessory; scrypted-api wrapper

New Scrypted admin user `Claude` (created by Aaron; 1Password `Scrypted - Claude Login`, ID dm7itbvhv2xyxgpypauhbg46ai; username is case-sensitive) and repo wrapper scrypted/scrypted-api (commits d6d4614, 251106e, c782956; Node, @scrypted/client 1.3.26; deployed to ~/.local/lib/scrypted-api, symlink ~/.local/bin/scrypted-api; in deployed.tsv). Protect plugin: ip 192.168.1.1, user `scrypted` (password piped from 1Password, never printed). Current Scrypted doesn't auto-add Protect cameras (log: "unknown device, sync needed?"); discovered and adopted the G6 Instant (nativeId 69fd51f202649a03e400043a, Scrypted device 30). Streams all H.264 (High 3840x2160 16 Mbps, Medium 1280x720 4 Mbps, Low 640x360 1 Mbps, 30 fps, AAC), so Super Encoding is off and Scrypted remuxes. Prebuffer High+Medium, stream roles left at Default. HomeKit mixin added, Standalone Accessory Mode on (HKSV 3 experimental, left off). Aaron paired it in the Home app; a live view from his iPhone streamed 141 s. Scrypted Core `localAddresses` set to 192.168.1.218 (was unset; the HA VM also has 172.30.x Docker bridge addresses, and the HomeKit plugin warned they can break streaming). Pairing code: `scrypted-api settings "G6 Instant"`, key homekit:pincode.
