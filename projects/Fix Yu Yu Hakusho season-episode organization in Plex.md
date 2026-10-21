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
