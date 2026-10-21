---
type: task
status: done
priority: medium
system:
- '[[Plex Media Server]]'
completed: 2026-09-28
notion_id: 3e97ae76-22ba-81d8-849f-dc471318290d
---

# Restore /transcode tmpfs on the Plex VM

Done 2026-09-28. Aaron added the fstab line and mounted it; Claude verified: /transcode is tmpfs 8.0G (rw,nosuid,nodev,noexec), one fstab entry, Plex TranscoderTempDirectory="/transcode" (per Aaron's grep). Survives reboot via fstab; confirm on the next homelab-update reboot.

## Goal

Restore the `/transcode` RAM disk described on [Plex Media Server](<../systems/Plex Media Server.md>): tmpfs, 8 GB, `mode=1777,nosuid,nodev,noexec`, and Plex's transcoder temp directory set to `/transcode`.

## Status (2026-09-28)

Checked live: `/etc/fstab` has no tmpfs line; `/transcode` exists and is empty, so mounting over it hides nothing; the VM has 12 GB RAM with about 11 GB free at idle, so an 8 GB cap leaves room for Plex even when the disk is full. tmpfs only uses RAM for what's actually written. `claude-maint` has no mount or fstab subcommand, so this needs Aaron's sudo.

## Steps (Aaron, from the Mac, while nothing is playing)

```bash
ssh plexadmin@192.168.1.116
echo 'tmpfs /transcode tmpfs size=8G,mode=1777,nosuid,nodev,noexec 0 0' | sudo tee -a /etc/fstab
sudo systemctl daemon-reload && sudo mount /transcode
findmnt /transcode
sudo grep -o 'TranscoderTempDirectory="[^"]*"' "/var/lib/plexmediaserver/Library/Application Support/Plex Media Server/Preferences.xml"
```
The last command should print `TranscoderTempDirectory="/transcode"`. If it prints nothing, set it in Plex → Settings → Transcoder → Show Advanced → Transcoder temporary directory = `/transcode`, then save.

## Verify (Claude)

`findmnt /transcode` shows tmpfs 8G; it survives the next reboot; a transcode writes chunks under `/transcode`.

## Rollback

Delete the fstab line, `sudo umount /transcode`.

## Changes

![[Changes.base#For this project]]
