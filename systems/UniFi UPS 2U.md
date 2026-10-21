---
status: active
category: hardware
ip: 192.168.1.12
last_verified: 2026-09-29
notion_id: 3e97ae76-22ba-81d7-a7ef-fb001fab72f6
---

Rack UPS, adopted in UniFi. NUT server on; TrueNAS shuts down 300 s after on-battery (configured 2026-09-29, untested; BIOS auto-power-on not set yet). 110 W load, ~1 h runtime.

## Overview

UniFi UPS 2U in the rack (216 Wh, 1,500 VA / 1,000 W; about 2.3 min at full load, 8 min at half load, per the purchase research). The goal is a clean shutdown of Big Boi on power loss, not long runtime. Installed by Aaron; adopted into UniFi Network and visible in HA through the UniFi integration (verified 2026-09-28).

## Access

- Managed in UniFi Network on the UDM Pro ([https://192.168.1.1](https://192.168.1.1/)). IP 192.168.1.12 (**static on the device since 2026-09-29**, gateway .1, DNS 1.1.1.1; it sits inside the LAN DHCP pool .6–.254, low conflict risk since the UDM checks for in-use addresses), MAC 1c:0b:8b:3a:f7:13, uplinked to **UDM Pro port 8** at 100 Mb. Model code USWDA25. **NUT server enabled 2026-09-29** on TCP 3493; UPS name `unifiups`. Credentials in 1Password "UPS 2U - NUT". Unlike stock NUT, reading variables (`LIST VAR`) needs a login (anonymous gets ERR ACCESS-DENIED); `LIST UPS` works anonymously. The UniFi API shows 8 outlets, all on and unnamed, with no battery/load data.
- HA: `device_tracker.ups_2u`, `sensor.ups_2u_state` (connected), `update.ups_2u`. The UniFi integration exposes device health only: no battery charge, load or on-battery state.

## Config

- Firmware 1.6.1.413 (current, auto-update off). Up since 2026-08-04.
- **Graceful shutdown configured 2026-09-29, partly tested** (a 30 s mains pull was ridden out correctly; full shutdown/restart not yet tested): TrueNAS UPS service runs as NUT secondary (Slave) to `unifiups@192.168.1.12:3493` over TLS and shuts Big Boi down 300 s after the UPS goes on battery (Power Off UPS off). Big Boi's BIOS is not yet set to power on after AC loss, so after a shutdown it stays off until someone presses the power button. TrueNAS UPS graphs stay empty because UniFi denies anonymous reads. Details: Changes "UPS 2U NUT server enabled; TrueNAS UPS service configured as NUT secondary".
- **Battery outlets (per Aaron, 2026-09-29):** 4 battery-backed ports in use, powering Big Boi (TrueNAS), USW Pro Max 16 PoE, UDM Pro and USW Flex 8 PoE (Basement). The ISP ONT is **not** on the UPS, so internet drops immediately on a power cut.
- **Measured load (UniFi UI, 2026-09-29):** 110 W / 1000 W (11%), 0.89 A, battery 100%, mode Line. UniFi estimates **1 h 7 min runtime at this load**, far more than the purchase-research figures suggested.
- **UniFi-side shutdown settings (2026-09-29):** Safe Shutdown trigger point = 5 min runtime remaining; Safe Shutdown Pairing: UDM Pro not paired; Power Cycle on Restore: off. Whether the trigger point also raises LB/FSD to NUT clients is unconfirmed.

## Dependencies

Protects: Big Boi (TrueNAS), UDM Pro, USW Pro Max 16 PoE, USW Flex 8 PoE (Basement). The USW Flex (Upstairs) is also covered indirectly, since it takes PoE from the Pro Max 16. The whole TrueNAS → switch → UDM Pro → UPS path is on battery, so network NUT keeps working during an outage.

## Decisions

- **2026-03-03:** chose the UniFi UPS 2U for the rack; the aim is graceful shutdown rather than runtime.

## Related

Project: "Rack Infrastructure — UPS + Power Management".

## Open work

![[Projects.base#Open for this system]]

## Runbooks

![[Runbooks.base#For this system]]

## Recent changes

![[Changes.base#For this system]]
