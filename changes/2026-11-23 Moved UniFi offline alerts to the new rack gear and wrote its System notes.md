---
date: 2026-11-23
type: config
system:
- '[[USW Enterprise 48 PoE]]'
- '[[USP PDU Pro]]'
- '[[Home Assistant (integrations and automations)]]'
---

# Moved UniFi offline alerts to the new rack gear and wrote its System notes

## What changed

Added label `homelab_watch` to `sensor.usw_enterprise_48_poe_state`, `sensor.usp_pdu_pro_state` and `sensor.usw_flex_2_5g_5_state` (Aaron's desk Flex, unlabelled since it was adopted: the gap recorded on 2026-10-17), then ran `alert2.reload`. Alert2's `homelab_unifi_offline` generator now has `alert2.homelab_usw_enterprise_48_poe_offline`, `_usp_pdu_pro_offline` and `_usw_flex_2_5g_5_offline`, all off.

Removing the label from the retired `sensor.usw_pro_max_16_poe_state` was refused by Claude Code's auto-mode classifier, so `alert2.homelab_usw_pro_max_16_poe_offline` is still on. It is muted only while maintenance mode is on. Either Aaron removes the label in HA (Settings → Entities → the sensor → Labels), or he forgets the Pro Max 16 in UniFi, which he needs to do before selling it anyway; the entity then goes unavailable and the alert's condition drops it.

New System notes: [USW Enterprise 48 PoE](<../systems/USW Enterprise 48 PoE.md>) and [USP PDU Pro](<../systems/USP PDU Pro.md>). [USW Pro Max 16 PoE](<../systems/USW Pro Max 16 PoE.md>) is deprecated, superseded by the Enterprise 48.

## Why

Aaron asked what the new UniFi gear needs. The core switch and the PDU had no offline alert, and the retired switch's alert would push as soon as maintenance mode went off.

## Notes

Findings left for Aaron, in the rack and patch panel projects: the Enterprise 48's STP priority is the default 32768 while the Upstairs Flex has 8192; the PDU's measured 171 W against the UPS's 160 W output says the PDU isn't on a UPS battery outlet as planned (or Big Boi, the UDM and the switch are on the PDU); the switch's first temperature read is 62 °C. Roll back the labels with `ha_set_entity(..., labels=['homelab_watch'], label_operation='remove')` and `alert2.reload`.
