---
date: 2026-03-07
type: config
system:
- '[[Plex Media Server]]'
notion_id: 31c7ae76-22ba-8109-9cfc-dc460f4d270e
---

# Configured Plex DVR recording library (Recordings → /mnt/dvr)

## What was done

Created a dedicated 'Recordings' library in Plex (type: TV Shows) pointed at `/mnt/dvr` on the Plex VM, which is the NFS RW mount for the `plex_recordings` dataset on TrueNAS.

## Why

Plex DVR writes recordings into whichever library is selected at record time, using a two-stage write: first to a `.grab` subfolder, then moving the finished file. The existing TV Shows library points to `/mnt/media/TV Shows`, which is mounted read-only — Plex was silently failing to write recordings. A dedicated writable library is the correct solution since Plex exposes no separate DVR path setting.

## Configuration

- NFS export: `192.168.1.248:/mnt/Big Boi/BIGBOI/plex_recordings` → `/mnt/dvr` (RW, NFS v3)
- Plex library name: **Recordings** | Type: TV Shows | Path: `/mnt/dvr`
- When recording OTA content, always select 'Recordings' library (not 'TV Shows')

## Gotchas

- Main TV Shows library at `/mnt/media/TV Shows` is intentionally read-only. DVR will silently fail if pointed there.
- Plex DVR 'Add to Library' dropdown only shows libraries of type **TV Shows** or **Movies** — 'Other Videos' type libraries do NOT appear as valid DVR destinations.
- Mount ownership must be `plex:plex` — `chown plex:plex /mnt/dvr` required after NFS mount is set up.
