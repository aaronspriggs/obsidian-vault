---
date: 2026-09-27
type: install
system:
- '[[ClaudeCode (VM)]]'
- '[[TrueNAS SCALE (Big Boi)]]'
- '[[Plex Media Server]]'
- '[[Dockhand]]'
notion_id: 3e87ae76-22ba-8168-b46d-e32b7d9fb537
---

# Created private GitHub repo spriggs-homelab for homelab code & config; runbooks now link to it

Project: "Homelab foundation: version-controlled repo for code & config". Repo: [https://github.com/aaronspriggs/spriggs-homelab](https://github.com/aaronspriggs/spriggs-homelab) (private; owned by Aaron, maintained by Claude Code on the ClaudeCode VM; clone at `~/homelab`). Work ran 2026-09-26 to 27.
**Access:** SSH deploy key with write access for this repo only. The key is `~/.ssh/id_ed25519_github_spriggs_homelab` on the ClaudeCode VM, fingerprint `SHA256:KGTonOtfI5tKYKt3zB6mjBihEfs6zVWq0b0xV9ZP8ps`, and `~/.ssh/config` maps `github.com` to it. To revoke it: repo Settings → Deploy keys. GitHub's suggestion to use a GitHub App instead was considered and deferred; for one VM and one repo it would still need a long-lived key on the VM.
**Contents:** `homelab-update/` (script, `install.sh`, host `.conf.example` templates), `truenas/` (`truenas-api`, `truenas-alert-relay`, relay units, JSON template, the stack-backup cron command), `plex-vm/` (`claude-maint`), `claudecode-vm/` (`claude-remote-control.service`), `stacks/` (servarr and uptime-kuma compose files, `servarr/.env.example` with names only). Every file was copied from its deployed location, except `install.sh`, which was restored from the runbook.
**Safety nets:** a `.githooks/pre-commit` hook runs gitleaks on staged changes plus shellcheck on shell scripts, and was verified to block a planted token. `.gitleaks.toml` adds rules for HA webhook IDs and Kuma push tokens, which the default rules miss. A full-history grep for the real webhook IDs and the TrueNAS API key found nothing. `make check` (`bin/check-drift` + `deployed.tsv`) compares the 8 deployed files on the ClaudeCode VM and Plex VM by sha256. All matched, and a simulated drift was flagged. The stacks can't be checked automatically, because the TrueNAS access is read-only with no file reads; the stacks README has the refresh procedure.
**Tooling installed on the ClaudeCode VM:** `shellcheck`, `make` (apt), and `gitleaks` 8.30.1 (upstream binary in `/usr/local/bin`, checksum-verified). Git identity: "Claude Code (ClaudeCode VM)".
**Commits:** `0eb8016` scaffold, `619b974` imports + drift check, `3b633ac` gitleaks rules, `2dd54a6` stacks.
**Docs:** the runbooks "homelab-update: weekly unattended VM updates", "TrueNAS read-only API access and alert relay" and "Updating the Plex VM" now link to repo files instead of embedding source. `CLAUDE.md` on the ClaudeCode VM gained a "Code lives in the repo" rule (commit, push, `make check`, no secrets). The Dockhand page was corrected: the compose files live in Dockhand's stacks dir, `${VAR}` substitution is still used for PUID/TZ/VPN, and Overseerr is now `seerr`.
**Gotcha:** the ClaudeCode VM only accepts SSH keys (`PasswordAuthentication no`), and Aaron's TrueNAS account has no home dir (`/var/empty`), so TrueNAS can't push to the VM directly. Route copies through the Mac instead: `ssh truenas 'cat …' | ssh claudecode '…'`.
