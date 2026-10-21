---
kind: procedure
status: active
system:
- '[[Servarr Stack (Docker Compose)]]'
- '[[ClaudeCode (VM)]]'
last_tested: 2026-10-17
repo: https://github.com/aaronspriggs/spriggs-homelab/blob/main/claudecode-vm/claude-fix-runbooks.json
notion_id: 3fb7ae76-22ba-8102-82fb-f2afc84cc940
---

# Fix run: servarr health alerts (Sonarr, Radarr, Prowlarr, Gluetun)

Fix-run runbook for alerts sonarr_health, radarr_health, prowlarr_health and gluetun_unhealthy: confirm, classify the health error, restart or recreate servarr containers if that's the fix, otherwise report. Followed by tap-started claude-fix runs; commands are exactly the run's allowlist.

## When to use

A "Fix with Claude" tap on one of these Alert2 alerts starts a `claude-fix` run on the ClaudeCode VM that follows this page:
- `sonarr_health`, `radarr_health`, `prowlarr_health` (generator `homelab_arr_health`): the app's `/health` has listed an error for 30+ minutes while the app itself is up. HA reads it into `sensor.<app>_health_messages`.
- `gluetun_unhealthy`: Gluetun's container health check has failed for 5+ minutes, so NZBGet and Prowlarr have no VPN. That alert already has a **Restart servarr stack** button; a fix run is for when the restart didn't help or the cause is unclear.
A person in a normal session can follow it too. Background: [Managing the Servarr Docker Stack](<Managing the Servarr Docker Stack.md>) and [Servarr Stack (Docker Compose)](<../systems/Servarr Stack (Docker Compose).md>); fetch them only if a step here isn't enough.

## Prerequisites (rules for the run)

