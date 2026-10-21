---
kind: setup
status: active
system:
- '[[Home Assistant OS (VM)]]'
- '[[ClaudeCode (VM)]]'
last_tested: 2026-09-03
notion_id: 3d07ae76-22ba-81f1-9879-d21fa7584b3b
---

How to install and connect homeassistant-ai/ha-mcp via HACS for AI-driven automation/dashboard authoring, including the correct repo path, auth mode tradeoffs, and a known Claude Code OAuth bug workaround.

## Why ha-mcp, not the built-in integration

Home Assistant's own **"Model Context Protocol Server"** integration is Assist-API-only — device control and state queries against entities exposed to Assist, nothing more. It cannot create or edit automations, scripts, scenes, or dashboards. `homeassistant-ai/ha-mcp` is a separate, community-built server that adds full read/write configuration access on top of device control. Re-verify this against [https://www.home-assistant.io/integrations/mcp_server/](https://www.home-assistant.io/integrations/mcp_server/) if revisiting later, since HA's built-in integration could gain write support in a future release.

## Which repo to use — this matters

There are several similarly-named, similarly-described community projects (`ganhammar/hass-mcp-server`, `achetronic/hass-mcp`, etc.). The one to use is **`homeassistant-ai/ha-mcp`** — confirmed as the de facto community standard by a wide margin (4,600+ GitHub stars vs. under 100 for the alternatives as of 2026-09, and it's the one discussed on the [HA Community Forum](https://community.home-assistant.io/t/brand-new-claude-ai-chatgpt-integration-ha-mcp/937847)).
For the actual HACS install, use the **`homeassistant-ai/ha-mcp-integration`** repo path specifically — that's a dedicated mirror repo created so HACS can install it cleanly. Adding `homeassistant-ai/ha-mcp` directly as the custom repository does not work as a HACS integration install.
If star counts or naming are ever unclear again, check via the GitHub API before installing:
```javascript
curl -s "https://api.github.com/repos/<owner>/<repo>" | python3 -c "import json,sys; d=json.load(sys.stdin); print(d['stargazers_count'], d['pushed_at'])"
```

## Install steps

1. HACS → Integrations → three-dot menu → **Custom repositories** → add `homeassistant-ai/ha-mcp-integration`, category **Integration** → Download.
2. Restart Home Assistant fully.
3. Settings → Devices & Services → Add Integration → search **HA-MCP Custom Component** → add the **HA-MCP Server** entry (this is the one that runs the full in-process server and starts it immediately on creation).
4. Skip the second entry type, **HA-MCP File & YAML Tools**, unless raw YAML file editing is specifically needed later — it's beta/opt-in and not required for automation, script, scene, or dashboard authoring, which go through dedicated tools instead.

## Dedicated Home Assistant account

Created a `claude` user (Settings → People → Users) for the integration to authenticate as: Administrator (needed for full write scope), **Local only** enabled (never needs remote/Nabu Casa login, only ever signs in to approve this integration's OAuth).

## Auth mode — and a known blocker as of 2026-09

The Configure screen's **Authentication mode** field offers three options:
- **Secret webhook URL (default)** — the URL itself is the only credential. Avoid; this is the bare-secret model the original plan wanted to avoid.
- **Home Assistant sign-in (OAuth)** — ties access to a real HA account (the `claude` user). This is the correct choice in principle.
- **Legacy OAuth** — issues a static Client ID/Secret for clients that can't do HA's native sign-in flow. Not needed for Claude Code.
**As of 2026-09, "Home Assistant sign-in (OAuth)" does not work from Claude Code**, due to an open upstream bug: [anthropics/claude-code#89671](https://github.com/anthropics/claude-code/issues/89671). Claude Code's own OAuth status-check code corrupts a freshly-issued valid token immediately after a successful browser authorization — the browser-side flow completes fine, but `claude mcp login` reports failure (`Couldn't complete authentication... no from the MCP SDK`) every time, regardless of server configuration. This affects any OAuth-protected HTTP MCP server in Claude Code, not anything ha-mcp-specific.
**Interim workaround:** connect via the integration's **direct-access URL** instead (shown on the Configure screen, format `http://<ha-ip>:9584/private_<random>`). This bypasses OAuth entirely — the secret path itself is the credential — so it isn't blocked by the Claude Code bug. Leave **Network access** at "Local network (default)" (not "Loopback only") so a separate machine like the ClaudeCode VM can reach it.
**Revisit once anthropics/claude-code#89671 is fixed**: switch Authentication mode back to "Home Assistant sign-in (OAuth)" and reconnect via the webhook URL (`http://<ha-ip>:8123/api/webhook/<webhook-id>`) for proper account-tied auth instead of a bare secret path.

## Connecting from Claude Code

```javascript
claude mcp add --transport http homeassistant <connect-url>
claude mcp list   # confirm "Connected"
```
Note: `claude mcp add` without `-s user`/`-s project` defaults to **local scope**, tied to the directory it's run from. On the ClaudeCode VM, run this from `/home/aspriggs/homelab-agent` — running it from `~` (home directory) will not find the server later (`claude mcp login`/`get`/etc. all need the same cwd).
Sanity-check the connection independent of Claude Code with a raw handshake:
```javascript
curl -s -X POST "<connect-url>" \
  -H "Content-Type: application/json" -H "Accept: application/json, text/event-stream" \
  -d '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2025-06-18","capabilities":{},"clientInfo":{"name":"test","version":"1.0"}}}'
```
A correct response includes `"serverInfo":{"name":"ha-mcp",...}` and a `capabilities` block.
**Session note:** MCP tools are discovered when a Claude Code session starts. If a server is added mid-session (e.g., via Bash during an existing conversation), that same session won't see its tools — start a fresh session to actually use them.

## Gotcha: copying secret URLs from the HA UI

HA's Configure-screen font renders lowercase `l` and uppercase `I` almost identically in these random secret paths/tokens. Transcribing by reading a screenshot is unreliable — this caused two separate failed-connection dead-ends during setup (once in an OAuth callback URL, once in the direct-access path). Always use **right-click → Copy Link Address** on these URLs rather than retyping them.

## Gotcha: auth mode mismatch causes silent empty tool discovery (fixed 2026-09-03)nIf the ha-mcp integration's **Authentication mode** doesn't match the URL type Claude Code is actually configured with, the transport still connects (`claude mcp list`/`get` both show "Connected") but **no tools show up at all** — not loaded, not even flagged as needing auth. This happened when the integration was left on "Home Assistant sign-in (OAuth)" while Claude Code pointed at the direct-access secret-path URL (the intended OAuth-bug workaround, see above). The server was enforcing an auth method the client wasn't using, so tool-list requests silently went nowhere.n**Fix:** make sure Authentication mode on the Configure screen is set to **"Secret webhook URL (default)"** whenever connecting via the direct-access URL (i.e., whenever OAuth is blocked by anthropics/claude-code#89671).n**Also required:** after fixing the auth mode (or any other server-side config change), restart the Claude Code Remote Control service to force fresh MCP tool discovery:n`javascript\nsudo systemctl restart claude-remote-control.service\n`nThe long-lived `claude-remote-control.service` (Restart=always) does **not** re-discover an already-connected server's tools just because something changed on the server side — it needs a fresh process start to re-run the discovery handshake. This will drop any active Remote Control session; reconnect from [claude.ai/code](http://claude.ai/code) or the mobile app afterward.nVerified working after this fix: `ha_get_overview` returned live system data (830 entities, 306 services, 25 areas, HA 2026.9.0) — first confirmed live tool call from an actual Claude Code session, not just a raw handshake.

## Tool Security Policies (approval gates)

Configured in the HA sidebar → **HA-MCP** settings → Tool Security Policies tab. A gated call returns `USER_APPROVAL_REQUIRED` and waits in Pending Approvals until Aaron approves it in the panel. All gates use "always" with remember-approval 0 (single-shot).
**Gated as of 2026-10-15** (Aaron relaxed the original 12 to these 5):
- `ha_remove_area_or_floor`
- `ha_remove_zone`
- `ha_config_remove_scene`
- `ha_config_delete_dashboard`
- `ha_manage_radio`
**Ungated since 2026-10-15:** `ha_restart`, `ha_remove_device`, `ha_remove_entity`, `ha_config_remove_automation`, `ha_config_remove_script`, `ha_remove_helpers_integrations`, `ha_manage_updates`.
**The panel gate isn't the authority rule.** KB Standards → Change authority still applies to every call, gated or not. Deleting HA entities, devices or integrations that Claude didn't create in the same session stays **Tier 3**, so Claude asks for an explicit yes in chat even where the panel no longer gates it.
