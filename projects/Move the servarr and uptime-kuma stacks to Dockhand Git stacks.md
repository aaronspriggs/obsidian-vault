---
type: idea
status: backlog
priority: low
system:
- '[[Dockhand]]'
- '[[Servarr Stack (Docker Compose)]]'
- '[[Uptime Kuma]]'
parent: '[[Dockhand - give Claude API access and build out Dockhand as the Docker platform]]'
notion_id: 3fa7ae76-22ba-81ca-ab43-c70676a61d43
---

Extracted 2026-10-15 from the Done Dockhand project (plan step 4). Deferred by Claude with Aaron's go-ahead: the repo + API-push deploy (stacks/[README.md](http://readme.md/)) already makes git the source of truth, so the gain is small and the risk (empty configs from relative paths, the 2026-03 incident) is real.

## Goal

Dockhand deploys `stacks/servarr` and `stacks/uptime-kuma` straight from `aaronspriggs/spriggs-homelab` as Git stacks. Today both are `internal` stacks that Claude updates through the API from the repo copy.

## Why deferred

The current API push already gives repo-as-source-of-truth and drift checks. What Git stacks would add is Dockhand pulling on its own (webhook or poll) and Aaron being able to deploy without Claude. Pick this up if that becomes worth the migration risk.

## Prerequisites (from the 2026-09-29 investigation)

- **Absolute volume paths first.** servarr still uses relative paths (`./gluetun`, `./sonarr`, ...; checked 2026-10-15) that resolve against the stack directory. A Git stack lives elsewhere, so they would silently point at empty folders (the 2026-03 "Dockhand migration reset configs" incident). Pin them to `"/mnt/.ix-apps/app_mounts/dockhand/data/stacks/Big Boi/servarr/<app>"`, or move the configs to a regular dataset first, which would also get normal ZFS snapshots.
- **Secrets.** Git stacks read the repo `.env` plus a local `.env.dockhand`. The WireGuard key (still in the on-host `.env` as of 2026-10-15) becomes a Dockhand secret, which is stored encrypted and injected at deploy, or a 1Password reference. uptime-kuma already uses Dockhand stack secrets for `KUMA_USERNAME`/`KUMA_PASSWORD`.
- Dry-run a throwaway Git stack, and snapshot `app_mounts` before switching (Tier 3).
