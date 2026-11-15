---
date: 2026-11-08
type: research
system:
- '[[TrueNAS SCALE (Big Boi)]]'
project: '[[Rebuild Big Boi into a new case with an HDD pool for bulk media]]'
---

## What changed

No system changes. The working-out of 2026-11-07 and 2026-11-08 on replacing the Designare and i9-9900 with an LGA1700 or AM4 platform, as the dated lines the project note carried. Moved here on 2026-11-15 from the [project](<../projects/Rebuild Big Boi into a new case with an HDD pool for bulk media.md>) note when it was slimmed under the rulebook's size rule; the text is as it stood in the note that day, with its original dates.

## Why

Aaron bought a second 64 GB kit on 2026-11-07 and asked whether a newer DDR4 platform was worth it. Outcome (Aaron, 2026-11-08): stay with the Designare, the i9-9900 and 128 GB.

## How

- **2026-11-07 (Aaron):** second CMK64GX4M2D3600C18 kit bought (128 GB total; supersedes the 2026-10-28 no-RAM decision). Exploring LGA1700 (12th–14th gen) in place of the Designare + i9-9900, open to reselling both; constraints: keep the DDR4 kits, Plex stays a VM (the earlier TrueNAS app had problems), budget not set. LGA1700 iGPU passthrough to a VM is unreliable per Proxmox reports ([thread](https://forum.proxmox.com/threads/intel-alder-lake-i5-12500-uhd-770-passthrough-the-dreaded-code-43-error.113229/)), so the plan assumes a discrete Arc card for the Plex VM.
- **2026-11-07 (Aaron):** future LLM GPU out of scope; TrueNAS apps should still be able to use a GPU. LGA1700 sketch (CPU not chosen; i7-12700 suggested as a starting point, still under discussion); HBA on the CPU x16 slot, Arc for the Plex VM on a chipset x4 slot (transcoding needs little bandwidth), NIC on a second chipset slot, UHD 770 stays with the host for apps (no AV1 encode on it). So x8/x8 isn't needed. Candidate: ASUS TUF GAMING Z790-PLUS (WIFI) D4, per [ASUS spec](https://www.asus.com/us/motherboards-components/motherboards/tuf-gaming/tuf-gaming-z790-plus-wifi-d4/techspec/): CPU PCIe 5.0 x16, chipset PCIe 4.0 x16 (x4), PCIe 4.0 x4, 2× x1; 4 SATA (SSD #5 on an HBA spare port); 4× M.2; 4 DIMM, 128 GB DDR4. Unchecked: whether the x4 slot takes the x8 82599EN (open-ended or not); MSI/Gigabyte pages blocked automated fetches.
- **2026-11-08 (Aaron):** CPU priority is headroom; somewhat hotter is fine, up to what the NH-U9S handles comfortably, nothing near 200 W; would buy new if a DDR4 board + CPU combo deal turns up. Leading option: i7-14700 non-K (8P+12E, 28T) bought new, latest BIOS microcode before first boot, power limits set in BIOS (sustained 65 W, boost capped around 125–150 W instead of the stock 219 W) to suit the 92 mm cooler. Not chosen.
- **2026-11-08:** checked ASUS PRIME B760M-A AX D4 (Micro Center, $129.99) per [ASUS spec](https://www.asus.com/us/motherboards-components/motherboards/prime/prime-b760m-a-ax-d4/techspec/): mATX; CPU PCIe 4.0 x16; chipset 1× x16 (x4 mode) + 2× x16 (x1 mode); 2× M.2 (CPU + chipset); SATA listed as 6 in one place and 4 in internal I/O; 4 DIMM, 128 GB DDR4. Works with one compromise: HBA on the CPU slot, NIC on the x4 slot, Arc on an x1 slot (PCIe 4.0 x1, about 2 GB/s, enough for transcoding). The TUF Z790-PLUS D4 is the better fit (two x4 chipset slots) if it can be found.
- **2026-11-08 (Aaron):** DDR4 Z790 boards are hard to find; considering AM4 (Ryzen 5000, DDR4) as an alternative. Trade-off framed: Intel B760/Z790 D4 keeps an iGPU (Quick Sync) for TrueNAS apps and lower idle power; AM4 Ryzen 9 (16 full cores, 142 W package power limit, no E-cores) gives more headroom and more DDR4 boards but no iGPU on non-G parts and higher idle. Current TrueNAS apps (servarr, uptime-kuma) don't use a GPU. Not decided.
- **2026-11-08:** owner reports on 4× 32 GB DDR4 at 3600 are mixed on both platforms (CPU memory-controller lottery). Ryzen 5950X: works for some, including 3600 at 18-22-22-42 (the same timings as our kit) on a Crosshair VIII Hero ([TechPowerUp](https://www.techpowerup.com/forums/threads/trident-z-neo-ram-4-channels-and-ryzen-5950x.284117/), [LTT](https://linustechtips.com/topic/1285160-128gb-3800mhz-on-5950x-and-dark-hero/)), fails even at 3333 for others. Z690 D4: 4× 32 GB kits often need BIOS updates, VCCSA/DRAM voltage or looser timings ([ASUS ROG forum](https://rog-forum.asus.com/t5/hardware-build-advice/help-me-understand-ram-qvl-please/m-p/920138)). AMD's official 2DPC DDR4 speed for Zen 3 not found. Plan either way: XMP first, then voltage, then 3466/3200; long memtest.
- **2026-11-08:** 30-day TrueNAS reporting (15-min averages): CPU mean 5%, p95 11%, max 20% of the i9-9900's 16 threads; ARC mean 16 GiB, max 23 GiB; available memory min 4.1 GiB. RAM is the constraint, not CPU. Recommendation: stay on the Designare + i9-9900 with 128 GB; a DDR4 platform swap doesn't improve the 3600-on-4-sticks odds, would need an Arc for the Plex VM (iGPU passthrough is proven on the UHD 630, not on LGA1700), and is itself end-of-line; revisit on a DDR5 platform if ECC, Arc B-series or more PCIe becomes a real need. Aaron's call pending.
- **2026-11-08 (Aaron):** staying with the Designare + i9-9900 + 128 GB; the LGA1700/AM4 platform swap is dropped. Possible later: move the Ryzen 9 5900X from the gaming PC into Big Boi when that PC is upgraded (DDR4, so the kits carry over). That would need an AM4 board that passes the slot check and an Arc card for the Plex VM (no iGPU), and costs some idle power; roughly 25–30% faster single-thread and 65–75% multi-thread than a 9900K ([cpu-benchmark.org](https://cpu-benchmark.org/index.php/compare/amd-ryzen-9-5900x/intel-core-i9-9900k/)).

## How to verify / roll back

Nothing to roll back. The 30-day figures came from TrueNAS reporting (15-minute averages) on 2026-11-08.
