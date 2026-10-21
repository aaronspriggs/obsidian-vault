---
date: 2026-09-28
type: fix
system:
- '[[Plex Media Server]]'
project:
- '[[Restore transcode tmpfs on the Plex VM]]'
notion_id: 3e97ae76-22ba-81f6-ad0f-d8f17cf1a490
---

# Restored /transcode tmpfs (8 GB) on the Plex VM

Re-added the missing tmpfs fstab entry and mounted /transcode; Plex already pointed its transcoder temp dir there, so transcodes had been hitting the 15 GB root disk.

**What:** Aaron appended `tmpfs /transcode tmpfs size=8G,mode=1777,nosuid,nodev,noexec 0 0` to `/etc/fstab` on the Plex VM and ran `sudo systemctl daemon-reload && sudo mount /transcode`.
**Why:** the entry had gone missing (found 2026-09-24), so Plex's transcoder temp directory `/transcode` was a plain folder on the 15 GB root LV.
**Verify:** `findmnt /transcode` shows tmpfs size=8388608k, rw,nosuid,nodev,noexec (Claude, 2026-09-28); `TranscoderTempDirectory="/transcode"` in Preferences.xml (Aaron's grep). Recheck after the next reboot.
**Roll back:** remove the fstab line, `sudo umount /transcode`.
