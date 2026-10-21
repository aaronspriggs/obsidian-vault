---
date: 2026-10-16
type: doc
system:
- '[[TrueNAS SCALE (Big Boi)]]'
project:
- '[[Claude access model - more admin access, secrets management, account hardening]]'
notion_id: 3fb7ae76-22ba-8152-b05a-f4094a2ceda9
---

# Wrote the Big Boi bare-metal rebuild runbook; DR runbook set complete

New runbook 'Rebuild Big Boi (TrueNAS) from bare metal': Case 1 (pool intact: reinstall 25.04, upload truenas-config.tar from the pool or B2 via rclone) and Case 2 (pool lost: new pool named 'Big Boi', recreate datasets, keep the B2 SYNC tasks disabled until restored, then VM runbooks; marked untested because config-onto-new-pool behaviour isn't documented). Desk-checked live via truenas-api (25.04.2.6, br0 on enp1s0, 4 local users, Dockhand app, stacks cron, NFS/SMB/SSH/UPS/SMART services). DR index step 1 now links it, so all four rebuild runbooks exist. Big Boi System page: Dockhand 1.1.38 (was 1.1.34), enabled services incl. UPS as NUT client of 192.168.1.12. No repo changes.
