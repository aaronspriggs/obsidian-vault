---
type: idea
status: backlog
priority: low
system:
- '[[Plex Media Server]]'
- '[[ClaudeCode (VM)]]'
notion_id: 31a7ae76-22ba-8174-ac5b-e4676e3a3631
---

## Problem

Plex VM and HA VM OS updates are currently managed manually via SSH. The Plex VM has unattended-upgrades enabled for security patches but full upgrades require manual intervention. No visibility into update status across both VMs without SSHing into each one.

## Goal

A centralized way to keep both VMs up to date with minimal manual effort and good visibility.

## Options to Evaluate

1. **Ansible** — playbooks that SSH into all hosts and run updates in one shot. Mac-friendly, terminal-based, fits existing workflow. Could expand to manage TrueNAS host too.
2. **Cockpit** — lightweight web UI installed on each Linux VM. Gives dashboard for updates, services, and resource usage. Less automation but very visual.

## Notes

- Plex VM: Ubuntu 24.04, unattended-upgrades already enabled, 81 pending updates as of 2026-03-05
- HA VM: HAOS — updates managed via HA UI, OS updates are separate
- Ansible is the preferred direction given terminal-based workflow and potential to expand to other infrastructure tasks

## Update 2026-09-26

Partly addressed without Ansible/Cockpit: the lightweight **homelab-update** service (weekly apt full-upgrade, optional app update, reboot if needed, post-update checks, HA and Kuma reporting) is now installed on the Plex VM and ClaudeCode VM. See the runbook "homelab-update: weekly unattended VM updates". Revisit a centralized tool only if the number of VMs grows enough that per-VM installs become a burden.
