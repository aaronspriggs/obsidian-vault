---
date: 2026-10-14
type: config
system:
- '[[Home Assistant OS (VM)]]'
project:
- '[[One-tap approval notifications (updates and similar)]]'
commit: https://github.com/aaronspriggs/spriggs-homelab/commit/4093232
notion_id: 3f97ae76-22ba-81dd-9f8a-ca36504ea1f3
---

# One-tap Restart on container down/unhealthy alerts; found a url hides the iOS button sheet

Restart button (CONTAINER_RESTART) on Alert2 container down/unhealthy alerts, handler automation.homelab_container_restart_on_approval. Live test passed. Any push with buttons must have no url (empty string): a url makes the tap just open the app.

**Restart button** ([cc26769](https://github.com/aaronspriggs/spriggs-homelab/commit/cc26769), [4093232](https://github.com/aaronspriggs/spriggs-homelab/commit/4093232)): `gluetun_down`, `gluetun_unhealthy` (button: **Restart servarr stack**, `button.big_boi_stacks_servarr_restart`), `homelab_container_down` and `homelab_container_unhealthy` (container restart button) now carry a `CONTAINER_RESTART` action. Their `data` is one whole template so the button only appears on Fire/reminder pushes, not on the recovery push (Alert2 renders per-field data templates as strings but parses a whole-data template into a dict).
New `automation.homelab_container_restart_on_approval`: condition is a Dockhand restart button and the alert in `action_data` still `on`; pushes "🔄 Restarting", presses the button, waits up to 5 min for the alert to clear, pushes ⚠️ only if it hasn't.
**Live test (Aaron approved):** stopped `gluetun-watchdog` via `switch.big_boi_containers_gluetun_watchdog` at 15:08; Alert2 fired at 15:13. Tapping the real push only opened the app. Side-by-side tests: push with `url` = app opens, no buttons; same push without url = Restart sheet; `url: ""` = Restart sheet. Restart tapped at 15:14:44, container running and alert cleared at 15:14:45.
**Fix:** Alert2 defaults give every alert `url: /home-health/overview#homelab-all`, so pushes with buttons now set `url: ""` (restart alerts and the container-update Install alert, which was affected too). Removed `url: /config/updates` from `automation.ha_updates_ask_for_approval` for the same reason; its message now says "Tap, then Install".
