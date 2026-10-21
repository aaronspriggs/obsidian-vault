---
date: 2026-10-15
type: config
system:
- '[[TrueNAS SCALE (Big Boi)]]'
- '[[Plex Media Server]]'
- '[[ClaudeCode (VM)]]'
project:
- '[[Plan backup strategy for TrueNAS and VMs]]'
commit: https://github.com/aaronspriggs/spriggs-homelab/commit/4d8fb33
notion_id: 3fa7ae76-22ba-817d-aef7-f1baadde0f80
---

# B2 offsite phase 1: staging pre-script, Plex DB export and Cloud Sync task settings written (not yet live)

Claude's half of Layer 2 phase 1, in repo backup/ (README has the exact task settings). Design: two Cloud Sync tasks because the TrueNAS folder picker only multi-selects within one parent. 'B2 offsite: BIGBOI' (01:00) syncs Media Library, servarr, uptime-kuma, autokuma, plex_config. 'B2 offsite: vmstore' (01:15) syncs dockhand-stacks-backup and a new vmstore/offsite-staging, filled by the task's pre-script: TrueNAS config tar (freenas-v1.db via SQLite backup API plus pwenc_secret, replacing the planned separate cron), consistent copies of kuma.db and dockhand.db (gzipped) plus Dockhand's .encryption_key, and the Plex export. The pre-script fails the run if the Plex export is over 9 days old, so the alert goes through the existing TrueNAS relay. Plex: new claude-maint plex-db-export copies Plex's own newest 3-day DB backup and Preferences.xml to plex_recordings/.plex-db-export over the VM's existing rw NFS mount (no new share); triggered by plex-db-export.timer on the ClaudeCode VM, Sunday 23:00 Mountain (deployed and enabled). check-drift now diffs Cloud Sync pre-scripts (deployed.tsv host 'cloudsync'). Findings: dockhand.db is 2.19 GB (not a few MB), so the Dockhand cron widening became a gzipped DB copy in the pre-script instead; the existing stacks cron is unchanged. BIGBOI/plex_config was last modified March 2025 (leftover from the TrueNAS Plex app, not live Plex data). The Plex Databases dir is world-readable; only Preferences.xml needs root. 2026-10-15 20:03 UTC: Aaron installed claude-maint (4d8fb33); first plex-db-export via the systemd unit succeeded (27 MB, from Plex's 2026-10-13 backup). The file came out 777 because plex_recordings (NFSv4 ACL, passthrough) has inherit-only everyone@ MODIFY ACEs; not reachable by others since the .plex-db-export dir's effective ACL is owner-only, but fixed anyway with an explicit chmod 600 (commit 3dfa8eb, staged at /tmp/claude-maint on the Plex VM, awaiting Aaron's reinstall). vmstore is POSIX ACL, so the pre-script's umask 077 holds there. Pending: reinstall claude-maint, B2 account/bucket/key, the two tasks. Roll back: sudo systemctl disable --now plex-db-export.timer; previous claude-maint is the parent commit.
