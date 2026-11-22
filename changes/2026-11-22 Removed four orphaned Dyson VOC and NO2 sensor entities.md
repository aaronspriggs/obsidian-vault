---
date: 2026-11-22
type: config
system:
- '[[Home Assistant (integrations and automations)]]'
---

# Removed four orphaned Dyson VOC and NO2 sensor entities

While comparing the ecobee and Dyson air readings, Aaron asked whether the Dysons' `unavailable` VOC and NO₂ sensors could be fixed. They weren't broken. The installed `custom_components/dyson_local/sensor.py` (modified 2025-08-17) only creates the index sensors, unique_ids `<serial>-voc-index` and `-no2-index`. The old `<serial>-voc` and `-no2` entities were left in the registry with `restored: true`. They had no long-term statistics since at least 2025-06, and no automation, script, scene, helper or dashboard referenced them. They looked new because every HA restart re-marked them `unavailable`, most recently the Core 2026.11.0 restart on 2026-11-09.

Removed with Aaron's Tier 3 yes, through `ha_remove_entity`:

- `sensor.bedroom_volatile_organic_compounds`, `sensor.bedroom_nitrogen_dioxide` (Bedroom Dyson, K3W-US-PNA1704A)
- `sensor.aaron_office_dyson_volatile_organic_compounds`, `sensor.aaron_office_dyson_nitrogen_dioxide` (Office Dyson, N9R-US-PJA6510A)

VOC and NO₂ now come only from `sensor.bedroom_{volatile_organic_compounds,nitrogen_dioxide}_index` and `sensor.office_{volatile_organic_compounds,nitrogen_dioxide}_index`, a low-is-good index, not µg/m³.

Verify: all four removed IDs return not found, and the four index sensors report (0.6, 0.2, 0.3, 0.0 at 05:25 MST). Roll back: none needed and none possible. The integration no longer creates these entities, so they can't come back short of a code change upstream.

Left alone: the system log has "Failed to request environmental data" from both Dysons, three times since about 2026-11-13. Those are dropped polls that recover on their own.
