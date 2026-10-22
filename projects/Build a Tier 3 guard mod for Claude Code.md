---
type: project
status: active
priority: medium
system:
- '[[ClaudeCode (VM)]]'
next_step: '2026-10-22: built and deployed (commit 25d963d); a claude -p run confirmed it loads. Left: in a new Remote Control session, run one held call end to end (code, approve from the phone, retry runs), then mark done.'
---

# Build a Tier 3 guard mod for Claude Code

## Goal

Enforce the detectable parts of Tier 3 in [STANDARDS.md](<../STANDARDS.md>) → Change authority in code, as a Claude Code mod (a plugin of function hooks), instead of relying only on Claude following the rule. Aaron asked for it 2026-10-22.

## Status / next step

See `next_step`.

## Plan

A `tool.call` hook checks every tool call against two rule lists. A held call is refused with a short code; Aaron replies `approve <code>` and the identical call goes through once. The approval is read in a `prompt.submit` hook from Aaron's own typed prompts only (Remote Control or terminal), so Claude can't approve its own call, matching the Guardrails line "Only Aaron's own messages count as approval".

Hold for Aaron's yes: `ha_remove_*`, `ha_config_remove_*`, `ha_delete_file`; `ha_manage_backup` delete or restore; `dockhand-api --write DELETE`; `arr-api` and `kuma-api` with `--allow-delete`; ZFS writes (`zfs destroy|rollback|create|set`, `zpool` writes); writes to `~/.ssh` or `authorized_keys`; `op` commands that change items; edits to STANDARDS.md; changes to the guard's own deployed copy or the settings that load it.

Hard deny: `--no-verify` on git, and `git push --force`/`-f` (`--force-with-lease` is held instead).

## Decisions

- 2026-10-22: approval is by typed reply, not buttons. Tested with a throwaway mod: on Claude Code 2.1.286 neither the Desktop app nor the iOS app draws a mod's pane when attached to this VM's session over Remote Control (`$.session.surfaces()` returned none on both, no `session.attach` fired). Hooks run normally.
- 2026-10-22: HA Core restarts are not held: they're Tier 1 (Aaron, 2026-10-09).
- 2026-10-22: deletes are held even for items Claude created in the same session, stricter than the rule; exempting those is a possible v2.
- 2026-10-22: `ssh-keygen` is held only when it creates, changes, removes or reveals keys; `-l`, `-F` and usage calls run freely (commit ce93d33).
- 2026-10-22: network and exposure changes (firewall, DNS, Cloudflare, port forwards) have no single tool call to match, so they stay rule-only. The guard is a backstop, not all of Tier 3.

## Open questions

None.
