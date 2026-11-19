---
date: 2026-11-19
type: fix
system:
- '[[Home Assistant (integrations and automations)]]'
- '[[TrueNAS SCALE (Big Boi)]]'
- '[[ClaudeCode (VM)]]'
commit: https://github.com/aaronspriggs/spriggs-homelab/commit/b2126fa09a3eb4cfe0aa87f58c0e881c84ebe2cc
---

# Made the TrueNAS relay and Alert2 exception pushes readable

Aaron sent screenshots of two ugly pushes from the 2026-11-19 power blip (about 21:10–21:16 UTC): "🔴 TrueNAS / U P S On Battery: UPS unifiups is on battery power. UPS Statistics: 'unifiups' Statistics recovered: 1) Battery charge (percent) &nbsp;&nbsp;&nbsp; battery.charge: 99 2)…" and the Alert2 global exception "An HA task (possibly unrelated to Alert2) died to due to an unhandled exception: &lt;class 'denonavr.exceptions.AvrNetworkError'&gt;…". Both came from the same blip: the UPS went on battery, the Denon receiver at 192.168.1.155 dropped off the network (unavailable 21:13:42, back 21:16:31), and the UPS was back on line power at 21:15:18 with 70% charge and 3857 s runtime left.

## Causes

- **TrueNAS push.** TrueNAS's `formatted` alert text is HTML (`<br>`, `&nbsp;`). The relay's `clean()` stripped tags but never decoded entities; `humanize()` split every capital, so `UPSOnBattery` became "U P S On Battery"; UPS alerts append every NUT statistic; and `automation.truenas_alert_relay` prefixed the message with the title, which repeated TrueNAS's own first sentence.
- **Alert2 push.** Alert2's `util.report()` HTML-escapes every message it reports itself (`<` → `&lt;`), and the global_exception text is fixed in its code. Tracked alerts take no `message` template (checked in `custom_components/alert2/config.py`, `SINGLE_TRACKED_SCHEMA`), so the escaping can't be undone from config. The exception itself is denonavr leaving an unretrieved task exception whenever the receiver is unreachable: 78 in HA's system log since 2026-11-12.

## Changes

- Relay ([`truenas/truenas-alert-relay`](https://github.com/aaronspriggs/spriggs-homelab/blob/main/truenas/truenas-alert-relay)): `clean()` strips tags, then `html.unescape`s, then collapses whitespace (that order keeps an escaped `&lt;` in alert text); `humanize()` keeps acronyms whole ("UPS On Battery", "SMART Test Failed"); new `push_message()` sends TrueNAS's first line only, plus "Battery N%, about M min left." when the alert carries `battery.charge`/`battery.runtime`. Tested against the captured UPS text and a live `--dry-run`; installed to `~/.local/bin`, `make check` clean. State is keyed by alert UUID, so nothing re-posted.
- `automation.truenas_alert_relay` (Tier 2, homelab alerting): the `alert2.report` message changed from `{{ repeat.item.title }}: {{ repeat.item.message }}` to `{{ repeat.item.message }}`. To roll back, set it back to the former. The logbook line keeps the title.
- Alert2 ([`ha/alert2.yaml`](https://github.com/aaronspriggs/spriggs-homelab/blob/main/ha/alert2.yaml)): `global_exception` also ignores `AvrNetworkError`. HA already shows the receiver unavailable, so the push said nothing new. Applied with `ha_config_set_yaml` (the diff also brought live comments up to the repo: quiet hours 22:00, garage-door report note), `alert2.reload`; no new `alert2_error`, open alerts unchanged (7, none with reminders).

The UPS push now reads "🔴 TrueNAS / UPS unifiups is on battery power. Battery 99%, about 64 min left."

## Rejected

- Patching Alert2's `report()` to stop escaping: HACS-managed code, overwritten on update, outside the repo.
- Routing global_exception through a native automation that unescapes and re-words it: would duplicate quiet hours, throttling and Snooze for a rare alert. Other global exceptions will still show `&lt;`/`&gt;`; an upstream issue on hass-alert2 (an option not to escape for notifiers) is the real fix, not filed.
- A per-alert title such as "🔴 UPS is on battery": Alert2 tracked titles can't see the reported message, so the title stays "🔴 TrueNAS" and the message carries the subject.
