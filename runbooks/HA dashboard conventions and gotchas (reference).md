---
kind: reference
status: active
system:
- '[[Home Assistant OS (VM)]]'
- '[[Home Health (HA dashboard + alerts)]]'
notion_id: 3ea7ae76-22ba-8138-bbc1-f4a8be300a8a
---

Rules and hard-won gotchas for building HA dashboards (sections view, Mushroom, card_mod, auto-entities). Read before editing any dashboard.

## When to use

Before building or editing any Home Assistant dashboard, by hand or through ha-mcp. This is a reference, not a procedure. Learned while building [Home Health (HA dashboard + alerts)](<../systems/Home Health (HA dashboard + alerts).md>), 2026-09-04 to 2026-09-05. Moved here from the Home Assistant OS page 2026-09-29.

## Design rules

- **Quiet when clean.** Keep a compact signal always visible; show detail only when something needs attention. Gate detail cards with `visibility` conditions. Native visibility needs a real entity, so back each check with a template helper (a count sensor), not inline Jinja.
- **Single-source thresholds.** Put thresholds in template helpers (e.g. `sensor.battery_critical_count`) and have every card reference the helper. Don't repeat the threshold logic per card.
- **Drive membership with labels** (`battery_watch`, `leak_sensor`, `signal_watch`), so adding a device means adding a label, not editing cards.
- **Proportional "N devices across buckets" data:** native `distribution` card (HA 2026.2+). **Binary health checks:** a visibility-gated card that's silent when clean.
- **Styled dynamic entity lists:** `custom:auto-entities` + `custom:card-mod`.

## Gotchas

- **Sections view is a Z-grid, not masonry.** Sections fill left to right in config order; each row is as tall as its tallest section, with no backfill. Give a tall section a `column_span` equal to `max_columns` so it takes its own row, and group sections of similar height.
- **Avoid custom-card grids** (button-card, mushroom stat tiles) in sections views: width won't stretch, aspect ratio ignores the container, icon badges deform.
- **No raw HTML styling in ****`markdown`**** cards:** HA strips `style=""` attributes regardless of escaping. Use card_mod instead.
- **Styling one mushroom chip with card_mod:** target `mushroom-template-chip$` (not `mushroom-chip`); select by position with `:host(:nth-of-type(N))`. Borders render reliably; a background fill set there is hidden by a nested, separately shadow-rooted `<mushroom-chip>`. Don't retry background fills without inspecting the live DOM.
- **ZHA LQI/RSSI sensors exist but are disabled by default.** Enable the per-device diagnostic entities; enabling them needs an HA Core restart (ask Aaron first).
- **Bubble Card pop-ups** open via `tap_action: navigate` to a hash (e.g. `#battery-low`).

## Verify

There's no automated screenshot check: the Puppet add-on that ha-mcp needs for screenshots was declined (unauthenticated listener on a flat LAN). Describe the change and have Aaron look at the rendered page, including at phone and wall-panel width.

## Rollback

Dashboards are in HA storage mode. Before a large edit, fetch the dashboard config through ha-mcp and keep the copy in the scratchpad; restore by writing it back.
