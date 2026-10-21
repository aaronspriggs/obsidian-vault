---
type: task
status: blocked
priority: medium
system:
- '[[Home Assistant OS (VM)]]'
parent: '[[Migrate thermostats from Nest to ecobee]]'
next_step: '2026-10-06: blocked until both thermostats are on ecobee AND the Nest cameras move off Nest (Migrate cameras from Nest to UniFi Protect, deferred for cost; Nest subscription renewed ~2026-10, runs about 11 months).'
notion_id: 3f17ae76-22ba-818f-a915-c77ac812f523
---

# Decommission Nest integration and its Google Cloud / Device Access project

Removes every open Google API path used by Nest: HA config entry, application credential, OAuth grant, Device Access project, Pub/Sub, Cloud project. Must not touch the separate Drive-backup project or the Google Calendar credential.

## Goal

Leave no Nest-related Google API connection, credential or project behind once nothing in HA uses Nest.

## Status

2026-10-06: Blocked. The Nest integration still serves four cameras (Driveway, Downstairs Camera, Backyard, Front Door doorbell) and their five HomeKit accessory bridges. Removing it before [Migrate cameras from Nest to UniFi Protect](<Migrate cameras from Nest to UniFi Protect.md>) is done would drop those cameras from HA and Apple Home.

## Don't touch

- The **Google Drive backup** Cloud project and OAuth client (created 2026-09-04, see [2026-09-04 Migrated Home Assistant backups to native Google Drive integration](<../changes/2026-09-04 Migrated Home Assistant backups to native Google Drive integration.md>)). HA offsite backups depend on it.
- The **Google Calendar** integration's credential (`google` domain, entry [spriggs.aaron@gmail.com](mailto:spriggs.aaron@gmail.com)). Before deleting any Cloud project, check whether this OAuth client lives in it.

## Plan

All steps are Tier 3 (deleting an integration, credentials and tokens): Aaron confirms each one when it comes up.
1. **Audit (read-only).** In Google Cloud Console, list projects and find the one holding the Nest OAuth client and the Pub/Sub topic/subscription. Note any other OAuth clients in it (Calendar? Drive?). In the [Device Access Console](https://console.nest.google.com/device-access), note the Device Access project ID; it should match the Nest config entry's project. Check whether a billing account is attached.
2. **HA:** confirm with `ha_search` that nothing references Nest entities, then delete the Nest config entry ("Spriggs Home") and the remaining camera HomeKit accessory bridges (should already be gone with the camera migration). Then Settings → Application Credentials → delete the Nest credential.
3. **Google account:** Google Account → Security → Your connections to third-party apps → revoke the Nest/HA grant. This is likely the unexplained second "Home Assistant" grant seen 2026-09-04; confirm the Drive backup grant stays. Also check the Google Home app for a linked partner connection and remove it.
4. **Device Access Console:** delete the Device Access project. The $5 registration fee was one-time; nothing recurring to cancel.
5. **Google Cloud:** in the Nest project, delete the Pub/Sub subscription and topic and the OAuth client, disable the Smart Device Management and Pub/Sub APIs, and then, if nothing else lives there, **shut down the project** (Google keeps it recoverable for 30 days).
6. **Verify:** HA backups still upload to Google Drive (run an automatic backup and check `google_drive` is among its agents); Google Calendar entities still update; no Nest entries remain under third-party connections.
7. **Nest hardware/account:** remove remaining Nest devices from the Google Home app. Deleting the Nest/Google Home structure is optional and separate.
8. **KB:** log a Changes entry, update the HA System page (integrations, Cameras decision), mark this Done.

## Open questions

- Is the Nest OAuth client in its own Cloud project, or shared with Calendar? Step 1 answers it.
