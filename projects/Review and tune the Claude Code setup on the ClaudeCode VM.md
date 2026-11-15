---
type: project
status: active
priority: medium
system:
- '[[ClaudeCode (VM)]]'
next_step: '2026-11-15: step 1 (session hook) done. Next: confirm in a new session that the hook block arrives whole, then step 2 (session length; Aaron decides the default model) and step 3 (tier3-guard Bash matching, Tier 3).'
---

## Goal

Review the whole Claude Code setup on this VM (settings, hooks, the tier3-guard mod, CLAUDE.md, memory, the KB tooling and how projects are organized) and fix what costs tokens, hides information or has drifted. Aaron asked for it on 2026-11-15 and wants each step checked as it goes, with the reasoning written down so later sessions know what was done and why.

## Status (2026-11-15)

Survey done, plan agreed by Aaron ("this all sounds good to me… let's do it"). Step 1 is done and deployed. Steps 2 to 8 are open; the split is three fresh sessions (1–3, 4–5, 6–8) because long sessions are the main token cost.

## Findings (measured 2026-11-15)

- **The session hook never arrived whole.** Claude Code caps hook stdout at 10,000 characters and replaces anything longer with a 2,000-character preview and a file path; no setting raises the cap ([hooks reference, "JSON output"](https://code.claude.com/docs/en/hooks)). All 13 hook records in the session transcripts since 2026-11-08 carry the preview; their outputs were 10,025 to 11,354 characters. The preview ended partway through open work, so the backlog list never reached context.
- **Long sessions are where the tokens go.** 68 transcripts hold 2.6 billion cache-read tokens; 12 sessions (320–750 turns each) account for 69%. 17 of 68 sessions ran past one calendar day. 98% of assistant turns were on Opus; the account is Claude Pro.
- **tier3-guard holds reads.** 15 holds on record (plus 3 hard denies): 9 were real automation deletes, 6 were read-only or unrelated Bash commands. The Bash check fires when a command writes anywhere and names a guarded path anywhere, and a `>` inside a quoted string counts as a write.
- **Docs drift.** STANDARDS.md "How Claude Code works the KB" predates the hook and `--map`; repo `README.md`, `claudecode-vm/README.md` and the `truenas-api` docstring still point at Notion; three System notes are over the 1,500-word limit.
- **CLAUDE.md and memory overlap.** Four memories restate CLAUDE.md rules, while guard approvals, maintenance mode and the `~/.local/bin` PATH gap are only in memory or the System note.
- **Active project notes are the KB read cost.** Four are 2,500 to 7,200 words; STANDARDS has a size rule for System notes only. Backlog: 43 notes, 17 of them ideas.
- **Unversioned files on a disk with no backup:** `~/rack-artifact/`, `~/work-claude-brief.md`, `~/homelab-agent/mockup*.html`, `out/gpu-plan/`, `.archive/`, `settings.local.json.bak`, two project skills never invoked.

Sound and left alone: `make check` clean, vault and repo pushed, memory symlinked into the repo, `truenas-api --write` has its own method allowlist.

## Plan

1. **Session hook fits the cap** (Tier 1). Done 2026-11-15, see [change](<../changes/2026-11-15 Trimmed the session-start hook to fit the 10,000-character cap.md>).
2. **Session length.** A text-only warning when context passes a threshold (the Cache Tax guard without keepwarm, from [the mods idea](<Consider nine Claude Code mods from a RoboNuggets video.md>)); default model policy is Aaron's call.
3. **tier3-guard Bash matching** (Tier 3: the guard's own code). Match the write target, not any mention of the path. Closes [this idea](<Stop tier3-guard holding Bash commands that only mention the rulebook.md>).
4. **CLAUDE.md rewrite**, reviewed by Aaron as a diff: retitle, fold stable memories in as one-liners, cut memory from 15 files to about 9.
5. **STANDARDS.md** (Tier 3): update the Claude Code section, add a size rule for project notes.
6. **Drift sweep:** READMEs, `truenas-api` docstring, the quarterly triage note, split the ClaudeCode System note.
7. **Loose files:** version or delete each; deletes need Aaron's yes.
8. **Backlog triage** (pulls [the quarterly triage](<Quarterly KB triage with Aaron (Deferred items and Ideas).md>) forward) and slim the four largest project notes.

## Decisions

- **2026-11-15, step 1: trim the output rather than tell Claude to read the saved file.** The cap can't be raised, and the docs say Claude Code doesn't ask Claude to read the file, so an instruction to read it would depend on the same kind of remembering that failed with `--map`. Rejected: splitting the output across several hooks (each is capped separately, but it adds moving parts for a list that fits in one).
- **2026-11-15, step 1: what was cut and why.** The by-System list repeated every active and blocked project already in open work, and repeated a project under each System it names (6.2 KB). Systems to verify and untested runbooks (1 KB) are upkeep, not something a task needs at its start, so they are now a count. Kept at full length: open work with next steps, since that is what stops a missed project. Result: 6,924 characters, all 18 open projects and all 43 backlog titles.
- **2026-11-15, step 1: the limit is enforced in code, not by a note.** `check.py --session` shortens next steps, then drops them, to stay under 8,500 characters, and the hook cuts itself with a warning at 9,800. A new project can't silently push it over again.
- **2026-11-15, step 1: cost accepted.** A backlog project that names several Systems is listed only under the first. The point of the list is spotting an existing project by title before proposing one; `check.py --map "<System>"` still lists it under every System.

## Open questions

- Default model for routine KB and ops work: Sonnet, with Opus for design and planning? Claude recommends yes; Aaron hasn't answered it on its own yet.
- Step 1 still needs its live check: the next new session should start with the whole block and no "Output too large" line.
