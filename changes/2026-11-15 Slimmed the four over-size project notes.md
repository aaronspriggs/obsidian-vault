---
date: 2026-11-15
type: doc
system:
- '[[ClaudeCode (VM)]]'
project: '[[Review and tune the Claude Code setup on the ClaudeCode VM]]'
---

## What changed

The four open project notes over the rulebook's 2,000-word limit were slimmed, largest first, one commit each. Every dated decision stays in its note with its outcome, its reason and what was rejected. Research and working-out moved word for word into change notes, and one phase became its own project.

| Note | Words | Moved to change notes | Other |
| --- | --- | --- | --- |
| [Rebuild Big Boi](<../projects/Rebuild Big Boi into a new case with an HDD pool for bulk media.md>) | 7,167 → 1,949 | Six: [case specs and build log](<2026-10-26 Recorded the JMCD 12S4 case specs and an owner's build log.md>), [HBA and boards](<2026-10-25 Researched the HBA and boards for the Big Boi rebuild.md>), [power and PSUs](<2026-11-01 Researched backplane power and PSUs for the Big Boi rebuild.md>), [GPUs](<2026-10-28 Researched GPUs for the Big Boi rebuild (AV1 encode and local LLMs).md>), [pool layout](<2026-10-29 Worked out the HDD pool layout for the Big Boi rebuild (RAIDZ2 grown by expansion).md>), [platform swap](<2026-11-08 Compared a platform swap (LGA1700, AM4) with keeping the Designare and i9-9900.md>) | New project [Move the homelab into the 30U floor rack](<../projects/Move the homelab into the 30U floor rack.md>) with `parent` set to the rebuild; the patch panel and gear-sale projects now have it as `parent` |
| [Home security](<../projects/Plan a home security system (Alarmo, door-window sensors, siren).md>) | 3,660 → 1,975 | Two: [UniFi Protect research](<2026-10-27 Researched UniFi Protect's Home Assistant integration for the alarm plan.md>), [U400 unlock test and entry points](<2026-10-28 Tested the Aqara U400's unlock sources and researched the alarm's entry points.md>) | Table of what HA has re-checked live (HA 2026.11.0) |
| [Backup strategy](<../projects/Plan backup strategy for TrueNAS and VMs.md>) | 3,112 → 1,225 | Two: [the March design, UNAS Pro layout and dataset audit](<2026-03-07 Recorded the three-layer backup design, the UNAS Pro layout and the BIGBOI dataset audit.md>), [bucket estimate, sizes and phase 1 steps](<2026-10-23 Estimated the B2 bucket size after one week and recorded the Layer 2 sizes and phase 1 steps.md>) | Finished steps keep one line and a link to the change note that already existed; snapshot and Cloud Sync task state re-checked live; two older change notes got a link to the moved detail |
| [Patch panels](<../projects/Re-terminate and label the patch panels for the 30U rack.md>) | 2,537 → 1,657 | One: [map v4 to v12](<2026-11-15 Designed the patch panel map for the 30U rack (v4 to v12, Enterprise 48).md>) | Stale lines fixed (status said v6, goal said layout v15) |

Left in git history only, because a later version replaced it and nothing reads it: rack layout drafts v3 to v15 and the 2026-11-14 draft patch scheme (rebuild note, before commit e9a0e2b), corrections of wrong entries (the A380 first recorded as a Sparkle), and wording trimmed inside sentences. Stale state that belongs to a System note was dropped from the rebuild note with a pointer (the SSD pool's fill as of 2026-10-15, VM disk sizes).

Also changed: the UPS project's 2026-11-11 line points at the rack project and records the 2026-11-15 outlet plan; the rack project took the "rack top venting" open question from the patch panel note.

## Why

Step 8 of the setup review. A long note costs tokens on every read and hides the next step; Aaron's condition was that nothing he decided is lost.

## How

Sections were cut from the last committed version of each note by line number with a script and written into the change notes unchanged, so nothing was retyped. Each change note is dated when the research was done and says it was moved on 2026-11-15. The decisions were then rewritten by hand against the old text, one dated line at a time.

Rejected: one large change note dated today (six topics, longer than any note in the vault, the wrong date); a reference runbook (it would sit in untested runbooks for good); leaving the research in git history alone (the builds will need it, and it can't be found from the note).

## How to verify / roll back

`~/obsidian-vault/.kb/check.py --health` lists no project note as over-size. To see a note as it was: `git -C ~/obsidian-vault show e9a0e2b~1:"projects/<note>.md"` (the commit before the first slim). Rolling back is `git revert` of the four commits; nothing outside the vault changed.
