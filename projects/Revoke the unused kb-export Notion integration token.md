---
type: task
status: active
priority: low
system:
- '[[ClaudeCode (VM)]]'
next_step: '2026-11-15: Aaron removes the kb-export integration at https://www.notion.so/profile/integrations (the token stays valid until he does). Claude then marks this done.'
---

## Goal

Remove the read-only Notion integration `kb-export` and its token now that the KB lives in the vault and kb-export is retired (2026-10-22).

## Status (2026-11-15)

Half done. At the quarterly triage Aaron approved the local half (Tier 3) and Claude deleted `~/.config/kb-export/notion-token`, `kb-export.json` and the then-empty directory ([change](<../changes/2026-11-15 Ran the first quarterly KB triage.md>)). The integration itself still exists in Notion until Aaron removes it; only he can.

## Decisions

- **2026-11-15: don't wait any longer for cross-checks.** The note had said to wait until the Notion archive was no longer needed. The archive stays readable through the claude.ai Notion connector, which doesn't use this token, and the only thing that did, `.kb/migrate.py --dry-run`, already lost its client when the kb-export script was removed from the VM in step 7 of the setup review. So the token was a credential with no reader.