- **Use the commands below exactly as written**, with the full path, the same quoting and no extra pipes or flags. A fix run's permissions match the command text, so anything else is denied. Read the JSON output yourself instead of piping it to other tools.
- **Tier 1 only:** reads, restarting a servarr container or the stack, and recreating the stack without pulling images. Anything else stops the run with `NEEDS YOU:`: image updates, `.env` or credential changes (WireGuard key, API keys), file ownership or ZFS work on Big Boi (needs Aaron's shell), and deletes.
- **Never test indexers or start searches.** They spend NZBgeek API calls, and that API limit caused the 2026-10 health-alert flapping.
- **At most two fix attempts.** If the error is still there after the second, stop and report (KB Standards guardrail).
- `<app>` below is `sonarr`, `radarr` or `prowlarr`. Sonarr and Radarr use `/api/v3`, Prowlarr `/api/v1`.

## Steps

### 1. Confirm it's still broken

For an arr alert, read the app's health (shown for Sonarr; same shape for the others):
```bash
/home/aspriggs/.local/bin/arr-api sonarr /api/v3/health
/home/aspriggs/.local/bin/arr-api radarr /api/v3/health
/home/aspriggs/.local/bin/arr-api prowlarr /api/v1/health
```
Only entries with `"type": "error"` count; warnings (e.g. an update is available) don't raise the alert and aren't to be fixed. If no error is left, it cleared by itself: finish with `FIXED:` saying nothing was needed.
For `gluetun_unhealthy`, read the container list and look at `gluetun`'s state and health:
```bash
/home/aspriggs/.local/bin/dockhand-api /api/containers?env=1
```
If it's healthy again, finish with `FIXED:` saying nothing was needed. Otherwise go to step 4.

### 2. Classify the error (arr alerts)

Match the error `message` (and `source`):
- **Indexers unavailable due to failures** (Prowlarr; or Sonarr/Radarr about their indexers): read Prowlarr's indexer status:
```bash
/home/aspriggs/.local/bin/arr-api prowlarr /api/v1/indexerstatus
```
Each entry has `disabledTill`. The app retries by itself after that time, so there's nothing to fix: finish with `NOT FIXED:` naming the indexer and when it retries. If the health message or an indexer error points at a rejected API key or login (401/403, "API key", "unauthorized"), finish with `NEEDS YOU:` (credential change, Tier 3).
- **Unable to communicate with NZBGet / download client unavailable** (Sonarr, Radarr): step 3.
- **Prowlarr: applications unavailable** (Sonarr/Radarr sync) or **Sonarr/Radarr: unable to communicate with Prowlarr**: check that the other app's container is running in the step 1 container list. If it's stopped or exited, restart it (step 5). If both are running, go to step 3, since Prowlarr shares Gluetun's network.
- **Missing root folder, import or permission errors**: finish with `NEEDS YOU:`. The fix is a `chown` on Big Boi (see the servarr runbook), which only Aaron's shell can do.
- **Anything else**: finish with `NEEDS YOU:` and quote the message.

### 3. Check the Gluetun network share

NZBGet and Prowlarr run inside Gluetun's network namespace. If Gluetun was recreated without them, they show running but have no network.
```bash
/home/aspriggs/.local/bin/dockhand-api /api/containers/gluetun?env=1
/home/aspriggs/.local/bin/dockhand-api /api/containers/nzbget?env=1
/home/aspriggs/.local/bin/dockhand-api /api/containers/prowlarr?env=1
```
Compare `HostConfig.NetworkMode` of nzbget and prowlarr (`container:<id>`) with Gluetun's `Id`, and read Gluetun's `State.Health.Status`.
- Gluetun not healthy: step 4.
- An ID doesn't match: recreate the stack without pulling (about 1–2 min of downtime for all 7 containers), then wait and go to step 6:
```bash
/home/aspriggs/.local/bin/dockhand-api --write POST /api/stacks/servarr/deploy?env=1 '{"pull":false,"build":false,"forceRecreate":true}'
sleep 90
```
- IDs match and Gluetun is healthy, but NZBGet isn't running or still can't be reached: restart NZBGet (step 5).

### 4. Gluetun unhealthy

Read its recent log first:
```bash
/home/aspriggs/.local/bin/dockhand-api "/api/containers/gluetun/logs?env=1&tail=100"
```
- WireGuard handshake or authentication failures, an invalid key, or a ProtonVPN account problem: finish with `NEEDS YOU:`. The key is in the stack's `.env` (Tier 3).
- Otherwise restart the stack. This is the same as the alert's Restart button; `gluetun-watchdog` brings NZBGet and Prowlarr back within 30 s once Gluetun is healthy.
```bash
/home/aspriggs/.local/bin/dockhand-api --write POST /api/stacks/servarr/restart?env=1
sleep 90
```
Then re-read the container list (step 1) and do step 3's ID check.

### 5. Restart one container

For an app that's stopped, or one whose own error persists with nothing else wrong:
```bash
/home/aspriggs/.local/bin/dockhand-api --write POST /api/containers/sonarr/restart?env=1
/home/aspriggs/.local/bin/dockhand-api --write POST /api/containers/radarr/restart?env=1
/home/aspriggs/.local/bin/dockhand-api --write POST /api/containers/prowlarr/restart?env=1
/home/aspriggs/.local/bin/dockhand-api --write POST /api/containers/nzbget/restart?env=1
sleep 60
```
Never restart Gluetun on its own here; use the stack restart in step 4.

### 6. Re-check

Ask the app to re-run its health checks, wait, and read health again:
```bash
/home/aspriggs/.local/bin/arr-api sonarr --write POST /api/v3/command '{"name":"CheckHealth"}'
/home/aspriggs/.local/bin/arr-api radarr --write POST /api/v3/command '{"name":"CheckHealth"}'
/home/aspriggs/.local/bin/arr-api prowlarr --write POST /api/v1/command '{"name":"CheckHealth"}'
sleep 30
```
After an NZBGet restart, run CheckHealth on both Sonarr and Radarr: they share NZBGet, so both alerts usually fire together.
If the error is gone, finish with `FIXED:`. **"All download clients are unavailable due to failures"** right after an NZBGet restart is the apps' retry backoff, not a new fault: their retries back off (about 1, 5, 15, 30 min…) and the next successful one clears it, along with the HA alert. Count that as `FIXED:` and say the alert clears after the next retry; don't restart anything for it. If the original error is still there, you may make one more attempt from steps 3–5; after that, finish with `NOT FIXED:` and what you saw.

## Verify

The app's `/health` has no `error` entries; Gluetun is `healthy`; nzbget and prowlarr `NetworkMode` match Gluetun's `Id`. The HA alert clears on HA's next poll (up to 5 min), so don't wait for it. `ha_get_state` on `sensor.<app>_health_messages` shows what HA last read.

## Log

If you restarted or recreated anything, add a Changes entry: `Type` Fix, `When` today, `System` Servarr Stack, title "Fix run: <what was fixed>", Details = alert, cause, action, result. Whether or not anything changed, set this page's `Last Tested` to today.

## Rollback

Nothing to roll back: restarts and a recreate without pulling keep the same images and compose file. If the stack doesn't come back after a recreate, finish with `NEEDS YOU:`.
