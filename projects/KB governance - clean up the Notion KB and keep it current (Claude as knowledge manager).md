---
type: project
status: done
priority: high
system:
- '[[ClaudeCode (VM)]]'
completed: 2026-09-29
notion_id: 3e87ae76-22ba-8143-ae0e-fbfade1e93ae
---

# KB governance: clean up the Notion KB and keep it current (Claude as knowledge manager)

Done 2026-09-29: KB audited and rewritten as current state, one rulebook (KB Standards) for both Claudes, weekly no-AI export + [HEALTH.md](http://health.md/). Upkeep is routine; quarterly triage is its own Backlog task.

## Outcome

Done 2026-09-29 (started 2026-09-27). The KB had drifted as the homelab grew: System pages had become diaries with superseded layers, to-dos lived in both "Known Gaps" and Projects, the homepage was six months stale, real systems had no page, a third of the Changes had no System, and nothing backed the KB up. Now:
- **Safety net:** weekly `kb-export` (read-only Notion token, no AI) commits every page to the `kb-export` branch of spriggs-homelab, runs gitleaks, and writes `HEALTH.md` (missing properties, stalled projects, unverified Systems, untested runbooks). Kuma push monitor "KB Export" watches it. Repo `kb-export/`.
- **One rulebook for both Claudes:** [KB Standards](<../STANDARDS.md>) (operating model, page skeletons, required properties, secrets policy, lifecycle, edit safety). `CLAUDE.md` is versioned in the repo and links to it; the Cowork project instructions point at it too.
- **Schema:** Systems `Status`/`Runs On`/`Last Verified`/`Repo`; Projects `Parent`/`Next Step`/Backlog status; Changes `Commit`/`Project`; Runbooks `Last Tested`/`Repo`; derived `Stalled`/`Needs Verification`/`Untested`/`Recent` formulas.
- **Audit and rewrite:** every System page checked live (TrueNAS API, ha-mcp, SSH, UniFi API) and rewritten as current state with a live Open work view; Home Health split out of HA OS; new pages for Uptime Kuma, UPS 2U, Home Health and the repo; homepage rewritten; all property gaps backfilled; stubs written or deprecated; orphan pages merged; long Done projects collapsed and buried follow-ups extracted. No secrets found.
Ongoing upkeep is in KB Standards and `CLAUDE.md` (read `HEALTH.md` at session start, write in the same turn, rewrite rather than append, bump `Last Verified`/`Last Tested`). Quarterly triage: Task "Quarterly KB triage with Aaron".

## Decisions

- **2026-09-27: Notion stays the only source of truth; git export is the backup.** Notion is on the Free plan (limited page history). The export goes to an orphan branch of the existing repo, not a new repo; on a gitleaks hit it skips the commit and alerts.
- **2026-09-27: governance must cost near-zero AI tokens** (Claude Pro). Everything mechanical (export, lint, secrets scan) is a plain script on a timer; no unattended Claude runs; audits read the local export with grep instead of fetching pages.
- **2026-09-27:** 1Password holds all passwords/secrets; Proton Authenticator holds all TOTP codes.
- **2026-09-27:** Home Health split into its own System; empty runbooks: write the Big Boi Reboot Checklist, deprecate "Home Assistant Recovery", "Plex VM Restart / Recovery" and the VS Code workflow page.
- **2026-09-28:** stalled-but-wanted projects move to a new **Backlog** status instead of Deferred (7 moved).
- **2026-09-28:** no UI filters on the time-based views: Aaron doesn't browse them, and the API can't filter on formulas; `HEALTH.md` is the working list.
- **2026-09-29:** orphan top-level pages are merged into the matching Projects entry, retitled `[DEPRECATED]` and moved under it.

## Links

Changes: phases 1, 2, 3 (kb-export fix + audit), Backlog status, phase 4 parts 1, 2a, 2b, 3a, 3b (all linked in the Changes relation). Commits: kb-export cd94671, a2c8c86, 6ea7299, 65bc103; [CLAUDE.md](http://claude.md/) 9e10db8. Full plan, phase-by-phase status and the 2026-09-28 audit table: KB export commit 726d914.

## Changes

![[Changes.base#For this project]]
