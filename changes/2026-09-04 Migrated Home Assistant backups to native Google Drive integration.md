---
date: 2026-09-04
type: config
system:
- '[[Home Assistant OS (VM)]]'
notion_id: 3d17ae76-22ba-8198-b2ee-fe41ca3a85b7
---

# Migrated Home Assistant backups to native Google Drive integration, retired community add-on

Replaced the community "Home Assistant Google Drive Backup" add-on (sabeechen/hassio-google-drive-backup) with HA Core's native `google_drive` backup integration as the offsite backup destination.

Context: the add-on ran its own independent daily schedule outside HA's core Backup feature (not one of the core feature's agent_ids — see "Fixed automatic backup failures", 2026-09-03). Native automatic backups had no cloud location configured after Nabu Casa cloud upload was removed as a target that same day, so only the add-on was actually getting anything offsite, while both systems ran full-instance backups daily in parallel.

Setup: created a dedicated Google Cloud Console project, enabled the Drive API, configured the OAuth consent screen (External audience) and published it to Production to avoid the 7-day refresh-token expiry Testing-status apps get. Two non-obvious Console blockers hit along the way: (1) uploading an app logo on the Branding page silently requires formal Google verification before you can publish — removed it; (2) the Homepage and Privacy Policy URL fields aren't marked required but Google blocks publishing to Production without them, and both must live on an Authorized Domain — set both to [home-assistant.io](http://home-assistant.io/) URLs since we don't have our own public site and that domain was already required for the redirect URI. Created a Web application OAuth client with redirect URI [https://my.home-assistant.io/redirect/oauth](https://my.home-assistant.io/redirect/oauth).

In HA: added the Google Drive integration using that Client ID/Secret, authorized via the consent flow (expected "unverified app" warning, clicked through — normal for a personal single-user client). Configured automatic backups via Settings → System → Backups → Set up backups → Custom: daily, retention raised from the 3-backup default, data scope = Home Assistant settings + History, all Apps, Media and Share folder excluded (camera recordings shouldn't route through HA backups, especially mid-migration off Nest). Added Google Drive as a backup location alongside existing local storage.

Verified end-to-end by forcing a real automatic backup via the backup.create_automatic action (not the raw snapshot-create API, which defaults local-only regardless of configured locations) and confirming the resulting backup's agent_ids included both hassio.local and google_drive.spriggs_aaron_gmail_com.

Cleanup: uninstalled the cebe7a76_hassio_google_drive_backup add-on. Its separate Google OAuth grant ("[Hass.io](http://hass.io/) Google Drive Backup" under Google Account → Connected apps) was identified and revoked manually. A second, unexplained "Home Assistant"-named entry also showed up under Connected apps alongside the new integration's own grant — left alone to avoid breaking the new setup; follow-up to identify it.

Open follow-ups (see System page Known Gaps): confirm the backup encryption key / emergency kit was saved somewhere durable off the HA instance (downloaded during setup but not independently verified saved); identify the second "Home Assistant" Google OAuth grant.

Superseded prior documentation: the Changes entry "Confirmed Home Assistant automated backups via Google Drive" (2026-02-18) and the Project "Create Home Assistant backup/snapshot" (Done, 2026-02-15) both describe the old add-on, not a native integration — the native google_drive integration didn't exist in HA at that time. Left as historical record with a clarifying note added to the Project page.
