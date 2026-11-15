---
type: task
status: done
system:
- '[[ClaudeCode (VM)]]'
completed: 2026-11-15
---

## Outcome

Done 2026-11-15, on Aaron's yes (Tier 3; [change](<../changes/2026-11-15 Allowed deprecated on project notes and dropped seven backlog notes.md>)). `deprecated` is now an allowed status for project notes in the rulebook's property table and in `.kb/check.py`, and the "Open for this system" view hides it. The seven notes Aaron agreed to drop at the [first quarterly triage](<../changes/2026-11-15 Ran the first quarterly KB triage.md>) are deprecated, each with its reason and, for three, `superseded_by`. The gap existed because the Lifecycle section and the triage note both described dropping a note this way while the table and the checker didn't allow it, and no project note had ever been dropped.

## Decisions

- **2026-11-15: ask, don't work around.** Rejected: marking the seven `done` (they weren't done, and a later search for finished work would find them), changing `check.py` without the table it enforces, and editing the rulebook on the strength of "Yes to all", which answered a different question.

## Links

![[Changes.base#For this project]]
