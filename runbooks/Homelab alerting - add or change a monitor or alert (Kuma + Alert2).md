---
kind: procedure
status: active
system:
- '[[Uptime Kuma]]'
- '[[Home Assistant OS (VM)]]'
last_tested: 2026-10-17
repo: https://github.com/aaronspriggs/spriggs-homelab/blob/main/ha/alert2.yaml
notion_id: 3f97ae76-22ba-81fe-aa1a-f5b8cf87357b
---

# Homelab alerting: add or change a monitor or alert (Kuma + Alert2)

How a new service, host, heartbeat, container or event source gets monitored and alerted, end to end: AutoKuma monitor file, HA label, Alert2 generator/alert in repo ha/alert2.yaml, apply and verify. Claude does all of it; nothing in the Kuma UI.

## How it fits together

Detect → decide → notify. **Detectors:** Uptime Kuma (reachability and push heartbeats; monitors are repo files applied by AutoKuma), ha-dockhand (container state, health, image updates), UniFi, HA `rest:` sensors (arr health), Battery Notes/ZHA/Hue (batteries), and two webhook receivers (TrueNAS relay, homelab-update) that call `alert2.report`. **Decide and notify:** Alert2, config in repo [`ha/alert2.yaml`](https://github.com/aaronspriggs/spriggs-homelab/blob/main/ha/alert2.yaml) (`alert2:` key in HA's configuration.yaml). Quiet hours 20:00–09:00 (notifier renders `[]`), 09:00 overnight report (`automation.homelab_alerts_09_00_report`), Sunday 09:00 weekly report (`automation.homelab_alerts_weekly_report_sunday_09_00`), native watchdog. Leak alerts and the HA update-approval flow are native on purpose.
Priorities: **high** = monitoring itself is blind (Kuma unreachable); **medium** = something is down or failing and needs action (time-sensitive push); **low** = needs attention eventually (batteries, updates; active/passive push, no reminders, listed in the Sunday weekly report).

## Add a service or host to Kuma

1. Add `stacks/uptime-kuma/monitors/<id>.toml` in the repo (copy a similar one). State every field: unset fields get AutoKuma defaults, not the old values. The file name is the permanent ID; never rename it (a rename recreates the monitor with a new Kuma ID and new HA entities).
2. `stacks/uptime-kuma/render`, commit, push, deploy with the `forceRecreate: false` command in repo `stacks/README.md`. Check AutoKuma's log (Dockhand) for "Creating" and `kuma-api monitor list`.
3. Reload the Uptime Kuma integration in HA, then add label `homelab_watch` to the new `sensor.<name>_status`.
4. `alert2.reload`: the `homelab_service_down` generator picks it up as `alert2.homelab_<name>_down`. Nothing else to edit.

## Add a push heartbeat (a job that checks in)

As above with `type = "push"` (no `push_token` in the file; after the first deploy read the token with `kuma-api` only to put it into the client's untracked config on its host). Then in `ha/alert2.yaml` add a line to the `homelab_heartbeat_missed` generator and the entity to the `homelab_service_down` exclusion list, apply, `alert2.reload`.

## Add a container

Nothing to do for health checks and image updates: the `homelab_container_unhealthy` and `homelab_container_update` generators match every `big_boi_containers_*` entity. If Kuma can't reach it (no web port), add it to the `homelab_container_down` generator list. If other services depend on it, give it its own alert with `supersedes` (see `gluetun_down`).

## Add an event source (webhook, script)

Declare the alert under `tracked:` in `ha/alert2.yaml` (domain `homelab`, priority, title, `data.push.interruption-level` for low ones) and have the receiver call `alert2.report` with `domain`, `name`, `message`. Example: `automation.homelab_vm_update_reports`.

## Apply and verify

1. Edit `ha/alert2.yaml` in the repo first. Apply with ha-mcp `ha_config_set_yaml` (`alert2`, replace; content = the file from `defaults:` on), check the diff preview, confirm, then `alert2.reload`. No restart.
2. Check: the new `alert2.*` entities exist, `alert2.alert2_error` didn't fire, generator sensors (`sensor.alert2generator_*`) count what you expect. Templates can be tested first with ha-mcp `ha_eval_template`.
3. Commit (`ha: …`), push, log in Changes.

## Push rules (Aaron, 2026-10-14)

The goal is that most pushes need nothing from Aaron. Every push is one of:
- **FYI** (VM updated, TrueNAS warning/info/update notices, recoveries "✅ …", confirmations, Alert2 summaries): no buttons, passive, tap opens the dashboard.
- **Approval** (HA update, container image update): **Install** only. Ignored = stays pending, listed in the Sunday report.
- **Problem** (condition alerts: service/container down or unhealthy, heartbeat missed, UniFi offline, arr health, Kuma unreachable, battery low, device offline): the fix button if there is one (Restart, and/or **Fix with Claude** where a fix runbook exists), then **Ack** and **Snooze (2hr)**. Ignored: medium/high remind every 4 h (daytime); low (battery, device offline) push once and wait for Sunday.
- **One-off problem** (event alerts that need a look: TrueNAS ERROR+, VM update failed, Alert2 global exception): **Snooze (2hr)** only.
- **Critical** (water leak, native): Shut Off Water / Dismiss, any hour.
**Wording (Aaron, 2026-10-17, "medium").** The original pushes were too wordy and a fragment-only pass was too terse; this is the middle. Title = emoji + "<subject> is <state>" ("🖥️ NZBGet is down", "⚠️ Sonarr reports an error"), no "Homelab:" prefix. Message = one plain sentence with what the title doesn't say, cause, duration or side effect, without repeating the title ("Uptime Kuma can't reach it (4+ min).", "Health check failing for 5+ min, so Prowlarr and NZBGet have no VPN."). Recovery = "✅ <subject> is <state> again." Reminders use the defaults `reminder_message` "Still on after <time>: <message>" (Alert2's built-in is "<name>: on for <time>"). **Action line (Aaron, 2026-10-17):** a push with a button that does something (Restart, Fix with Claude, Install, Update all; not Ack/Snooze/Open dashboard) carries an iOS `subtitle` "👆 Tap to <button> or <button>" ("👆 Tap to Restart servarr stack or Fix with Claude"), so Aaron can tell from the banner what needs him. No subtitle = nothing to act on. Build it from the same list as the buttons so they can't drift: `fix` = the action buttons, then `{{ dict(d, subtitle='👆 Tap to ' ~ fix | map(attribute='title') | join(' or ')) if fix else d }}` (Alert2 data templates and the Snooze re-push do this; static pushes set the subtitle literally). Handler confirmations are one sentence ("I'll remind you at 9:53 PM if it's still open."). Claude fix-run results carry one sentence for FIXED. Apply this to every new alert, handler push and report line.
**One cause, one alert.** When an alert's cause is another monitored thing, suppress the dependent alert rather than pushing both: with `supersedes` when both fire at about the same time (`gluetun_down`), or with a condition on the upstream sensor when the dependent alert has a long delay (arr health skips while `sensor.nzbget_status` is down or Gluetun is down/unhealthy, since 2026-10-17; the 30-min delay restarts on recovery, so the arrs' download-client retry backoff clears first). The upstream alert carries the fix button.
**Ack** = "I know, I'll get to it": no more pushes; it stays on the dashboard and in the Sunday report until fixed. **Snooze (2hr)** = re-push in 2 h if still broken (moved to 09:00 if that lands in quiet hours); built in the handler because Alert2's own snooze only mutes and never re-notifies. An HA restart during the 2 h drops that reminder; the Sunday report still lists the problem.
**Reports:** 09:00 daily = only what happened overnight (still open / happened and cleared) plus an Install push per update found overnight. Sunday 09:00 weekly = everything still open (acked or not), low batteries, offline devices, pending updates; an all-clear push if nothing. When container updates are pending it carries **Update all containers (N)** (`automation.homelab_container_update_all_on_approval`: installs each pending container update in turn, Gluetun excluded, then reports what updated). HA Core/OS/app updates are listed but keep their own Install push.

## Maintenance mode (since 2026-10-14)

`input_boolean.homelab_maintenance_mode` mutes Alert2 pushes for domain `homelab` (the defaults `notifier` renders `[]`); batteries/offline devices and the native leak alert still push. Turning it on starts `timer.homelab_maintenance_mode` (2 h, survives restarts) and sends a passive "🔧 Maintenance mode on"; it switches itself off when the timer ends. Turning it off pushes "🔧 Maintenance over": homelab alerts that started during maintenance and are still open (time-sensitive) or all clear (passive). Logic: `automation.homelab_maintenance_mode`. Toggle: wrench button on the Home Health dashboard's Homelab heading (an amber banner shows while it's on; tap it to end).
**Claude:** turn it on before planned disruptive work (stack deploys/redeploys, container restarts, Kuma or Dockhand changes, Big Boi reboots) with `input_boolean.turn_on`; for work longer than 2 h follow with `timer.start` and a `duration`. Turn it off when done and read the summary push. Leave it off for anything Aaron didn't plan, since it hides real outages.

