---
date: 2026-09-02
type: install
system:
- '[[ClaudeCode (VM)]]'
notion_id: 3cf7ae76-22ba-81a2-95f8-c45ab47b6c71
---

# Built ClaudeCode VM — Claude Code Remote Control host on TrueNAS

New Ubuntu 26.04 LTS VM on Big Boi running Claude Code in Remote Control server mode via systemd, built with a cloud-image + injected cloud-init approach (no installer).

Built a new VM (`ClaudeCode`, 192.168.1.156, 2 vCPU / 8GB RAM / 40GB disk) on Big Boi to host Claude Code so it has direct LAN access to homelab systems — starting with Home Assistant — without exposing anything to the public internet. Reachable from any device via [claude.ai/code](http://claude.ai/code) or the Claude mobile app using Remote Control, which only makes outbound connections, so no Cloudflare Tunnel, reverse proxy, or VPN dependency was needed.
Provisioned via a new method for this homelab: an Ubuntu cloud image with a cloud-init NoCloud seed injected directly into the disk (via qemu-nbd) before writing it to the Zvol, rather than either the appliance-image-import approach (used for HA) or an interactive ISO install. Full process, including several gotchas hit along the way (ACL permissions on vmstore, `aspriggs`'s home directory being the non-writable `/var/empty`, a YAML paste corruption with bracketed list syntax, qemu-nbd needing an explicit `--format=qcow2`, the newer VM wizard's CPU-topology multiplication and Trust-Guest-Filters/bridge incompatibility, and a systemd service that needed a one-time interactive consent answered manually before it would start clean) is documented in the new Runbook.
Software: Node.js (NodeSource LTS) and Claude Code (native install, not npm-global, so it can self-update without sudo), running as `claude-remote-control.service` out of `/home/aspriggs/homelab-agent`.
Next step: point this Claude Code instance at Home Assistant's REST API with a long-lived token to start actually building automations and dashboards.
