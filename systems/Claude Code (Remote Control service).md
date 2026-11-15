---
status: active
category: software
runs_on:
- '[[ClaudeCode (VM)]]'
last_verified: 2026-11-15
repo: https://github.com/aaronspriggs/spriggs-homelab/tree/main/claudecode-vm
---

Claude Code on the ClaudeCode VM: the Remote Control service Aaron's sessions attach to, with its settings, session hook, tier3-guard mod, MCP connectors and fix runs.

## Overview

Claude Code runs on the [ClaudeCode VM](<ClaudeCode (VM).md>) in Remote Control server mode, so Aaron works on the homelab from the desktop app, claude.ai/code or the iOS app while Claude has direct LAN access. Remote Control only makes outbound connections to Anthropic, so nothing is exposed and no VPN is needed. This note holds the current state of that setup. The rules Claude follows are in [CLAUDE.md](https://github.com/aaronspriggs/spriggs-homelab/blob/main/claudecode-vm/CLAUDE.md) and the [rulebook](<../STANDARDS.md>). It was split from the VM's note on 2026-11-15; changes before that date are listed under the VM.

## Access

- **Remote Control:** shows as "ClaudeCode VM" in the session list at [claude.ai/code](https://claude.ai/code), in the desktop app and in the iOS app's Code tab, on Aaron's claude.ai account (Claude Pro).
- **On the VM:** `/home/aspriggs/.local/bin/claude`, working directory `/home/aspriggs/homelab-agent` (trusted workspace). `~/.local/bin` isn't on the PATH of non-interactive shells, so use the full path.
- **Login:** `~/.claude/.credentials.json`, not versioned; log in again after a rebuild.

## Config

- **Install:** native install (npm-global would need sudo to auto-update), v2.1.321 on 2026-11-15. Update with `claude update`, then `sudo systemctl restart claude-remote-control.service`; the restart drops every attached session.
- **Service:** `/etc/systemd/system/claude-remote-control.service` runs as aspriggs in the working directory with `Restart=always`. Its ExecStart, `~/.local/bin/claude-remote-control-start`, reads the ha-mcp URL from 1Password into `HA_MCP_URL` and runs `claude remote-control --name "ClaudeCode VM"`. The first run needs the "Enable Remote Control? (y/n)" prompt answered once by hand, over SSH from the same directory; until then the unit crash-loops. A VM reboot drops all sessions and the unit starts again at boot. After a hard reset it can register a new environment ID, and the desktop app then files earlier sessions under "Other"; they're still on disk and can be resumed.
- **Settings**, all versioned in repo `claudecode-vm/` and watched by `make check`: `~/homelab-agent/CLAUDE.md` (a symlink into the repo), `~/homelab-agent/.mcp.json`, `~/homelab-agent/.claude/settings.local.json` (6 allow rules, `enabledMcpjsonServers`, `autoCompactWindow`, the SessionStart hook) and `~/.claude/settings.json` (the `env` block that loads tier3-guard). Auto-memory, `~/.claude/projects/-home-aspriggs-homelab-agent/memory`, is a symlink to `claudecode-vm/claude/memory` and is committed after each write; it holds three procedures, and settled rules live in CLAUDE.md. Not versioned, recreated on a rebuild: the login, `~/.claude.json` and the session transcripts.
- **Context:** sessions compact at 400k tokens (`autoCompactWindow`, since 2026-11-15; the default is about 967k on a 1M window). CLAUDE.md's "Compact instructions" say what the summary keeps.
- **Session-start hook** (since 2026-11-08): `~/.local/bin/kb-session-context` runs on startup, resume, clear and compact. It pulls the vault and prints `check.py --session` (open work with next steps, stalled projects, gaps, every backlog title once) and the last 5 KB commits. Claude Code cuts hook output over 10,000 characters to a 2 KB preview, so `check.py` holds the block to 8,500 characters and the hook warns at 9,800. Fix runs don't load local settings, so they skip it.
- **tier3-guard mod** (since 2026-10-22): a Claude Code plugin in `~/.claude/mods/tier3-guard`, loaded into every session, fix runs included, by `CLAUDE_CODE_PLUGIN_DIRS` and `CLAUDE_CODE_ENABLE_FUNCTION_HOOKS=1` in `~/.claude/settings.json`. It holds the Tier 3 tool calls it can detect until Aaron approves: a plain yes releases the calls held since his previous message and covers Tier 3 calls in the turn it starts; `approve <code> [<code> …]` releases named holds. It always denies `--no-verify` and plain force pushes. Guarded paths are the rulebook, `.ssh/`, `~/.claude/mods` and `~/.claude/settings.json`: Edit and Write to them are always held, and a Bash command is held only where it writes one (since 2026-11-15). Known false holds: a Bash command that only names `ssh-keygen` or `authorized_keys`, reads included. Claude edits and tests the guard in the repo (`claude plugin test claudecode-vm/mods/tier3-guard`, 89 tests), but the auto mode classifier refuses Claude's commit of it, so Aaron runs the commit-and-deploy line over SSH.
- **Mod UI over Remote Control** (tested 2026-10-22 on 2.1.286): hooks work, UI doesn't. A mod can block, hold or rewrite tool calls and prompts, and its slash commands can answer in text. Panes, buttons, toasts and status-line entries don't render in the desktop or iOS app. Re-check with repo `claudecode-vm/mods/ui-test`; see [Use mod UI once Remote Control clients draw it](<../projects/Use mod UI once Remote Control clients draw it.md>).
- **MCP connectors:** Home Assistant (ha-mcp) is the only locally configured server, at project scope in `.mcp.json` with its URL from the 1Password item `HA-MCP URL`; `~/.claude.json` has no `mcpServers`. Runbook: [Setting Up ha-mcp](<../runbooks/Setting Up ha-mcp (Home Assistant MCP Server) for Claude Code.md>). Notion (read-only archive of the old KB), Box and Claude Docs are account-level claude.ai connectors that sessions inherit; add or remove them in claude.ai connector settings, not on the VM. Gmail, Google Calendar and Google Drive show as needing authorization and stay that way: Aaron won't connect them (2026-10-17).
- **Fix runs:** `claude-fix-listener.service` (`~/.local/bin/claude-fix serve`, port 8765) accepts `POST /fix {alert_id}` with a bearer token from Home Assistant (192.168.1.218) only, and starts a capped `claude -p` run for alert IDs allowlisted in `~/.config/homelab/claude-fix-runbooks.json`: one at a time, 3 per 24 h, Sonnet, `dontAsk` with that runbook's tools only, outcome posted to an HA webhook. Token and webhook ID are in the 1Password item `Claude Fix Listener`; runs are logged in `~/.local/state/claude-fix/`; Kuma monitor `Claude fix listener` watches `/health`. The last real run was 2026-10-17. Since the KB moved to the vault on 2026-10-22 the runs' vault tools have only been through a dry run. Design and caps: repo [claudecode-vm/README.md](https://github.com/aaronspriggs/spriggs-homelab/blob/main/claudecode-vm/README.md), "Fix runs".

## Dependencies

Runs on the ClaudeCode VM and needs outbound HTTPS to Anthropic. The launcher needs 1Password (service account `claudecode-vm`) for the ha-mcp URL; if 1Password is down, Remote Control starts without the HA tools. The HA tools need the ha-mcp integration in [Home Assistant](<Home Assistant (integrations and automations).md>). The session hook needs the vault clone at `~/obsidian-vault`. What depends on it: all homelab work Aaron does with Claude, and the "Fix with Claude" action on HA alerts.

## Decisions

- **2026-10-06:** the ha-mcp URL is a secret path, so it comes from 1Password through the launcher and is never stored in a file ([change](<../changes/2026-10-06 ha-mcp URL moved from Claude Code config to 1Password (loaded at service start).md>)). Sign-in by OAuth is blocked upstream: [Switch ha-mcp auth to Home Assistant sign-in (OAuth)](<../projects/Switch ha-mcp auth to Home Assistant sign-in (OAuth).md>).
- **2026-10-16:** fix runs are tap-started and capped, the one exception to "no scheduled or self-starting Claude runs" ([change](<../changes/2026-10-16 Allowed tap-started, capped Claude fix runs (token-budget rule amended).md>)).
- **2026-10-22:** Tier 3 approval is enforced by a mod's hooks and typed replies, because hooks work over Remote Control and mod UI doesn't ([project](<../projects/Build a Tier 3 guard mod for Claude Code.md>)).
- **2026-11-15:** compaction at 400k, CLAUDE.md as the one home for settled rules, the hook block under the cap and the guard holding only writes all came out of [Review and tune the Claude Code setup on the ClaudeCode VM](<../projects/Review and tune the Claude Code setup on the ClaudeCode VM.md>), which records the reasons and what was rejected.
- **2026-11-15:** split from the VM's note along the line between the machine and the software on it, the same line as Dockhand or Uptime Kuma on Big Boi. This half changes most often, so the VM's note stays stable.

## Open work

![[Projects.base#Open for this system]]

## Runbooks

![[Runbooks.base#For this system]]

## Recent changes

![[Changes.base#For this system]]

## Related

Repo `claudecode-vm/`: [README.md](https://github.com/aaronspriggs/spriggs-homelab/blob/main/claudecode-vm/README.md) (deploy commands, 1Password, fix-run design), [mods/tier3-guard](https://github.com/aaronspriggs/spriggs-homelab/tree/main/claudecode-vm/mods/tier3-guard) (source and tests), [kb-session-context](https://github.com/aaronspriggs/spriggs-homelab/blob/main/claudecode-vm/kb-session-context).
