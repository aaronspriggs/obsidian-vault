---
type: task
status: active
priority: low
system:
- '[[UniFi (UDM Pro)]]'
next_step: '2026-11-02 Aaron: ship each unit as it sells; mark done when all three are sold.'
---

## Goal

Wipe and sell the three AmpliFi Alien routers that formed the mesh before the UniFi switch. Aaron has all three boxes and all cables. They were never reset, so each one still holds the Wi-Fi SSID/password, admin settings and the AmpliFi account link.

## Status

2026-11-02: listed on eBay, quantity 3 at $120 each (eBay suggested $115), Best Offer on with a $110 minimum. None sold yet. The dead AmpliFi `upnp` integration was already removed from HA on 2026-09-03 ([change](<../changes/2026-09-03 Removed dead AmpliFi router integration.md>)).

## Plan

Reset each unit by itself with no WAN cable so nothing reconnects to the old mesh: power it on, wait for the touchscreen to finish booting, press a paperclip into the reset hole on the bottom next to the WAN port and power plug and hold until the screen shows it resetting. Done when the screen comes back at the first-time setup prompt. In-app reset (router icon → General → Factory Reset) also works if the AmpliFi app still sees them, but it isn't needed. If any unit was added to Apple Home (the Alien gained HomeKit in 2022), remove it from the Home app, or the buyer can't pair it. If the units still show in the AmpliFi app, remove/hide them there too.

List after reset on eBay as one multi-quantity listing, condition Used, calculated shipping. Pricing checked 2026-11-02: used Alien routers ask roughly $145 to $250, with one $159.99 buy-it-now listing showing 45 sold, so $100 should move quickly. Ubiquiti has stopped selling AmpliFi and firmware/app updates appear to have stalled since 2024 (not officially announced).

## Open questions

Whether the boxes are three single-router boxes or a two-pack Alien Kit box plus a single; a kit box can't ship as a single unit, so it may need its own listing.
