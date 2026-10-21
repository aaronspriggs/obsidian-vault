---
date: 2026-03-07
type: upgrade
system:
- '[[TrueNAS SCALE (Big Boi)]]'
- '[[Home Assistant OS (VM)]]'
notion_id: 31c7ae76-22ba-81e9-9f50-ede577bd34a6
---

# Moved haos_disk zvol into vmstore dataset

Moved the HA VM zvol from the pool root into `vmstore` to consolidate all VM zvols under a single parent dataset.

## What was done

- Took pre-rename snapshot: `Big Boi/haos_disk@pre-rename`
- Stopped HA VM from TrueNAS UI
- Ran: `sudo zfs rename "Big Boi/haos_disk" "Big Boi/vmstore/haos_disk"`
- Updated disk device path in TrueNAS VM config UI to `/dev/zvol/Big+Boi/vmstore/haos_disk`
- TrueNAS did NOT auto-update the libvirt XML — updated manually via `sed` and verified
- Started HA VM — booted successfully, wall panel and automations confirmed working
- Deleted pre-rename snapshot

## Result

`vmstore` now contains both VM zvols: `haos_disk` and `Plex-9wert`. Pool root is clean.

## Gotcha noted

TrueNAS does not automatically update `/etc/libvirt/qemu/3_HomeAssistant.xml` when you edit the VM disk path in the UI. Always verify with `sudo grep -i haos_disk /etc/libvirt/qemu/3_HomeAssistant.xml` after any VM disk path change and update manually if needed. `virsh define` is not available on TrueNAS — the sed edit to the XML file is sufficient as TrueNAS middleware reads it directly.
