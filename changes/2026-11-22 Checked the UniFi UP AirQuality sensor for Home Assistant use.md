---
date: 2026-11-22
type: research
system:
- '[[UniFi (UDM Pro)]]'
- '[[Home Assistant (integrations and automations)]]'
---

# Checked the UniFi UP AirQuality sensor for Home Assistant use

No system changes. Aaron asked about the [UP-AirQuality](https://store.ui.com/us/en/category/physical-security-sensors-alarms/products/up-airquality) ("Vape Detection & Air Quality Sensor") after we compared the ecobee and Dyson readings and found Poppy's room has no humidity sensor.

**Specs** ([tech specs](https://techspecs.ui.com/unifi/physical-security/up-airquality)): $99. PoE only (37–57 V, 2.2 W, 10/100 RJ45, no Wi-Fi or Bluetooth). It measures temperature (±1 °C), humidity (0–90 %, **±8 % RH**), CO₂ (±50 ppm + 3 %), PM1/2.5/4/10, a VOC index, a NOx index, an AQI and a vape index. It needs Protect 7.1+. Indoor only, Ø93 × 40.5 mm.

**Home Assistant: no readings.** The [unifiprotect docs](https://www.home-assistant.io/integrations/unifiprotect/) say Protect reports no sensor capabilities for the UP Air Quality, so HA gets only general device entities. Protect's public API carries the readings only inside threshold events. uiprotect won't add private-API features ([uiprotect #1007](https://github.com/uilibs/uiprotect/issues/1007), declined 2026-06-19). The request is open in [uiprotect #1154](https://github.com/uilibs/uiprotect/issues/1154) (`wait-for-ui`) and [core #178669](https://github.com/home-assistant/core/issues/178669), with no timeline as of 2026-11-22. Community MQTT bridges use the private API; not evaluated.

**Takeaway:** not a fit while HA can't read it. For Poppy's room in particular, the ±8 % RH accuracy is too coarse to hold a 40–45 % target, and it needs a cable run. Re-check #1154 if Aaron still wants one.
