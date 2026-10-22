---
kind: recovery
status: active
system:
- '[[TrueNAS SCALE (Big Boi)]]'
repo: https://github.com/aaronspriggs/spriggs-homelab/tree/main/backup
notion_id: 3fb7ae76-22ba-81d0-a8b0-f8b71a952427
---

Reinstall TrueNAS on Big Boi and bring back its config (network, users, shares, VMs, tasks, API keys, B2 credential) from the nightly config export, either onto the surviving pool (boot drive lost) or onto a new pool (pool lost, data from B2). Aaron does the console and UI work; Claude verifies over the API once the keys work again.

## When to use

Big Boi's TrueNAS install is gone or Big Boi is new hardware: the boot NVMe died, a TrueNAS upgrade left it unbootable (try the previous boot environment from the GRUB menu first), or the box was lost or rebuilt. It's step 1 of [Disaster recovery - rebuild order (index)](<Disaster recovery - rebuild order (index).md>); every VM and app depends on it. Two cases:
- **Case 1, pool intact** (boot drive or OS lost): reinstall, upload the config, and the pool, VMs, apps and shares come back as they were. About 1 hour.
- **Case 2, pool lost** (disks dead, fire, theft): reinstall, upload the config, make a new pool, restore data from B2, then rebuild the VMs from their runbooks. Most of a day. **Untested**: how TrueNAS treats a config that names a pool which no longer exists isn't documented, so expect some fixing up (step 6).
Desk-checked against the live system on 2026-10-16 (TrueNAS 25.04.2.6); not yet test-rebuilt.

## What comes back from where

| Item | Source |
| --- | --- |
| Network (`br0` on `enp1s0`, 192.168.1.248/24, gw/DNS 192.168.1.1), users (`truenas_admin`, `aspriggs`, `claude-readonlyapi`, `claude-maint`) and their API keys, NFS/SMB shares, snapshot tasks, Cloud Sync tasks and the B2 credential, the stacks cron job, VM definitions, Dockhand app settings, certificates (`truenas-ca`), UPS (NUT client of 192.168.1.12), timezone | The TrueNAS config: `truenas-config.tar` (`freenas-v1.db`  • `pwenc_secret`, which decrypts the stored secrets), written nightly to `vmstore/offsite-staging` and uploaded to B2 `/vmstore/offsite-staging` |
| Pool data, zvols, `ix-apps` | Case 1: the pool itself. Case 2: B2 (small set only, see the B2 runbook) and the VM runbooks |
| Bulk media (`plex_content`), DVR recordings | Case 2: not backed up; re-download through Seerr |
| Scripts deployed on TrueNAS (Cloud Sync pre-script) | Inside the config; also repo `backup/cloudsync-vmstore-prescript.sh` |

## Prerequisites

