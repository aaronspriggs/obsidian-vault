---
type: project
status: done
priority: medium
system:
- '[[Dockhand]]'
- '[[Servarr Stack (Docker Compose)]]'
- '[[Uptime Kuma]]'
completed: 2026-10-15
notion_id: 3ea7ae76-22ba-81d9-857e-d909d09e19fa
---

# Dockhand: give Claude API access and build out Dockhand as the Docker platform

API access, git-sourced stack deploys, update detection and HA alerts done; closed 2026-10-15. HTTPS/settings and Git stacks split out as their own items.

## Outcome (Done 2026-10-15)

Claude reads and operates Dockhand directly, and Dockhand is now the homelab's Docker platform rather than just a compose editor.
- **API access (2026-10-01):** `dockhand-api` on the ClaudeCode VM (commits a8e66c7, 30623bb, 82cc092) uses the `claude` user's token. It reads by default and writes only with `--write`, under the Change authority tiers in KB Standards. A Claude Code allow rule in `~/homelab-agent/.claude/settings.local.json` (Aaron, 2026-10-01) lets `dockhand-api --write` past the auto-mode classifier.
- **Stacks deploy from git:** `servarr` and `uptime-kuma` live in [`stacks/`](https://github.com/aaronspriggs/spriggs-homelab/tree/main/stacks). Claude commits there, then pushes the compose file through the API (`PUT /api/stacks/<name>/compose`, `forceRecreate: false`) and checks drift against `GET` of the same path. Both stay Dockhand `internal` stacks; Git stacks were deferred (see below).
- **Update detection:** the Big Boi update check is on again, notify-only (verified 2026-10-15). Updates surface in HA as ha-dockhand update entities.
- **Container alerts in HA** via ha-dockhand (Done 2026-10-07, replaced the planned MQTT channel). HA connects as the Dockhand user `homeassistant`.
Current state and known Dockhand behaviour: the [Dockhand](<../systems/Dockhand.md>) system page.
Follow-ups (own items): [Serve Dockhand over HTTPS and review its settings](<Serve Dockhand over HTTPS and review its settings.md>), [Trial HA Install for image updates](<Trial HA Install (Dockhand update entities) for container image updates.md>) (the update-policy decision), [Rotate the claude API token](<Rotate the Dockhand API token for claude (90-day expiry, ~late Dec 2026).md>) (~late Dec 2026), [Move the stacks to Git stacks](<Move the servarr and uptime-kuma stacks to Dockhand Git stacks.md>) (Deferred Idea, with the absolute-path and secrets prerequisites).

## Decisions

- **2026-09-29: no scoped tokens on Free.** Dockhand `dh_` tokens inherit the user's role, and on the Free edition every user is a full admin; RBAC is Enterprise-only ($1,499/host/yr). So any token means full Docker control, which is root on Big Boi. Sources: [dockhand.pro](https://dockhand.pro/) (pricing) and [dockhand.pro/manual](https://dockhand.pro/manual) (RBAC).
- **2026-09-30 (Aaron): full-access token for a dedicated ****`claude`**** user, 90-day expiry.** It lives only in `~/.config/homelab/dockhand-api-token` (600) on the ClaudeCode VM, with the value in 1Password. Guardrails are policy, not enforcement. Accepted risk: a compromised ClaudeCode VM has full control of Docker on Big Boi. **Git is the source of truth** for the stacks, and the UI editor is no longer used for them.
- **2026-10-06: ha-dockhand instead of Dockhand's MQTT channel** for container alerts (reasoning on the [task page](<Monitoring - Dockhand container alerts to HA via ha-dockhand.md>)).
- **2026-10-15 (Claude, with Aaron's go-ahead): close without migrating to Git stacks.** The repo plus API push already gives repo-as-source and drift checks, and the migration risks empty configs from relative volume paths (the 2026-03 incident). HTTPS and the settings review became their own task.

## Links

Changes linked in the `Changes` property (2026-10-01 to 2026-10-14). API reference: [dockhand.pro/manual/#api-reference](https://dockhand.pro/manual/#api-reference); releases [v1.0.25 API tokens](https://github.com/Finsys/dockhand/releases/tag/v1.0.25), [v1.0.43 OpenAPI spec](https://github.com/Finsys/dockhand/releases/tag/v1.0.43). Community MCP server (not used): [github.com/intarweb/mcp-dockhand](https://github.com/intarweb/mcp-dockhand).

## Sub-items

![[Projects.base#Sub-items]]

## Changes

![[Changes.base#For this project]]
