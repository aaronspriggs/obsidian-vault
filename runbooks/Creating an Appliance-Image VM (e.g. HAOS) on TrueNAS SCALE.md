---
kind: setup
status: active
system:
- '[[TrueNAS SCALE (Big Boi)]]'
notion_id: 3087ae76-22ba-812d-a84f-e6d129f9d89f
---

Import a prebuilt appliance disk image (HAOS .qcow2) into a vmstore zvol and create the VM. General Linux VMs use the cloud-init runbook, which also holds the shared VM wizard settings.

## When to use

Creating a VM on Big Boi from a **prebuilt appliance disk image** (e.g. Home Assistant OS, shipped as a `.qcow2`). For a general-purpose Linux VM (Ubuntu etc.), use [Creating a Cloud-Init Seeded Linux VM](<Creating a Cloud-Init Seeded Linux VM on TrueNAS SCALE.md>) instead. Both import the image into a zvol under `Big Boi/vmstore` rather than booting a qcow2 file, and both use that runbook's Step 6 for the VM wizard.

## Prerequisites

- TrueNAS shell with sudo (SSH `aspriggs@192.168.1.248`, or System → Shell).
- Free space in the pool; `Big Boi/vmstore` already exists (POSIX ACL, mode Discard) and is snapshotted daily.

## Steps

**Step 1. Create the zvol** in the UI under `Big Boi/vmstore`: a descriptive name (e.g. `haos_disk`) and the size the appliance needs (HAOS: 128 GiB).
**Step 2. Download and unpack the image** (take the current release; the version below is an example):
```bash
cd "/mnt/Big Boi/vmstore"
sudo wget https://github.com/home-assistant/operating-system/releases/download/<ver>/haos_ova-<ver>.qcow2.xz
sudo unxz haos_ova-<ver>.qcow2.xz
```
**Step 3. Write it into the zvol** (the space in the pool name becomes `+` in device paths; no output while it runs is normal):
```bash
sudo qemu-img convert -O raw haos_ova-<ver>.qcow2 "/dev/zvol/Big+Boi/vmstore/haos_disk"
sudo rm haos_ova-<ver>.qcow2
```
**Step 4. Create the VM** with the wizard settings in the cloud-init runbook's Step 6: Host Passthrough CPU (1 vCPU × N cores × 1 thread), memory set explicitly (HAOS: 4 GiB), UEFI, existing disk image = the zvol with type **VirtIO**, NIC on bridge **`br0`** (Trust Guest Filters off; TrueNAS rejects it on a bridge), console bound to 192.168.1.248, installation media none. Appliance-specific: add any USB passthrough (HA: the Sonoff ZBDongle-E) and enable autostart.
**Step 5. Start and verify:** start the VM, watch the SPICE console boot, find its MAC/IP in the UniFi client list, then add a DHCP reservation there.

## Verify

The VM reaches its web UI at the reserved IP (HA: `:8123`) and shows as autostart in Virtualization. Add a Kuma monitor and, if it's a new System, a Systems page.

## Common failures

- **UEFI shell instead of the OS:** the image wasn't fully written to the zvol, or the VM disk isn't the zvol / not VirtIO. Rerun Step 3 and check the disk device.
- **`path must reside within a pool mount point`****:** use a zvol under a pool dataset, not an ad-hoc file path.
- **Zvol device not found:** it's `/dev/zvol/Big+Boi/vmstore/<name>`, never `/dev/zvol/Big Boi/...`.
- **No IP / MAC not in UniFi:** NIC must be VirtIO on `br0`; stop and start the VM.
- **Migrating HA:** don't run old and new HA instances on the LAN at the same time; integrations and automations will fight.

## Rollback

Stop and delete the VM (Virtualization), then delete the zvol. Nothing else is touched.
