---
date: 2026-10-14
type: install
system:
- '[[Uptime Kuma]]'
project:
- '[[AutoKuma - Uptime Kuma monitors as code, managed by Claude]]'
commit: https://github.com/aaronspriggs/spriggs-homelab/commit/f15ce4e
notion_id: 3f97ae76-22ba-8193-854d-d1cb79b2887b
---

# Deployed AutoKuma: Kuma monitors now managed from the repo

What (Aaron said go ahead 2026-10-14): stored the Kuma login as Dockhand stack secrets KUMA_USERNAME/KUMA_PASSWORD on uptime-kuma (from 1Password 'Uptime Kuma', never printed); kuma-adopt tagged the 17 monitors; deployed compose.yaml (commit 75e52e9) via PUT /api/stacks/uptime-kuma/compose at 13:51. AutoKuma's first start migrated (adopted) 17 monitors and deleted the tag; Kuma IDs 1-17 and every field unchanged; no Prometheus label errors (Kuma restarted while the tag existed, so no extra restart needed). HA: all 14 non-weekly Kuma sensors up at 13:54. End-to-end test (commit 9a6eb24): added a 'Managed by AutoKuma: edit stacks/uptime-kuma/monitors/<id>.toml' description to every monitor; AutoKuma applied all 17 within a minute, nothing else changed, relay push token still accepted. Found: Dockhand's compose PUT defaults forceRecreate to true, which recreated Kuma on both deploys (Kuma stayed 2.5.6); deploys now send forceRecreate false (commit f15ce4e), verified with a no-op deploy (both containers stayed Running). Side effect of the two recreates: weekly push monitors (Plex VM updates, ClaudeCode VM updates, KB export) read unavailable in HA until their next weekly push. Verify: kuma-api monitor list (17, descriptions set); AutoKuma container healthy; dockhand-api /api/stacks/uptime-kuma/compose equals repo compose.yaml.
