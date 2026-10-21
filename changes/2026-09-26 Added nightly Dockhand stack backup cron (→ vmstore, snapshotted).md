---
date: 2026-09-26
type: config
system:
- '[[TrueNAS SCALE (Big Boi)]]'
- '[[Dockhand]]'
notion_id: 3e77ae76-22ba-815e-a5f2-e0ae9f89a82c
---

# Added nightly Dockhand stack backup cron (→ vmstore, snapshotted); deleted unused expired truenas_default certificate

**Stack backup:** `Big Boi/ix-apps` (holding Dockhand's stack definitions, including servarr's `.env` with the VPN secrets) had no snapshot task and can't be selected in the UI. Aaron added a TrueNAS cron job: root, daily 23:30, `rsync -a --delete --chmod=D700,F600 /mnt/.ix-apps/app_mounts/dockhand/data/stacks/ "/mnt/Big Boi/vmstore/dockhand-stacks-backup/"`. The destination is `vmstore`, not `BIGBOI`, because `BIGBOI` is exported as an SMB share (checked via the API) and would have exposed the `.env` secrets. `vmstore` is unshared and snapshotted daily for 30 days. Run Now verified by Claude via the read-only API: both stacks present, file sizes match the source, dir mode 700.
**Certificate:** the CRITICAL `truenas_default` expired alert (expired 2026-03-01) was for an **unused** cert. The UI serves `truenas-cert` (internal CA, valid to 2035), confirmed via `openssl s_client` against :9443. Aaron deleted `truenas_default`. The alert was still listed right after deletion; it should clear on TrueNAS's next alert check.
**Noted (not changed):** the NFS exports for `plex_content` and `plex_recordings` have no network restriction. The earlier notes said 192.168.1.0/24.
