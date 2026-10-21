---
date: 2026-09-25
type: install
system:
- '[[Plex Media Server]]'
- '[[ClaudeCode (VM)]]'
- '[[Home Assistant OS (VM)]]'
notion_id: 3e67ae76-22ba-8113-90db-c35c29b2c473
---

# Installed homelab-update weekly auto-update service on Plex VM and ClaudeCode VM, with HA reports and Kuma heartbeats

Reusable `homelab-update` service (full source and add-a-VM steps: runbook "homelab-update: weekly unattended VM updates"). Installed by Aaron as root on the **Plex VM** (Sun 04:00, Plex updated from [plex.tv](http://plex.tv/), 7 checks) and the **ClaudeCode VM** (Sun 04:30, 3 checks). First real runs: **Sun 2026-09-27**. The ClaudeCode VM's run will apply its 18 pending updates and boot kernel 7.0.0-34 (it had been running 7.0.0-30).
**HA side:**
- `automation.homelab_vm_update_reports`: local-only webhook. Failed runs get a time-sensitive push; runs that changed something get a passive "updated" push; runs with no changes are silent (logbook only); install test reports get a passive push.
- Kuma push monitors `Plex VM Updates` and `ClaudeCode VM Updates` (8-day window) show up as `sensor.*_vm_updates_status`. They're added to the `homelab_watch` label and to `automation.homelab_service_device_alerts` with a new `heartbeat_missed` trigger ("missed its weekly update"). The Home Health Homelab card text was updated to match.
**Verified:** both install test reports reached HA (webhook runs at 21:48:36 and 21:50:11 UTC). Plex 7/7 and ClaudeCode 3/3 checks passing. Both push monitors are `up`. Timers are scheduled correctly: Plex Sun 04:00 MDT, ClaudeCode Sun 10:30 UTC (04:30 MDT). The deployed script's sha256 is identical on both VMs.
**Issue found and fixed:** the installer piped `systemctl list-timers` into `head` under `set -o pipefail`, and a SIGPIPE aborted it on the ClaudeCode VM just before the test report. The install itself had completed. Claude ran `homelab-update test` there manually and fixed the installer (runbook copy is the corrected version).
