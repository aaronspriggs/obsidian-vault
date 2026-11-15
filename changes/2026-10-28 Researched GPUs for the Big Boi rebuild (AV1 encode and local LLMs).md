---
date: 2026-10-28
type: research
system:
- '[[TrueNAS SCALE (Big Boi)]]'
project: '[[Rebuild Big Boi into a new case with an HDD pool for bulk media]]'
---

## What changed

No system changes. GPU research of 2026-10-28 for two jobs: a cheap AV1 encoder and a card for local LLMs. Moved here on 2026-11-15 from the [project](<../projects/Rebuild Big Boi into a new case with an HDD pool for bulk media.md>) note when it was slimmed under the rulebook's size rule; the text is as it stood in the note that day, with its original dates.

## Why

Aaron wanted AV1 encode for the re-encode pipeline and was weighing a card for local LLMs. Outcome: an Intel Arc A380 for AV1 (ordered 2026-11-09); the LLM card went out of scope on 2026-11-07 (decisions in the project note). Written when the PSU was still the SF750 and before the Designare's Resizable BAR support (BIOS F9) was confirmed on 2026-11-09.

## How

### The AV1 card rule as decided

- **2026-10-28 (Aaron):** AV1-encode card: Nvidia only if one with AV1 encode costs about $200, otherwise an Arc A380 (about $169 on Amazon; A310 over $200 at the time). Cheapest Nvidia AV1 encoders on 2026-10-28: RTX 5050 (MSRP $249; $419.99 at Amazon per [videocardprices](https://videocardprices.com/card/nvidia-rtx-5050/)), used RTX 4060 about $250–290 (July 2026, [videocardprices](https://videocardprices.com/card/nvidia-rtx-4060/)), so the A380 it is. Buy after the 4th-gen Apple TV (2026-11-13) confirms Plex AV1 direct play. The 2026-10-25 "Nvidia" line applies to an LLM card.

### Reference: future GPU for local LLMs (2026-10-28)

Limits: Nvidia only, ≤ 250 mm long, PCIEX16 slot at PCIe 3.0 x8 (with the HBA in PCIEX8), SF750 has 2 PCIe cables. VRAM decides model size.

- **RTX 2000 Ada:** 16 GB, 70 W from the slot (no power cable), 168 mm, dual slot, low-profile bracket included, PCIe 4.0 x8, launch price under $650 ([Tom's Hardware](https://www.tomshardware.com/pc-components/gpus/nvidias-new-pro-gpu-costs-less-than-dollar650-rtx-2000-ada-generation-arrives-with-2816-cuda-cores-and-16gb-ecc-vram)). 128-bit memory bus, so slower generation than wider-bus cards.
- **RTX A4000:** 16 GB, 140 W, 241 mm, single slot (NVIDIA datasheet via search); used about $800–850 (Sept 2026, [GPU Dojo](https://gpudojo-v2.pages.dev/articles/used-gpu-prices-ai-boom)).
- **RTX 3060 12 GB:** used about $290 (2026, [ResalePrices](https://resaleprices.com/gpu/nvidia-rtx-3060)); length varies by model, pick one ≤ 250 mm.
- **Low-power alternatives priced 2026-10-28:** RTX A2000 12 GB used about $370–600 on eBay; Tesla T4 16 GB used about $660–1,030 (passive, needs ducted airflow). Neither is cheaper than an RTX 2000 Ada by enough to matter. Aaron (2026-10-28): about $700 is more than he wants to spend now; RTX 3060 12 GB (~$290) or deferring the GPU are the options.
- **Cheap AV1-encode stand-ins (2026-10-28):** Intel Arc A310 (e.g. Sparkle A310 ECO: 4 GB, 50 W from the slot, low profile, single slot, about $140 new on Amazon); AV1 encode on all Arc A-series. Outside Intel's official platform list for 9th gen, but Jellyfin users report Resizable BAR doesn't affect encode/decode (Jellyfin docs cite about 10% transcoding speed) ([Jellyfin forum](https://forum.jellyfin.org/t-arc-a310-performance), [Unraid forum](https://forums.unraid.net/topic/172549-recommended-arc-gpu-for-transcoding-and-av1/)). RTX 4060 (8 GB, AV1 NVENC) about $279–319 new in 2026 ([TweakTown](https://www.tweaktown.com/news/97151/nvidia-rtx-4060-drops-to-279-lowest-price-ever-so-are-you-ready-buy-the-gpu-yet/index.html)). The Loft PC's RX 9070 already has AV1 encode (VA-API on Linux). Plex forum reports on the A310 without Resizable BAR: transcoding unaffected, including HDR tone mapping inside a passthrough VM; but one 8th-gen ASRock board refused to POST with an A310 installed ([Plex forum](https://forums.plex.tv/t/arc-w-o-rebar-for-transcode-performance/878339)). Buy with a return window. Used prices (July 2026, [ResalePrices](https://resaleprices.com/gpu/intel-arc-a310)): A310 about $138, A380 about $172, i.e. no saving over a new A310. Nothing older than the 2022 generation (Arc A-series, RTX 40, RX 7000) encodes AV1 in hardware.
- **Arc Pro B60 (24 GB) — no (2026-10-28):** B-series needs 10th gen+ per Intel, and for LLMs a missing Resizable BAR is cited as the top cause of poor Arc performance ([guide](https://bestllmfor.com/guide/intel-arc-llm-local/)); unlike media encode, that's the workload it would be bought for. Sizes: Sparkle blower 289 mm (too long), Sparkle passive 190 mm single slot (needs server-grade airflow) ([BuildCores](https://www.buildcores.com/products/GPU/yy9csux2j/Sparkle-Intel-Arc-Pro-B60-Blower-24GB-GDDR6)); 1× 8-pin; one AU retailer AU$2,078 incl. GST.
- **Out:** cards over 250 mm (e.g. Tesla P40, most RTX 3090s); Intel Arc as the LLM card (B-series is unvalidated on 9th gen; Resizable BAR is available from Designare BIOS F9, corrected 2026-11-09). Arc A-series stays in as a media-only AV1 encoder. AMD RX 6500 XT (Navi 24): no hardware encoder at all and no AV1 decode ([TechPowerUp](https://techpowerup.com/review/asus-radeon-rx-6500-xt-tuf-gaming/single-page.html)); AMD AV1 encode starts with the RX 7000 series.
- **Pooling GPUs across machines:** llama.cpp's RPC backend runs `rpc-server` on other hosts and splits a model across them over TCP, mixing CUDA and Metal; the project calls it proof-of-concept, fragile and insecure, LAN-only. Benchmarks show faster prompt processing but slower generation when split ([llama.cpp RPC README](https://git.mitjafelicijan.com/r/llmnpc/blob/llama.cpp/tools/rpc/README.md), [benchmarks](https://github.com/kjaiswal/llama-cpp-distributed-benchmarks)). Other GPUs in the house: Workstation RTX 3080 Ti (12 GB, Windows, not always on) and [Loft PC](<../systems/Loft PC.md>) RX 9070 (16 GB; llama.cpp via Vulkan or ROCm). Pooled with a 16 GB card in Big Boi: about 44 GB.

## How to verify / roll back

Nothing to roll back.
