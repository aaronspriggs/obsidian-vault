---
type: project
status: active
priority: low
system:
- '[[UniFi UPS 2U]]'
- '[[TrueNAS SCALE (Big Boi)]]'
next_step: '2026-10-16: TrueNAS UPS config re-verified unchanged (SLAVE to unifiups@192.168.1.12:3493, shutdown BATT, 300 s). Still parked until Aaron picks a maintenance window: shut Big Boi down, 20 s pull to test Power Cycle on Restore, BIOS Power On, full >5 min test, runbook. Until then a >5 min outage leaves Big Boi off until powered on by hand. Later: UPS data into HA via NUT. Aaron confirmed 2026-10-16 he wants this finished, not dropped.'
notion_id: 3187ae76-22ba-814f-a287-d9785fedac44
---

Graceful shutdown live 2026-09-29 but untested: UPS 2U NUT server on, TrueNAS Slave shuts down 300 s after on-battery; 110 W load, ~1 h runtime. Remaining: Power Cycle on Restore check, BIOS power-on, staged test, runbook.

## Goal

On a power cut, ride out short blips, and on anything longer shut Big Boi (TrueNAS + its VMs) down cleanly before the UPS battery runs out, then bring everything back when power returns.

## Status (2026-09-29)

**Graceful shutdown is live but untested** (steps 1, 2, 4 done; see Changes "UPS 2U NUT server enabled; TrueNAS UPS service configured as NUT secondary"). Load measured, timer raised to 300 s, 30 s mains-pull test passed (7b). UPS IP 192.168.1.12 to be pinned as a fixed IP in UniFi (TrueNAS connects by IP). Remaining (maintenance window): Power Cycle on Restore safety check, then BIOS power-on, staged test, runbook. The bullets below are the 2026-09-28 baseline.
**2026-09-28 baseline: hardware done, nothing configured.**
- UniFi UPS 2U bought and installed, up since 2026-08-04, adopted in UniFi Network. Firmware 1.6.1.413 (current). Uplinked to the **UDM Pro port 8**. See [UniFi UPS 2U](<../systems/UniFi UPS 2U.md>).
- **NUT server off:** TCP 3493 on the UPS (192.168.1.12) refuses connections, and the UPS's `nut_client_ips` / `nut_client_table` are empty (UniFi API, read-only account, 2026-09-28).
- **TrueNAS UPS service stopped**, no driver or remote host set (TrueNAS API 2026-09-28).
- UniFi OS 5.1.33 / Network 10.6.106, above the UniFi OS 4.4.3 minimum for UPS graceful shutdown.
- UniFi's API shows 8 battery outlets, all on and unnamed; no battery %, load or runtime is exposed to the Network API or HA.
- So today a long outage hard-powers-off Big Boi when the battery empties. Aaron recalls the 2026 Gluetun failure and rebuild followed a power outage where the server didn't come back cleanly.

## How the UPS 2U does shutdown (researched 2026-09-28)

