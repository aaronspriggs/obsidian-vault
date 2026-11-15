---
type: task
status: backlog
priority: low
system:
- '[[Plex Media Server]]'
notion_id: 31a7ae76-22ba-8109-8a22-f348ac1b5d98
---

# Fix Yu Yu Hakusho season/episode organization in Plex

## Problem

Yu Yu Hakusho appears in Plex but seasons look incorrectly organized. Likely a mismatch between how the files were named/downloaded and how Plex/Sonarr expect the episodes to be structured.

## Possible Causes

1. Files named with absolute episode numbers (e.g. E001-E112) instead of season/episode format (S01E01)
2. Sonarr used a different series database entry than what Plex is matching against
3. Source NZBs had inconsistent naming across seasons
4. Plex matched the show to the wrong metadata agent entry

## Steps to Investigate

1. Check actual filenames on disk: `ls "/mnt/Big Boi/BIGBOI/plex_content/TV Shows/Yu Yu Hakusho/"`
2. Check how Sonarr has the show organized (Series page → season breakdown)
3. Verify Plex matched to the correct series (check the metadata source in Plex)
4. If filenames are wrong, use Sonarr's rename function to fix them
5. If Plex matched wrong metadata, use Fix Incorrect Match in Plex library

## Findings (2026-11-15, read-only check during the quarterly triage)

Cause 1 confirmed. `TV Shows/Yu Yu Hakusho/` is one flat folder of 93 files: episodes 1 to 66 carry absolute numbers (`Yu.Yu.Hakusho.01.…mkv`), the next 27 are named `S03E01` to `S03E27`, and episodes 94 to 112 are missing. The show is not in Sonarr (5 series, none of them this). Simplest fix, using what is already there: add the series to Sonarr as type Anime, pointed at the existing folder, let it match the absolute numbers and rename into season folders, then refresh Plex. The media share is read-only on the Plex VM, so the rename has to come from Sonarr on Big Boi.
