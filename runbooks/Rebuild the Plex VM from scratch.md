---
kind: recovery
status: active
system:
- '[[Plex Media Server]]'
- '[[TrueNAS SCALE (Big Boi)]]'
repo: https://github.com/aaronspriggs/spriggs-homelab/tree/main/plex-vm
notion_id: 3fb7ae76-22ba-816b-bbaa-f32b6608b44d
---

Rebuild the Plex VM when its zvol is lost or a snapshot rollback can't help. The VM disk isn't backed up: the OS and config come back from the repo, and Plex's library DB and Preferences.xml from the weekly export (local on plex_recordings, or B2). Aaron runs the root steps; Claude handles the rest over `ssh plex`.

## When to use

The Plex VM is gone or unusable: the zvol `vmstore/Plex-9wert` was lost, the VM won't boot, or Big Boi itself was rebuilt. If the zvol is intact and the problem is under 30 days old, roll back the daily `vmstore` snapshot instead (Rollback in [Updating the Plex VM (OS + Plex)](<Updating the Plex VM (OS + Plex).md>)): it's faster and keeps everything. Media and DVR recordings live on NFS and aren't touched by any of this. The VM disk is **not** in B2, so the VM is rebuilt: OS and config from the repo, Plex's library DB and `Preferences.xml` from the weekly export. Restoring `Preferences.xml` keeps the same server identity and claim, so clients and the Plex account see the same server. Expect about 1-2 hours. Desk-checked against the live VM and its TrueNAS definition on 2026-10-16; not yet test-rebuilt.

## What comes back from where

| Item | Source |
| --- | --- |
| VM, Ubuntu, user `plexadmin` | [Creating a Cloud-Init Seeded Linux VM on TrueNAS SCALE](<Creating a Cloud-Init Seeded Linux VM on TrueNAS SCALE.md>), with the settings in step 1 |
| NFS mounts, `/transcode` tmpfs | fstab lines in step 2 (same as [Plex VM NFS Mount Setup & Troubleshooting](<Plex VM NFS Mount Setup & Troubleshooting.md>)) |
| `claude-maint`, `homelab-update`, apt timer overrides, unattended-upgrades Plex origin | Repo `plex-vm/` and `homelab-update/` (all in `deployed.tsv`) |
| Plex library DB + blobs DB, `Preferences.xml` (claim, server identity, transcoder settings) | `plex-db.tar.gz`: on `plex_recordings/.plex-db-export/` if the pool survived, otherwise from B2 `/vmstore/offsite-staging` per [Offsite backup to B2 - what's covered and how to restore](<Offsite backup to B2 - what's covered and how to restore.md>) |
| Posters, artwork, thumbnails (`Metadata`, `Media` dirs) | Not backed up. Plex re-downloads them; custom posters picked by hand are lost |
| Watch history and changes since Plex's last own DB backup | Lost. Plex backs up every 3 days and the export is weekly, so up to about 10 days |
| EasyAudioEncoder codec | Plex downloads it; see step 7 |
| `homelab-update` webhook and Kuma push URL | Webhook ID from the HA automation `homelab_vm_update_reports` (Claude); push URL of Kuma monitor `Plex VM Updates` (*Aaron*, Kuma UI: `kuma-api` redacts it) |
| Claude's SSH key | Unchanged on the ClaudeCode VM (`~/.ssh/id_ed25519_plex`); only the Plex side is recreated |

## Prerequisites

