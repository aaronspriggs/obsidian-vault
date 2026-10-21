---
kind: procedure
status: active
system:
- '[[Plex Media Server]]'
- '[[ClaudeCode (VM)]]'
- '[[Home Assistant OS (VM)]]'
last_tested: 2026-09-25
notion_id: 3e67ae76-22ba-8115-9432-f8d5ef638e31
---

# homelab-update: weekly unattended VM updates (install, add a VM, troubleshoot)

Reusable weekly update service for any Debian/Ubuntu VM: apt full-upgrade + optional app update + reboot-if-needed + post-update checks, reporting to an HA webhook (notices) and an Uptime Kuma push monitor (missed-run heartbeat). Full source, per-host configs, install and add-a-VM steps.

## What it does

Each Sunday, a systemd timer on every enrolled VM runs `/usr/local/sbin/homelab-update run`:
1. `apt-get update` and a non-interactive `full-upgrade` that keeps existing config files, then `autoremove`.
2. The optional per-host app update (e.g. Plex via `claude-maint upgrade-plex`).
3. If `/var/run/reboot-required` exists, it saves a summary, sets a `pending` flag and reboots. At boot, `homelab-update-verify.service` (conditional on the flag) finishes the job.
4. It runs the host's check list, retrying for up to 5 minutes while services come up.
5. It POSTs the result to the HA webhook, which `automation.homelab_vm_update_reports` reports to Alert2 (since 2026-10-14; repo `ha/alert2.yaml`):
    - **failed:** `homelab.vm_update_failed` (medium, time-sensitive)
    - **success with changes** (and installer test reports): `homelab.vm_updated` (low, passive). Runs happen before 09:00, so these are held by quiet hours and listed in the 09:00 report.
    - **nothing changed:** logbook only, no push
6. On success, it pings the host's **Uptime Kuma push monitor** (8-day window). A missed week makes that monitor go `down`, and Alert2's `alert2.homelab_<vm>_updates_missed` sends "heartbeat missed".
Nightly Ubuntu `unattended-upgrades` (security only) keeps running too. This adds the weekly full-upgrade and the reboot.
**Home Assistant OS is not enrolled.** HAOS isn't apt-based, and Core/OS upgrades need approval. HA uses its own update-approval notifications instead.

## Source code

Lives in the repo, not here: [`homelab-update/`](https://github.com/aaronspriggs/spriggs-homelab/tree/main/homelab-update) in `aaronspriggs/spriggs-homelab` (clone on the ClaudeCode VM: `~/homelab`).
- [`homelab-update`](https://github.com/aaronspriggs/spriggs-homelab/blob/main/homelab-update/homelab-update): the script
- [`install.sh`](https://github.com/aaronspriggs/spriggs-homelab/blob/main/homelab-update/install.sh): installer; generates the three systemd units
- [`hosts/`](https://github.com/aaronspriggs/spriggs-homelab/tree/main/homelab-update/hosts): per-VM config templates (`plex-vm.conf.example`, `claudecode-vm.conf.example`) with the webhook ID removed
`make check` in the repo confirms the deployed script on each VM matches the repo.

## Enrolled VMs

| VM | Schedule (America/Denver) | App update | Checks | Kuma push monitor |
| --- | --- | --- | --- | --- |
| Plex VM (192.168.1.116) | Sun 04:00 | Plex from [plex.tv](http://plex.tv/) | 7 | Plex VM Updates |
| ClaudeCode VM (192.168.1.156) | Sun 04:30 | none | 3 | ClaudeCode VM Updates |

Installed 2026-09-25. Both install test reports reached HA (Plex 7/7, ClaudeCode 3/3 checks passing).

## Files on each VM

- `/usr/local/sbin/homelab-update` (root 755): the script, identical on every VM
- `/etc/homelab-update.conf` (root **600**, because it holds the webhook URL and Kuma push URL): per-host settings
- `/etc/systemd/system/homelab-update.{service,timer}` and `homelab-update-verify.service`
- `/var/log/homelab-update.log` and `/var/lib/homelab-update/` (state)
Manual commands, as root: `homelab-update test` sends a test report and heartbeat without updating anything; `homelab-update run` does a real update now and may reboot.

## Add another VM

1. In Kuma, add a monitor: Type **Push**, name `<VM name> Updates`, heartbeat interval **691200** (8 days), retries 0. Copy its push URL.
2. In the repo, add `homelab-update/hosts/<vm>.conf.example` (copy an existing one): set `HOST_LABEL`, `UPDATE_TIME` (stagger 30 min after the previous VM), an optional `APP_NAME`/`app_update`/`app_version`, and `CHECKS`. Commit it, and add the VM's script path to `deployed.tsv`.
3. Copy the `homelab-update/` directory to the VM, make `<vm>.conf` from the template with the real webhook ID filled in (it's in the trigger of `automation.homelab_vm_update_reports`), then run `sudo bash install.sh <vm>.conf` and paste the push URL when asked. Needs root, so Aaron runs it.
4. In HA, add `sensor.<vm>_updates_status` to the `homelab_watch` label, add a line for it to the `homelab_heartbeat_missed` generator and to the `homelab_service_down` exclusion list in repo `ha/alert2.yaml`, apply it and run `alert2.reload`. (Step 1 is now a file under `stacks/uptime-kuma/monitors/` deployed by Claude; see the Uptime Kuma page.)
5. Update this page's Enrolled VMs table.

## Updating the script

Edit in the repo, commit and push, then on each VM: `sudo install -m 755 -o root -g root homelab-update /usr/local/sbin/homelab-update` (Claude can do the ClaudeCode VM; Aaron does the Plex VM). Run `make check` afterwards.

## Troubleshooting

- "heartbeat missed": check `systemctl list-timers homelab-update.timer`, `systemctl status homelab-update.service`, and the log.
- "update needs attention": the push names the failed step or checks. The full apt output is in `/var/log/homelab-update.log`.
- The installer's `systemctl list-timers … | head` pipe could abort it under `set -o pipefail`. **Fixed** in the repo version (seen once on the ClaudeCode VM on 2026-09-25; that install completed but skipped the test report).
The webhook ID is shared by all VMs and is in the HA automation's trigger. It only accepts local POSTs (`local_only: true`). If it's ever exposed, change it in both the automation and each VM's `/etc/homelab-update.conf`.
