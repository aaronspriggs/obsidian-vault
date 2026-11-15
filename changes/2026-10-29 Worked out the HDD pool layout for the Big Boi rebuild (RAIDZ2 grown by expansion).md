---
date: 2026-10-29
type: research
system:
- '[[TrueNAS SCALE (Big Boi)]]'
project: '[[Rebuild Big Boi into a new case with an HDD pool for bulk media]]'
---

## What changed

No system changes. The capacity math behind the HDD pool decision of 2026-10-29. Moved here on 2026-11-15 from the [project](<../projects/Rebuild Big Boi into a new case with an HDD pool for bulk media.md>) note when it was slimmed under the rulebook's size rule; the text is as it stood in the note that day, with its original dates.

## Why

Aaron wants to start with 4 drives and add 1 or 2 at a time; this shows what that costs against building 12-wide at once, and why a rewrite at full width recovers it.

## How

### The decision

- **2026-10-29 (Aaron):** HDD pool = one RAIDZ2 vdev, started 4-wide and grown 1–2 drives at a time by RAIDZ expansion (OpenZFS 2.3, in 25.04) up to 12-wide. Every drive the same size (a vdev counts each disk at its smallest member). At full width, rewrite the data once (`zfs rewrite` on 25.10, or dataset copy-and-swap on 25.04) so old blocks move from the narrow parity ratio to 10+2; expire the media dataset's snapshots first or the rewrite costs space. Mirrors rejected (50% forever), RAIDZ1 rejected (expansion can't change parity later). Math in Reference: HDD pool layout.

### Reference: HDD pool layout (2026-10-29)

RAIDZ2 of N drives holds (N − 2) × drive size when built fresh; with 20 TB drives: 4-wide 40 TB (50%), 6-wide 80, 8-wide 120, 10-wide 160, 12-wide 200 TB (83%), about 182 TiB as TrueNAS shows it. After expansion, existing blocks keep the ratio they were written at and new blocks use the new width ([TrueNAS docs](https://www.truenas.com/docs/tags/raidz/), [extension calculator](https://www.truenas.com/docs/references/extensioncalculator/)); parity level can't change ([forum](https://forums.truenas.com/t/does-electriceel-support-change-vdevs-parity-ratio-for-existing-vdev/23421)). Simple model (no metadata/padding), adding one drive each time the pool reaches a fill level, 20 TB drives: at 80% full the vdev ends at about 167 TB at 12-wide, at 100% about 159 TB, versus 200 TB fresh. The loss scales with data written while narrow; a rewrite recovers it. The dashboard can show less than this after expansion because free space is estimated at the original ratio.

## How to verify / roll back

Nothing to roll back.
