---
type: task
status: done
priority: medium
system:
- '[[Plex Media Server]]'
- '[[ClaudeCode (VM)]]'
- '[[Home Assistant OS (VM)]]'
completed: 2026-09-28
notion_id: 3e77ae76-22ba-8137-84cb-e869500c06a3
---

Verified 2026-09-28. homelab-update 2026-09-27: Plex VM finished 04:00 MDT (journal), ClaudeCode VM ran 04:30 MDT with 0 upgrades (/var/lib/homelab-update/step.log). HA: ha_updates_ask_for_approval fires (last 2026-09-28 09:00), but the Install tap can't arrive while iOS action buttons are broken upstream (tracked: "Restore iOS notification action buttons", Blocked), so Aaron installed Core 2026.9.4 by hand. install_on_approval gets its first real test once that task unblocks.

## homelab-update first real runs: Sun 2026-09-27

- **Plex VM at 04:00 MDT:** expect a passive "✅ Plex VM updated" push, or no push if nothing changed. Check `/var/log/homelab-update.log` (readable by the `claude` user via `ssh plex`), `automation.homelab_vm_update_reports` traces, and that `sensor.plex_vm_updates_status` stays up.
- **ClaudeCode VM at 04:30 MDT:** it should apply its **18 pending updates** and **reboot into kernel 7.0.0-34**. Check `sudo tail /var/log/homelab-update.log`, that the verify service reported after the reboot, that `claude-remote-control.service` came back, and that the truenas-alert-relay timer resumed (its Kuma push should have stayed up).
- If anything failed, the push says which step. See the runbook "homelab-update: weekly unattended VM updates".

## First real HA update approval

When the next HA Core/OS/app update appears:
- Confirm the "⬆️ Update available" push arrives in daytime (09:00–21:00).
- Tapping it should open `/config/updates`; install from there with backup.
- For a Core/OS update, check that `automation.ha_updates_report_after_restart` sends the ✅ notice after the restart. The Install button itself won't work until iOS #5881 is fixed.
