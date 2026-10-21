---
kind: troubleshooting
status: active
system:
- '[[Plex Media Server]]'
- '[[TrueNAS SCALE (Big Boi)]]'
last_tested: 2026-09-29
notion_id: 3087ae76-22ba-8136-84af-f11ce0989d41
---

Check, remount and troubleshoot the two NFS automounts on the Plex VM (/mnt/media ro, /mnt/dvr rw) from Big Boi.

## When to use

Plex shows empty or missing libraries, DVR recordings fail, or `/mnt/media` / `/mnt/dvr` on the Plex VM hangs or is empty. Also for rebuilding the mounts on a new VM.

## Current config (verified live 2026-09-29)

Two NFS v3 exports from Big Boi, both restricted to the Plex VM (TrueNAS export `hosts` = 192.168.1.116):
- `/mnt/Big Boi/BIGBOI/plex_content` → `/mnt/media`, read-only (Movies, TV Shows).
- `/mnt/Big Boi/BIGBOI/plex_recordings` → `/mnt/dvr`, read-write (DVR).
Both mount on first access through systemd automount, so boot never waits on TrueNAS. `/etc/fstab` on the VM (the space in "Big Boi" is written `\040`):
```plain text
192.168.1.248:/mnt/Big\040Boi/BIGBOI/plex_content /mnt/media nfs ro,vers=3,proto=tcp,resvport,_netdev,x-systemd.automount 0 0
192.168.1.248:/mnt/Big\040Boi/BIGBOI/plex_recordings /mnt/dvr nfs rw,vers=3,proto=tcp,resvport,_netdev,x-systemd.automount 0 0
```

## Prerequisites

SSH to the Plex VM (`ssh plex` as `claude`; root actions through `claude-maint`, or Aaron as `plexadmin`).

## Steps

**Step 1. Check the mounts:**
```bash
ls /mnt/media /mnt/dvr            # triggers the automount; expect Movies/ TV Shows/ ...
findmnt -t nfs -o TARGET,SOURCE,OPTIONS
```
**Step 2. Check Big Boi is serving:**
```bash
showmount -e 192.168.1.248        # both exports, 192.168.1.116
ping -c2 192.168.1.248
```
**Step 3. Remount if stale** (e.g. after Big Boi rebooted while the VM stayed up):
```bash
sudo umount -l /mnt/media /mnt/dvr
sudo systemctl restart mnt-media.automount mnt-dvr.automount
ls /mnt/media
```
**Step 4.** If the files are there but Plex still shows nothing, rescan the libraries in Plex ([http://192.168.1.116:32400/web](http://192.168.1.116:32400/web)).

## Common failures

- **"Access denied by server":** the export's `hosts` doesn't include 192.168.1.116 (e.g. the Plex VM changed IP). Fix the DHCP reservation or the export under TrueNAS Shares → NFS.
- **"No such file or directory":** the path's space isn't escaped (`\040` in fstab, quotes in a shell).
- **No route to 192.168.1.248:** the VM's NIC isn't on TrueNAS bridge `br0`; check the VM's NIC in TrueNAS and reboot the VM.
- **Plex writes to the DVR fail:** `/mnt/dvr` mounted read-only or the dataset's ownership changed; check with `findmnt /mnt/dvr` and `touch /mnt/dvr/.test`.

## Verify

`findmnt -t nfs` lists both mounts (media `ro`, dvr `rw`) and Plex libraries show content.

## Rollback

Nothing here changes config except a remount. If you edit fstab, copy it first (`sudo cp /etc/fstab /etc/fstab.bak-$(date +%F)`) and run `sudo systemctl daemon-reload && sudo mount -a` to test before rebooting.