## Buttons on alerts (how they're built)

Alert2 firing pushes and reminders get **Ack**, **Snooze (2hr)** and **Open dashboard** from the defaults `data` template (handler `automation.homelab_alert_ack_snooze_on_tap`); event alerts override `actions` in their `tracked:` entry (`[]` for FYI, Snooze only for one-off problems). Container alerts add their own: Restart (`automation.homelab_container_restart_on_approval`), Install (`automation.homelab_container_update_on_approval`). Kuma `*_down` alerts get Restart too when `button.big_boi_containers_<name>_restart` exists (sonarr, radarr, prowlarr, nzbget, seerr; since 2026-10-17); `action_data.button` is set only then, because the Snooze re-push adds Restart whenever it's present. **Fix with Claude** (`CLAUDE_FIX`, since 2026-10-16) is on the arr health alerts and `gluetun_unhealthy`: its `action_data` carries `alert` and `fix_id`; `automation.homelab_claude_fix_run_on_tap` calls `rest_command.claude_fix` (repo `ha/rest-command.yaml`) while the alert is still firing, which starts a capped Claude fix run on the ClaudeCode VM, and `automation.homelab_claude_fix_run_result` pushes the outcome (direct push, not Alert2, so quiet hours don't hold it). To give another alert the button: write its fix runbook, add an entry with its `fix_id` to repo `claudecode-vm/claude-fix-runbooks.json` (see that README's "Fix runs"), then add `CLAUDE_FIX` and `fix_id` to the alert's `data` as the arr health generator does. Rules that every actionable push follows (Alert2 or native):
- Aaron sees buttons by **tapping** the push (Companion setting "show actions when tapped"); long-press is broken upstream (home-assistant/iOS#5881).
- **No ****`url`**** or ****`entity_id`** on a push with buttons: either makes the tap open a page and the sheet never shows. In Alert2 set `url: ""` to blank the default.
- **No ****`authenticationRequired`**: the sheet hides Face ID-gated buttons.
- A list of buttons can't be a per-field Alert2 data template (it renders as a string). Use a whole-`data` template that returns a dict, as the defaults and the restart alerts do. `alert_entity_id`, `alert_domain`, `notify_reason` and generator variables are available in it.
- Alerts override the defaults `data` one top-level key at a time; an alert that sets `actions` replaces the Ack/Snooze buttons, so include them if you still want them.
- Handlers must re-check state before acting (still firing / still pending), so stale taps do nothing.
- `alert2.notification_control` `snooze_until` needs a timezone (`now().isoformat()`), despite its docs. A naive time raises an `alert2_error`. (Not used by Snooze (2hr) any more, which acks, waits and unacks + re-pushes.)
- An FYI event alert must set its own non-empty `url` and `actions: []`, otherwise it inherits the problem buttons and the blank url from the defaults.

## Gotchas

- Kuma 2.5.6: a tag created after Kuma starts breaks `/metrics` for tagged monitors until Kuma restarts (HA entities go unavailable). Don't use Kuma tags; restart Kuma if one is ever created.
- Dockhand's compose PUT recreates every container unless `forceRecreate: false`.
- After any Kuma restart, weekly push monitors read `unavailable` in HA until their next push. Alert2 conditions ignore `unavailable`.
- Event alerts are fired only by `alert2.report` or a `trigger`; undeclared names raise an `alert2_error`.
- `alert2.reload` re-arms reminders, so any alert that is on and has reminders gets re-pushed at once. Check `states.alert2` for open alerts before reloading during the day.
- Monthly: look at Alert2 fire counts and lengthen delays, lower priority or delete alerts that fired without needing action.
