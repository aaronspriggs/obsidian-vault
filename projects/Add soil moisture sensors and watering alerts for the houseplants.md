---
type: project
status: active
priority: low
system:
- '[[Home Assistant OS (VM)]]'
next_step: '2026-11-09: Aaron orders 3–4 Zigbee router plugs and 2 ThirdReality Gen2 soil sensors as a pilot; Claude installs Plant Monitor + OpenPlantbook + flower-card when they arrive.'
---

## Goal

A soil moisture sensor in each of about 30 houseplants, with per-plant watering alerts and a plant dashboard in Home Assistant.

## Status / next step

2026-11-09: hardware chosen, nothing ordered yet. Pilot with 2 sensors before buying the other 28.

## Plan

1. **Zigbee routers first.** The ZHA network had 9 devices on 2026-11-09 (verified live), all battery end devices (Aeotec/Samjin leak and multipurpose sensors, one Sonoff SNZB-02P), so there are no routers. The coordinator (Sonoff ZBDongle-E) is on Big Boi, and 30 more sleepy end devices would all have to parent directly to it, which is beyond its child-table limit and its range across floors. Put 3–4 mains-powered Zigbee plugs (routers) around the plant areas, pair them first.
2. **Pilot:** 2 ThirdReality Smart Soil Moisture Sensor Gen2 (Zigbee, native ZHA support, IP67, 1×AA). Check they pair cleanly and that moisture shows as a moisture sensor (buyers report it shows as humidity by default).
3. **Software (well-trodden route):** [Olen/homeassistant-plant](https://github.com/Olen/homeassistant-plant) (HACS custom repository; replaces the unused core `plant` integration; 883 stars, release v2026.11.1 on 2026-11-07), [Olen/home-assistant-openplantbook](https://github.com/Olen/home-assistant-openplantbook) (HACS default; needs a free OpenPlantbook API key, which Aaron creates and stores in 1Password), and [Olen/lovelace-flower-card](https://github.com/Olen/lovelace-flower-card). Each plant becomes a device with species thresholds pre-filled from OpenPlantbook.
4. **Alerts:** one automation on all plant entities going to `problem` for moisture, with a delay so a reading hovering at the threshold doesn't alert repeatedly. Batteries go through Battery Notes (already installed) like the other battery devices.
5. **Dashboard:** flower-card per plant, grouped by area (auto-entities is installed).
6. Roll out the remaining 28 sensors once the pilot is good; tune thresholds per pot after about a week of readings.

## Decisions

- 2026-11-09: ThirdReality Gen2 over the [SmartHomeScene test](https://smarthomescene.com/reviews/smart-soil-sensors-tested/) winners. The test ran on Zigbee2MQTT; its best Zigbee pick, the Tuya ZG-303Z, needs a ZHA quirk with reported swapped moisture/humidity values ([HA forum](https://community.home-assistant.io/t/zigbee-soil-moisture-sensor-zg-303z-by-hobeian/982876)), and one ZG-303Z listing in the test was a dud. Ecowitt WH51 was most accurate but needs a gateway, and most Ecowitt gateways are believed to cap soil sensors at 8 channels (not verified), too few for 30 plants. The ZWA-2 (Z-Wave) doesn't help: there are no mainstream Z-Wave soil sensors.
- 2026-11-09: Aaron chose the HACS Plant Monitor route over native threshold helpers.

## Open questions

- Which router plugs (ThirdReality, IKEA, Sonoff) and where; depends on where the plants are.
  - 2026-11-11 IKEA: INSPELNING (E2206, Zigbee, energy monitoring) is a Zigbee router and works in ZHA; TRETAKT is Zigbee but discontinued. GRILLPLATS, its replacement, ships as Matter over Thread and only becomes Zigbee through an undocumented 8-press reset ([Z2M issue](https://github.com/Koenkk/zigbee2mqtt/issues/31474)), so don't buy it for this. After pairing, confirm the device type shows as Router in ZHA.
  - 2026-11-11 IKEA US site (checked live): INSPELNING isn't sold in the US (its US product URL redirects to the catalogue). TRETAKT (40556511, $9.99) is still sold online and in stock but tagged "Last chance". The other US plugs, GRILLPLATS and TOFSMYGGA (outdoor), are Matter over Thread.

## Changes

![[Changes.base#For this project]]
