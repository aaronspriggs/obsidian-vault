---
kind: setup
status: active
system:
- '[[TrueNAS SCALE (Big Boi)]]'
- '[[ClaudeCode (VM)]]'
- '[[Home Assistant OS (VM)]]'
last_tested: 2026-10-15
repo: https://github.com/aaronspriggs/spriggs-homelab/tree/main/truenas
notion_id: 3e77ae76-22ba-8146-97f8-e11b11905670
---

How Claude reads TrueNAS (`claude-readonlyapi`, key on disk for the relay) and does allowlisted maintenance writes (`claude-maint`, key in 1Password) with `truenas-api`, plus the `truenas-alert-relay` timer that forwards TrueNAS alerts and stale-snapshot warnings to HA. Setup, rebuild and troubleshooting.

## Pieces

- **TrueNAS:** local user `claude-readonlyapi` (renamed from `claude` on 2026-10-14 by Aaron; the same key kept working, though the first login right after the rename failed for a few minutes; full name "Claude (Read-Only API)"; password disabled, nologin, no sudo, no SMB). Its primary group `claude` has the **Read-Only Administrator** privilege (Credentials → Groups → Edit → Privileges; 25.04's Add User form has no role field). It has a user-linked API key `claude-readonly` (account menu → My API Keys).
- **ClaudeCode VM (192.168.1.156):**
    - `~/.config/homelab/truenas-api-key` (600): the key, written by Aaron over SSH. **Only ever use it over WSS/HTTPS**, because 25.04 auto-revokes keys sent over HTTP.
    - `~/.local/bin/truenas-api <method> '<json params>'`: one-off read-only JSON-RPC queries. `alert.dismiss` returns EACCES, which confirms read-only. The read-only role has no file-read method (`filesystem.listdir` works; `filesystem.file_get_contents` doesn't exist for it).
    - `~/.local/bin/truenas-alert-relay`: run every 5 min by `truenas-alert-relay.timer` (system unit, `User=aspriggs`, installed by Aaron as root). Config is in `~/.config/homelab/truenas-alert-relay.json` (600: HA webhook URL and Kuma push URL); state is in `~/.local/state/truenas-alert-relay/state.json`. Depends on apt `python3-websocket`.
- **Home Assistant:**
    - `automation.truenas_alert_relay`: local-only webhook; sets `input_number.truenas_active_alerts` and `input_text.truenas_alert_summary`; reports each new alert to Alert2 with `alert2.report` (since 2026-10-14; repo `ha/alert2.yaml`, `tracked:` section), which handles the push, quiet hours (20:00–09:00, held for the 09:00 report) and throttling.
    - The count feeds `sensor.homelab_issue_count`, which drives the Home Health hero banner and the Homelab card.
    - Kuma push monitor **TrueNAS Alert Relay** (900 s, retries 0) is `sensor.truenas_alert_relay_status`. It's in `homelab_watch`; Alert2's `alert2.homelab_truenas_alert_relay_missed` fires when it goes down.

## Maintenance writes (`claude-maint`, since 2026-10-14)

- **TrueNAS:** user `claude-maint` ("Claude maintenance (API)", password disabled, nologin), group `claude-maint` with privilege **Claude maintenance**: `READONLY_ADMIN`, `APPS_WRITE`, `VM_WRITE`, `SYSTEM_UPDATE_WRITE`, `POOL_SCRUB_WRITE`, `SNAPSHOT_WRITE` and `SNAPSHOT_DELETE` (both added by Aaron 2026-10-15). Its API key is in 1Password item **TrueNAS API Key (claude-maint)** (vault Homelab - Claude), read at each run via `homelab-secret`; never on disk. Created by Aaron.
- **Use:** `~/.local/bin/truenas-api --write <method> '<json params>'`. Only these run: `app.upgrade`, `app.redeploy`, `app.start`, `app.stop`, `vm.start`, `vm.stop`, `vm.restart`, `update.download`, `update.update`, `zfs.snapshot.create` and `zfs.snapshot.delete` (since 2026-10-15; commits [4798143](https://github.com/aaronspriggs/spriggs-homelab/commit/4798143), [a32b34c](https://github.com/aaronspriggs/spriggs-homelab/commit/a32b34c), [3c5fa62](https://github.com/aaronspriggs/spriggs-homelab/commit/3c5fa62)). Delete takes one `<dataset>@<name>` and refuses scheduled `auto-*` snapshots and bare datasets. The TrueNAS roles would also allow deleting/reconfiguring apps and VMs, adding registries and rolling back snapshots, so the allowlist in the script is the guard. Jobs are waited on (`update.update` reboots Big Boi, so a dropped connection is expected there). Every write is logged to `~/.local/state/homelab/truenas-api.log`.
- **Authority:** the KB Standards tiers decide (Aaron, 2026-10-14): app and TrueNAS OS updates and VM restarts are Tier 2. Pools, datasets, network and users stay Tier 3 and aren't possible with this key. Creating and deleting manual snapshots is **Tier 2** (Aaron, 2026-10-15). It was verified end to end the same day with a throwaway `app_mounts@claude-delete-test`. Rollbacks stay Tier 3 and aren't allowlisted.
- **Scrubs:** `POOL_SCRUB_WRITE` only edits scrub *schedules*; starting a scrub on demand needs `POOL_WRITE`, deliberately not granted.
- **Permission:** Claude Code may need `Bash(~/.local/bin/truenas-api --write:*)` in `~/homelab-agent/.claude/settings.local.json` (Aaron adds).
- Verified 2026-10-15: `vm.delete` refused by the allowlist; `vm.start` on the running Plex VM reached TrueNAS as `claude-maint` and returned "already running" (nothing changed).

## Source code

Lives in the repo `aaronspriggs/spriggs-homelab` under [`truenas/`](https://github.com/aaronspriggs/spriggs-homelab/tree/main/truenas) (clone on the ClaudeCode VM: `~/homelab`):
- [`truenas-api`](https://github.com/aaronspriggs/spriggs-homelab/blob/main/truenas/truenas-api) and [`truenas-alert-relay`](https://github.com/aaronspriggs/spriggs-homelab/blob/main/truenas/truenas-alert-relay)
- [`systemd/`](https://github.com/aaronspriggs/spriggs-homelab/tree/main/truenas/systemd): the relay's `.service` and `.timer`
- [`truenas-alert-relay.json.example`](https://github.com/aaronspriggs/spriggs-homelab/blob/main/truenas/truenas-alert-relay.json.example): config template with the webhook ID removed
- The README also records the TrueNAS cron job that backs up the Dockhand stacks.
`make check` in the repo confirms the deployed copies match.

## What gets relayed

- TrueNAS alerts at **WARNING, ERROR, CRITICAL, ALERT, EMERGENCY**, plus **AppUpdate/HasUpdate** (INFO level). Alert2 alerts by level: ERROR and above → `homelab.truenas_error` (medium, 🔴 time-sensitive), WARNING → `truenas_warning` (low, 🟠 passive FYI, no buttons, since 2026-10-14), updates → `truenas_update` (low, ⬆️ passive). Cleared alerts are logbook-only (no "resolved" push since 2026-10-14).
- **Ignored:** `PoolUpgraded` (the one-way ZFS feature upgrade, deliberately deferred). Edit `IGNORE` in the script to change that.
- **Synthetic "Snapshot Task Stale"** (WARNING): an enabled snapshot task whose newest snapshot is more than 26 h old, for example a disabled or broken schedule, which TrueNAS doesn't alert on. Snapshot names are parsed with the task's naming schema in TrueNAS's timezone, read on every run (America/Denver since 2026-10-15; the relay's first run after the change exited 0).
- It POSTs to HA **only when the active set changes**. It pings Kuma after every successful run. Any failure (TrueNAS unreachable, auth, HA webhook) exits non-zero with no ping, so Kuma goes down after 15 min and Alert2 sends "TrueNAS alert relay heartbeat missed".

## Operate

- Status: `systemctl list-timers truenas-alert-relay.timer`, `systemctl status truenas-alert-relay.service`, `sudo journalctl -u truenas-alert-relay`.
- Preview without posting: `~/.local/bin/truenas-alert-relay --dry-run`.
- To re-send everything (e.g. after HA lost its helpers): delete the state file; the next run posts all active alerts as new.
- Errors: both tools print/log only the TrueNAS error *reason*, never the raw reply, because TrueNAS error tracebacks echo the call parameters including the API key (it happened once, 2026-10-14; fixed in repo commit [cd0a113](https://github.com/aaronspriggs/spriggs-homelab/commit/cd0a113)).
- **Login rate limit:** every `truenas-api` call logs in fresh, and TrueNAS 25.04 returns `auth failed: [EBUSY] Rate Limit Exceeded` after a burst of roughly 20 calls in a minute (hit 2026-10-15). It clears within about 90 s. Space out bulk reads so the relay's own 5-minute login isn't starved.
- **Params format:** the wrapper passes its argument as the JSON-RPC params array, so query filters need three brackets, e.g. `truenas-api service.query '[[["service","=","smartd"]]]'`.
- **`smart.test.results`**** is broken in 25.04** for the SATA SSDs: it fails schema validation (`OROperator failed to dump all schemas ... power_on_hours`). Check the schedule with `smart.test.query`; failures still raise TrueNAS alerts, which the relay forwards.
- Key rotation: create a new key for `claude-readonlyapi` in TrueNAS, re-run the SSH `cat >` step, and delete the old key.
- Changing a script: edit in `~/homelab`, commit and push, then `install -m 755 truenas-api truenas-alert-relay ~/.local/bin/` and `make check`.

## Rebuild on a fresh VM

1. `sudo apt-get install -y python3-websocket`
2. Aaron writes the key: `ssh aspriggs@192.168.1.156 'umask 077; mkdir -p ~/.config/homelab && cat > ~/.config/homelab/truenas-api-key'` (paste, Enter, Ctrl-D).
3. Clone the repo to `~/homelab` (see its README for the deploy key), then from `~/homelab/truenas`: `install -m 755 truenas-api truenas-alert-relay ~/.local/bin/`. Create `~/.config/homelab/truenas-alert-relay.json` (600) from the `.example`, filling in the webhook ID from the trigger of `automation.truenas_alert_relay` and the Kuma push URL without its query string.
4. As root: `install -m 644 systemd/truenas-alert-relay.* /etc/systemd/system/`, then `systemctl daemon-reload && systemctl enable --now truenas-alert-relay.timer`.
