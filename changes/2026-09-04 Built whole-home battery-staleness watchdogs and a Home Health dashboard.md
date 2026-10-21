---
date: 2026-09-04
type: config
system:
- '[[Home Assistant OS (VM)]]'
notion_id: 3d17ae76-22ba-81cc-a9ce-f0bcae4a0d7c
---

# Built whole-home battery/staleness watchdogs and a Home Health dashboard

Extended the water-leak automation work into general whole-home health monitoring, at Aaron's request (chose "whole-home" over "leak sensors only" when offered the choice).
Created label `battery_watch` and applied it to 24 physical battery-powered entities: door/window multipurpose sensors, IKEA motion sensors, dimmer/switch batteries, the basement freezer temp sensor, and all 4 water leak sensors (which now carry both `leak_sensor` and `battery_watch`). Deliberately excluded personal electronics that are already monitored elsewhere — phone, Apple Watch, Sonos Roam, Rivian.
Built two automations via the ha-mcp config API:
- `automation.battery_low_notify` — `battery.became_low` purpose-specific trigger targeting the `battery_watch` label (mode: parallel). Sends an active-priority push naming the specific device.
- `automation.battery_watch_stale_unavailable_digest` — daily 9am check. No native trigger covers "hasn't reported in N hours" across a dynamic label, so this uses a `variables:` template iterating `label_entities('battery_watch')`, flagging anything `unavailable`/`unknown` or with no state update in 48+ hours, and sends one consolidated push only if something's actually wrong (avoids per-entity notification spam). Verified the template renders correctly via `ha_eval_template` before relying on the 9am schedule — it immediately caught a real fault: Living Room Fan Dimmer Battery is already unavailable.
Built a new "Home Health" dashboard (storage-mode, `home-health` url_path, shown in sidebar) at `/home-health/overview` with four sections: Water Leak & Shutoff (sensors + Flo valve/flow/pressure), Battery Levels (all 24 tracked devices), Sensor Health (live templated list of anything stale/unavailable), and HA System (pending updates count, shortcut buttons to Repairs/Updates). Dashboard screenshot verification wasn't possible — the ha-mcp "dashboard screenshot" beta feature is disabled on this instance — so the layout is unverified visually; Aaron should eyeball it in-browser.
Corrected a documentation bug in the process: an earlier `update_content` (diff-style) edit on the water-leak Project page had written literal backslash-n text instead of real line breaks, garbling the page's headers/checkboxes. Fixed by rewriting the page with `replace_content` instead — worth knowing `content_updates` diff edits are the riskier path for multi-paragraph content on this Notion setup.
See the Home Assistant OS (VM) System page's new "Home Health Monitoring & Dashboard" section and the water-leak Project page's updated Scope checklist for full detail.
