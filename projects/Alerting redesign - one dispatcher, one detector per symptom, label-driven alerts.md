---
type: project
status: active
priority: medium
system:
- '[[Home Assistant OS (VM)]]'
- '[[Home Health (HA dashboard + alerts)]]'
- '[[Uptime Kuma]]'
parent: '[[Homelab health monitoring with Home Assistant alerts (silent when nominal)]]'
next_step: '2026-10-14: all planned sources are on Alert2 except the HA update-approval flow (left native on purpose: an interactive workflow, not an alert) and leaks (native by decision). Kuma monitors are code (AutoKuma). Runbook written: ''Homelab alerting: add or change a monitor or alert''. Remaining: (a) ~10-21 after a quiet week, delete homelab_service_device_alerts, homelab_container_alerts_dockhand, homelab_container_restart_on_tap, battery_low_notify, battery_watch_stale_unavailable_digest, then mark this project Done; (b) first monthly prune from Alert2 fire counts mid-November. HDHomeRun forced test still open, no date.'
notion_id: 3f47ae76-22ba-81e0-a282-dfc43d44bf3b
---

# Alerting redesign: one dispatcher, one detector per symptom, label-driven alerts

Started as Claude's 2026-10-09 review of the HA error/notification system; Aaron approved Alert2 the same day. As of 2026-10-14 every planned source runs on Alert2 except leaks (native by decision) and the HA update-approval flow (native on purpose). Battery-low alerts are Alert2 per-device alerts (alert2.home_health_*_battery_low), verified firing for the Water Filter/Softener sensor 2026-10-17. What's left is the old-automation cleanup and the monthly prune (see Next Step).

## Why this exists

Aaron asked on 2026-10-09 for a step back from the arr-health fixes: evaluate the whole error-handling and notification setup and propose systematic changes that keep it expandable and sustainable. Trigger: the arr health work had just created a second poller for the same /health endpoints Kuma already watches, and the 10-07 findings showed about 32 pushes in 7 days from one flapping source.

## What exists today (verified live 2026-10-09)

Thirteen automations push to the phone, and every one calls `notify.mobile_app_aarons_iphone_17_pro` directly:

| Source | Automation | Detects |
| --- | --- | --- |
| Uptime Kuma (via HA integration) | `homelab_service_device_alerts` | 13 service/host monitors, 3 arr health JSON monitors, 3 push heartbeats, Kuma itself |
| UniFi integration | same automation | 7 network devices offline 5+ min |
| ha-dockhand | `homelab_container_alerts_dockhand` (+ restart-on-tap) | 8 containers not running or unhealthy, image updates |
| truenas-alert-relay (VM webhook) | `truenas_alert_relay` | TrueNAS's own alerts, stale snapshots, app updates |
| homelab-update (VM webhook) | `homelab_vm_update_reports` | weekly VM update results |
| HA updates | `ha_updates_*` (3) | Core/OS/app updates, approval flow |
| Home Health | leak notify + actions, `battery_low_notify`, stale digest | leaks, low batteries, silent sensors |
| Misc | `companion_app_updated_re_test_notification_buttons` | iOS button bug check |

Each automation re-implements the same plumbing on its own: the iOS interruption level as its severity, a `tag` so the recovery replaces the alert, a `for:` debounce, a "recovery only if it lasted long enough to have alerted" template, and a `logbook.log` call. The watched entities are hand-listed in trigger lists *and* in the `homelab_watch` label, and the automation description warns that both must be kept in sync.

## Problems, in order of how much they'll hurt as this grows

