---
date: 2026-10-15
type: doc
system:
- '[[Dockhand]]'
project:
- '[[Dockhand - give Claude API access and build out Dockhand as the Docker platform]]'
notion_id: 3fa7ae76-22ba-81a1-8a18-d00145d81a95
---

# Closed the Dockhand platform project and updated the Dockhand system page

Project to Done with HTTPS/settings (Backlog Task) and Git stacks (Deferred Idea) split out; Dockhand page made current.

## What changed

- **Dockhand: give Claude API access and build out Dockhand** → Done 2026-10-15, collapsed to Outcome / Decisions / Links. Plan steps 1–3 were done: API access, update detection, and HA alerts via ha-dockhand. Step 5 (update policy) is already its own trial task.
- New items: "Serve Dockhand over HTTPS and review its settings" (Task, Backlog, Medium) from step 6, and "Move the servarr and uptime-kuma stacks to Dockhand Git stacks" (Idea, Deferred) from step 4. The second keeps the absolute-path and secrets prerequisites.
- **Dockhand system page:** user list now includes `homeassistant`. The stale lines "redeploy via the UI" and "Aaron stages the stack files" are replaced by the repo + API deploy. The HTTPS pointer and the pending-upgrade note are updated, and "Known behaviour" moved here from the project page.

## Why

The project's next step hadn't changed since 2026-10-01, and most of it was finished. Aaron agreed (2026-10-15) to close it and defer Git stacks: the repo + API push already makes git the source of truth, and migrating risks empty configs from relative volume paths.

## How

Live checks 2026-10-15 via `dockhand-api` (read-only): both stacks are `internal`, the update check is on and notify-only, the users are admin, claude and homeassistant. In the repo, servarr still has relative volume paths. Pre-edit page copy is in the session scratchpad; the weekly kb-export is the restore path.

## Verify / roll back

Both pages re-fetched and checked after editing. To roll back, set the project to Active and restore the body from the previous kb-export commit.
