---
kind: recovery
status: active
system:
- '[[ClaudeCode (VM)]]'
repo: https://github.com/aaronspriggs/spriggs-homelab/tree/main/claudecode-vm
notion_id: 3fb7ae76-22ba-8175-90ce-daff7329032d
---

Rebuild the ClaudeCode VM (Claude Code Remote Control host) when its disk is lost or needs a clean reinstall. The disk isn't backed up: everything comes back from the repo, 1Password and freshly issued keys. Aaron drives steps 1-6; Claude can do most of the rest from a Remote Control session.

## When to use

The ClaudeCode VM is gone or unusable: the zvol was lost, the VM won't boot, or Big Boi itself was rebuilt. Also for a deliberate clean reinstall. The VM's disk is **not** backed up (the B2 offsite tasks skip VM disks), so nothing is restored from a backup: the VM is rebuilt from the repo, 1Password and newly issued keys. Claude lives on this VM, so it can't do the first part; Aaron runs steps 1-6 over SSH, then a Remote Control session can do the rest (the steps marked *Aaron* still need him). Expect about 1-2 hours. Desk-checked against the live VM on 2026-10-16; not yet test-rebuilt.

## What comes back from where

| Item | Source |
| --- | --- |
| VM, OS, user `aspriggs`, Aaron's SSH keys | [Creating a Cloud-Init Seeded Linux VM on TrueNAS SCALE](<Creating a Cloud-Init Seeded Linux VM on TrueNAS SCALE.md>) |
| Scripts, systemd units, `CLAUDE.md`, `.mcp.json`, `settings.local.json`, Claude's memory | Repo `spriggs-homelab`. `deployed.tsv` lists every deployed path; `claudecode-vm/README.md` has the details |
| Wrapper credentials (Dockhand, UniFi, *arr, Kuma, TrueNAS `claude-maint`, ha-mcp URL) | 1Password vault `Homelab - Claude`, read via service account `claudecode-vm` |
| The service account token itself | *Aaron* issues a new one |
| TrueNAS read-only key (`claude-readonlyapi`) | *Aaron* issues a new one (it was only on the old disk) |
| kb-export Notion token | *Aaron* refreshes the Notion integration `kb-export` secret |
| HA webhook and Kuma push URLs (relay, kb-export, homelab-update) | Read back from HA and Kuma by Claude; not secret enough to need 1Password |
| SSH keys (GitHub deploy key, Plex) | Generated new; *Aaron* swaps the public keys |
| Claude login | Log in again with Aaron's [claude.ai](http://claude.ai/) account |
| Notion, Gmail and other connectors | Account-level on [claude.ai](http://claude.ai/); nothing to do on the VM |

## Prerequisites

- Big Boi up with the `vmstore` dataset available.
- Aaron at his Mac: an SSH key from the cloud-init seed, a browser for the Claude login, 1Password, GitHub (repo admin for deploy keys), and the TrueNAS UI.
- The Plex VM reachable as `plexadmin` (to re-key the `claude` user).
- If the old VM still exists: rename it and leave it **stopped**. Never run both: they share a MAC.

## Steps

1. **VM** (*Aaron*). Follow the cloud-init runbook with these settings: name `ClaudeCode`, CPU Host Passthrough, 1 vCPU / 2 cores / 1 thread, 8192 MB, UEFI, 40 GiB zvol `vmstore/claudecode_disk`, VirtIO NIC bridged on `br0` with **MAC ****`00:a0:98:1e:c7:5c`**, Trust Guest Filters **off**, SPICE bound to 192.168.1.248. Ubuntu Server 26.04 LTS cloud image; user `aspriggs`, sudo NOPASSWD, SSH key-only. Keeping the MAC matters: the UDM fixed IP 192.168.1.156 is tied to it, and the Plex VM only accepts Claude's key from .156. If the MAC can't be reused, change the UDM reservation to the new MAC before going on.
2. **Packages** (*Aaron*, over `ssh aspriggs@192.168.1.156`):
```bash
sudo apt update && sudo apt install -y git make shellcheck jq python3-requests python3-websocket
```
Then install `gitleaks` (v8.19+) from its upstream release into `/usr/local/bin` (not apt), and `1password-cli` from 1Password's apt repo as `claudecode-vm/README.md` describes.
1. **Repo** (*Aaron*). Create the deploy key and the SSH config:
```bash
ssh-keygen -t ed25519 -N '' -C 'claudecode-vm deploy key' -f ~/.ssh/id_ed25519_github_spriggs_homelab
cat >> ~/.ssh/config <<'EOF'
Host github.com
    HostName github.com
    User git
    IdentityFile ~/.ssh/id_ed25519_github_spriggs_homelab
    IdentitiesOnly yes
EOF
cat ~/.ssh/id_ed25519_github_spriggs_homelab.pub
```
On GitHub, repo `aaronspriggs/spriggs-homelab` → Settings → Deploy keys: delete the old ClaudeCode VM key, add this one with **Allow write access**. Then:
```bash
git clone git@github.com:aaronspriggs/spriggs-homelab.git ~/homelab && make -C ~/homelab setup
git config --global user.name "Claude Code (ClaudeCode VM)"
git config --global user.email spriggs.aaron+claudecode@gmail.com
git config --global init.defaultBranch main
```
1. **Kernel and watchdog** (*Aaron*): run the `nomodeset` and softdog block under Deploy in `claudecode-vm/README.md`, then `sudo reboot`. Without `nomodeset` the VM can hang on reboot (2026-09-27 incident).
2. **1Password** (*Aaron*). In 1Password, revoke the old `claudecode-vm` service account token and issue a new one with **read** on `Homelab - Claude` only. From the Mac:
```bash
ssh aspriggs@192.168.1.156 'umask 077; mkdir -p ~/.config/homelab && cat > ~/.config/homelab/op-service-account-token'
```
Paste the token, press Enter, then Ctrl-D. Install the wrappers and test:
```bash
cd ~/homelab && mkdir -p ~/.local/bin
for f in claudecode-vm/homelab-secret claudecode-vm/claude-remote-control-start dockhand/dockhand-api unifi/unifi-api servarr/arr-api uptime-kuma/kuma-api uptime-kuma/kuma-adopt truenas/truenas-api truenas/truenas-alert-relay kb-export/kb-export; do install -m 755 "$f" ~/.local/bin/; done
~/.local/bin/homelab-secret 'jmgo2477tslf6dipcz3bsobj34/password' >/dev/null && echo 1password-ok
```
1. **Claude Code and Remote Control** (*Aaron*):
```bash
curl -fsSL https://claude.ai/install.sh | bash
mkdir -p ~/homelab-agent/.claude ~/.claude/projects/-home-aspriggs-homelab-agent
ln -s ~/homelab/claudecode-vm/CLAUDE.md ~/homelab-agent/CLAUDE.md
install -m 644 ~/homelab/claudecode-vm/mcp.json ~/homelab-agent/.mcp.json
install -m 644 ~/homelab/claudecode-vm/claude/settings.local.json ~/homelab-agent/.claude/settings.local.json
ln -s ~/homelab/claudecode-vm/claude/memory ~/.claude/projects/-home-aspriggs-homelab-agent/memory
cd ~/homelab-agent && ~/.local/bin/claude
```
In Claude: trust the folder, run `/login`, open the URL on the Mac and sign in, then `/exit`. Accept the one-time Remote Control consent (systemd can't answer it, and the service crash-loops until it's accepted): run `~/.local/bin/claude remote-control --name "ClaudeCode VM"` from `~/homelab-agent`, answer `y`, then Ctrl-C. Install the service:
```bash
sudo install -m 644 ~/homelab/claudecode-vm/systemd/claude-remote-control.service /etc/systemd/system/
sudo systemctl daemon-reload && sudo systemctl enable --now claude-remote-control
```
"ClaudeCode VM" should appear at [claude.ai/code](http://claude.ai/code). **From here, open a Remote Control session and let Claude do the rest**, pointing it at this runbook.
1. **Plex access** (Claude generates the key, *Aaron* installs it). Claude: `ssh-keygen -t ed25519 -N '' -f ~/.ssh/id_ed25519_plex` and append the `Host plex` block (HostName 192.168.1.116, User `claude`, that IdentityFile, IdentitiesOnly yes) to `~/.ssh/config`. Aaron, as `plexadmin` on the Plex VM: replace the line in `/home/claude/.ssh/authorized_keys` with `from="192.168.1.156",no-agent-forwarding,no-port-forwarding,no-X11-forwarding <new id_ed25519_plex.pub>`. Claude then runs `ssh plex true` to accept the host key. The access model is in [Updating the Plex VM (OS + Plex)](<Updating the Plex VM (OS + Plex).md>).
2. **TrueNAS read-only key** (*Aaron*): in TrueNAS, revoke the old API key of `claude-readonlyapi`, create a new one, and write it to `~/.config/homelab/truenas-api-key` the same way as step 5. See [TrueNAS API access (read-only + maintenance writes) and alert relay (ClaudeCode VM)](<TrueNAS API access (read-only + maintenance writes) and alert relay (ClaudeCode VM).md>). Claude checks it with `truenas-api system.info`.
3. **Timers** (Claude, plus *Aaron* for the Notion token):
    - Relay: fill `~/.config/homelab/truenas-alert-relay.json` (600) from `truenas/truenas-alert-relay.json.example`, with the HA webhook URL and the `TrueNAS Alert Relay` Kuma push URL read back over ha-mcp and `kuma-api`.
    - kb-export: *Aaron* refreshes the secret of the Notion integration `kb-export` and writes it to `~/.config/kb-export/notion-token` (600, as in step 5). Claude fills `~/.config/kb-export/kb-export.json` from its `.example` (`KB Export` push URL) and does the one-time clone in `kb-export/README.md`.
    - homelab-update: fill a copy of `homelab-update/hosts/claudecode-vm.conf.example` (webhook ID from the HA automation `homelab_vm_update_reports`, the `ClaudeCode VM Updates` push URL) and run `sudo bash install.sh <conf>` per `homelab-update/README.md`.
    - Install and enable the units: `truenas-alert-relay`, `kb-export` and `plex-db-export` (`.service` + `.timer` from `truenas/systemd/`, `kb-export/systemd/`, `backup/systemd/`), then `sudo systemctl daemon-reload && sudo systemctl enable --now <each>.timer`.
4. **Drift check**: `make -C ~/homelab check`. Every line should say `ok`.

## Verify

- `make -C ~/homelab check` is all `ok`.
- `systemctl is-active claude-remote-control softdog` both active. `systemctl list-timers` shows `homelab-update`, `kb-export`, `plex-db-export`, `truenas-alert-relay`.
- `/proc/cmdline` contains `nomodeset`; `wdctl` shows softdog.
- In a Remote Control session, the Home Assistant (ha-mcp) tools load and a Notion search works.
- `ssh plex sudo claude-maint unattended-dry-run` succeeds; `truenas-api system.info` returns; `git -C ~/homelab push --dry-run` succeeds.
- Uptime Kuma: `ClaudeCode VM` is up, and `TrueNAS Alert Relay` turns green within about 15 minutes. `KB Export` and `ClaudeCode VM Updates` are weekly, so check them after the next Sunday.
- Log the rebuild in the Changes DB and update the ClaudeCode VM System page (Claude Code version, any spec changes).

## Rollback

The rebuild doesn't touch the old VM, so keep it (renamed and stopped) until the new one passes Verify. To go back: stop the new VM and start the old one. Same MAC, so never run both. Any key or token revoked during the rebuild stays revoked; issue fresh ones for the old VM if you go back.
