---
type: project
status: backlog
priority: medium
system:
- '[[Servarr Stack (Docker Compose)]]'
notion_id: 31b7ae76-22ba-8155-96c9-c1c7d1463786
---

## Goal

Design and build a full community-facing media request and notification ecosystem around the homelab stack. The vision is more than just external Seerr access — it's a Discord-centered hub where friends and family can request content, get notified when it's available, and feel like they're part of a curated streaming service.

## Scope

- How others expose Seerr to external users (native invite flow, Plex SSO)
- Discord bot integrations (Requestrr, etc.) bridging Discord → Seerr/Radarr/Sonarr
- Auto-posting to Discord channels when content is downloaded/available
- Notification design: what gets posted, what format, what channels
- Plex user invite management alongside request access
- Auth options: local accounts vs. Plex SSO for friends
- Moderation, per-user request limits, approval workflows
- Whether to expose Seerr directly (Cloudflare Tunnel?) or keep Discord as the only front door
- Optional future: new release alerts, "now trending on Plex" posts, watchlist integrations

## Architecture Options to Evaluate

### Option A — Seerr Native (Simple)

Invite friends as Plex SSO users, expose Seerr via Cloudflare Tunnel at a clean URL. They get a polished web UI. No Discord required.

### Option B — Discord Bot Only (Requestrr)

Users submit requests entirely via Discord slash commands. Bot forwards to Radarr/Sonarr or Seerr. Keeps everything inside Discord if that's already the social layer.

### Option C — Hybrid Hub (Full Vision)

Discord server as the front door + Requestrr for request submission + Seerr on the backend for approval/management + automated posting bots for download notifications, new arrivals, and library updates. This is the most complex and most scalable path.

## Automation Ideas (Brainstorm)

- **#now-available** channel: auto-post when Radarr/Sonarr completes a download (via webhook)
- **#new-to-plex** channel: post newly added content with poster art + Plex deep link
- **#requests** channel: Requestrr lives here; users submit and track their requests
- **#announcements**: manual posts for outages, new features, library milestones
- Radarr/Sonarr → webhook → Discord (native webhook support in both apps)
- Overseerr/Seerr also has notification webhooks — could post request status updates
- Tautulli (Plex analytics) can post "X is now playing" or "new content added" to Discord
- Bot could DM users when their specific request is fulfilled

## Open Questions

- Do friends/family actually want Discord, or is a simple link easier for them?
- Should this be invite-only to keep it curated?
- Approval flow: auto-approve everything, or queue for review?
- Cloudflare Tunnel vs. existing DDNS+port-forward for Seerr exposure
- Is Tautulli worth adding to the stack for the analytics/notification value?
- Seerr migration (Overseerr → Seerr fork) is complete as of 2026-03-05 — no dependency on this project.

## Notes

Intentionally scoped broad — this is a "build something cool and scalable" project, not a quick fix. Worth researching what the self-hosted community has built here before designing the architecture.
