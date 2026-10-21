---
date: 2026-09-04
type: config
system:
- '[[Home Assistant OS (VM)]]'
notion_id: 3d17ae76-22ba-810c-8a4c-fd13b832b634
---

# Built water leak notification automations; documented existing Flo shutoff integration

Built the first piece of the "Build out water leak sensor automations" project (Projects DB, still Active — several scope items remain).
Created a `leak_sensor` label and applied it to all 4 currently-paired Zigbee leak sensors (Dishwasher, Kitchen Sink, Utility Room, Water Filter/Softener — more sensors than the project page had tracked; it previously said only one Aeotec sensor was paired).
Built two automations via the ha-mcp config API:
- `automation.water_leak_detected_notify` — purpose-specific `moisture.detected` trigger targeting the `leak_sensor` label (mode: parallel, so simultaneous sensors don't block each other). Sends a critical, actionable push notification to `notify.aarons_iphone_17_pro` naming the specific wet sensor. Tapping the notification body opens that sensor's more-info card (via `data.entity_id`); tag is per-sensor so repeat alerts replace rather than stack.
- `automation.water_leak_notification_handle_actions` — listens for `mobile_app_notification_action` events from the two buttons on that notification: "Shut Off Water" (marked `destructive`+`authenticationRequired` so it needs Face ID/passcode, closes `switch.shutoff_valve`, confirms back to the phone) and "Dismiss" (log only). Both write a logbook entry for an audit trail.
While scoping entity targets, discovered a whole-home Flo by Moen shutoff valve already integrated into HA (`switch.shutoff_valve` and several water-flow/pressure/usage sensors) that wasn't documented anywhere in the KB. Added a new "Water Leak Detection & Shutoff" section to the Home Assistant OS (VM) System page covering both the leak sensors and the Flo integration.
Key decision, made with Aaron: **notify-only, no auto-shutoff.** The Flo valve is closed only via an explicit tap on the notification button, never automatically on a wet sensor — avoids a false positive cutting water to the whole house. Documented as an explicitly-resolved open question on the Project page, revisitable later.
Also surfaced in passing: the Water Filter/Softener sensor (`binary_sensor.samjin_water`) is at 3.5% battery — logged as a new Known Gap on the System page, needs a physical battery swap.
Remaining scope (Project page updated with a checklist): pair the Sonoff SNZB-05P, descriptive entity renames, a "hasn't reported in N hours" staleness watchdog, a battery-low watchdog, sensor placement decisions, and a standalone non-networked backup alarm as belt-and-suspenders redundancy.
