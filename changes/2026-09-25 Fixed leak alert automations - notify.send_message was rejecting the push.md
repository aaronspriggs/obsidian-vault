---
date: 2026-09-25
type: fix
system:
- '[[Home Assistant OS (VM)]]'
notion_id: 3e67ae76-22ba-810f-83ae-ec9b1c3fa02c
---

# Fixed leak alert automations: notify.send_message was rejecting the push options, so alerts would never have been sent

**Found while building the homelab monitoring alerts.** `automation.water_leak_detected_notify`, `automation.water_leak_notification_handle_actions` and `automation.battery_low_notify` all sent via `notify.send_message` (target `notify.aarons_iphone_17_pro`) with a companion-app `data:` payload: critical interruption level, tag, and the Shut Off Water / Dismiss buttons.
**Verified live 2026-09-25:** `notify.send_message` **with** a `data` payload returns **HTTP 400 Bad Request** and sends nothing. The same call **without** `data` succeeds. The legacy `notify.mobile_app_aarons_iphone_17_pro` action **accepts** the `data` payload. This matches a known upstream limitation: mobile-app notify entities (added in 2026.5) only support title and message, and advanced companion options still need the legacy action ([https://github.com/orgs/home-assistant/discussions/3684](https://github.com/orgs/home-assistant/discussions/3684), open with no fix as of Sept 2026).
**Impact:** a real leak would have triggered the automation, but the notify step would have failed validation. **No leak alert would have reached Aaron's phone.** Neither automation had ever run (0 traces), so this was never caught. The valve-close action in the button handler came before the confirmation, so the shutoff itself would have worked; only the confirmation back to the phone would have failed.
**Fix:** switched both leak automations to `notify.mobile_app_aarons_iphone_17_pro`, with the payload otherwise unchanged. Test pushes sent to Aaron's phone: the plain send_message one (OK) and the mobile_app one with data (OK).
**Not changed:** `automation.battery_low_notify` has the same notify bug on top of its existing trigger bug. Aaron asked to hold the battery fix, so both get fixed together later; this is noted on its Projects task.
**Still to do:** a real end-to-end leak test, e.g. dampen a sensor with Aaron present. It sends a *critical* alert that breaks through silent mode, so it needs him there. **Convention going forward:** use `notify.mobile_app_*` whenever phone-specific options are needed.
