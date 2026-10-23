---
date: 2026-10-23
type: config
system:
- '[[ClaudeCode (VM)]]'
project:
- '[[Let tier3-guard accept a plain yes and several codes at once]]'
commit: https://github.com/aaronspriggs/spriggs-homelab/commit/0cea432
---

# tier3-guard accepts a plain yes and several codes per approve

**What changed:** [hooks/register.ts](https://github.com/aaronspriggs/spriggs-homelab/blob/main/claudecode-vm/mods/tier3-guard/hooks/register.ts) has two new approval paths, both only from Aaron's own prompts (terminal or Remote Control). (1) `approve <code> <code> …` releases each listed code; commas, "and" and a repeated "approve" all work. (2) A plain yes (the message opens with yes, yup, yeah, ok, sure, go ahead, do it, approve, works for me, 👍 and similar, and contains no no, not, don't, wait, hold, stop, but, except, instead or unless) releases every call held since his previous prompt. It also lets Tier 3 calls run without a code until the next prompt of any origin, or 30 min at most. Peer, scheduled, task-notification and SDK prompts never approve and end an open yes. Hard denies are unchanged. Two new state keys: `consentAt` and `lastPromptAt`.

`~/homelab-agent/.claude/settings.local.json` gained Aaron's allow rules `Edit(//home/aspriggs/homelab/claudecode-vm/mods/**)` and `Edit(//home/aspriggs/.claude/mods/**)`, so Claude can edit mod source and the deployed copy in auto mode. The deployed copy is still held by the guard.

**Why:** Aaron, 2026-10-23: a single yes is enough. Approving five deletes had taken three messages.

**How:** Claude edited the repo and ran `claude plugin validate` (passed) and `claude plugin test` (74 pass, 27 of them new). The auto mode classifier blocked Claude from committing and deploying a change to its own approval gate and permission rules, so Aaron ran the commit, push and `install -m 644` of `register.ts` and `types/index.d.ts` into `~/.claude/mods/tier3-guard/` over SSH. `make check` showed all four guard files and settings.local.json `ok`.

**Verify / roll back:** the next Tier 3 call after Aaron's yes runs without a code. Roll back by reverting 0cea432 and re-installing the two files.
