---
date: 2026-10-30
type: config
system:
- '[[Home Assistant OS (VM)]]'
commit: https://github.com/aaronspriggs/spriggs-homelab/commit/c94aa2a
---

# Container update alerts offer Install only when ha-dockhand can install

ha-dockhand 1.11 turns a container's update entity on without Install for updates HA can't apply, so the Alert2 Install alert now requires Install support and a new button-less alert covers tag and pin changes.

## What changed

In `ha/alert2.yaml` ([c94aa2a](https://github.com/aaronspriggs/spriggs-homelab/commit/c94aa2a)), applied with ha-mcp `ha_config_set_yaml` and `alert2.reload`: the `homelab_container_update` generator's condition now also requires `supported_features` to include Install (odd), and a new generator `homelab_container_update_advisory` (alerts `alert2.homelab_<container>_update_advisory`, passive push, no button) fires when an update entity is on without Install and not held: a newer version tag than the stack pins, or a digest-pinned image whose tag moved. Its message names the new tag (or the stale pin) and says to ask Claude to change the stack. Updates Dockhand holds for minimum image age (`update_held_hours` set) get no alert; they become installable after Dockhand's next check and then alert with Install. The [Homelab alerting](<../runbooks/Homelab alerting - add or change a monitor or alert (Kuma + Alert2).md>) runbook describes both generators.

## Why

Found while updating ha-dockhand to v1.11.1 the same day ([upstream logic](https://github.com/raetha/ha-dockhand/blob/v1.11.1/custom_components/dockhand/update.py): `_advisory_only()` withholds `UpdateEntityFeature.INSTALL` for those cases). Without this, those updates would have pushed an Install button that does nothing: `automation.homelab_container_update_on_approval` already stops at its Install-support condition. Aaron asked to make sure it works right.

## Notes

The 09:00 report and `automation.homelab_container_update_all_on_approval` already only count installable updates (same `supported_features` check), so they needed no change; advisory alerts appear in the 09:00 overnight list like any other alert. Verified: the routing logic rendered correctly for four simulated cases (normal update → Install alert; newer tag → advisory; moved pin → advisory with the pin message; held → neither); after the reload all 8 advisory alerts exist and are off, the existing update alerts are unchanged, and `alert2_error` did not fire. A real advisory case hasn't occurred yet. Dockhand is 1.0.53, so the moved-pin case (needs 1.0.54+) can't occur until it's updated.
