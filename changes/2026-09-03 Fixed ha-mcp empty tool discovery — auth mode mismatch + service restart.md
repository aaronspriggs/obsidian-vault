---
date: 2026-09-03
type: fix
system:
- '[[Home Assistant OS (VM)]]'
- '[[ClaudeCode (VM)]]'
notion_id: 3d07ae76-22ba-81ff-affb-e30b1f74eb1c
---

# Fixed ha-mcp empty tool discovery — auth mode mismatch + service restart

ha-mcp's transport connected fine (claude mcp list / get both showed "Connected") but no HA tools were appearing in the Claude Code session at all — not even loaded, not even flagged as needing auth.

Root cause: the ha-mcp integration's Configure screen had Authentication mode set to "Sign in with Home Assistant (OAuth)", while Claude Code's local MCP config for `homeassistant` pointed at the direct-access secret-path URL ([http://192.168.1.218:9584/private_](http://192.168.1.218:9584/private_)...) — the intended workaround for the open anthropics/claude-code#89671 OAuth bug. The server was enforcing an auth method the client wasn't using, so tool-list requests were silently going nowhere.

Fix: switched the integration's Authentication mode to "Secret webhook URL (default)" to match the direct-access URL already configured on the Claude Code side. Then ran `sudo systemctl restart claude-remote-control.service` on the ClaudeCode VM to force a fresh MCP handshake — the long-lived Remote Control service (Restart=always) doesn't re-run tool discovery against an already-connected server just because its auth config changed underneath it.

Verified fixed: after reconnecting, `ha_get_overview` returned real live data (830 entities, 306 services, 25 areas, HA Core 2026.9.0, all 7 existing automations reporting `on`). This is the first confirmed live tool call from a Claude Code session, closing out the one open item on the original ha-mcp install (see "Installed ha-mcp..." Change entry from earlier today).

Also surfaced along the way (unrelated to ha-mcp, flagged for Aaron): Spotify integration needs reauth (config_entry_reauth_spotify, error severity), and automatic HA backup upload has been failing since 2026-08-29 (warning).

Follow-up: revisit OAuth once anthropics/claude-code#89671 ships a fix — tracked as its own Task in Projects DB ("Switch ha-mcp auth to Home Assistant sign-in (OAuth)", Blocked).
