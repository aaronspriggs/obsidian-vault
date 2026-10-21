---
date: 2026-02-15
type: fix
system:
- '[[Home Assistant OS (VM)]]'
notion_id: 3087ae76-22ba-8111-9ea2-c6f67405cbec
---

# Home Assistant MFA recovery performed (TOTP lockout)

Lost access to HA after MFA device change. Recovered via SPICE console + docker exec path. Removed /config/.storage/auth_module.totp and restarted HA core. Post-recovery: re-enroll MFA, save backup codes, create HA snapshot.