- The **NUT server runs on the UPS itself** (its own IP), port **3493**, once enabled in UniFi Network on the UPS device. Credentials are set/shown in UniFi (community reports mention `nut`/`nut` defaults; set our own). UPS name is found with `LIST UPS` against the UPS IP. Clients connect as NUT **secondary** (TrueNAS "Slave" mode). [gist: NUT client on UniFi UPS](https://gist.github.com/ksolheim/bb8c91851b227afce300e149bd285dfa), [kilala.nl: UniFi UPS with Proxmox, 2026-03-09](https://www.kilala.nl/index.php?id=2663)
- Reportedly it raises low-battery / shutdown at about **2 minutes of runtime left** (not yet confirmed on ours), which is too late for Big Boi plus three VMs. Community threads ask for a configurable delay. [community.ui.com](https://community.ui.com/questions/UniFi-UPS-2U---Configurable-Shutdown-Delay-is-Critical/a178eaac-8047-4097-9632-eb94e16a57df), [koromatech hands-on](https://koromatech.com/unifi-2u-ups-hands-on-graceful-shutdown-for-unas-my-entire-rack/)
- Runtime about 2.3 min at full load, 8 min at half load (216 Wh). Transfer 6–10 ms; recharge 6–8 h to ~90%.
- Reported limits: Ubiquiti caps the NUT server at 3 clients, and one user only got one client stable. We need exactly one (TrueNAS).

## Plan (approved by Aaron 2026-09-28, not started)

1. ✅ **Done 2026-09-29:** battery outlets power Big Boi, USW Pro Max 16 PoE, UDM Pro and USW Flex 8 PoE (Basement); USW Flex (Upstairs) is covered through PoE from the Pro Max 16. Network path is covered. Original step: **Aaron: record what's on each outlet.** For network NUT to work during an outage, the path TrueNAS → switch → UDM Pro → UPS must stay up, so the **UDM Pro and USW Pro Max 16 PoE must be on battery outlets** too, not just Big Boi. Check the combined load fits (see Open questions).
2. ✅ **Done 2026-09-29:** NUT server on, id `unifiups`, port 3493, credential required, user in 1Password "UPS 2U - NUT"; UniFi `nut_client_table` lists 192.168.1.248. Original step: **Aaron (UniFi):** enable the NUT server on the UPS 2U, set a non-default username/password (save in 1Password as "UPS 2U - NUT"), and allow only Big Boi (192.168.1.248) as a client if UniFi offers an allowlist.
3. **Changed 2026-09-29:** UniFi's NUT denies anonymous `LIST VAR` (ERR ACCESS-DENIED), so plain `upsc` can't read it from the VM or from TrueNAS; TrueNAS's UPS reporting graphs stay empty for the same reason. Did step 4 first; load to be read from the UniFi UI instead. Original step: **Claude (read-only):** from the ClaudeCode VM, confirm 3493 answers, get the UPS name with `LIST UPS` (plain `nc`), and read status with `upsc` (needs apt `nut-client` on the VM; one-off reads, no persistent monitor, so it doesn't hold one of the UPS's NUT client slots) (`ups.status` = OL, `battery.charge`, `ups.load`, `battery.runtime`). Record the load; that's the first real runtime number.
4. ✅ **Done 2026-09-29:** `ups.config` verified via API: SLAVE, `unifiups@192.168.1.12:3493`, shutdown BATT, timer 60 s (raised to 300 s and re-verified via API later on 2026-09-29), powerdown off; service RUNNING, start on boot. Upsmon login confirmed in the TrueNAS journal (over TLS), including after the password rotation. Original step: **Aaron (TrueNAS → System → Services → UPS):** Mode **Slave**, Remote Host 192.168.1.12, Remote Port 3493, Identifier = the `LIST UPS` name, Monitor User/Password from step 2, **Shutdown Mode = "UPS goes on battery"** with a **Shutdown Timer** (start at 60 s, tune once the load is known). Enable the service and Start Automatically. "On battery + timer" is used instead of "low battery" because low battery arrives with only ~2 min left.
5. **Big Boi BIOS:** set "Restore on AC power loss" to **Power On** so it boots when power returns (VMs already autostart). Needs a reboot, so do it in a maintenance window.
6. **Checked 2026-09-29 (partly):** TrueNAS alert classes UPSOnBattery, UPSCommbad, UPSReplbatt (CRITICAL) and UPSBatteryLow (ALERT) are all in `truenas-alert-relay`'s RELAY_LEVELS, so they reach HA. **Gap:** the relay polls every 5 min, and both the relay (ClaudeCode VM) and HA run on Big Boi, so with a 60 s timer the on-battery alert will usually not reach HA before everything shuts down. Also, unknown whether the ISP modem/ONT is on battery (it isn't on the outlet list), which HA's phone push would need. Decide in step 7b whether that matters. Original step: **Alerting:** confirm TrueNAS raises UPS on-battery / comm-lost alerts and that `truenas-alert-relay` forwards them to HA; otherwise add a check.
7. **Test in stages.** First, at the start of the maintenance window with Big Boi already shut down manually: pull UPS mains ~20 s and watch whether the UDM/switches reboot. If they don't, enable Power Cycle on Restore and pair the UDM Pro (Aaron's plan); if they do, keep both off. Then:  (a) TrueNAS shows the UPS online; (b) ✅ **Done 2026-09-29 ~22:08:** Aaron unplugged mains 30 s with Big Boi running. TrueNAS raised UPSOnline at 22:08:52 (so the on-battery event arrived over NUT and cleared), Big Boi uptime unaffected (85 days), no shutdown. Alert stats: battery.runtime 4000 s, battery.charge 65% (suspiciously low after 30 s at 110 W; likely a voltage-sag estimate, check it recovers to 100% in UniFi). Original: unplug the UPS mains for ~20 s (shorter than the timer): alert fires, status returns to OL, no shutdown; (c) in a maintenance window, unplug longer than the timer: TrueNAS stops VMs and powers off cleanly with battery to spare, then replug and confirm Big Boi boots and all three VMs and Dockhand stacks come back.
8. Write a runbook ("UPS power loss: what happens and how to test") and link it to the UPS 2U and TrueNAS pages.

