---
kind: procedure
status: active
system:
- '[[Plex Media Server]]'
- '[[ClaudeCode (VM)]]'
last_tested: 2026-09-24
notion_id: 3e57ae76-22ba-81b7-8c5f-c60b6133add7
---

Hands-off Ubuntu + Plex Media Server upgrade of the Plex VM, run by Claude Code from the ClaudeCode VM via the scoped `claude` account and `claude-maint` wrapper. Includes pre-flight, upgrade, reboot, validation, rollback, and how the access is set up.

Trigger: Aaron says "update Plex/the Linux VM to the newest version and validate everything." Claude Code on the ClaudeCode VM runs this end to end. Aaron shouldn't need to log in.

## Access model

- `ssh plex` from the ClaudeCode VM logs in as `claude@plex-vm`, using key `~/.ssh/id_ed25519_plex`. The key is pinned to `from="192.168.1.156"` with forwarding disabled. The `claude` account has no password, so key login is the only way in, and it's in `adm` + `systemd-journal` for reading logs.
- Root access is **only** `sudo -n /usr/local/sbin/claude-maint <subcommand>` (NOPASSWD, via `/etc/sudoers.d/claude-maint`). Any other sudo prompts for a password and fails. The wrapper is a guardrail against mistakes, not a hard security boundary, because installing packages as root is effectively root.
- Plex VM host key: ED25519 `SHA256:FrGffFi83VNZIGNkLrKR92hkHJ+OsfEDXeNTiKCqpJo`.

## Procedure

1. **Rollback point:** the Plex VM disk lives under `Big Boi/vmstore`, which has a daily recursive 00:00 snapshot. For a fresher rollback point, Aaron takes a manual snapshot of the Plex zvol in TrueNAS (Datasets → zvol → Create Snapshot). Claude has no TrueNAS access.
2. **Pre-flight baseline:** record kernel, OS, Plex version (`curl -s http://127.0.0.1:32400/identity`), NFS mounts, `/dev/dri`, disk and failed units. Check for active transcodes with `ps -eo args | grep "[P]lex Transcoder"`. *Don't use **`pgrep -c -f`** over ssh; it matches the remote shell's own command line.* Direct-play streams can't be seen without a Plex token, so the reboot may interrupt someone.
3. `sudo -n /usr/local/sbin/claude-maint update`, then `apt list --upgradable` to see what's pending.
4. `sudo -n /usr/local/sbin/claude-maint upgrade`: non-interactive full-upgrade that keeps existing config files. A few packages may be "not upgraded" because of Ubuntu **phased updates**. That's normal and they'll land later.
5. `sudo -n /usr/local/sbin/claude-maint upgrade-plex`: installs the latest *public* Plex build from `https://plex.tv/api/downloads/5.json`, only accepts `downloads.plex.tv` URLs, checks the SHA-1, and refuses downgrades. The Plex apt repo is stale, so don't rely on it.
6. If `/var/run/reboot-required` exists: `sudo -n /usr/local/sbin/claude-maint reboot`. SSH is back in about 25 s.
7. **Validate:** the new kernel is running and `reboot-required` is gone; `plexmediaserver` is active and enabled; `/identity` reports the new version, both on the VM and over the LAN; `ls /mnt/media /mnt/dvr` triggers the automounts and both show as NFS; `/dev/dri` has `card*` + `renderD128` and the `plex` user is in `video` + `render`; root disk has room; `systemctl --failed` is empty; `journalctl -b -u plexmediaserver -p err` has no errors.
8. `sudo -n /usr/local/sbin/claude-maint autoremove`
9. Log to the Changes DB (Type Upgrade) and update versions on the Plex Media Server System page.

## Rollback

Shut down the Plex VM in TrueNAS, then Datasets → Plex zvol → Manage Snapshots → Rollback. This is destructive: anything written after the snapshot is lost, including Plex watch history and metadata. Media and DVR live on NFS and aren't affected. Needs Aaron's explicit confirmation.

## Rebuilding the access (if the Plex VM is rebuilt)

1. On the ClaudeCode VM (Aaron runs this; Claude Code's auto-mode classifier blocks Claude from creating standing credentials): `ssh-keygen -t ed25519 -N "" -C "claude@claudecode-vm (plex-maint)" -f ~/.ssh/id_ed25519_plex`, plus a `Host plex` block in `~/.ssh/config` (HostName 192.168.1.116, User claude, IdentityFile ~/.ssh/id_ed25519_plex, IdentitiesOnly yes).
2. On the Plex VM as root: `adduser --disabled-password claude`; `usermod -aG adm,systemd-journal claude`; put `from="192.168.1.156",no-agent-forwarding,no-port-forwarding,no-X11-forwarding <pubkey>` in `/home/claude/.ssh/authorized_keys` (700/600, owned by claude); install the wrapper from the repo ([`plex-vm/claude-maint`](https://github.com/aaronspriggs/spriggs-homelab/blob/main/plex-vm/claude-maint)) at `/usr/local/sbin/claude-maint` (root:root 755); write `claude ALL=(root) NOPASSWD: /usr/local/sbin/claude-maint` to a temp file, check it with `visudo -cf`, then install it as `/etc/sudoers.d/claude-maint` (440).

### claude-maint source

Lives in the repo: [`plex-vm/claude-maint`](https://github.com/aaronspriggs/spriggs-homelab/blob/main/plex-vm/claude-maint) (with access notes in [`plex-vm/README.md`](https://github.com/aaronspriggs/spriggs-homelab/blob/main/plex-vm/README.md)). Subcommands: `update`, `upgrade`, `upgrade-plex`, `autoremove`, `unattended-dry-run`, `plex-restart`, `plex-stop`, `plex-start`, `reboot`.
To change the wrapper: Claude edits it in the repo, commits and pushes. It's root-owned, so Aaron deploys the new version with his plexadmin sudo (`sudo install -m 755 -o root -g root claude-maint /usr/local/sbin/claude-maint`). `make check` in the repo then confirms the deployed copy matches.
