---
date: 2026-09-04
type: research
system:
- '[[Home Assistant OS (VM)]]'
notion_id: 3d17ae76-22ba-81b5-b758-d261bd38c363
---

# Reconciled stale MFA/Mosquitto anonymous-access items on Known Gaps list

Investigated a discrepancy: the System page's Known Gaps/TODO list said MFA was disabled and Mosquitto anonymous access was unverified, but the Projects DB showed both corresponding tasks ("Re-enable MFA on Home Assistant", "Verify Mosquitto anonymous access is disabled") marked Done since 2026-03-05 — meaning the System page just never got updated after those closed.
MFA: confirmed directly by Aaron — enabled on the `aaronspriggs` account via an authenticator app (Proton). Not independently verifiable via the HA API; ha-mcp's `config/auth/list` websocket command returns account metadata (username, groups, credentials) but not MFA enrollment, which HA only exposes as a self-service endpoint for the currently logged-in user.
Mosquitto: checked the installed `core_mosquitto` add-on (v7.1.0) config schema directly via `ha_get_app` — there is no `anonymous` option in this version at all. Auth is via the (empty) `logins` list or HA user credentials through the Supervisor auth API (`auth_api: true`). No anonymous-access path exists to disable, so the original TODO doesn't apply to the current add-on.
Removed both stale bullets from the System page's Known Gaps section and added a Security section documenting the confirmed state.
