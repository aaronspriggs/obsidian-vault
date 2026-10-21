---
kind: setup
status: active
system:
- '[[Home Assistant OS (VM)]]'
last_tested: 2026-09-04
notion_id: 3d17ae76-22ba-81cb-86b4-d4487a147a07
---

Step-by-step for replacing the community Google Drive Backup add-on with HA Core's native google_drive backup integration — Google Cloud Console OAuth app setup (including two non-obvious Branding-page blockers), HA-side integration + automatic backup config, and end-to-end verification.

## Why replace the add-on

The community "Home Assistant Google Drive Backup" add-on (sabeechen/hassio-google-drive-backup) predates HA Core's native backup system. It runs its own independent daily schedule outside the core Backup feature (not one of its agent_ids — see "Fixed automatic backup failures", Changes, 2026-09-03), so it and the native automatic-backup schedule ran in parallel, duplicating full-instance backups daily. Only the add-on was actually getting anything offsite — native automatic backups had no cloud location configured (agent_ids: hassio.local only) once Nabu Casa cloud upload was dropped as a target. Migrating to the native `google_drive` backup integration consolidates onto one schedule with a real offsite destination and no per-add-on donation-funded proxy dependency.

## Part 1 — Google Cloud Console (OAuth app)

1. [https://console.cloud.google.com/](https://console.cloud.google.com/) → create a new project (e.g. `homeassistant-backup`).
2. APIs & Services → Library → enable **Google Drive API**.
3. Google Auth Platform → **Branding**:
    - App name: `Home Assistant`; User support email + Developer contact email: your account.
    - **Do not upload a logo.** Doing so silently requires submitting for Google's formal app verification before you can leave Testing status. Remove it if one gets auto-populated.
    - **Application home page** and **Application privacy policy link** aren't marked required (no asterisk), but Google blocks publishing to Production without them, and both URLs must live on an Authorized Domain. With no public site of your own, use `https://www.home-assistant.io/` and `https://www.home-assistant.io/privacy/` — [home-assistant.io](http://home-assistant.io/) is already the Authorized Domain you need for the redirect URI below.
    - Authorized domain: `home-assistant.io` (covers the `my.home-assistant.io` redirect subdomain — Google authorizes at the root registrable domain, not the exact subdomain).
4. Google Auth Platform → **Audience**: set to External, then **Publish app** (Production status). Skipping this means refresh tokens expire every 7 days and HA nags for re-auth weekly. A "further verification may be required based on scope" notice may appear when publishing — click through; formal verification is not actually required for a personal single-user client.
5. Google Auth Platform → **Clients** → Create Credentials → OAuth client ID → **Web application** → Authorized redirect URI: `https://my.home-assistant.io/redirect/oauth`. Save the resulting Client ID and Client Secret.

## Part 2 — Home Assistant

1. Settings → Devices & Services → Add Integration → **Google Drive** → paste the Client ID/Secret → complete the Google consent flow. Expect a **"Google hasn't verified this app"** interstitial — click Advanced → Go to Home Assistant (unsafe). This is expected for an unverified personal client, not a misconfiguration.
2. Settings → System → Backups → **Set up backups** → **Custom** (not "Recommended" — that preset is a fixed daily/3-day-local preset with no location picker):
    - Schedule/time: any cadence; "System optimal" time is fine.
    - Retention: default is 3 backups — raise it if you want more history. Native retention is a flat count, not the add-on's generational (daily/weekly/monthly/yearly) scheme — there's no equivalent long-tail retention natively.
    - Data: Home Assistant settings (always included) + History; leave Media and Share folder off unless camera recordings should specifically route through HA backups.
3. Back on the Backups page → **Automatic backup → Locations** (shows "Local backup only" until a cloud location is added) → add **Google Drive**.

## Part 3 — Verify it actually reached Drive

Adding the integration and toggling the location doesn't prove uploads work — confirm before trusting it:
- Don't test with the raw backup-create API/action — it defaults to local storage only, regardless of the configured automatic-backup locations.
- Instead trigger the real path: call the `backup.create_automatic` action, then check the resulting backup's `agent_ids` — should include both `hassio.local` and `google_drive.<account_id>` (via the Backups UI, or `ha_manage_backup(scope="snapshot", action="list")` over MCP).

## Part 4 — Retire the add-on

1. Uninstall the add-on (Settings → Add-ons → Home Assistant Google Drive Backup → Uninstall, or `ha_manage_app(action="uninstall", slug="cebe7a76_hassio_google_drive_backup")` over MCP).
2. The add-on's Google OAuth grant is separate from the new integration's — revoke it at [https://myaccount.google.com/permissions](https://myaccount.google.com/permissions), listed as **"**[**Hass.io**](http://hass.io/)** Google Drive Backup"**. Don't touch other "Home Assistant"-named entries there without checking last-accessed date/scopes first — one of them is the live grant for the integration just set up, and revoking the wrong one breaks it.

## Gotchas encountered (2026-09-04)

- `ha_manage_backup` snapshot deletion is disabled by default on ha-mcp (`enable_snapshot_delete=false`). A human has to flip that server-side (env var / web settings UI / Supervisor options) — it can't be enabled from a tool call, so delete stray backups via the HA UI directly instead.
- Manually save the **encryption key / emergency kit** (Backups page → Encryption key → Download) somewhere durable outside the HA instance. Without it, none of these backups — old or new — are restorable.
