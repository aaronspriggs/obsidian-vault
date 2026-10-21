---
type: project
status: backlog
priority: low
system:
- '[[TrueNAS SCALE (Big Boi)]]'
notion_id: 3187ae76-22ba-81dc-965c-d8a7c7f00759
---

Superseded 2026-10-15: Aaron chose to rebuild Big Boi with an HDD pool instead of buying a UNAS Pro. Kept for the research (rack depth, drive pricing).

> **Superseded 2026-10-15 (Aaron):** the UNAS Pro is no longer planned. Bulk storage becomes an HDD pool in a rebuilt Big Boi; see [Rebuild Big Boi into a new case with an HDD pool](<Rebuild Big Boi into a new case with an HDD pool for bulk media.md>). The research below is kept for reference: rack depth limit, drive pricing, RAID 6 reasoning.

## Overview

Add a second storage tier to the homelab to accommodate growing Overseerr media library, cold storage, and archive content. The existing 5x Samsung 870 Evo 4TB SSDs in RaidZ1 on Big Boi remain **Tier 1** (performance, VM storage, config, ZFS integrity). The UNAS Pro serves as **Tier 2** bulk spinning rust — content is re-downloadable via Overseerr/Servarr, so ZFS integrity guarantees are not required at this tier.

## Selected Hardware

### UniFi UNAS Pro (7-bay NAS)

- **Price:** $499
- **Bays:** 7x 3.5" hot-swap
- **Dimensions:** 442.4 × 325 × 87.4 mm (17.4" × **12.8" depth** × 3.4") — fits 14.6" rack constraint
- **Networking:** 1x 10G SFP+ (connects to USW Pro Max 16 PoE), 1x GbE RJ45
- **Management:** Native UniFi Network app
- **Shutdown integration:** Native graceful shutdown support with UniFi UPS 2U
- **Shares:** NFS and SMB supported

### Why UNAS Pro (and not alternatives)

The rack has a **14.6" (370mm) max mountable depth** constraint. The UNAS Pro at 12.8" is the only rackmount NAS in the target capacity range that fits:
- UNAS Pro 4 (1U, 4-bay): 15.7" deep — too deep
- UNAS Pro 8 (2U, 8-bay): 18.9" deep — too deep
- Synology/QNAP rackmount options at 8+ bays: all exceed 14.6"
- Sliger CX3702 (3U chassis for Big Boi with internal HDDs): 18" deep — too deep
UniFi ecosystem integration (shared management with existing switches, native UPS shutdown) reduces management overhead and is the right fit for a homelab that's already all-in on UniFi networking.

### Known Limitations

- No ZFS (proprietary RAID implementation)
- No Docker/VM support
- Limited cloud backup targets (no native S3/Backblaze B2)
- No iSCSI
- Software platform less mature than Synology/QNAP
All accepted: Tier 2 content is replaceable, and the UniFi fit outweighs the feature gaps for this use case.

## RAID Configuration

**Selection: RAID 6** (2-drive parity across 7 drives)
- **Usable capacity:** 5 drives equivalent
- **Failure tolerance:** Any 2 simultaneous drive failures
- **Rationale:** Large HDD rebuilds take days. Probability of a second failure during rebuild is real. RAID 5 (1-parity) leaves the array completely exposed during any rebuild. RAID 10 requires even drive count and loses half capacity — overkill for sequential media reads.

## Drive Selection & Capacity Planning

| Drive Size | Price/drive (est. 2026) | Total cost (×7) | Usable capacity (5×) | $/TB usable |
| --- | --- | --- | --- | --- |
| 8TB | ~$170 | ~$1,190 | 40TB | ~$29.75/TB |
| 12TB | ~$240 | ~$1,680 | 60TB | ~$28.00/TB |
| 16TB | ~$310 | ~$2,170 | 80TB | ~$27.13/TB |
| 18TB | ~$390 | ~$2,730 | 90TB | ~$30.33/TB |
| 20TB | ~$420 | ~$2,940 | 100TB | ~$29.40/TB |

**Sweet spot: 12TB–16TB.** The 16TB tier hits the lowest $/TB usable at ~$27/TB. 80TB usable (7×16TB) accommodates roughly 1,100–1,600 4K movies at 50–70GB each, or a mixed library of 500–800 movies + 50–100 complete TV series — multi-year runway for Overseerr accumulation.

### HDD Market Context (as of early 2026)

Prices surged ~46% on average since September 2025 (range 23–66% depending on model), driven by AI data center demand consuming enterprise HDD supply. WD sold out through 2026; manufacturers at full utilization. Historical reference: 12TB drives now at ~$240 were ~$160–170 a year ago.
**Recommended sourcing strategy:** ServerPartDeals recertified Seagate Exos drives are somewhat insulated from new-drive pricing (sourced from enterprise lease returns). Monitor [**diskprices.com**](http://diskprices.com/) for current $/TB sweet spot before purchasing.

### Drive Upgrade Path (RAID 6)

RAID 6 allows incremental drive size upgrades but uses the smallest drive as the common denominator until all drives are replaced:
1. Replace drive 1 with larger size → rebuild (24–48 hrs, array degraded to single-parity)
2. Repeat for each drive sequentially
3. After all 7 replaced, expand volume to claim new space
Viable long-term expansion strategy, but not fast — plan weeks of elapsed time.

## Network Integration

UNAS Pro connects via its 10G SFP+ port to the **USW Pro Max 16 PoE** (which has 2x 10G SFP+ ports; one already used by Big Boi). Plex VM and servarr stack on Big Boi access bulk media via NFS share over the 10G backbone.

## Action Items

- [ ] Purchase UNAS Pro when bulk storage becomes an active need
- [ ] Source 7x HDDs via ServerPartDeals recertified Exos (check [diskprices.com](http://diskprices.com/) for timing)
- [ ] Configure RAID 6 array on UNAS Pro
- [ ] Set up NFS share and mount on Big Boi / Plex VM
- [ ] Configure Sonarr/Radarr to write to bulk tier path
- [ ] Test graceful shutdown integration with UPS 2U

## Changes

![[Changes.base#For this project]]
