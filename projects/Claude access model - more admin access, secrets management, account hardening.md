---
type: project
status: done
priority: high
system:
- '[[ClaudeCode (VM)]]'
completed: 2026-10-17
notion_id: 3ee7ae76-22ba-81b6-9b7d-e716632d23f3
---

# Claude access model: more admin access, secrets management, account hardening

Started 2026-10-03. Aaron wants to move from per-change approval to a middle ground: Claude holds admin access to most tools, consults on destructive changes, and can fix things from a one-tap HA alert. The cost is that the ClaudeCode VM and Aaron's Claude account become the keys to the kingdom, so secrets handling and account security come first.

## Outcome (Done 2026-10-17)

Claude holds standing admin access to the homelab tools, gated by reversibility rather than by system, and can fix problems from a one-tap HA alert without Aaron opening a session.
1. **Secrets:** a read-only 1Password service account (`claudecode-vm`) on vault `Homelab - Claude`; the VM keeps only its token, and wrappers fetch credentials with `op read` (`homelab-secret`). Aaron stores and rotates every credential.
2. **Account hardening:** Claude account sign-in is the Gmail magic link, so the Gmail account carries the protection (decision below).
3. **Change authority:** three tiers in [KB Standards](<../STANDARDS.md>) → Change authority and in [CLAUDE.md](http://claude.md/), with matching allow rules in `claudecode-vm/claude/settings.local.json`.
4. **Rebuild runbooks:** [Disaster recovery - rebuild order (index)](<../runbooks/Disaster recovery - rebuild order (index).md>) plus rebuild runbooks for the ClaudeCode VM, Plex VM, Home Assistant and Big Boi, all desk-checked against live config (2026-10-16). None is test-rebuilt; [HEALTH.md](http://health.md/) flags them as untested until one is. The ClaudeCode VM's memory and allow rules are now versioned in the repo.
5. **One-tap fixes:** `claude-fix` on the ClaudeCode VM (listener + capped wrapper; see the [ClaudeCode (VM)](<../systems/ClaudeCode (VM).md>) page and repo `claudecode-vm/` README "Fix runs"). Pilot runbook [Fix run - servarr health alerts (Sonarr, Radarr, Prowlarr, Gluetun)](<../runbooks/Fix run - servarr health alerts (Sonarr, Radarr, Prowlarr, Gluetun).md>). Tested 2026-10-17 on a real `sonarr_health` alert: tap → run restarted NZBGet → `FIXED`, 18 turns, $0.47; a no-op run costs $0.16. Caps: one run at a time, 3 per rolling 24 h, Sonnet, 30 turns, $1.00 budget, 20 min. More alerts get the button as their fix runbooks are written (alerting runbook, "Buttons on alerts").
6. **Alerting cleanup found during the test:** one alert per NZBGet/Gluetun outage, Restart on Kuma down alerts for Big Boi containers, "medium" push wording, a `reminder_message` default and a "👆 Tap to …" action line on actionable pushes. Rules are in [Homelab alerting - add or change a monitor or alert (Kuma + Alert2)](<../runbooks/Homelab alerting - add or change a monitor or alert (Kuma + Alert2).md>).

## Decisions

- **2026-10-03 (Aaron): the middle ground.** Claude can hold admin-level access to the homelab tools. Gate actions by reversibility and blast radius, not by system: Claude acts and logs routine reversible actions, says before taking anything that briefly takes a shared service down, and gets an explicit yes for destructive or irreversible actions every time. Reason: the setup is self-contained, and few people have access to it. An alert that only says "something's broken" isn't much use if fixing it still means opening another Claude session.
- **2026-10-03 (Aaron): HA having more power is acceptable.** Settled the Dockhand alerting choice in favour of ha-dockhand (done 2026-10-07, [Monitoring - Dockhand container alerts to HA via ha-dockhand](<Monitoring - Dockhand container alerts to HA via ha-dockhand.md>)).
- **2026-10-05 (Aaron): secrets go in a dedicated 1Password vault** (Families plan) that a service account can only read. Read-only for now: Claude hands Aaron any new credential to save, and Aaron rotates them. Revisit write access if Claude ever needs to rotate credentials itself. Families limits: 1,000 reads/hr per token, 1,000 requests/day per account, so timers keep a local config or cache instead of fetching every run.
- **2026-10-05: Claude account sign-in is the email magic link.** Whoever controls the Gmail account controls the Claude account, so it's one factor. Anthropic doesn't document authenticator-app 2FA for personal accounts; protect the Gmail account with a passkey or hardware key.
- **2026-10-16 (Aaron): plan 4 scope.** A short DR index plus rebuild runbooks (ClaudeCode VM, Plex VM, Home Assistant, Big Boi), desk-checked, not test-rebuilt; `Last Tested` only where a real restore was done.
- **2026-10-16 (Aaron): fix-run design.** Still no scheduled or self-starting Claude runs; a tap-started fix run is allowed under caps enforced by the VM wrapper, not by Claude (one at a time, 3/day, max turns, max budget, Sonnet, fresh session per run). Deterministic fixes get a plain HA button with no Claude at all; a Claude run is only for fixes that need diagnosis. HA sends only the alert ID; the VM maps it to a runbook from a fixed allowlist, so alert text can't inject instructions, and the run may use only the tools that runbook names. Not chosen: Claude Code channels (research preview, events land in the long-running session) and a tap that opens a pre-filled chat (Remote Control has no prefill link).
- **2026-10-17 (Aaron): project closed** without waiting on two items: the arr-health dependency suppression gets validated when a real NZBGet/Gluetun outage happens, and the rebuild runbooks stay untested ([HEALTH.md](http://health.md/) tracks them). EasyAudioEncoder needed no record: Plex downloads it itself (checked 2026-10-17; noted in the Plex rebuild runbook).
- **2026-10-17 (Aaron): the KB export stays as the KB's weekly text backup and health check.** Claude uses it only for [HEALTH.md](http://health.md/), page-ID lookup and restores, never for page content (KB Standards → Who does what; [CLAUDE.md](http://claude.md/), commit 85ec9c7). Answers the 2026-10-03 follow-up after Claude twice read stale export copies.

## Links

Changes: see the `Changes` relation (21 entries, 2026-10-05 to 2026-10-17). Key commits: b86831c (claude-fix), 3d7323c (pilot allowlist), d794d85 (HA button), cad96d1 and 7cff08d (budget, push format), 7ac2d66, 60d1c84 and 3e1ae09 (alert wording and action line), 85ec9c7 (export rule). Follow-up task: [Serve Dockhand over HTTPS and review its settings](<Serve Dockhand over HTTPS and review its settings.md>) (Backlog; also covers ha-mcp HTTPS).

## Changes

![[Changes.base#For this project]]
