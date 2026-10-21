---
kind: recovery
status: active
system:
- '[[Home Assistant OS (VM)]]'
notion_id: 3087ae76-22ba-81a4-851f-facbc7e2ec23
---

How to recover access to Home Assistant when locked out due to lost MFA/TOTP device. Uses SPICE console + docker exec path. SSH recovery is not available on HAOS.

## Overview

Use this runbook if you are locked out of Home Assistant because your TOTP authenticator device was lost, replaced, or reset. SSH recovery does not work on HAOS — use the SPICE console path instead.

## Preconditions

- Access to TrueNAS SCALE web UI ([https://192.168.1.248:9443/](https://192.168.1.248:9443/))
- Home Assistant VM (ID 3) is running
- You can reach the SPICE console via TrueNAS

## Recovery Procedure

### Step 1: Open SPICE Console

1. Log into TrueNAS at [https://192.168.1.248:9443/](https://192.168.1.248:9443/)
2. Go to Virtualization → find VM "HomeAssistant" (ID 3)
3. Open the SPICE/web console
4. You should see the `ha >` CLI prompt (not a Linux login prompt)

### Step 2: Get Root Shell

At the `ha >` prompt:
```javascript
login
```
This drops you to a root shell inside HAOS without needing a password.

### Step 3: Find the HA Container

```bash
docker ps
```
Look for the container named `homeassistant`.

### Step 4: Enter the Container

```bash
docker exec -it homeassistant bash
```

### Step 5: Back Up and Remove TOTP File

```bash
cd /config/.storage
cp auth auth.backup
rm auth_module.totp
```

### Step 6: Restart HA Core

```bash
ha core restart
```

### Step 7: Verify Access

- Browse to [http://192.168.1.218:8123](http://192.168.1.218:8123/)
- Log in with your username and password (no MFA prompt should appear)

## Post-Recovery Steps

- Re-enroll MFA on your new authenticator device via Profile → Security
- Save MFA backup/recovery codes in your password manager
- Create a full HA backup/snapshot immediately after
- Verify SSH add-on is installed and running for future emergency access

## Important Notes

- Do NOT try to log in at the `homeassistant login:` Linux prompt — use `ha >` + `login` instead
- SSH to HA returns `connection refused` — the SPICE console is the only reliable recovery path
- `/config` does not exist on the TrueNAS host shell — you must enter the Docker container
- `nano` is not available inside the HA container — use `vi` if you need to edit files
- TOTP state is stored in `/config/.storage/auth_module.totp`, not in the main `auth` file

## VM Quick Reference

- VM Name: HomeAssistant | VM ID: 3
- Disk: /dev/zvol/Big+Boi/haos_disk
- NIC: VIRTIO on br0
- Display: SPICE port 5900, web port 5901
