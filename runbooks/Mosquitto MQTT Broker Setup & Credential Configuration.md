---
kind: setup
status: active
system:
- '[[Home Assistant OS (VM)]]'
notion_id: 3087ae76-22ba-8133-9c13-f0c1fbe4cabd
---

How to correctly configure Mosquitto credentials and the HA MQTT integration. Covers the critical ordering requirement and common auth failure.

## Overview

Mosquitto runs as a Home Assistant add-on and serves as the MQTT broker for all local devices including the Raspberry Pi wall panel (TouchKio). This runbook covers correct credential setup and the most common failure mode.

## Key Concepts

- **Internal hostname (within HA):** core-mosquitto
- **External hostname (for devices like RPi):** 192.168.1.218
- **Port:** 1883
- **TLS:** Disabled (local network only, acceptable for homelab use)

## Critical Ordering Rule

This is the most common source of auth failures. Always follow this order:
1. Define users in Mosquitto add-on config first
2. Save and restart Mosquitto
3. Verify clean startup in logs
4. Then reconfigure the HA MQTT integration to match
**The HA MQTT integration cannot create or change broker credentials.** It can only use credentials that already exist in Mosquitto. Doing it in the wrong order causes authentication failures.

## Mosquitto Add-on Configuration

Go to Settings → Add-ons → Mosquitto broker → Configuration and apply:
```yaml
logins:
  - username: mqtt_user
    password: YOUR_PASSWORD_HERE

anonymous: false
require_certificate: false
```
- Use a dedicated named user per device where possible
- Disable anonymous access
- Current MQTT user for wall panel: mqttdashboard

## Reconfigure HA MQTT Integration

After restarting Mosquitto:
- Go to Settings → Devices & Services → MQTT
- Broker: core-mosquitto
- Port: 1883
- Username: mqtt_user (or relevant user)
- Password: matching value

## Validating the Broker

From the Raspberry Pi or any device with mosquitto-clients installed:
```bash
# Test subscribe
mosquitto_sub -h 192.168.1.218 -p 1883 -u mqtt_user -P YOUR_PASSWORD -t test/topic

# Test publish (separate terminal)
mosquitto_pub -h 192.168.1.218 -p 1883 -u mqtt_user -P YOUR_PASSWORD -t test/topic -m hello
```

## Future Considerations

- Separate MQTT users per device (e.g. one for TouchKio, one for future sensors)
- TLS/certificates for external MQTT access if ever needed outside LAN