**One failure, several pushes.** The detectors overlap with no notion of cause. If Sonarr's container dies, Kuma's Sonarr monitor, Dockhand's container alert and (later) the Sonarr Health monitor can all fire. If Gluetun goes unhealthy, Dockhand alerts on Gluetun while Kuma alerts on Prowlarr and NZBGet, which share its network. The arr health work added a fourth path (HA's own `rest:` poll of the same endpoints Kuma polls). Big monitoring stacks solve this with inhibition, meaning a firing parent alert mutes its children ([Alertmanager docs](https://prometheus.io/docs/alerting/latest/alertmanager/)). We have one hand-made instance of it ("Kuma down" sends one alert instead of 16) and nothing general.
**Plumbing copied 13 times.** Severity mapping, tags, recovery rules, logbook and the target phone live in every automation. Changing phones, adding a second person (e.g. for leaks) or adding quiet hours means editing all thirteen, and each copy drifts. The 2026-09-29 `notify.send_message` breakage hit two automations separately for the same reason.
**Adding a monitor takes edits in several places.** A new Kuma monitor needs the label, the trigger list, sometimes the recovery list, and a Kuma reload. That's why the description carries a warning, and why it will eventually be missed.
**No alert lifecycle.** Nothing repeats an unhandled urgent alert, nothing can be acknowledged or snoozed (iOS action buttons are broken upstream anyway), and there's no maintenance switch, so planned work such as stack redeploys has to be absorbed by `for:` delays instead.
**No measurement.** The only way we found the 32-pushes week was a manual history read. There's no count of pushes per alert, so there's no signal for which alerts are being ignored.
**Single point of failure (known, accepted 2026-09-24).** Kuma, HA and the push path all run on Big Boi; if it goes down, nothing alerts. Aaron declined an off-box dead-man check. It's raised again only as an open question below.

## What others do

Google's SRE guidance is the usual reference: page on symptoms rather than causes, every page must be actionable and need judgement, and for every rule ask whether you'd ever ignore it as benign ([SRE book, Monitoring Distributed Systems](https://sre.google/sre-book/monitoring-distributed-systems/)). Prometheus Alertmanager is the common reference design for the notify side: routing by severity, grouping related alerts into one message, inhibition and silences ([Alertmanager](https://prometheus.io/docs/alerting/latest/alertmanager/)). AWS's guidance says the same about actionable alerts with a clear next step ([AWS Well-Architected OPS08-BP04](https://docs.aws.amazon.com/wellarchitected/2023-10-03/framework/ops_workload_observability_create_alerts.html)).
Inside Home Assistant there are two ready-made pieces. The built-in [`alert`](https://www.home-assistant.io/integrations/alert/)[ integration](https://www.home-assistant.io/integrations/alert/) adds repeat intervals (including escalating ones), acknowledge, `skip_first` and a done message, but it's YAML-only and watches a single entity, so anything richer needs a template binary sensor in front of it. [Alert2](https://github.com/redstone99/hass-alert2) (HACS) is the community's fuller answer: low/medium/high priority, `delay_on_secs` debounce, throttling of flapping alerts with a summary afterwards, snooze, ack, reminder schedules, per-alert notifier routing, generators that create one alert per matching entity, and a UI card to manage them. It's actively maintained (v1.22 released 2026-09-30) but small (88 stars, essentially one maintainer), which is a dependency risk. The common homelab dead-man pattern is a free external heartbeat service such as [Healthchecks.io](https://healthchecks.io/docs/) that alerts when pings stop.

## Proposal

The core idea is to separate the three jobs that are currently fused inside each automation: **detect** (Kuma, Dockhand, UniFi, the relays, HA sensors), **decide** (is this an alert, how severe, is a parent already firing) and **notify** (who, how loud, when, with what lifecycle).
**1. One notify script.** `script.homelab_notify` takes `severity`, `title`, `message`, `tag`, `url` and an optional `parent`. It alone knows the target device(s), maps severity to iOS interruption level, writes the logbook, counts pushes, applies quiet hours and a global maintenance switch, and implements inhibition (skip if the named parent alert is active). All thirteen automations call it instead of `notify.mobile_app_*`. This is the highest-value, lowest-risk change and is fully native. Severity is defined once:

| Level | Use | iOS level | Quiet hours |
| --- | --- | --- | --- |
| critical | water leak, anything that damages the house | critical | always delivered |
| urgent | service/host/container down past its debounce, failed update, TrueNAS ERROR+ | time-sensitive | delivered |
| info | recoveries, successful updates, available updates, TrueNAS WARNING | passive | held for the digest |
| digest | daily summary of info items and anything still open | passive | morning only |

**2. One detector per symptom, with explicit parents.** For each failure, decide which signal owns it and make the others its children. A suggested split: Kuma owns reachability (service down) and heartbeats; Dockhand owns container state only for containers Kuma can't see (Gluetun, its watchdog) and image updates; app health is owned by HA's `rest:` sensors, and Kuma's three JSON health monitors are deleted (this answers the duplication question from earlier today); Gluetun is the parent of Prowlarr and NZBGet; Kuma-unreachable is the parent of everything Kuma reports. Recovery-only-if-alerted moves into the shared logic.
**3. Label-driven membership.** An entity being monitored is decided by labels (`homelab_watch` already exists, plus a severity label or a small mapping), not by trigger lists. In native HA, the automations trigger on the label (purpose-specific triggers with label targets where they exist, otherwise a template binary sensor per alert family built from `label_entities()`). In Alert2, a generator over the label does the same. Adding a monitor becomes: add it in Kuma, add the label.
**4. Lifecycle.** Urgent alerts repeat (e.g. after 60 min, then every 4 h) until they clear or are acknowledged. Ack, snooze and maintenance mode live on the Home Health dashboard, since iOS action buttons are broken (home-assistant/iOS#5881). Claude can switch maintenance mode on around planned work such as stack redeploys and Big Boi reboots, and off again afterwards.
**5. Measure and prune.** The notify script increments a per-alert counter. A monthly look (could be a section of the digest) lists the noisiest alerts; anything that fired repeatedly without needing action gets a longer debounce, a lower severity or deletion. The working target is a handful of non-info pushes per week.

## Build or adopt (original analysis; decided 2026-10-09, see Decisions)

Phase 1 should be native whatever we decide later: the notify script, severity table, inhibition by parent and label-driven triggers need nothing new installed and fix the biggest problems (duplicate pushes, copied plumbing, multi-place edits). Ack, snooze and reminders are where native gets clumsy: the built-in `alert` integration does repeat/ack/done but is YAML-only and per-entity, while Alert2 does all of it plus throttling and a UI, at the cost of a single-maintainer HACS dependency in the alert path. Claude's recommendation is to build phase 1, run it for two to three weeks, and then decide between built-in `alert` and Alert2 for the lifecycle features with real push counts in hand.

## Phases (original; superseded by Revised plan)

1. Phase 1 (Tier 2, each automation saved before editing): create `script.homelab_notify` and the maintenance/quiet-hours helpers; move the thirteen automations onto it one source at a time; add per-alert counters.
2. Phase 2: set detector ownership and parents; delete the three Kuma JSON health monitors (Aaron, in Kuma) and point the arr alert at the HA `rest:` sensors; replace hand-listed triggers with label-driven ones.
3. Phase 3: morning digest; lifecycle (repeat, ack, snooze) via built-in `alert` or Alert2, decided from phase 1 data; dashboard controls.
4. Ongoing: monthly prune from the counters; update KB Standards or a runbook so new monitors follow the pattern.

## Decisions

- **2026-10-09 (Aaron): quiet hours 20:00–09:00.** Alerts that arrive in that window are held and delivered at 09:00. Nothing on the homelab side is life or death, so homelab alerts never use the iOS critical level. **Exception (Aaron, 2026-10-09): water leak alerts** are sent immediately at any hour at the iOS critical level.
- **2026-10-09 (Aaron): leak alerts go to Aaron only.** No second recipient.
- **2026-10-09 (Aaron): off-box dead-man check deferred** to a later project (not a priority now).
- **2026-10-09 (Claude, delegated by Aaron): adopt Alert2** for homelab alerts instead of building the lifecycle natively. Its docs (README, v1.22) cover most of the proposal out of the box: `priority`, `delay_on_secs` debounce, `throttle_fires_per_mins` with a summary afterwards (flapping), snooze, ack, `reminder_frequency_mins`, `supersedes` (parent/child inhibition), generators over entity lists (label-driven alerts), `done_message`, per-alert `data` for the iOS payload, and `alert2_*` events plus `alert2.ack`/`notification_control` actions for automations. Building the same natively would mean a hand-written alert manager in Jinja and helpers (a queue, per-alert ack/snooze state, repeat timers, inhibition logic) that Claude would have to maintain, which is more custom code than one integration. Gaps and mitigations: Alert2 has no deferred delivery, so quiet hours are a notifier template that suppresses pushes 20:00–09:00 plus a 09:00 morning report of everything still firing and what fired overnight; it has no "recovery only if alerted" option, which `delay_on_secs` largely makes moot; and it's a single-maintainer dependency, so alerts are defined in YAML (`alert2:` key, tracked in the repo, editable with ha-mcp) rather than UI storage, a small native watchdog pushes directly if the integration stops loading, and **water leak alerts stay native**, so the critical path never depends on a third-party integration.

## Revised plan (2026-10-09, supersedes the Phases below)

1. Install Alert2 and its UI card from HACS; HA restart (Tier 2). Add the native watchdog.
2. Pilot on the noisiest source: rebuild `homelab_service_device_alerts` as Alert2 alerts generated from the `homelab_watch` label, with `supersedes` (Kuma unreachable over everything, service down over app health, Gluetun over Prowlarr/NZBGet), quiet-hours notifier and the 09:00 report. Arr app health uses the HA `rest:` sensors; Aaron deletes Kuma's three JSON health monitors. Run old and new side by side for a few days with the old one logbook-only, then remove the old automation.
3. Migrate the other sources one at a time: Dockhand containers, UniFi, TrueNAS relay, homelab-update, HA updates, battery and stale-sensor alerts. Leak alerts stay native and critical.
4. Dashboard: Alert2 overview card on Home Health for ack/snooze (works without the broken iOS action buttons).
5. Write the pattern into a runbook (how to add a monitor: create it, label it, done) and prune monthly from Alert2's fire counts.

## Open questions for Aaron (original, answered above except 3)

1. Quiet hours: what window, and should urgent (not critical) alerts wait for morning or still come through at night?
2. Should anyone else get critical alerts (leaks) as a second recipient?
3. Is a single-maintainer HACS integration acceptable in the alert path, or native only?
4. The 2026-09-24 decision declined an off-box dead-man check. It's now the remaining blind spot (Big Boi down = silence). A free [Healthchecks.io](http://healthchecks.io/) check pinged by HA every few minutes would cover it with no new hosts. Still no?

## Sub-items

![[Projects.base#Sub-items]]

## Changes

![[Changes.base#For this project]]
