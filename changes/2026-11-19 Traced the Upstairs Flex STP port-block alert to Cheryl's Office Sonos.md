---
date: 2026-11-19
type: research
system:
- '[[USW Flex 2.5G 8 PoE]]'
- '[[USW Pro Max 16 PoE]]'
- '[[UniFi (UDM Pro)]]'
---

# Traced the Upstairs Flex STP port-block alert to Cheryl's Office Sonos

At about 21:15 UTC on 2026-11-19 the UDM sent "USW Flex 2.5G 8 PoE - Upstairs Port 1 was blocked by STP to prevent a network loop". The device on that port is Cheryl's Office Sonos, and the loop runs through SonosNet. Nothing was changed yet.

## What was found

- Upstairs Flex port 1: 100 Mb, `stp_state: discarding`, last MAC 38:42:0b:1f:31:a6 at 192.168.1.205 (unifi-api `stat/device`).
- That MAC is HA's Sonos device "Cheryl's Office" (One SL, firmware 27.1, connection `mac 38:42:0b:1f:31:a6`).
- UniFi `stat/sta` lists that Sonos as wired on Pro Max port 9, uptime 431 s at 21:22, so it had just restarted and come back over SonosNet to the wired kitchen Sonos (.32 on Pro Max port 8, .171 on port 9). Wired upstairs plus a wireless SonosNet link to a wired kitchen speaker is a loop, and RSTP on the Upstairs Flex blocks the wired leg. Poppy's Room (Era 100 SL, .108) is a plain Wi-Fi client on the Upstairs AP and isn't part of it.
- The KB already showed .205 on Pro Max port 9 on 2026-09-28 and 2026-11-15, so the block isn't new; the alert fires again whenever the Sonos restarts and the loop re-converges. The Pro Max note had read this as "something daisy-chained" on port 9, and the Flex note had port 1 as an unknown device; both are corrected.

## Effect

Nothing is down. Cheryl's Office plays over a wireless hop to the kitchen instead of its cable, and each re-convergence briefly flushes MAC tables. STP is doing its job; don't turn it off.

## Fix (pending Aaron's choice)

Turn off the Wi-Fi radio on the wired Sonos so it uses only its cable; STP then has no loop to block and port 1 goes to forwarding.
