---
date: 2026-10-16
type: fix
system:
- '[[ClaudeCode (VM)]]'
- '[[spriggs-homelab repo]]'
project:
- '[[Claude access model - more admin access, secrets management, account hardening]]'
commit: https://github.com/aaronspriggs/spriggs-homelab/commit/bb2c3e0
notion_id: 3fb7ae76-22ba-81d3-80a2-d478b7fe9edf
---

# Fixed kb-export failing since 2026-10-11 on a gitleaks false positive (narrow allowlist)

gitleaks generic-api-key matched a prose phrase about the arr health checks in a Changes entry; export skipped commits for 5 days. Added a line-scoped exact-phrase allowlist to .gitleaks.toml.

## What changed

Added one `[[allowlists]]` entry to `.gitleaks.toml` in spriggs-homelab: `regexTarget = "line"`, matching only the exact phrase from the arr health-check write-up that gitleaks' `generic-api-key` rule reads as a key.

## Why

`kb-export.service` had failed since 2026-10-11 ("secrets found, not committing"), so `HEALTH.md` and the export were 5 days stale. The match was in the Changes entry for the Alert2 move, which quotes the earlier identical false positive (2026-10-04), so rewording pages wouldn't stop it recurring. Checked with `gitleaks --redact`: the matched value is plain prose, not a secret.

## How

Commit [bb2c3e0](https://github.com/aaronspriggs/spriggs-homelab/commit/bb2c3e0). Re-ran `kb-export.service`: export commit `8bca314` (2026-10-16), 289 pages.

## Verify / roll back

`systemctl status kb-export.service` shows success; `git -C ~/kb-export log -1` is dated today. Roll back by reverting bb2c3e0.
