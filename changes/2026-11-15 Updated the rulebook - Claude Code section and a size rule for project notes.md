---
date: 2026-11-15
type: doc
system:
- '[[ClaudeCode (VM)]]'
project:
- '[[Review and tune the Claude Code setup on the ClaudeCode VM]]'
---

# Updated the rulebook: Claude Code section and a size rule for project notes

## What changed

Three edits to [STANDARDS](<../STANDARDS.md>), approved by Aaron on 2026-11-15 after reviewing the diff (Tier 3):

- **How Claude Code works the KB** is rewritten. It names `CLAUDE.md` in the repo as the home of the working procedure and states the four KB rules: the session-start block (`check.py --session` through the SessionStart hook), lookups start from `check.py --map`, read every note the task touches in full and verify it live, and an open project's `next_step` and Status stand on their own for a fresh session. The old text told Claude to run `--health` by hand at session start and to "read only the notes the task needs".
- **Writing rules → Size** gains a rule for project notes: an open project note over about 2,000 words is slimmed the next time it's worked on. A finished step keeps one line and its change-note link, a settled decision keeps its outcome, reason and what was rejected, and a phase with its own plan becomes its own project note with `parent`.
- **Derived checks** gain "over-size note".

`.kb/check.py --health` now lists over-size notes (System notes over 1,500 words, open project notes over 2,000), and the session-start block counts them in its "Not listed here" line.

## Why

The Claude Code section predated the SessionStart hook and `--map`, and its "read only the notes the task needs" contradicted what Aaron agreed on 2026-11-15: read in full, don't carry stale context. Four active project notes were 2,500 to 7,200 words and the rulebook only had a size rule for System notes. Reasoning and rejected options are in the [setup review](<../projects/Review and tune the Claude Code setup on the ClaudeCode VM.md>), step 5.

## How

Edited in the vault with Aaron's yes (the tier3-guard holds edits to the rulebook). `check.py`: a `SIZE_WORDS` table, an "Over-size notes" list in the health report and a count in `print_session`. Over the limit is reported, never a commit error, so a long design session isn't blocked from committing.

## Verify / roll back

Verified 2026-11-15: `check.py --health` lists 8 over-size notes (5 open projects, 3 System notes), matching a separate word count; `check.py --session` is 6,517 characters and the full hook output 7,275, under the 10,000-character cap; a plain `check.py` run still exits 0. Roll back: revert the vault commit that carries this note.
