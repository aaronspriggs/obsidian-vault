---
date: 2026-03-03
type: doc
system:
- '[[TrueNAS SCALE (Big Boi)]]'
notion_id: 3187ae76-22ba-816b-9be3-d60a839dcda7
---

# Storage architecture planning — two-tier strategy, UNAS Pro, UPS, rack layout

Full storage architecture planning session. Outcomes: (1) Two-tier storage strategy confirmed — existing 5x 870 Evo 4TB SSDs stay as Tier 1, UNAS Pro bulk HDD as Tier 2. (2) UNAS Pro selected as only rackmount NAS fitting 14.6" rack depth constraint. (3) RAID 6 chosen for 7-drive UNAS array — 2-drive parity, 5 drives usable, 80TB with 7x16TB. (4) 12–16TB drives are cost sweet spot at ~$27/TB usable; source recertified Exos from ServerPartDeals, monitor [diskprices.com](http://diskprices.com/). (5) UniFi UPS 2U ($279, 2U, 11.8" deep) selected. (6) Big Boi PCIe slot plan finalized: x16=Arc A380 GPU, x4/x8=existing 10Gtek 82599EN NIC, x1=USB expansion card for UPS NUT cable. (7) Rack wall mount confirmed solid: 13/16" backing board screwed to studs. (8) Three project entries updated/created: Big Boi Server Upgrade (updated NIC + PCIe plan + rack context), UNAS Pro Storage Expansion (new), UPS Power Management (new).
