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

Turn off Wi-Fi on every wired Sonos (Cheryl's Office and both kitchen One SLs), so SonosNet never forms and each uses only its cable; STP then has nothing to block and Flex port 1 goes to forwarding. Poppy's Room stays a Wi-Fi client. Leave STP on.

Checked against outside sources on 2026-11-19:

- Sonos staff's UniFi tutorial (Atom P, April 2026, updated through June 2026) recommends either fully wireless or "Fully Wired: ... WiFi is manually disabled on each player via the Sonos app". A mixed setup with Wi-Fi left on needs classic STP (not RSTP), switch priorities 4096/8192, and Sonos ports with edge Auto, BPDU guard off, root guard off, path cost 10. https://en.community.sonos.com/ask-a-question-228987/sonos-unifi-best-practices-recommended-settings-6933597
- Sonos support: Wi-Fi can only be turned off while the product is on Ethernet. In the app it's Settings → the room → the product's model name → Connection → Disable WiFi. If the cable is unplugged the product drops out of the app until it's plugged back in. https://support.sonos.com/en-us/article/disable-or-enable-wi-fi-on-your-sonos-products
- AirPlay keeps working on a wired Sonos with Wi-Fi off, because it runs over IP (community answer from 2022, not Sonos staff). https://en.community.sonos.com/controllers-and-music-services-228995/does-turning-off-the-network-wireless-wifi-ability-of-a-sonos-device-also-turn-off-it-s-airplay-ability-6870089
- Ubiquiti's own article (help.ui.com 18930473041047) returned 403 to the fetcher and wasn't read. Search snippets say it also recommends turning off SonosNet and Wi-Fi.
