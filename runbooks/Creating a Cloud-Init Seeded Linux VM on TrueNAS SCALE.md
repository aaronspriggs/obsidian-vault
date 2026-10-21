---
kind: setup
status: active
system:
- '[[ClaudeCode (VM)]]'
last_tested: 2026-09-02
notion_id: 3cf7ae76-22ba-818c-aefe-c58c424ee279
---

Step-by-step process for building a general-purpose Linux VM (not a prebuilt appliance image like HAOS) on TrueNAS SCALE, using a cloud image with cloud-init seeded directly into the disk via qemu-nbd. No installer or ISO required.

## Overview

Use this runbook for a general-purpose Linux VM (Ubuntu/Debian, not an appliance image like HAOS). Unlike the existing "Creating a New VM on TrueNAS SCALE" runbook — which imports a prebuilt appliance disk image as-is — this method takes a cloud image (which boots with no configured user/password) and injects a cloud-init NoCloud seed directly into it before writing it to the Zvol, so the VM comes up with SSH access and no interactive installer or console login needed at any point.

## Prerequisites

- SSH access to Big Boi shell
- An SSH public key to authorize on the new VM
- `vmstore` dataset already exists under the target pool (created once, shared by all VMs)

## Step 1: Create the Zvol

GUI: **Storage → Big Boi → vmstore → Add Zvol**, or shell:
```bash
sudo zfs create -V 40G "Big Boi/vmstore/<name>_disk"
```
Note: `zfs` commands need `sudo` even for read-only listing — `aspriggs`'s shell PATH doesn't include `/sbin`/`/usr/sbin` the way `sudo`'s does, so plain `zfs list` reports "command not found" even though the binary exists.

## Step 2: Download the cloud image

```bash
cd "/mnt/Big Boi/vmstore"
sudo wget <cloud image URL, e.g. https://cloud-images.ubuntu.com/releases/26.04/release/ubuntu-26.04-server-cloudimg-amd64.img>
```
`vmstore` is ACL-governed — `aspriggs` can't write there directly, `sudo wget` is required (matches the existing "use UI ACL editor, not chmod" gotcha for this dataset).

## Step 3: Write the cloud-init seed files

Write `meta-data` and `user-data` to a scratch directory — **use ****`/tmp`****, not ****`~`**. On this box `aspriggs`'s home directory is `/var/empty` (a locked-down TrueNAS placeholder, not writable), so anything using `~` for scratch files fails with "Operation not permitted."
```bash
mkdir -p /tmp/<name>-seed
cat > /tmp/<name>-seed/meta-data <<'EOF'
instance-id: <name>-01
local-hostname: <name>
EOF
```
For `user-data`, write real `#cloud-config` YAML with hostname, a `users` entry (name, groups, sudo, ssh_authorized_keys), `ssh_pwauth: false`, and a `growpart`/`resize_rootfs` block so the OS uses the full Zvol size instead of the image's original small partition.
**Gotcha:** avoid inline bracket YAML syntax (e.g. `groups: [sudo]`, `sudo: ['ALL=(ALL) NOPASSWD:ALL']`, `devices: ['/']`). Pasting a large heredoc containing brackets over SSH corrupted the file mid-paste in practice (a chunk of `growpart`/`resize_rootfs` got dropped and reordered). Use block-list YAML instead (`groups:\n  - sudo`) and paste `meta-data` and `user-data` as two separate commands rather than one combined block — easier to catch corruption if it happens again, and it didn't recur once brackets were removed.
Always `cat` the file back and diff it against what you intended before proceeding — don't assume a paste succeeded cleanly.

## Step 4: Inject the seed via qemu-nbd

```bash
sudo modprobe nbd max_part=8
sudo qemu-nbd --connect=/dev/nbd0 --format=qcow2 "/mnt/Big Boi/vmstore/<image file>"
```
Pass `--format=qcow2` explicitly — without it, the connect can report exit code 0 and create the device node but expose it with **0B size** (nothing actually attached), which looks like success but isn't. If `lsblk /dev/nbd0` shows `0B`, disconnect (`sudo qemu-nbd --disconnect /dev/nbd0`) and reconnect with the format flag.
Before mounting, confirm the actual root partition rather than assuming `p1`:
```bash
sudo partprobe /dev/nbd0
lsblk /dev/nbd0
sudo blkid /dev/nbd0p1
```
Look for `TYPE="ext4"` and ideally `LABEL="cloudimg-rootfs"`. Ubuntu's current cloud image layout has 4 partitions (root + a few small boot-related ones) — root is `p1` but verify, don't assume.
Mount and drop the seed into the path cloud-init checks on first boot:
```bash
sudo mkdir -p /mnt/<name>-seed
sudo mount /dev/nbd0p1 /mnt/<name>-seed
sudo mkdir -p /mnt/<name>-seed/var/lib/cloud/seed/nocloud
sudo cp /tmp/<name>-seed/user-data /mnt/<name>-seed/var/lib/cloud/seed/nocloud/user-data
sudo cp /tmp/<name>-seed/meta-data /mnt/<name>-seed/var/lib/cloud/seed/nocloud/meta-data
sudo umount /mnt/<name>-seed
sudo qemu-nbd --disconnect /dev/nbd0
```

