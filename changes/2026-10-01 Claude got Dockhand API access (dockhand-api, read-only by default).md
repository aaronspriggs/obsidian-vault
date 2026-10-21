---
date: 2026-10-01
type: install
system:
- '[[Dockhand]]'
- '[[ClaudeCode (VM)]]'
project:
- '[[Dockhand - give Claude API access and build out Dockhand as the Docker platform]]'
commit: https://github.com/aaronspriggs/spriggs-homelab/commit/a8e66c7
notion_id: 3ec7ae76-22ba-81de-b30e-fa701ecf8303
---

# Claude got Dockhand API access (dockhand-api, read-only by default)

Aaron created a 90-day token for Dockhand user 'claude' (in 1Password; ~/.config/homelab/dockhand-api-token 600 on the ClaudeCode VM). New repo tool dockhand-api: GET only unless --write (writes logged), redacts secrets incl. env KEY=VALUE. gitleaks rule for dh_ tokens. [CLAUDE.md](http://claude.md/) approval rule (commit 30623bb).

**Verified:** token authenticates; `/api/environments` shows one environment ("Big Boi", id 1, socket); `/api/stacks?env=1` lists servarr, uptime-kuma and ix-dockhand (Dockhand's own TrueNAS app). Gluetun inspect prints `WIREGUARD_PRIVATE_KEY=<redacted>`. A non-`/api/` argument is refused, so a GET can't be turned into a write by accident. `make check` ok.
**First finding through the API:** servarr reports `updatesAvailable: false` / `updateCount: 0` although newer images exist (linuxserver ls326/ls318/ls162, Seerr v3.5.0). Step 2 of the project.
**Notes:** most endpoints need `?env=1`; `/api/docs` returns 404 until `FEAT_API_DOCS` is set on the app. Usage and paths: repo `dockhand/README.md`.
