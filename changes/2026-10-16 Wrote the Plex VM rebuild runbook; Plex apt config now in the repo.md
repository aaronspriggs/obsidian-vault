---
date: 2026-10-16
type: doc
system:
- '[[Plex Media Server]]'
project:
- '[[Claude access model - more admin access, secrets management, account hardening]]'
commit: https://github.com/aaronspriggs/spriggs-homelab/commit/18071af
notion_id: 3fb7ae76-22ba-8113-9f2b-d8eaf85248a5
---

# Wrote the Plex VM rebuild runbook; Plex apt config now in the repo

New runbook 'Rebuild the Plex VM from scratch', desk-checked against the live VM and its TrueNAS definition (4x2x2 vCPU, 12 GiB, 32 GiB zvol, MAC 00:a0:98:31:ab:d0, iGPU pci_0000_00_02_0); linked from the DR index step 5, and the Plex account added to its credentials table. The apt timer overrides and unattended-upgrades Plex origin existed only on the VM: copied into repo plex-vm/ and added to deployed.tsv (18071af, README 4a45216); make check ok. Gaps found: the manual EasyAudioEncoder install was never recorded, and plex-db-export fails on a fresh install until Plex's first scheduled DB backup (noted in the runbook).
