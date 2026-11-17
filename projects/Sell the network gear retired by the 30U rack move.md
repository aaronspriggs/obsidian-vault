---
type: project
status: active
priority: medium
system:
- '[[USW Pro Max 16 PoE]]'
- '[[USW Flex 2.5G 8 PoE]]'
parent: '[[Move the homelab into the 30U floor rack]]'
next_step: '2026-11-17: Aaron bought the USW Aggregation on 2026-11-11 with 30 days to return it (window closes about 2026-12-11) and expects to return it the week of 2026-11-16. The open questions below (boxes, Flex mount model, Isobar and 12U rack, where to sell) wait for their own chat; listings go up once the 30U rack has run cleanly on the Enterprise 48 for a week.'
---

## Goal

Sell the network gear the USW Enterprise 48 PoE replaces, and return the Aggregation, to offset the switch ($851 with shipping and tax, ordered 2026-11-15).

## Status (2026-11-15)

Enterprise 48 ordered. Nothing returned or listed yet. The Pro Max 16 and the Basement Flex stay in service until the 30U move is done and stable, so they're sold last.

## Plan

### Items

| Item | What goes with it | UI list price (US) | Suggested asking (used) | Action |
| --- | --- | --- | --- | --- |
| USW Aggregation (USW-Aggregation) | as bought | $297 + tax paid | n/a | Return for refund, inside the return window (about $316 with tax) |
| USW Pro Max 16 PoE (USW-Pro-Max-16-PoE) | its 210 W power adapter (comes with the switch) and the Pro Max 16 Rack Mount (UACC-Pro-Max-16-RM) | $399 + $49 rack mount | $300–330 the set | Sell after the move |
| USW Flex 2.5G 8 PoE, the Basement unit (USW-Flex-2.5G-8-PoE) | switch only; its 210 W adapter moves to the Upstairs Flex | $199 (adapter $79 separately) | $140–150 | Sell after the move |
| Flex 1U keystone mount | model not recorded | to check | to check | Sell with the Flex or separately (confirm) |
| Tripp Lite Isobar IBAR12ULTRA (1U) | — | to check | to check | Candidate: surplus once the PDU Pro is in (confirm) |
| 12U wall rack | — | to check | to check | Candidate: surplus after the move (confirm) |

List prices are from the Ubiquiti US store ([Pro Max 16 PoE](https://store.ui.com/us/en/products/usw-pro-max-16-poe), [Pro Max 16 Rack Mount](https://store.ui.com/us/en/products/uacc-pro-max-16-rm), [Flex 2.5G PoE](https://store.ui.com/us/en/category/all-switching/products/usw-flex-2-5g-8-poe)), checked 2026-11-15. Asking prices assume 60–75% of list for current UniFi gear in good condition; check recent sold listings before posting. Expected total: roughly $440–480 from the two switches plus the Aggregation refund; eBay fees take about 13%, a local sale none.

### Before listing each switch

1. Confirm its replacement is carrying the traffic (the move is done and has run a week).
2. In UniFi Network, remove (forget) the device so the buyer can adopt it.
3. Factory-reset it.
4. Remove the patch-panel labels and tidy the cables; photograph the front, ports, back and label, with the adapter and rack mount.
5. Note the firmware version from UniFi before removing it (Pro Max 16: 7.5.15.17146 on 2026-09-28).

### Draft listings

**Ubiquiti UniFi USW Pro Max 16 PoE with rack mount and power adapter**

Used, working, pulled from a home rack after an upgrade to a larger switch. Factory reset and removed from my UniFi controller, ready to adopt. 16 RJ45 ports: 12× 1 GbE PoE+ and 4× 2.5 GbE PoE++, plus 2× 10G SFP+ uplinks, with a 180 W total PoE budget ([UI specs](https://techspecs.ui.com/unifi/switching/usw-pro-max-16-poe)). Includes the 210 W external power adapter and the official Pro Max 16 Rack Mount (UACC-Pro-Max-16-RM), which fits it in 1U. [Box: yes/no]. Local pickup or shipped.

**Ubiquiti UniFi Flex 2.5G 8 PoE (USW-Flex-2.5G-8-PoE), switch only**

Used, working, factory reset and removed from my UniFi controller. 8× 2.5 GbE PoE++ ports, a 10 GbE RJ45 uplink that also takes PoE+++ input, and a 10G SFP+ uplink ([UI specs](https://techspecs.ui.com/unifi/switching/usw-flex-2-5g-8-poe)). Power adapter not included: it runs from PoE input (PoE+++ gives a 76 W PoE budget, PoE++ 46 W, PoE+ 16 W) or from UI's 210 W adapter (196 W budget), sold separately. [Box: yes/no]. Local pickup or shipped.

## Decisions

- **2026-11-15 (Aaron):** return the Aggregation rather than sell it; sell the Pro Max 16 with its rack mount and adapter (not kept as a cold spare); sell the Basement Flex but keep its 210 W adapter for the Upstairs Flex; keep the desk Flex 2.5G 5.
- **2026-11-15:** list the switches only after the 30U move has run cleanly on the Enterprise 48 for a week, so there's a fallback if the new switch has a problem.

## Open questions

- Where was the Aggregation bought? (Bought 2026-11-11, 30-day return window, so about 2026-12-11; Aaron, 2026-11-17.)
- Are the original boxes kept for the Pro Max 16 and the Flex?
- What is the Flex's 1U keystone mount (model), and does it go with the Flex or separately?
- Sell the Tripp Lite Isobar and the 12U wall rack once the 30U is up, or keep them?
- Local sale, eBay, or r/homelabsales?
