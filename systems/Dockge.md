---
status: deprecated
category: docker
ip: 192.168.1.248 (host)
superseded_by: '[[Dockhand]]'
notion_id: 30d7ae76-22ba-8106-b4f0-fd24620ae556
---

Docker Compose stack manager WebUI. Manages servarr stack.

## Overview

Dockge is a lightweight Docker Compose stack manager providing a visual WebUI for managing compose stacks. Installed via `docker run` on TrueNAS Big Boi. Manages the servarr media automation stack.
**Access:** [http://192.168.1.248:5001](http://192.168.1.248:5001/)
**Auth:** admin / (password)
**Image:** louislam/dockge:1

---

## Installation

Deployed as a standalone container (not part of the servarr compose stack):
```javascript
sudo docker run -d \
  --name dockge \
  --restart unless-stopped \
  -p 5001:5001 \
  -v /var/run/docker.sock:/var/run/docker.sock \
  -v "/mnt/Big Boi/BIGBOI/servarr/dockge:/app/data" \
  -v "/mnt/Big Boi/BIGBOI/servarr:/opt/stacks" \
  -e DOCKGE_STACKS_DIR=/opt/stacks \
  louislam/dockge:1
```

---

## Key Details

- Mounts Docker socket for container management
- Stacks directory: `/mnt/Big Boi/BIGBOI/servarr/` (mapped to `/opt/stacks` inside container)
- Data directory: `/mnt/Big Boi/BIGBOI/servarr/dockge/`
- The servarr stack must be started/stopped from Dockge UI for full management (not `docker compose` CLI)
- compose.yaml must use absolute paths, not relative `./` paths, because Dockge resolves from its own stacks directory

---

## Notes

- Dockge is NOT visible in TrueNAS Apps UI — it's a standalone Docker container
- To adopt an existing CLI-deployed stack, stop it via `docker compose down`, then start it from Dockge UI
- Dockge by the same developer as Uptime Kuma

## Runbooks

![[Runbooks.base#For this system]]

## Recent changes

![[Changes.base#For this system]]
