---
status: active
category: hardware
ip: 192.168.1.248
url: https://192.168.1.248:9443/
last_verified: 2026-11-15
repo: https://github.com/aaronspriggs/spriggs-homelab/tree/main/truenas
notion_id: 2ff7ae76-22ba-8153-8df1-d4ca673fae00
---

Big Boi, the homelab's one server: TrueNAS SCALE 25.04 on an i9-9900 with 64 GB. Hosts the HA, Plex and ClaudeCode VMs and Dockhand. Its pool, shares and backups are in the storage note.

## Overview

"Big Boi" is the homelab's NAS and hypervisor, a 2U rackmount box running TrueNAS SCALE. This note holds the box: its hardware, network, the TrueNAS install and its services, how Aaron and Claude get in, and the guests it runs. The pool, datasets, shares, snapshots and offsite backup are in [Big Boi storage](<Big Boi storage (pool, datasets, shares, backups).md>), split out on 2026-11-15; changes before that date are all listed here. Checked on 2026-11-15 through the read-only API and UniFi unless dated otherwise.

## Access

- **Web UI:** [https://192.168.1.248:9443/](https://192.168.1.248:9443/) (HTTP redirects to HTTPS; hostname `truenas`, domain `local`). Admin user `truenas_admin` (UID 950, FULL_ADMIN, 2FA not configured); password in the 1Password item **TrueNAS - Admin**.
- **SSH:** user `aspriggs` (UID 3000, sudo), port 22, password login allowed. Claude has no SSH here.
- **Claude, read-only:** local user `claude-readonlyapi` (UID 3002, no password, nologin shell, no sudo; renamed from `claude` on 2026-10-14) in the group `claude`, which holds the Read-Only Administrator privilege. Its API key `claude-readonly` has no expiry and is stored only on the ClaudeCode VM at `~/.config/homelab/truenas-api-key` (mode 600). Client: `~/.local/bin/truenas-api <method> '<json>'`. Setup and rotation: [TrueNAS API runbook](<../runbooks/TrueNAS API access (read-only + maintenance writes) and alert relay (ClaudeCode VM).md>).
- **Claude, maintenance (since 2026-10-14):** local user `claude-maint` (UID 3001, no password, nologin) with the roles `READONLY_ADMIN`, `APPS_WRITE`, `VM_WRITE`, `SYSTEM_UPDATE_WRITE`, `POOL_SCRUB_WRITE`, `SNAPSHOT_WRITE` and `SNAPSHOT_DELETE`. Its key expires 2027-10-14 and lives in the 1Password item **TrueNAS API Key (claude-maint)**, read at run time, never on disk. Used only through `truenas-api --write`, which allowlists app upgrade and restart, VM start, stop and restart, TrueNAS updates, and creating or deleting manual snapshots (Tier 2; never `auto-*`, no rollback). The change-authority tiers apply unchanged. Same runbook.
- **API gotchas (25.04):** REST is deprecated; use JSON-RPC over `wss://192.168.1.248:9443/api/current`. A user-linked key is revoked automatically if it is ever sent over plain HTTP, so the client is hard-coded to WSS. Read-only keys get 403 on legacy REST. Method names: `zfs.snapshot.query` (not `pool.snapshot.query`), `update.check_available`. Every `truenas-api` call logs in, and after about 25 in a row TrueNAS answers `[EBUSY] Rate Limit Exceeded` until it has had a pause, so batch reads (seen 2026-11-15).

## Config

**Hardware** (parts from the 2026-03 build notes unless marked; the API reads only the CPU, RAM and disks)

- CPU Intel Core i9-9900 (8C/16T, since 2026-03-04; read live). Its UHD 630 iGPU is passed through to the Plex VM.
- RAM 64 GB non-ECC (read live): Corsair Vengeance LPX 2×32 GB DDR4-3600, kit CMK64GX4M2D3600C18 (XMP 18-22-22-42, 1.35 V; bought 2025-01-24, per Aaron's order page 2026-11-06).
- Board ASRock Z390M-ITX/ac (Mini-ITX, LGA1151) in a MyElectronics 19" 2U Mini-ITX rack case, 225 mm deep.
- PSU Corsair SF750 Platinum, 2018 model CP-9020186: standard SFX (125 × 63.5 × 100 mm; not SFX-L, corrected by Aaron 2026-10-11), Corsair Type 4 modular cables only, 3 "Peripheral & SATA" sockets, shipped with 2× 4-connector SATA cables and 1× 3-connector Molex cable.
- 10 GbE card: 10Gtek Intel 82599EN SFP+, low-profile.
- Boot disk: Patriot P300 128 GB NVMe (read live). The five pool SSDs are in the storage note.

**Network:** `enp1s0`, the 10 GbE card, runs over a DAC to the USW Pro Max 16 PoE's port "SFP+ 2" at 10 Gb and is bridged as `br0` (192.168.1.248/24, fixed IP in UniFi, gateway and DNS 192.168.1.1). The onboard `eno1` and `enp2s0` are down. `br0` must persist for the VMs to reach the LAN; it rolled back once during "Test Changes" when first created, so check VM connectivity after any network change.

**Software:** TrueNAS SCALE 25.04.2.6 (Fangtooth), no update pending. Up since 2026-07-05. Timezone `America/Denver` (set 2026-10-15), so every schedule here and in the storage note is Mountain time.

**Services (enabled and running):** SMB, NFS, SSH, S.M.A.R.T., and UPS as a NUT client: mode SLAVE of `unifiups@192.168.1.12:3493`, shutdown when the UPS goes on battery, after 300 s. What is still untested about a power cut is in [Rack Infrastructure — UPS + Power Management](<../projects/Rack Infrastructure — UPS + Power Management.md>).

**Certificate:** the web UI uses `truenas-cert` from the internal CA `truenas-ca`: RSA 4096, CN `truenas.local`, SANs 192.168.1.248, truenas.local and truenas.thespriggs.com, valid to 2035-03-15.

**Alerts open on 2026-11-15:** a NOTICE that the pool's ZFS feature flags can be upgraded (see the storage note), and two INFO: a Dockhand app update is available, and the UPS is online.

**Creating VMs:** import an appliance image into a zvol rather than booting a qcow2: `qemu-img convert -O raw <image.qcow2> /dev/zvol/Big+Boi/vmstore/<zvol_name>` (the pool name's path quirks are in the storage note). Runbooks: [appliance image](<../runbooks/Creating an Appliance-Image VM (e.g. HAOS) on TrueNAS SCALE.md>), [cloud-init Linux VM](<../runbooks/Creating a Cloud-Init Seeded Linux VM on TrueNAS SCALE.md>).

## Dependencies

Needs the UDM Pro (gateway, DNS, its fixed address), its switch port, and the [UPS 2U](<UniFi UPS 2U.md>) for power and the shutdown signal.

**Hosts (all autostart):**

| Guest | Kind | IP | vCPU threads / RAM | Notes |
| --- | --- | --- | --- | --- |
| [Home Assistant OS (VM)](<Home Assistant OS (VM).md>) | VM | 192.168.1.218 | 2 / 4 GiB | USB passthrough (Zigbee dongle) |
| [Plex Media Server](<Plex Media Server.md>) | VM | 192.168.1.116 | 16 / 12 GiB | iGPU (PCI) passthrough |
| [ClaudeCode (VM)](<ClaudeCode (VM).md>) | VM | 192.168.1.156 | 2 / 8 GiB | Claude Code's host |
| [Dockhand](<Dockhand.md>) | TrueNAS app | :3001 | — | App 1.1.38 (Dockhand v1.0.53); runs the `servarr` and `uptime-kuma` (:3002) stacks |

If Big Boi goes down, all of them go down with it, and so does everything in the storage note.

## Decisions

- **2026-02-06:** Pi-hole and nginx-proxy-manager were removed as TrueNAS apps; if they come back, they go on a VM or separate hardware (both are backlog projects).
- **2026-03-04:** the upgrade was limited to a CPU swap (i5-9400 → i9-9900, same board). No new case or board and no discrete GPU: the UHD 630 handles Plex transcoding. Details: the done project "Big Boi Server Upgrade — CPU Swap (i9-9900)".
- **2026-10-15 (Aaron):** two-tier storage inside Big Boi: rebuild it into a new case with an HDD pool for bulk media, while the SSD pool keeps VMs, containers, apps and configs. A possible offsite TrueNAS box would receive ZFS replication. This replaced the 2026-03-03 UniFi UNAS Pro plan, and the GPU question from 2026-03-04 is settled there too. See [Rebuild Big Boi](<../projects/Rebuild Big Boi into a new case with an HDD pool for bulk media.md>).
- **2026-11-08:** stay on native TrueNAS VMs, not Proxmox. Proxmox is ahead on backups (PBS), clustering, LXC and passthrough tooling, and TrueNAS's VM layer has been less stable (the Incus switch and its partial walk-back), but none of that pays off on one NAS-first box, and running TrueNAS as a Proxmox VM would make storage depend on a VM booting. Revisit if a second compute box is added, the VM count outgrows TrueNAS's VM UI and backups, or a TrueNAS upgrade breaks the VMs again.
- **2026-11-15:** this note was split along the line between the box and its storage ([change](<../changes/2026-11-15 Split the Big Boi System note into the box and its storage.md>)).

## Open work

![[Projects.base#Open for this system]]

## Runs on this

![[Systems.base#Runs on this]]

## Runbooks

![[Runbooks.base#For this system]]

## Recent changes

![[Changes.base#For this system]]

## Related

- Repo [truenas/](https://github.com/aaronspriggs/spriggs-homelab/tree/main/truenas): `truenas-api` and `truenas-alert-relay` with its systemd timer, deployed on the ClaudeCode VM.
- Rebuild from bare metal: [Rebuild Big Boi (TrueNAS) from bare metal](<../runbooks/Rebuild Big Boi (TrueNAS) from bare metal.md>). Reboots: [Big Boi Reboot Checklist](<../runbooks/Big Boi Reboot Checklist.md>).
