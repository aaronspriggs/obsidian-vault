---
type: task
status: done
system:
- '[[ClaudeCode (VM)]]'
completed: 2026-11-17
---

## Outcome

Done 2026-11-17 ([change](<../changes/2026-11-17 Updated open work from Aaron's answers after the triage.md>)). Aaron deleted the read-only `kb-export` integration in Notion, which revokes its token; Claude had deleted the local copy (`~/.config/kb-export/notion-token`, `kb-export.json` and the directory) on 2026-11-15 on his yes ([change](<../changes/2026-11-15 Ran the first quarterly KB triage.md>)). The Notion archive stays readable through the claude.ai Notion connector. The vault's `.kb/migrate.py --dry-run` no longer works, which is fine: the migration finished on 2026-10-22.

## Decisions

- **2026-11-15: don't wait any longer for cross-checks.** The note had said to wait until the Notion archive was no longer needed. The archive stays readable through the claude.ai Notion connector, which doesn't use this token, and the only thing that did, `.kb/migrate.py --dry-run`, already lost its client when the kb-export script was removed from the VM in step 7 of the setup review. So the token was a credential with no reader.

## Links

![[Changes.base#For this project]]