## Step 5: Convert into the Zvol

```bash
sudo qemu-img convert -O raw "/mnt/Big Boi/vmstore/<image file>" "/dev/zvol/Big+Boi/vmstore/<name>_disk"
```
Runs silently with no progress output — normal, not a hang. Verify with `sudo zfs list -o name,used,refer "Big Boi/vmstore/<name>_disk"` — REFER should jump from near-zero to roughly the image's actual data size once written.

## Step 6: Create the VM (GUI)

TrueNAS's VM wizard has changed since the original appliance-image runbook was written — it's now a 7-step flow (Operating System → CPU And Memory → Disks → Network Interface → Installation Media → GPU → Confirm) with several fields that didn't exist before:
- **System Clock:** set to UTC for a Linux guest (defaults to Local)
- **Boot Method:** UEFI is fine for current cloud images
- **Secure Boot / TPM:** leave both off
- **Bind:** the display/console now requires an explicit password, and Bind defaults to `0.0.0.0` — scope it to the host's own IP if offered, and set a real password (not something trivial — it gates console access, which briefly shows cloud-init running on first boot)
- **CPU And Memory:** the warning "product of vCPUs, cores, and threads must not exceed 255" means these three fields **multiply**, they don't add. To get N total logical CPUs matching how other VMs on this box are configured (1 socket, multiple cores), set Virtual CPUs=1, Cores=N, Threads=1. Also explicitly set **CPU Mode to Host Passthrough** — it defaults to Custom with no model selected. Memory Size defaults to 512 MiB — must be changed explicitly.
- **Disks:** select "Use existing disk image" (not "Create new disk image", which is the default), point at the Zvol from Step 5, and change **Disk Type from the AHCI default to VirtIO**.
- **Network Interface:** select the `br0` bridge (matches HA/Plex; confirmed via an existing VM's NIC config rather than guessed). **Do not enable Trust Guest Filters when attaching to a bridge device** — TrueNAS rejects this combination with `[EINVAL] attributes.trust_guest_rx_filters: This can only be set when "nic_attach" is not a bridge device`. That setting only applies to direct/macvtap-style attachment to a physical interface, which is what the *old* appliance-image runbook's "attach to enp1s0, Trust Guest Filters enabled" instruction was actually describing — it doesn't carry over to bridge attachment.
- **Installation Media:** None — the OS is already on the Zvol.

## Step 7: Boot and verify

Start the VM, watch the console (should show a normal login prompt like `<hostname> login:` once cloud-init finishes — there's intentionally no password to type here since only SSH key auth was configured). Check the UniFi client list for the new DHCP lease, set a static reservation, then:
```bash
ssh <user>@<ip>
```
Should log straight in with no password prompt.
**If SSH says ****`Permission denied (publickey)`**** despite the seed looking correct:** double check you're running `ssh` from the machine (and local user account) that actually holds the matching private key. A key generated as `user@MachineA` won't be found by a shell running as a different local account or on a different machine, even if both resolve `~` to what looks like a similar path.
To add more machines afterward, no need to touch cloud-init again — just append to the live VM's authorized_keys from a session that's already in:
```bash
echo "<new public key>" >> ~/.ssh/authorized_keys
```

## Step 8: Install software

For Node-based tooling, NodeSource's setup script plus apt is the straightforward path. Two npm gotchas worth knowing:
- A fresh npm may block a package's postinstall script by default (`npm warn install-scripts`) — rerun the install with `--allow-scripts=<package>` if you see this, don't leave it half-installed.
- If the package supports a native (non-npm) install method, prefer it over npm-global — npm-global installs typically need `sudo` to self-update, which defeats an otherwise unattended service. Remove the leftover npm-global copy after switching (`sudo npm -g uninstall <package>`) to avoid two binaries on PATH.

## Step 9: Long-running foreground services under systemd

If the software being installed needs to run continuously and prompts for a one-time interactive confirmation on first launch, **systemd's Type=simple with no TTY can't answer it** — the process will read EOF, exit cleanly (exit code 0, not a crash), and systemd's `Restart=always` will loop it forever with no useful error in the logs beyond the prompt text itself repeating.
Fix: run the exact command manually once over a real SSH session (same working directory the systemd unit will use, since some tools tie trust/consent to the directory), answer the prompt interactively, confirm it starts running correctly, stop it, then start the systemd service — the consent should now be persisted in the software's own config and the service starts clean on its own.
Always check `journalctl -u <service> -n 50 --no-pager` if a systemd service is flapping (`activating (auto-restart)`) with a 0/SUCCESS exit — that combination specifically points to a swallowed interactive prompt rather than an actual crash.
