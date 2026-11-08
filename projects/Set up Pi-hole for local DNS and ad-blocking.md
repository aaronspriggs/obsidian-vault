---
type: project
status: backlog
priority: medium
system:
- '[[UniFi (UDM Pro)]]'
parent: '[[Get full use out of the UDM Pro (segmentation, security, built-in features)]]'
notion_id: 3087ae76-22ba-81d2-a43d-d737bba52f97
---

Previously installed on TrueNAS and removed on 2026-02-06; plan to re-implement. Part of [Get full use out of the UDM Pro](<Get full use out of the UDM Pro (segmentation, security, built-in features).md>).

## Options (researched 2026-11-08)

- **UDM Pro native Ad Blocking first.** A free per-network toggle (Settings → CyberSecure → Ad Blocking). The gateway intercepts plain DNS on port 53, so DHCP can keep handing out 1.1.1.1. It uses Ubiquiti's own list: no custom blocklists or query logs, only per-network allow/block site lists ([Ubiquiti help](https://help.ui.com/hc/en-us/articles/12568927589143)). Off as of 2026-11-08. Aaron hasn't decided whether to trial it.
- **Pi-hole on a dedicated Raspberry Pi** if the native toggle isn't enough (custom lists, logs, local DNS records). Not on Big Boi: DNS there would make every TrueNAS reboot a whole-house outage, and a 1.1.1.1 secondary leaks queries past the filter. Optionally add a second instance on Big Boi later as a synced (nebula-sync) secondary. Don't use the wall panel Pi.
