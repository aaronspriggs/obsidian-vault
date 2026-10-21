---
date: 2026-09-03
type: fix
system:
- '[[Home Assistant OS (VM)]]'
notion_id: 3d07ae76-22ba-8141-85b9-fccede238e61
---

# Fixed automatic backup failures (removed Nabu Casa cloud upload target)

The "automatic_backup_failed" repair (open since 2026-08-29, failed_agents: cloud) was caused by the automatic backup's target agent list being ["hassio.local", "[cloud.cloud](http://cloud.cloud/)"] — Aaron confirmed he does not have an active Nabu Casa subscription, so the [cloud.cloud](http://cloud.cloud/) upload was always going to fail. Local uploads were succeeding fine.

Note: the "Home Assistant Google Drive Backup" add-on (also installed) is a separate standalone add-on with its own independent backup/upload schedule — it is not one of the core Backup feature's agent_ids and was unaffected by this issue either way.

Fix: via ha_call_service(ws_command="backup/config/update"), set create_backup.agent_ids to ["hassio.local"] only, dropping [cloud.cloud](http://cloud.cloud/). Verified via backup/config/info. Next scheduled automatic backup is 2026-09-04 ~05:24 America/Denver — the repair issue should clear on its own once that one succeeds without the cloud target.
