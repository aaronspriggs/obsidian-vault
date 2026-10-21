---
date: 2026-09-26
type: upgrade
system:
- '[[Dockhand]]'
- '[[TrueNAS SCALE (Big Boi)]]'
notion_id: 3e77ae76-22ba-81e6-8888-e360a4828c21
---

# Upgraded Dockhand v1.0.20 → v1.0.49 (TrueNAS app 1.1.4 → 1.1.34); verified no exposure to the March 2026 Trivy compromise

**Versioning note:** TrueNAS shows apps as `<app version>_<catalog version>`. `v1.0.20_1.1.4` means Dockhand 1.0.20 with catalog package 1.1.4. The real jump was Dockhand 1.0.20 → 1.0.49.
**Pre-checks (Claude, via release notes and the read-only TrueNAS API):**
- No breaking changes, migrations or manual steps between 1.0.20 and 1.0.49.
- Security fixes included:
    - **1.0.22:** the Trivy supply-chain compromise of 2026-03-19. `aquasec/trivy:0.69.4` was malicious; 1.0.22 pins the scanner to 0.69.3.
    - **1.0.34:** GHSA-f6q3-chhc-4hxm.
    - **1.0.45:** API hardening.
- **Exposure check:** there's no `aquasec/trivy` image on Big Boi (`app.image.query`), and the untagged images all predate 2026-03-19. Dockhand's scanner appears never to have run here, so exposure is very unlikely. Dockhand also ran Trivy without credentials, for under a minute, versus the payload's 5-minute delay.
**Rollback point:** the `ix-apps` dataset isn't selectable in the TrueNAS UI, so Aaron took a manual snapshot over SSH: `Big Boi/ix-apps/app_mounts@pre-dockhand-update-2026-09-26` (recursive).
**Upgrade:** done by Aaron in TrueNAS Apps → dockhand → Update.
**Verified after:**
- `app.query` shows RUNNING, `v1.0.49_1.1.34`, no upgrade available; Dockhand UI returns HTTP 200.
- All 15 Uptime Kuma monitors are up, including NZBGet and Prowlarr via Gluetun; homelab issue count 0.
- The TrueNAS AppUpdate alert cleared.
- The old `fnsys/dockhand:v1.0.20` image is kept as a rollback option; remove it later.
**Also found (not acted on):** a stale `lscr.io/linuxserver/overseerr:latest` image from before the Seerr migration, and several untagged images from January–February 2026. Cleanup candidates.
