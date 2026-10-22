---
kind: procedure
status: active
system:
- '[[TrueNAS SCALE (Big Boi)]]'
notion_id: 2ff7ae76-22ba-8120-8570-ea91e2bf0456
---

Planned restart of Big Boi: timing, Claude pre-checks, VM shutdown order, restart, post-checks (pool, VMs, HA Zigbee, Plex NFS, Gluetun IP), failure modes. Takes Claude's session down with it.

## When to use

A planned restart of Big Boi (TrueNAS SCALE, 192.168.1.248): TrueNAS updates, hardware work, or anything that needs the host down. **Everything goes down with it:** the Home Assistant, Plex and ClaudeCode VMs, Dockhand, the servarr stack and Uptime Kuma. That means no HA automations or alerts, no wall panel, no Plex, and **no Claude session** (Claude Code runs on the ClaudeCode VM). Expect about 5–10 minutes. For an unplanned outage (power cut, crash), skip to After the reboot.

## Prerequisites

- TrueNAS web UI [https://192.168.1.248:9443](https://192.168.1.248:9443/) as `truenas_admin` (1Password "TrueNAS - Admin"). SSH `aspriggs@192.168.1.248` as a fallback.
- **Pick a time outside the scheduled jobs:** pool scrub Sunday 00:00, Plex VM update Sunday 04:00, ClaudeCode VM update Sunday 04:30, Dockhand stack backup nightly 23:30.
- There's no graceful UPS shutdown yet (the UPS 2U isn't configured), so every reboot should be a planned one.

## Steps

**Step 1. Pre-checks (ask Claude before you start).** Claude checks through the read-only TrueNAS API: pool `Big Boi` ONLINE and healthy, no scrub or resilver running, no unexpected alerts (the "new ZFS feature flags" notice is expected; don't upgrade the pool as part of a reboot), all three VMs running, Dockhand app running. Claude also commits and pushes any open work in the repo and the KB vault, because the session ends at step 4.
**Step 2. Tell the household:** no Plex, and no smart-home automations or wall panel, for about 10 minutes. Physical light switches still work.
**Step 3. Optional: shut the VMs down yourself** (Virtualization → each VM → Stop), in this order: ClaudeCode, Plex, HomeAssistant. TrueNAS does this anyway on restart, but it forces off any VM still running after 90 s (`shutdown_timeout` is 90 for all three), so stopping them first lets you see that each one shut down cleanly. HA takes the longest.
**Step 4. Restart:** the power icon in the TrueNAS top bar → **Restart**, confirm. Over SSH instead: `sudo midclt call system.reboot "planned reboot"` (the argument is the reason text).

## After the reboot

All three VMs and Dockhand autostart; you don't need to start anything by hand unless a check fails.
**Step 5. Host:** the web UI loads (allow 3–5 minutes), Storage shows `Big Boi` ONLINE, and Virtualization shows HomeAssistant, Plex and ClaudeCode running.
**Step 6. Claude:** once the ClaudeCode VM is up, `claude-remote-control.service` starts at boot. Open a new session from [claude.ai/code](http://claude.ai/code) or the app and ask Claude to run the post-checks. Earlier sessions may be listed under "Other" if the VM registered a new environment ID. Claude checks:
- TrueNAS API: pool healthy, 3 VMs running, Dockhand app running, no new alerts.
- ha-mcp: HA answers, and ZHA has its devices (Zigbee depends on the Sonoff ZBDongle-E USB passthrough) and no integrations stuck retrying beyond the usual ones.
- `ssh plex`: `/mnt/media` and `/mnt/dvr` mount on access (systemd automount), `/transcode` tmpfs is mounted, Plex is running.
- Uptime Kuma via HA: every monitor up.
**Step 7. Servarr (you, over SSH):** after a host restart Docker starts all containers at once, which is exactly when `gluetun-watchdog` can take Gluetun's 172.39.0.2:
```bash
sudo docker network inspect servarrnetwork --format '{{range .Containers}}{{.Name}} {{.IPv4Address}}{{"\n"}}{{end}}'
```
If `gluetun` doesn't hold .2, or NZBGet/Prowlarr are unreachable, follow [Recovering Gluetun](<Recovering Gluetun - stuck exited - address already in use on restart.md>).
**Step 8.** Set this runbook's `Last Tested`, and log the reboot in Changes if it was for a change (update or hardware).

## Verify

Pool ONLINE; 3 VMs running; HA, Plex, all five servarr UIs, Dockhand (:3001) and Kuma (:3002) load; every Kuma monitor is up, so HA has no open homelab alert.

## Failure modes

- **Pool doesn't import / DEGRADED:** don't reboot again. Check Storage → the pool's disks and `sudo zpool status -v "Big Boi"`. The VMs and apps won't start without it. Get Claude to read the alert text from the API once the ClaudeCode VM is back, or work from the console if it isn't.
- **A VM won't start:** read the error under Virtualization. Plex depends on iGPU (PCI) passthrough, HA on the Zigbee USB dongle; a missing or busy device blocks the start. Start the others anyway.
- **HA up but Zigbee devices unavailable:** the dongle didn't reattach. Check the HA VM's USB device in TrueNAS, then restart the VM.
- **ClaudeCode VM hangs at shutdown:** TrueNAS forces it off after 90 s. That's fine; it has a watchdog and comes back on boot.
- **Plex shows empty libraries:** NFS wasn't ready when Plex scanned. See [Plex VM NFS Mount Setup & Troubleshooting](<Plex VM NFS Mount Setup & Troubleshooting.md>); usually `ls /mnt/media` on the VM followed by a library rescan is enough.

## Rollback

A reboot changes nothing. If it was for a TrueNAS update that went wrong, pick the previous boot environment under System → Boot and restart again.