## Decisions

- **2026-09-29:** measured load 110 W / ~1 h runtime, ONT not on UPS. Keep TrueNAS on "UPS goes on battery" but raise the timer from 60 s to 300 s: rides out short outages, shuts down with ~1 h of battery left, shallow discharges. UniFi trigger point (5 min remaining) kept as a backstop. Rejected "low battery" mode: relies on unconfirmed LB-over-NUT and the aging runtime estimate, and gains little with no internet.
- **2026-03-03:** UniFi UPS 2U chosen over the UPS Tower (bigger battery, rack mount). Goal is clean shutdown, not runtime. Mount low in the rack.
- **2026-09-28:** use **network NUT** from TrueNAS to the UPS, not USB. It needs no extra hardware; the 2026-03 plan for a USB 3.2 PCIe card only makes sense if network NUT proves unreliable (and it's unconfirmed that the UPS 2U's USB port speaks standard NUT/HID).

## Open questions

- Answered 2026-09-29: total load is 110 W (11%), UniFi estimates 1 h 7 min runtime (UniFi UI; see UPS 2U page). Runtime is not the constraint.
- **Power Cycle on Restore** (UniFi, off): tooltip says "Briefly cycles power when AC returns during battery use to restart connected devices." Reads as cycling on *any* return from battery, which would hard-cut Big Boi after a blip shorter than the TrueNAS timer. Kept off until tested safely: with Big Boi already shut down, pull mains ~20 s and see whether the UDM/switches reboot. Without it, if power returns after Big Boi's shutdown but before the battery empties, Big Boi stays off until powered on by hand (no IPMI: consumer board, `ipmi.is_loaded` false, 2026-09-29).
- UDM Pro Safe Shutdown Pairing: don't pair while Power Cycle on Restore is off. A paired UDM that shuts down at the trigger would stay off if AC returns before the battery empties, taking the whole network down.
- How long does a clean TrueNAS shutdown with three VMs take? Measure during test (c).
- Answered 2026-09-29: UniFi has a NUT client list (set to 192.168.1.248), and upsmon connects over TLS (no cert verification). Was: Does UniFi's NUT server offer a client allowlist, and is its traffic plain NUT (not TLS)? Treat the NUT password as low-value but keep it out of Notion.
- 2026-09-29: the read-only `claude` TrueNAS API user can read `ups.config.monpwd` in clear text. Filter it out of any `ups.config` output.
- Future UNAS Pro: UniFi's native graceful shutdown covers it; it doesn't use a NUT slot.
- **UPS data in HA via NUT** (Aaron 2026-10-15: later, as part of this project). HA has discovered a NUT server advertised by TrueNAS at 192.168.1.248:3493; the discovery card is left un-ignored on purpose. Before adding it, check whether TrueNAS actually serves upsd as a secondary. Pointing HA at TrueNAS would avoid using one of the UPS 2U's NUT client slots (capped at 3, and one user reported only one stable client). Pointing it at the UPS (192.168.1.12) would need the "UPS 2U - NUT" credential and a second slot.

## Changes

![[Changes.base#For this project]]
