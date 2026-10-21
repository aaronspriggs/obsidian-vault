---
date: 2026-10-16
type: doc
system:
- '[[Home Assistant OS (VM)]]'
project:
- '[[Claude access model - more admin access, secrets management, account hardening]]'
notion_id: 3fb7ae76-22ba-81ae-959e-d6756154961b
---

# Wrote the Home Assistant restore runbook

New runbook 'Restore Home Assistant from backup (new VM or in place)', desk-checked live: backup diagnostics show daily automatic backups with include_all_addons and include_database true (so the Matter fabric and Mosquitto come back), retention 7 days local / 30 days Google Drive, encrypted; TrueNAS VM definition (1x2x1 vCPU, 4 GiB, UTC clock, MAC 00:a0:98:61:a7:c1, USB CP210x 10c4:ea60 as usb_1_5). Linked from the DR index step 3. HA System page backup line corrected (it said 'retention above the default 3') and USB/clock details added. No repo changes.
