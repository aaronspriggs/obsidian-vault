---
date: 2026-10-16
type: doc
system:
- '[[ClaudeCode (VM)]]'
project:
- '[[Claude access model - more admin access, secrets management, account hardening]]'
commit: https://github.com/aaronspriggs/spriggs-homelab/commit/18def9c
notion_id: 3fb7ae76-22ba-810f-ab53-c8de47dea834
---

# Allowed tap-started, capped Claude fix runs (token-budget rule amended)

Aaron approved: no scheduled/self-starting Claude runs, but a run Aaron starts by tapping an HA alert action is allowed under wrapper-enforced caps (1 at a time, 3/day, max turns, max budget, Sonnet, fresh session).

## What changed

Claude Code's token-budget memory rule on the ClaudeCode VM now allows tap-started fix runs. Still no scheduled or self-starting Claude runs.

## Why

Plan 5 of the Claude access model project (one-tap fixes). The rule existed because unrequested runs spend Pro usage; a tap is per-incident and human-initiated. Aaron approved 2026-10-16.

## How

Caps, enforced by the VM wrapper rather than Claude: one run at a time, max 3 per day, `--max-turns`, `--max-budget-usd`, Sonnet by default, a fresh session per run (never injected into the Remote Control session). Deterministic fixes stay plain HA/VM actions with no Claude. Memory file versioned in commit [18def9c](https://github.com/aaronspriggs/spriggs-homelab/commit/18def9c). KB Standards needed no change: Tier 2 already covers unattended alert-driven actions and the guardrails already limit a tap to that alert's designed fix.

## Verify / roll back

`claudecode-vm/claude/memory/feedback_token_budget.md` in the repo. Roll back by reverting 18def9c.