- Big Boi up, with the NFS exports for `BIGBOI/plex_content` (ro) and `BIGBOI/plex_recordings` (rw), both `hosts` 192.168.1.116, Mapall User `root`. They come back with the TrueNAS config.
- `plex-db.tar.gz` reachable at `/mnt/Big Boi/BIGBOI/plex_recordings/.plex-db-export/`. If it's gone, restore it from B2 first and copy it there.
- The ClaudeCode VM up (it holds Claude's Plex key). If both are gone, rebuild the ClaudeCode VM first (see the DR index).
- Aaron at his Mac: SSH key for the cloud-init seed, the TrueNAS and Kuma UIs, and the Plex account login (only needed if the claim doesn't carry over).
- If the old VM still exists: rename it and leave it **stopped**. Never run both: they share a MAC.

## Steps

1. **VM** (*Aaron*). Follow the cloud-init runbook with: name `Plex`, CPU Host Passthrough, 4 vCPU / 2 cores / 2 threads (16 threads, as live), 12288 MB, UEFI, Autostart on, 32 GiB zvol `vmstore/plex_disk`, VirtIO NIC on `br0` with **MAC ****`00:a0:98:31:ab:d0`**, Trust Guest Filters off, SPICE display, and a **PCI Passthrough** device `pci_0000_00_02_0` (the Intel UHD 630 iGPU, for hardware transcoding). Ubuntu Server **24.04 LTS** cloud image (what's live and verified with the iHD 24.1 driver), hostname `plex-vm`, user `plexadmin`, sudo, SSH key-only. The MAC carries the UDM fixed IP 192.168.1.116, which both NFS exports, the UDM port forward (TCP 32400) and Claude's key restriction depend on. If the MAC can't be reused, move the UDM reservation to the new MAC before going on.
2. **Base system** (*Aaron*, `ssh plexadmin@192.168.1.116`):
```bash
sudo timedatectl set-timezone America/Denver
sudo apt update && sudo apt full-upgrade -y
sudo apt install -y nfs-common intel-media-va-driver-non-free vainfo intel-gpu-tools qemu-guest-agent unattended-upgrades
sudo mkdir -p /mnt/media /mnt/dvr /transcode
sudo tee -a /etc/fstab >/dev/null <<'EOF'
192.168.1.248:/mnt/Big\040Boi/BIGBOI/plex_content /mnt/media nfs ro,vers=3,proto=tcp,resvport,_netdev,x-systemd.automount 0 0
192.168.1.248:/mnt/Big\040Boi/BIGBOI/plex_recordings /mnt/dvr nfs rw,vers=3,proto=tcp,resvport,_netdev,x-systemd.automount 0 0
tmpfs /transcode tmpfs size=8G,mode=1777,nosuid,nodev,noexec 0 0
EOF
sudo systemctl daemon-reload && sudo mount -a && ls /mnt/media /mnt/dvr && findmnt /transcode
ls -l /dev/dri   # expect card*, renderD128
```
1. **Claude's account** (*Aaron*). Claude prints its public key with `cat ~/.ssh/id_ed25519_plex.pub`. On the Plex VM:
```bash
sudo adduser --disabled-password --gecos '' claude
sudo usermod -aG adm,systemd-journal claude
sudo install -d -m 700 -o claude -g claude /home/claude/.ssh
echo 'from="192.168.1.156",no-agent-forwarding,no-port-forwarding,no-X11-forwarding <PASTE id_ed25519_plex.pub>' | sudo install -m 600 -o claude -g claude /dev/stdin /home/claude/.ssh/authorized_keys
```
1. **Stage the repo files** (Claude, on the ClaudeCode VM). The host key changed, so drop the old one and accept the new one:
```bash
ssh-keygen -R 192.168.1.116; ssh-keygen -R plex
ssh -o StrictHostKeyChecking=accept-new plex 'mkdir -p rebuild'
scp -r ~/homelab/plex-vm/claude-maint ~/homelab/plex-vm/apt ~/homelab/plex-vm/systemd ~/homelab/homelab-update plex:rebuild/
ssh-keygen -lf <(ssh-keyscan -t ed25519 192.168.1.116 2>/dev/null)
```
Record the new fingerprint in the Access model section of the updating runbook. Claude also fills a copy of `homelab-update/hosts/plex-vm.conf.example` (webhook ID from the HA automation `homelab_vm_update_reports`) and copies it to `plex:rebuild/plex-vm.conf`.
1. **Install them** (*Aaron*, as `plexadmin`; root reads Claude's home). `install.sh` asks for a Kuma push URL: paste the one from the Kuma monitor `Plex VM Updates`.
```bash
R=/home/claude/rebuild
sudo install -m 755 -o root -g root $R/claude-maint /usr/local/sbin/
sudo install -m 644 $R/apt/52unattended-upgrades-plex /etc/apt/apt.conf.d/
sudo install -D -m 644 $R/systemd/apt-daily.timer.d/override.conf /etc/systemd/system/apt-daily.timer.d/override.conf
sudo install -D -m 644 $R/systemd/apt-daily-upgrade.timer.d/override.conf /etc/systemd/system/apt-daily-upgrade.timer.d/override.conf
printf 'APT::Periodic::Update-Package-Lists "1";\nAPT::Periodic::Unattended-Upgrade "1";\n' | sudo tee /etc/apt/apt.conf.d/20auto-upgrades >/dev/null
echo 'claude ALL=(root) NOPASSWD: /usr/local/sbin/claude-maint' > /tmp/cm && sudo visudo -cf /tmp/cm && sudo install -m 440 -o root -g root /tmp/cm /etc/sudoers.d/claude-maint && rm /tmp/cm
sudo systemctl daemon-reload && sudo systemctl enable --now fstrim.timer
sudo bash $R/homelab-update/install.sh $R/plex-vm.conf
```
1. **Plex** (Claude installs, *Aaron* restores). Claude: `ssh plex sudo -n /usr/local/sbin/claude-maint upgrade-plex` (latest public build from [plex.tv](http://plex.tv/); the old Plex apt repo is stale and isn't needed). Then Aaron, on the Plex VM:
```bash
sudo usermod -aG video,render plex
sudo systemctl stop plexmediaserver
PMS="/var/lib/plexmediaserver/Library/Application Support/Plex Media Server"
sudo mkdir -m 700 /root/plexdb && sudo tar -xzf /mnt/dvr/.plex-db-export/plex-db.tar.gz -C /root/plexdb
sudo find "$PMS/Plug-in Support/Databases" -maxdepth 1 \( -name '*.db-wal' -o -name '*.db-shm' \) -delete
sudo install -m 644 -o plex -g plex /root/plexdb/com.plexapp.plugins.library.db /root/plexdb/com.plexapp.plugins.library.blobs.db "$PMS/Plug-in Support/Databases/"
sudo install -m 644 -o plex -g plex /root/plexdb/Preferences.xml "$PMS/"
sudo rm -rf /root/plexdb && sudo systemctl start plexmediaserver
```
1. **Plex settings** (*Aaron*, [http://192.168.1.116:32400/web](http://192.168.1.116:32400/web)). The server should come up under its old name, already claimed. If it asks to be claimed, sign in with the Plex account. Check: libraries Movies, TV Shows and Recordings point at `/mnt/media/Movies`, `/mnt/media/TV Shows` and `/mnt/dvr`; Settings → Transcoder has hardware acceleration on and temp directory `/transcode`; Remote Access is green; Live TV & DVR lists the HDHomeRun at 192.168.1.106 (re-add it if not: zip 80602, recordings to the **Recordings** library). Then Manage → Libraries → **Refresh All Metadata** to bring posters back. EasyAudioEncoder: play something that needs audio transcoding (TrueHD). Plex downloads EasyAudioEncoder into `Codecs/` itself, with no manual step (checked 2026-10-17: the live copy was unpacked by Plex on 2026-09-24 alongside its codec pack and is used for transcodes; the `EasyAudioEncoder-*.zip` dated 2026-01-19 is a leftover of the old manual install). If the Plex log shows 429 errors fetching it, Plex is rate-limited and retries later.
2. **Finish** (Claude): `ssh plex 'rm -rf rebuild'` (the conf copy holds the webhook URL), then `ssh plex sudo -n /usr/local/sbin/claude-maint reboot` so the automounts and groups come up clean.

## Verify

- `make -C ~/homelab check`: every `plex:` line is `ok`.
- `ssh plex sudo -n /usr/local/sbin/claude-maint unattended-dry-run` succeeds.
- Run the homelab-update checks once (*Aaron*: `sudo systemctl start homelab-update.service`, or wait for Sunday 04:00): all 7 pass, the HA report arrives, and Kuma `Plex VM Updates` goes green.
- Kuma's `Plex` keyword monitor is green; `findmnt -t nfs,tmpfs` on the VM shows media `ro`, dvr `rw` and `/transcode`.
- Hardware transcoding: force a transcode (play a 4K file at a lower quality) and confirm the Plex dashboard shows `(hw)`, or `sudo intel_gpu_top` shows the Video engine busy.
- Remote access over cellular works.
- **DB export**: `claude-maint plex-db-export` needs one of Plex's own DB backups, and a fresh install has none until Plex's next scheduled backup (Settings → Scheduled Tasks, every 3 days, in the maintenance window). Until then the ClaudeCode VM's Sunday `plex-db-export` run fails, and the B2 pre-script keeps uploading the old export but alerts once it's over 9 days old. After 3 days, Claude runs `sudo systemctl start plex-db-export.service` on the ClaudeCode VM and checks it succeeds.
- Log the rebuild as a change note and update the Plex Media Server System note (zvol name, kernel, Plex version, host key).

## Rollback

The rebuild doesn't touch the old VM or its zvol, so keep it (renamed and stopped) until the new one passes Verify. To go back: stop the new VM and start the old one; never run both (same MAC). If the restored DB turns out bad, stop Plex and try an older `plex-db.tar.gz` version from B2 (30 days of versions). As a last resort, start Plex with an empty DB and re-add the libraries, which loses watch history.