- TrueNAS SCALE ISO on a USB stick: **25.04 (Fangtooth), the latest point release** (live was 25.04.2.6). A config can be uploaded to the same or a newer version, never an older one. Upgrade trains only after the rebuild passes Verify.
- 1Password: **TrueNAS - Admin** and **Backblaze B2 - truenas-bigboi** (keyID, applicationKey, encryption password and salt).
- A Mac with `rclone` (`brew install rclone`), for getting the config from B2 without TrueNAS.
- Keyboard and monitor on Big Boi (or the board's console) for the installer.
- Case 2: new disks for the pool.

## Steps

1. **Get the config** (*Aaron*, on the Mac). Use the newest copy you can reach:
    - Case 1, after step 3: it's on the pool. `ssh truenas_admin@192.168.1.248 "sudo cat '/mnt/Big Boi/vmstore/offsite-staging/truenas-config.tar'" > truenas-config.tar` (turn on SSH with password login in the fresh install first).
    - Otherwise from B2: `rclone config` to create a `b2` remote (keyID, applicationKey) and a `crypt` remote named `bb` on `b2:spriggs-bigboi-backup/vmstore` with filename encryption **off**, directory name encryption **false**, and the password and salt from 1Password. Then `rclone copy bb:offsite-staging/truenas-config.tar .` The same is in step 6 of [Offsite backup to B2 - what's covered and how to restore](<Offsite backup to B2 - what's covered and how to restore.md>).
    Check it: `tar -tf truenas-config.tar` lists `freenas-v1.db` and `pwenc_secret`.
2. **Install TrueNAS** (*Aaron*) onto the boot NVMe (Patriot P300 128 GB, or its replacement). Choose "Administrative user (truenas_admin)" and any temporary password; the config replaces it. In Case 1, **don't** select the pool's SSDs as the install target.
3. **Temporary network** (*Aaron*, console menu → Configure network interfaces): give `enp1s0` (the 10 GbE port cabled to the USW Pro Max) static 192.168.1.248/24, gateway 192.168.1.1. On new hardware the NIC may have another name; use whichever port is cabled. Open [https://192.168.1.248](https://192.168.1.248/) (the custom port 9443 returns with the config).
4. **Upload the config** (*Aaron*): System → General Settings → Manage Configuration → Upload File → `truenas-config.tar`. TrueNAS reboots. Log in as `truenas_admin` with the 1Password password at [https://192.168.1.248:9443](https://192.168.1.248:9443/).
5. **Case 1:** the pool `Big Boi` imports on boot (if not: Storage → Import Pool), VMs and Dockhand start (autostart), shares come back. Go to step 7.
6. **Case 2 (pool lost):** the config still names the old pool, now missing.
    1. Storage: if the old `Big Boi` shows as offline or unavailable, Export/Disconnect it with **"Delete saved configurations" unchecked**, so shares, tasks and VM definitions stay.
    2. Create the new pool named exactly `Big Boi` (paths like `/mnt/Big Boi/...` are what shares, tasks and the Cloud Sync pre-script use). If HDDs and SSDs both exist by then (the planned rebuild), the SSD pool keeps the name `Big Boi`.
    3. Recreate the datasets: `vmstore` (POSIX ACL, ACL mode Discard), `BIGBOI` (SMB preset), `BIGBOI/plex_content`, `BIGBOI/plex_recordings`, and `vmstore/offsite-staging` (`mkdir -m 700` is enough). Re-apply the `apps` group ACL on `BIGBOI` and `plex_content` (System page, ACLs).
    4. Check that every share, snapshot task, Cloud Sync task and the cron job points at a path that exists; fix any that TrueNAS disabled. **Disable both B2 Cloud Sync tasks** until the restore is done: they're PUSH/SYNC, and a run against an empty pool would mirror the deletions to B2. B2 keeps old versions for 30 days, but don't rely on it.
    5. Apps → choose pool `Big Boi`. If Dockhand doesn't come back, install it again, then restore its DB, key and stacks per step 4 of the B2 runbook.
    6. Restore the rest from B2 (Uptime Kuma, Seerr, Media Library) per the B2 runbook, then rebuild the VMs: ClaudeCode, then Home Assistant, then Plex (DR index order). Re-enable the Cloud Sync tasks only after that.
7. **New hardware only:** PCI and USB addresses may change. Fix the Plex VM's iGPU device (it was `pci_0000_00_02_0`), the HA VM's Zigbee USB device ("CP210x UART Bridge", it was `usb_1_5`) and `br0`'s member port (Network), then start those VMs.
8. **Hand over to Claude**: the API keys come back with the config, so `truenas-api system.info` from the ClaudeCode VM should work as soon as that VM is up. If it doesn't (key revoked, config rebuilt by hand), *Aaron* issues new keys per [TrueNAS API access (read-only + maintenance writes) and alert relay (ClaudeCode VM)](<TrueNAS API access (read-only + maintenance writes) and alert relay (ClaudeCode VM).md>).

## Verify

Claude, over `truenas-api`, unless marked:
- `system.info`: expected version; `pool.query`: `Big Boi` ONLINE and healthy; no new alerts (`alert.list`) beyond the known ZFS feature-flag notice.
- `vm.query`: HomeAssistant, Plex and ClaudeCode RUNNING with autostart; `app.query`: `dockhand` RUNNING.
- `sharing.nfs.query`: both exports enabled, hosts 192.168.1.116; the Plex VM sees `/mnt/media` and `/mnt/dvr`.
- `pool.snapshottask.query`: both daily tasks enabled; `cloudsync.query`: both B2 tasks enabled (Case 2: only after the restore); `cronjob.query`: the stacks rsync job.
- `make -C ~/homelab check`: the `cloudsync:` pre-script line is `ok`.
- After the next 01:15 run: both Cloud Sync tasks SUCCESS (the pre-script fails if the Plex export is over 9 days old, which is expected right after a Plex rebuild).
- *Aaron*: SMB share `BIGBOI` opens from the Mac; the UPS shows on the dashboard.
- Uptime Kuma all green; HA Home Health clear. Log the rebuild as a change note and update the Big Boi System page (version, hardware, boot device).

## Rollback

Case 1 doesn't write to the pool's data, and the old boot drive (if it still works) can simply be put back. The config upload only replaces the new install's config; to undo it, reinstall and upload a different `truenas-config.tar` (B2 keeps 30 days of versions). Never upgrade the pool's ZFS feature flags during a rebuild: it's one-way and blocks going back to an older TrueNAS.
