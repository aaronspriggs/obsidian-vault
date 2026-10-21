---
date: 2026-02-19
type: fix
system:
- '[[TrueNAS SCALE (Big Boi)]]'
notion_id: 30d7ae76-22ba-8155-a81e-d8decf7045e6
---

# Changed ZFS aclmode to passthrough on Big Boi/BIGBOI

Docker LinuxServer containers failed with 'chmod operation not permitted' because aclmode was set to 'restricted'. Changed to 'passthrough' with: sudo zfs set aclmode=passthrough "Big Boi/BIGBOI". Required for any Docker containers that modify permissions at startup.
