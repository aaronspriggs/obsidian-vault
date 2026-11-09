---
date: 2026-11-09
type: research
system:
- '[[UniFi (UDM Pro)]]'
project: '[[Bring Ting Fiber 2000 online as a second WAN on the UDM Pro]]'
---

## What changed

No system changes. I researched how to bring Ting Fiber 2000 (install 2026-12-07) onto the UDM Pro next to CenturyLink and wrote the plan into the [project](<../projects/Bring Ting Fiber 2000 online as a second WAN on the UDM Pro.md>).

## Why

Aaron ordered Ting and wants it plugged straight into the UDM Pro like CenturyLink is, with both lines running until one is cancelled.

## How

Read the current WAN config with `unifi-api rest/networkconf stat/device` (read-only). Internet 1 is PPPoE on VLAN 201 on Port 9. Internet 2 is DHCP, failover-only, with no port. SFP+ 1 is empty. Sources (Ting help center, Ubiquiti tech specs) are linked from the project.

## How to verify / roll back

Nothing to roll back.
