---
type: project
status: done
system:
- '[[ClaudeCode (VM)]]'
completed: 2026-10-22
---

# Build a Tier 3 guard mod for Claude Code

## Outcome

Done 2026-10-22. `tier3-guard`, a Claude Code plugin of function hooks, runs in every session on the ClaudeCode VM, fix runs included. It enforces the parts of Tier 3 in [STANDARDS.md](<../STANDARDS.md>) → Change authority that a tool call shows. A held call is refused with a 4-hex code. When Aaron types `approve <code>` (terminal or Remote Control), the identical call runs once within 30 minutes. Only his own typed prompts count; peers, schedules, task notifications, plugins and `claude -p` runs can't approve.

Held for Aaron's yes: Home Assistant deletes (`ha_remove_*`, `ha_config_remove_*`, `ha_config_delete_*`, `ha_delete_*`) and `ha_manage_*` delete, remove, uninstall or restore; `dockhand-api --write DELETE`; `arr-api` and `kuma-api` with `--allow-delete`; ZFS dataset and pool writes; SSH keys (`authorized_keys`, `ssh-copy-id`, key-changing `ssh-keygen`, writes under `~/.ssh`); `op` item changes; STANDARDS.md edits; writes to the guard's deployed copy or `~/.claude/settings.json`; `git push --force-with-lease`. Always denied: `--no-verify` (and `git commit -n`) and plain force pushes.

Verified live 2026-10-22 in a Remote Control session from the iOS app: `ssh-keygen --help` was held as 79dc, Aaron replied "Approve 79dc, then retry it", and the call ran once. (The ssh-keygen rule was narrowed afterwards, so that call no longer holds.)

## Decisions

- 2026-10-22: approval is by typed reply, not buttons. Tested with a throwaway mod: on Claude Code 2.1.286 neither the Desktop app nor the iOS app draws a mod's pane when attached to this VM's session over Remote Control (`$.session.surfaces()` returned none on both, no `session.attach` fired). Hooks run normally.
- 2026-10-22: HA Core restarts are not held: they're Tier 1 (Aaron, 2026-10-09).
- 2026-10-22: deletes are held even for items Claude created in the same session, stricter than the rule. Follow-up: [Let tier3-guard skip deletes of items Claude created in the same session](<Let tier3-guard skip deletes of items Claude created in the same session.md>).
- 2026-10-22: `ssh-keygen` is held only when it creates, changes, removes or reveals keys; `-l`, `-F` and usage calls run freely.
- 2026-10-22: network and exposure changes (firewall, DNS, Cloudflare, port forwards) have no single tool call to match, so they stay rule-only. The guard is a backstop, not all of Tier 3.

## Links

- Changes: [Added the tier3-guard mod](<../changes/2026-10-22 Added the tier3-guard mod to Claude Code on the ClaudeCode VM.md>), [Narrowed the ssh-keygen rule](<../changes/2026-10-22 Narrowed the tier3-guard ssh-keygen rule to key changes.md>)
- Commits: [25d963d](https://github.com/aaronspriggs/spriggs-homelab/commit/25d963d), [ce93d33](https://github.com/aaronspriggs/spriggs-homelab/commit/ce93d33)
- Source and tests: repo `claudecode-vm/mods/tier3-guard`
