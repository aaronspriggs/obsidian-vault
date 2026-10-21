---
kind: recovery
status: deprecated
system:
- '[[Home Assistant OS (VM)]]'
notion_id: 2ff7ae76-22ba-813a-9f08-fe73a4bf348c
---

**Deprecated 2026-09-28:** a generic stub that was never filled in or tested (KB governance decision 3). For restores, see the [Google Drive backup runbook](<Set up native Google Drive backup integration for Home Assistant (retire the add-on).md>) and the [Home Assistant OS (VM)](<../systems/Home Assistant OS (VM).md>) page.

## Preconditions

- Home Assistant OS VM exists and is assigned a static IP.
- TrueNAS SCALE host is reachable.

## Procedure

1. Access TrueNAS SCALE UI and locate the Home Assistant VM.
2. Restart the Home Assistant VM.

## Verification

- Confirm Home Assistant web UI loads.
- Verify key integrations are online.

## Failure Modes & Recovery

- If UI fails to load, check VM console and network configuration.
