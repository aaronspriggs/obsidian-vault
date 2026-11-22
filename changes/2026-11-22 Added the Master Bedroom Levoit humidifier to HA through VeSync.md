---
date: 2026-11-22
type: install
system:
- '[[Home Assistant (integrations and automations)]]'
---

# Added the Master Bedroom Levoit humidifier to HA through VeSync

Aaron added the core VeSync integration (cloud polling) from the add-integration link Claude gave him, logging in with his own VeSync account; the credentials never passed through Claude. It found one device, the Superior 6000S (LEH-S602S-WUS, firmware 1.0.04, up to date), which landed in the Master Bedroom area on its own. Entities: `humidifier.master_bedroom_superior_6000s` (modes auto, humidity, normal, sleep; target 30–80 %), `sensor.master_bedroom_superior_6000s_{humidity,temperature,filter_lifetime}`, `number.master_bedroom_superior_6000s_mist_level` (1–9), `binary_sensor.master_bedroom_superior_6000s_{low_water,water_tank_lifted}`, switches for display, child lock, auto off and drying mode, and a firmware update entity.

**Why:** Aaron felt its humidity reading ran high. The Bedroom Dyson in the same room gives a second reading to check it against.

**First comparison (07:21 MST):** the 6000S read 58 % at 60.4 °F. The Bedroom Dyson read 46 % at 67.6 °F and the ecobee Master Bedroom sensor 66.0 °F. Saturation vapour pressure is about 1.80 kPa at 60.4 °F and 2.31 kPa at 67.6 °F, so 46 % at the room temperature equals about 59 % at the unit's temperature. The two sensors agree on the moisture in the air; the 6000S measures air about 7 °F cooler, probably evaporatively cooled at the wick. So it reads RH about 12 points high. It was in sleep mode with a 50 % target and mist level 1, so it thinks the room is already humid enough and holds the room near 46 %. One reading so far; a few days of history will show whether the offset holds.

Verify: [History, both sensors](http://192.168.1.218:8123/history?entity_id=sensor.master_bedroom_superior_6000s_humidity%2Csensor.bedroom_humidity%2Csensor.master_bedroom_superior_6000s_temperature%2Csensor.bedroom_temperature). Roll back: delete the VeSync integration entry (Tier 3).
