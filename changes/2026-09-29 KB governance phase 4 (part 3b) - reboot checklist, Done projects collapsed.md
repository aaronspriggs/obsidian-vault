---
date: 2026-09-29
type: doc
system:
- '[[TrueNAS SCALE (Big Boi)]]'
- '[[Plex Media Server]]'
project:
- '[[KB governance - clean up the Notion KB and keep it current (Claude as knowledge manager)]]'
notion_id: 3ea7ae76-22ba-819e-a378-c36dbcf2e753
---

# KB governance phase 4 (part 3b): reboot checklist, Done projects collapsed, VM and NFS runbooks fixed

Wrote Big Boi Reboot Checklist from live TrueNAS data; rewrote Plex NFS runbook from the live VM; collapsed 5 Done projects and trimmed the monitoring project (3,805 words); narrowed the old VM runbook to appliance images; 3 follow-ups extracted; Last Tested set on 8 runbooks.

## What

- **Big Boi Reboot Checklist:** written from the stub, using live TrueNAS API data (3 VMs autostart, `shutdown_timeout` 90 s each, UPS service off, scrub Sun 00:00, stack backup 23:30). Covers timing, Claude pre-checks, the fact that the reboot ends the Claude session, post-checks (pool, VMs, HA Zigbee dongle, Plex NFS, Gluetun .2 race) and failure modes. `Last Tested` empty until first use.
- **Plex VM NFS Mount runbook:** rewritten from the live VM (both automount entries, exports restricted to 192.168.1.116, automount unit names). It still said exports allow 192.168.1.0/24 and "no automount". Check steps run 2026-09-29.
- **Done projects collapsed** to Outcome/Decisions/Links: repo foundation (also fixed the relative "this week's work"), CPU swap, Plex VM SSH, haos_disk move, ha-mcp setup. Board/case/PSU/NIC and the CPU-swap decision moved to the TrueNAS page.
- **Monitoring project** trimmed from 3,805 words to status + remaining work (linked) + dated decisions; Next Step set.
- **Follow-ups extracted:** "Confirm the HA backup encryption key is saved in 1Password" (Task, Active, High), "Evaluate Renovate" (Idea, Deferred), "Check whether Cowork can read the spriggs-homelab repo" (Task, Backlog).
- **VM runbooks:** "Creating a New VM" renamed "Creating an Appliance-Image VM (e.g. HAOS)", scoped to appliance images and pointed at the cloud-init runbook's wizard step. Its NIC instruction (`enp1s0` + Trust Guest Filters) was wrong for the `br0` bridge.
- **`Last Tested`** set from Changes history: homelab-update 2026-09-25, TrueNAS API/relay 2026-09-26, ha-mcp 2026-09-03, cloud-init VM 2026-09-02, Google Drive backup 2026-09-04, Updating the Plex VM 2026-09-24, Recovering Gluetun 2026-07-11, Plex NFS 2026-09-29.

## Roll back

Pre-change copies of every page: KB export 4ac914e (branch `kb-export`).
