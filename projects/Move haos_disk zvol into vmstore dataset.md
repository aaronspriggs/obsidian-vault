---
type: task
status: done
priority: low
system:
- '[[TrueNAS SCALE (Big Boi)]]'
completed: 2026-03-07
notion_id: 31c7ae76-22ba-8196-b6bd-cedabe069049
---

Audited 2026-03-07 — only two path references: TrueNAS middleware and /etc/libvirt/qemu/3_HomeAssistant.xml. Blast radius is contained. Low priority — not blocking backup setup.

## Outcome

Done 2026-03-07: the HA OS disk zvol was renamed from `Big Boi/haos_disk` to `Big Boi/vmstore/haos_disk`, so all three VM disks sit under `vmstore` and its daily snapshot task covers them. Confirmed via the TrueNAS API 2026-09-28: `vmstore/haos_disk` exists and the `@pre-rename` safety snapshot is gone. Current layout: [TrueNAS SCALE (Big Boi)](<../systems/TrueNAS SCALE (Big Boi).md>) → Datasets and zvols.

## Decisions and lessons (2026-03-07)

- Only two things referenced the zvol path: the TrueNAS VM config (`/dev/zvol/Big+Boi/haos_disk`) and the libvirt XML `/etc/libvirt/qemu/3_HomeAssistant.xml`. So a rename is low-risk: stop the VM, `zfs rename` (metadata only, instant), update the disk path under Virtualization → VM → Edit, and grep the libvirt XML to confirm TrueNAS rewrote it before starting the VM.
- Take a `@pre-rename` snapshot first and keep it until the VM is confirmed healthy. Rollback is the same rename in reverse plus restoring the old path.

## Links

Pre-collapse checklist: KB export commit 4ac914e.
