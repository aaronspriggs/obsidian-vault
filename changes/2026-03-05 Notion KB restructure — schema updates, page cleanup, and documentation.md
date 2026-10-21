---
date: 2026-03-05
type: doc
system:
- '[[TrueNAS SCALE (Big Boi)]]'
notion_id: 31b7ae76-22ba-8123-9cdf-fae3bd38673f
---

# Notion KB restructure — schema updates, page cleanup, and documentation

Full Notion KB restructuring session. Schema changes: added Type (Task/Project/Idea) and Date Completed to Projects DB; added Research option to Changes DB Type field; added two-way System relation to Runbooks DB. Project cleanup: typed and stamped all existing projects; marked Done with completion dates — CPU Swap (2026-03-04), WireGuard (2026-02-17), Dockge→Dockhand migration (2026-03-05), Deploy Servarr (2026-02-20), Gluetun watchdog (2026-03-05). Page cleanup: moved three orphaned homepage pages (WireGuard narrative, Local DNS deferred, Servarr narrative) to workspace level; WireGuard content preserved as a proper Changes DB entry. Created Dockhand system page in Systems DB with correct details (v1.1.4, port 3001, TrueNAS catalog install, UID 568/docker group). Renamed Dockge system page to [DEPRECATED — replaced by Dockhand]. Renamed Projects entry from Portainer to Dockhand. Produced two updated project reference files: [homelab-cheatsheet.md](http://homelab-cheatsheet.md/) (updated CPU, Plex version, added Docker services table, Dockhand/Seerr, new gotchas) and [homelab-notion-kb-guide.md](http://homelab-notion-kb-guide.md/) (full KB management guide with DB schemas, session workflow, and page organization rules). Updated Claude project custom instructions to reflect new structure and session workflow.
