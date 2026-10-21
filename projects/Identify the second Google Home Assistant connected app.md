---
type: task
status: done
priority: low
system:
- '[[Home Assistant OS (VM)]]'
completed: 2026-10-17
notion_id: 3e97ae76-22ba-81bb-bbbf-f05bf59ee704
---

# Identify the second Google "Home Assistant" connected app

Closed 2026-10-17 as a duplicate: step 3 of 'Decommission Nest integration and its Google Cloud / Device Access project' already covers reviewing and revoking this grant. HA holds three Google OAuth grants (verified live 2026-10-17): google_drive (backups), google (Calendar, [spriggs.aaron@gmail.com](mailto:spriggs.aaron@gmail.com)) and nest (Spriggs Home), so the second 'Home Assistant' entry may be Calendar or Nest, not a retired add-on. Don't revoke it blind.

## Goal

At [myaccount.google.com/permissions](https://myaccount.google.com/permissions) there are two "Home Assistant" entries. One is the live `google_drive` backup integration. Identify the other (likely the retired backup add-on) and revoke it if unused.
