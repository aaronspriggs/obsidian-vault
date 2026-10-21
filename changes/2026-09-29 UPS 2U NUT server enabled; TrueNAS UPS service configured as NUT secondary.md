---
date: 2026-09-29
type: config
system:
- '[[UniFi UPS 2U]]'
- '[[TrueNAS SCALE (Big Boi)]]'
project:
- '[[Rack Infrastructure — UPS + Power Management]]'
notion_id: 3ea7ae76-22ba-812d-b641-e8540a0aed1d
---

# UPS 2U NUT server enabled; TrueNAS UPS service configured as NUT secondary

NUT server on UPS 2U (id unifiups, 3493, creds in 1Password "UPS 2U - NUT"). TrueNAS UPS: Slave, shutdown on battery after 300 s (60 s at first), powerdown off, start on boot. Upsmon login confirmed over TLS. Password rotated same day after exposure in a Claude session.

## What

Aaron enabled the NUT server on the UniFi UPS 2U (UniFi Network, UPS device settings): ID `unifiups`, port 3493, credential required, user and password in 1Password "UPS 2U - NUT"; client list set to Big Boi (192.168.1.248). In TrueNAS → System → Services → UPS: Mode Slave, Remote Host 192.168.1.12, port 3493, Identifier `unifiups`, Monitor User from 1Password, Shutdown Mode "UPS goes on battery", Shutdown Timer 60 s (raised to **300 s** later the same day, after measuring 110 W load / ~1 h runtime; see project Decisions), Power Off UPS off, other fields default. Service started and set to start automatically.
The outlet layout was also recorded: battery outlets power Big Boi, UDM Pro, USW Pro Max 16 PoE and USW Flex 8 PoE (Basement), so the NUT network path stays up during an outage.

## Findings

- UniFi's NUT server requires a login even for `LIST VAR` (anonymous gets `ERR ACCESS-DENIED`); only `LIST UPS` is anonymous. So plain `upsc` can't read it, and TrueNAS's UPS reporting graphs (upscharge, upsload, upsruntime) stay empty. Shutdown is unaffected: upsmon logs in.
- upsmon connects over TLS ("Connected to NUT server 192.168.1.12 in SSL", no cert verification).
- The read-only `claude` TrueNAS API user can read `ups.config.monpwd` in clear text. It was printed once in a Claude session, so Aaron rotated the NUT password in 1Password, UniFi and TrueNAS the same day. Filter `monpwd` from any `ups.config` output.

## Verify

`truenas-api ups.config` (drop `monpwd`): SLAVE, `unifiups@192.168.1.12:3493`, shutdown BATT, timer 300 (verified after the change). `service.query` shows ups RUNNING, enabled. On TrueNAS: `sudo journalctl -u nut-monitor -n 30 --no-pager` shows "Connected to NUT server 192.168.1.12 in SSL" after the 14:44:59 restart with no login or poll failures after it. UniFi API `stat/device` for the UPS: `nut_server.enabled` true, `nut_client_ips` [192.168.1.248].

## Not done yet

Power Cycle on Restore safety check, BIOS power-on, staged test (see project).
