---
status: active
category: hardware
---

Desktop PC in the loft with an AMD Radeon RX 9070 (Aaron, 2026-10-28). Other specs not recorded yet.

## Overview

Second desktop in the house. Recorded because its GPU is a candidate for pooled local-LLM inference with the [Workstation (Desktop)](<Workstation (Desktop).md>) and a future GPU in [TrueNAS SCALE (Big Boi)](<TrueNAS SCALE (Big Boi).md>).

## Hardware

- **GPU:** AMD Radeon RX 9070 (RDNA 4, gfx1201, 16 GB). llama.cpp runs on it through Vulkan or ROCm; a 2026 benchmark found Vulkan faster for token generation and ROCm with flash attention faster for prompt processing on the RX 9070 XT ([write-up](https://vachsark-homepage.pages.dev/blog/vulkan-beats-rocm)).
- **CPU, RAM, OS, network:** not recorded.

## Open work

![[Projects.base#Open for this system]]

## Runbooks

![[Runbooks.base#For this system]]

## Recent changes

![[Changes.base#For this system]]
