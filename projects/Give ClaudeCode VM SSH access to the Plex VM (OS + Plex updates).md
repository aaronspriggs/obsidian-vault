---
type: project
status: done
priority: medium
system:
- '[[Plex Media Server]]'
- '[[ClaudeCode (VM)]]'
completed: 2026-09-24
notion_id: 3e57ae76-22ba-8109-b82b-c268e270cc2b
---

Done 2026-09-24. Claude Code maintains the Plex VM through `ssh plex` (scoped `claude` account + `claude-maint` wrapper). First run done: Ubuntu 24.04.5 / kernel 6.8.0-142, Plex 1.43.4. Procedure: "Updating the Plex VM (OS + Plex)" runbook. Follow-up: restore the /transcode tmpfs (Plex System page Known Gaps).

## Outcome

Done 2026-09-24. Claude Code maintains the Plex VM itself over `ssh plex`: a password-less `claude` account (groups `adm`, `systemd-journal`) whose only root path is `/usr/local/sbin/claude-maint`. The first run brought it to Ubuntu 24.04.5, kernel 6.8.0-142 and Plex 1.43.4 (from 1.43.0, 11 weeks without a reboot). The weekly **homelab-update** job now does this unattended. Current state: [Plex Media Server](<../systems/Plex Media Server.md>); procedure: "Updating the Plex VM (OS + Plex)" runbook; wrapper source: repo `plex-vm/`.

## Decisions (2026-09-24)

- **Dedicated ****`claude`**** account, not ****`plexadmin`****,** with key `~/.ssh/id_ed25519_plex` on the ClaudeCode VM (`Host plex` in `~/.ssh/config`). The `authorized_keys` entry is pinned `from="192.168.1.156"` and disables agent, port and X11 forwarding. Aaron generated the key from his Mac because Claude Code's safety check won't let Claude create standing credentials.
- **Root only through ****`claude-maint`** (NOPASSWD, root-owned), a fixed list of subcommands: `update`, `upgrade`, `upgrade-plex`, `autoremove`, `unattended-dry-run`, `plex-restart`/`-stop`/`-start`, `reboot`; anything else exits 2. It's a guardrail against mistakes, not a security boundary (package installs as root are root); the real boundary is the key living only on the ClaudeCode VM and working only from its IP.
- **Excluded on purpose:** `do-release-upgrade` and editing apt sources/keyrings; those need Aaron.
- **Plex updates bypass the apt repo.** Root cause of Plex never updating: `downloads.plex.tv/repo/deb` was stale (newest 1.42.2, older than the installed 1.43.0). `claude-maint upgrade-plex` takes the latest **public** (not Plex Pass beta) Debian x86_64 build from `plex.tv/api/downloads/5.json`, only from `downloads.plex.tv`, checks its SHA-1, and installs with apt (which refuses downgrades).

## Links

Follow-ups already split out: /transcode tmpfs (restored 2026-09-28), wall-panel SSH ("Give the ClaudeCode VM SSH access to the wall panel Pi", Backlog). Pre-collapse diagnosis: KB export commit 4ac914e.
