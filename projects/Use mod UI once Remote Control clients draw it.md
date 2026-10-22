---
type: idea
status: backlog
priority: low
system:
- '[[ClaudeCode (VM)]]'
---

# Use mod UI once Remote Control clients draw it

Aaron wants to use Claude Code mods more once their UI works over Remote Control (2026-10-22). On Claude Code 2.1.286, mod hooks work over Remote Control but nothing a mod draws (panes, buttons, toasts, status line) shows in the Desktop app or the iOS app. Tested with the `ui-test` mod, `$.session.surfaces()` returned none and no `session.attach` fired. Running Claude Code in the VM's own terminal over SSH would probably draw mod UI there, but that's untested.

## How to re-check

Ask Claude in a session to load the `plugin-authoring` skill and copy repo `claudecode-vm/mods/ui-test` into that session's dev-mods folder. Answer "Enable for this session" to the hot-reloading question, then send `/ui-test` from the Desktop app and from the phone. It's fixed when the reply names a surface instead of "none" and the "Mod UI test" pane appears with working buttons. Worth re-checking when Claude Code release notes mention Remote Control or plugins.

## Ideas for when it works

- `tier3-guard`: an approval card with Approve once / Deny buttons on top of the typed `approve <code>`. That needs no change to the hold logic. The mockup is in the claude.ai artifact "Tier 3 Guard Mockup".
- A session-start band showing `check.py --health`, the vault's last commits and the pull result, so the session-start routine runs as a script instead of costing tokens.
- A status line showing homelab maintenance mode and whether either repo has uncommitted or unpushed work.
