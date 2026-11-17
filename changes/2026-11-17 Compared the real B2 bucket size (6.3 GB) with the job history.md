---
date: 2026-11-17
type: research
system:
- '[[Big Boi storage (pool, datasets, shares, backups)]]'
project: '[[Plan backup strategy for TrueNAS and VMs]]'
---

## What changed

No system changes. Aaron read the size of bucket `spriggs-bigboi-backup` in the B2 web UI: **6.3 GB**. Claude compared it with the TrueNAS job history and corrected the estimate in the [project](<../projects/Plan backup strategy for TrueNAS and VMs.md>) note.

## Why

The 2026-10-23 estimate said the bucket would settle at 4–5 GB. Claude has no B2 credentials, so the real number had to come from Aaron, and it came in higher.

## How

`truenas-api core.get_jobs` filtered to `cloudsync.sync`: 66 jobs from 2026-10-16 to 2026-11-16, all SUCCESS. Uploaded per night, from each job's progress line:

| Nights | BIGBOI | vmstore |
| --- | --- | --- |
| 2026-10-16 (first runs) | 2,044 MiB | 430 MiB |
| 2026-10-17 to 10-23 (before the fix) | 15–24 MiB | 204–257 MiB |
| 2026-10-24 to 11-03 | 18–24 MiB | 91–118 MiB |
| 2026-11-04 to 11-16 | 18–25 MiB | 91–138 MiB |

Total uploaded since the start: 7.04 GiB (7.56 GB), 2,656 MiB by BIGBOI and 4,550 MiB by vmstore.

What this shows:

- **The estimate's nightly figure was wrong.** The 2026-10-23 note expected 60–70 MiB a night after the fix. The real figure is about 125 MiB (vmstore averages about 105, BIGBOI about 20). The fix did halve the vmstore upload, from about 205 MiB.
- **The bucket holds less than was ever uploaded,** 6.3 GB against 7.56 GB, because B2 deletes a prior version 30 days after it was replaced. Only the versions replaced on 2026-10-17 (about 0.2 GB) are certain to have gone by now. Claude can't account for the other 1 GB from here; B2's own figure is the one to trust.
- **Where it settles.** The seven nights before the fix each left about 100 MiB more behind than a night does now; those versions leave between 2026-11-16 and 2026-11-23. After that, by upload arithmetic the bucket holds the current files (about 2.5 GiB) plus 30 nights at 125 MiB, about 6.6 GB; since the arithmetic runs 1.2 GB above B2's figure today, expect between 5.5 and 6.5 GB.
- **The vmstore upload is creeping up,** from 91–95 MiB most nights in late October to 108–138 MiB in mid-November. Not traced. It would have to more than double to reach the free tier's edge.

Cost: nothing under 10 GB; $6.95 per TB a month above it, which is $0.007 per GB.

## How to verify / roll back

Nothing to roll back. Bucket size: https://secure.backblaze.com/b2_buckets.htm (Aaron's login). Job history: `truenas-api core.get_jobs '[[["method","=","cloudsync.sync"]]]'`; it is kept in memory and is lost when Big Boi reboots.
