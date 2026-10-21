---
type: project
status: active
priority: medium
system:
- '[[TrueNAS SCALE (Big Boi)]]'
- '[[UniFi (UDM Pro)]]'
- '[[Home Assistant OS (VM)]]'
next_step: 'Verify HKSV: Aaron sets Recording Options in Home and walks past the G6; Claude checks Scrypted''s log for a recording session, then closes the project'
notion_id: 3997ae76-22ba-81d8-bf4b-c2c82629b5f2
---

Scrypted as an HA app on the HAOS VM (installed 2026-10-17) bridging UniFi Protect cameras (1 G6 Instant now, about 6 plus a doorbell within a year) into Apple Home with HKSV. Chosen over Big Boi Docker/macvlan/own VM: everything else bridges to HomeKit via HA, least maintenance, TrueNAS mDNS stays on. Resize the HA VM as cameras grow.

## Overview

Bridge UniFi Protect cameras into Apple Home via Scrypted, with HomeKit Secure Video. Today that's 1 camera (G6 Instant); roughly 6 cameras plus a doorbell within a year as the Nest cameras are replaced (see Migrate cameras from Nest to UniFi Protect). The only goal is HomeKit: UniFi Protect has no native HomeKit support (checked 2026-10-17). No Scrypted NVR or local object detection; HKSV records to iCloud and the Apple home hub does person/car/package detection.

## Placement decision (2026-10-17, Aaron): Scrypted as an HA app

Runs as the official Scrypted app (add-on) on the Home Assistant OS VM, not on Big Boi.
Why:
- HA is already where every other device is bridged into HomeKit, and the app keeps the maintenance overhead lowest: no extra OS, HA's backups and update flow cover it, and ha-mcp can monitor and manage it.
- TrueNAS mDNS stays on. Aaron wants Big Boi in Finder and a future Time Machine share, and TrueNAS 25.04 won't allow a Time Machine share with mDNS off. A host-network container on Big Boi can't share UDP 5353 with TrueNAS's avahi (upstream compose notes; TrueNAS forum reports). The app uses the HA VM's own IP instead.
Alternatives considered: Docker on Big Boi with TrueNAS mDNS off (blocks Time Machine and Finder); Docker on Big Boi with macvlan on 192.168.1.2 (works, but fragile networking and Kuma can't reach it); a dedicated Scrypted VM (cleanest isolation, what most homelabbers converge on, but another OS to run); HA's own HomeKit Bridge (no HKSV). The September choice of Big Boi Docker was superseded; the draft stack (commit 2e60b6b) was removed in 7510fa6.
Trade-offs accepted: Scrypted shares the HA VM's CPU/RAM and reboots. HAOS updates that reboot the VM drop the cameras from Apple Home for a few minutes, and heavy Scrypted load would slow HA and the wall panel. **Resize the HA VM as cameras are added** (plan: 4 vCPU / 8 GiB before going past ~3 HKSV cameras; TrueNAS UI plus one HA restart). If coupling becomes a problem, move to a dedicated VM; that means re-pairing every camera in Apple Home.

## Other decisions (2026-10-17, Aaron)

- **HKSV on**, not live view only. Needs an Apple home hub (HomePod or Apple TV) and an iCloud+ plan. Scrypted pairs each camera as its own accessory, not through a bridge.
- **UniFi Protect is added to HA now** too, reversing the 2026-09-26 "leave it until the Nest migration" note. HA gets the camera entity and motion/detection events; Scrypted still owns HomeKit.

## Install (2026-10-17)

- App `09e60fb6_scrypted` from repository `https://github.com/koush/scrypted`, version v0.147.0-noble-full. Boot auto, watchdog on, auto-update off (updates should go through the approval flow). Host network on the HA VM: UI `https://192.168.1.218:10443` (also via HA ingress, port 11080). Idle RAM about 100 MB at install.
- Plugins: HomeKit, UniFi Protect, plus their dependencies Rebroadcast (prebuffer), WebRTC and Snapshot; the app ships the Home Assistant plugin. Installed by Claude through the app's ingress (`POST /web/component/script/install/<pkg>` via ha-mcp's app proxy; ingress requests count as Scrypted admin).
- mDNS verified 2026-10-17 by querying `_hap._tcp` from the ClaudeCode VM: `Scrypted FE0A` announces from 192.168.1.218 next to all five of HA's own HomeKit accessories, which are still loaded. **Don't pair the "Scrypted" bridge accessory**; pair the per-camera codes only.
- Admin login: the app auto-creates admin `homeassistant` with a random password and is reached through HA ingress (HA → Settings → Apps → Scrypted → Open Web UI; no sidebar panel). Claude has its own Scrypted admin user `Claude` (case-sensitive; 1Password `Scrypted - Claude Login`) and uses it through the repo wrapper `scrypted/scrypted-api` on the ClaudeCode VM (devices, settings, put, mixin, discover, adopt, streams).
- Monitoring: Uptime Kuma monitor `Scrypted` (repo `stacks/uptime-kuma/monitors/scrypted.toml`, commit fc7bd6f) → `sensor.scrypted_status` → Alert2 `homelab_service_down` via label `homelab_watch`.
- Backups: HA's daily native backups (local plus Google Drive) include apps with their data; the app's manifest excludes only plugin code and NVR storage.
- Hardware: the HA VM has no GPU, so there's no hardware decode. That's fine as long as streams are H.264 and Scrypted remuxes rather than transcodes.

## Camera prep (UniFi Protect)

- **Protect 7.3+ (Oct 2026): turn off "Super Encoding"**, a per-camera checkbox in the camera's **Recording Quality** panel, next to Resolution, FPS and Video Compression (seen on the G6 Instant 2026-10-20; the articles below describe it as a Storage Budgeting group setting, which doesn't match this install). It replaced the older Enhanced Encoding (H.265) and Advanced Encoding toggles.
- G6 Instant as set 2026-10-20: 4K, 30 FPS, compression Custom 2–16 Mbps, Super Encoding off. Scrypted's reference for a 4K main stream is about 8 Mbps VBR at 10–30 fps ([camera prep docs](https://docs.scrypted.app/camera-preparation.html)); lowering the cap is optional and only affects storage and quality. Use Protect's lower-resolution streams in Scrypted for remote viewing and HKSV. On older Protect versions, turn off "Enhanced Encoding" instead. Either way the goal is an H.264 main stream so Scrypted remuxes and doesn't transcode. Sources: [Willie Howe, Protect 7.3](https://williehowe.com/2026/10/03/unifi-protect-7-3-what-s-new/), [Emerald Security](https://emeraldsecurity.net/2026/10/07/unifi-protect-7-3-super-encoding-do-the-retention-math-before-you-flip-the-switch/).
- After connecting the camera, confirm the actual stream codec in Scrypted before enabling HKSV.
- Cost: recordings on the UDM take more storage than they would with Super Encoding on.

## Accounts

- Scrypted's Protect plugin needs a **local** UniFi OS user (2FA and SSO won't work) with Protect Full Management while it adds cameras, which enables RTSP; per the plugin README it may then be downgraded to read-only. Other apps None, local access only.
- HA's UniFi Protect integration uses **API key only** mode (a Protect API key from Protect → Integrations, no user). That covers the camera, binary sensors and events; it gives up button/media-player/text entities and media-source browsing, and can be reconfigured to full mode later. Confirmed 2026-10-20: HA's setup dialog claims API-key-only gives only "the alarm manager, cameras and lights", but the G6 Instant got 38 entities incl. motion/person/vehicle sensors and `event.g6_instant_*` detection events.
- Both secrets are in 1Password vault `Homelab - Claude` (added 2026-10-20): `Unifi - Scrypted` (item `4qzjqm25x7gxmjpzlm2u4yy3v4`, username `scrypted`) and `Unifi Protect - HA API Key` (item `vykc4myvrh3xvwpz3vtp27pvca`, key in the password field). Claude reads them at run time with `homelab-secret` and enters them through ha-mcp (Scrypted plugin settings via the app's ingress proxy, HA integration config flow), never writing them to a file.
- **Decided 2026-10-17 (Aaron): a separate UniFi user for Scrypted**, not reusing `claude-readonly`. Sharing it would have meant one password in two systems (and in HA's Google Drive backups through Scrypted's DB), UniFi logs crediting Scrypted's actions to Claude, possible login rate-limit collisions (the UDM returns 429 after a few quick logins), and a misleading account name.

## Next Steps

- [x] Placement decided: HA app (2026-10-17)
- [x] Install the Scrypted app with the HomeKit and UniFi Protect plugins; verify mDNS; Kuma monitor (2026-10-17)
- [x] Aaron: create the local UniFi user for Scrypted and the Protect API key for HA, both in `Homelab - Claude`; turn off Super Encoding (Protect 7.3+; Enhanced Encoding on older versions) for the G6 Instant; confirm the Home hub and iCloud+ (2026-10-20: Apple TV is the hub, iCloud+ active)
- Permissions (2026-10-20): Claude Code's auto-mode classifier refuses both write paths, and approval given in chat doesn't clear it. (1) Scrypted settings need its RPC client; the only admin credential is the ingress session token, and using it from the VM shell was refused as credential materialization. (2) `ha_set_integration` was refused as modifying a shared resource. Workarounds: switch the session to Manual mode and approve the prompt, or add an allow rule in `settings.local.json` (on the ClaudeCode VM as `aspriggs`, not HA's SSH app). Longer-term option for Scrypted: a dedicated Scrypted user for Claude in `Homelab - Claude` plus a `scrypted-api` wrapper.
- [x] `update.scrypted_update` labelled `ha_update_approval`; `sensor.scrypted_status` labelled `homelab_watch` (2026-10-17)
- [x] Configure the Protect plugin, adopt the camera, enable HomeKit (2026-10-20). Current Scrypted doesn't auto-add Protect cameras: run `scrypted-api discover "Unifi Protect Plugin"`, then `adopt`, then `mixin <camera> add HomeKit` and `put <camera> homekit:standalone true`. G6 Instant streams are all H.264 (4K/720p/360p, 30 fps), so remux only. HKSV 3 (experimental) left off. Pairing code: `scrypted-api settings "G6 Instant"`, key `homekit:pincode`.
- [x] Aaron: pair the camera in the Home app (2026-10-20; live view verified from Scrypted's log). Scrypted Core server address set to 192.168.1.218 the same day.
- [ ] Verify HKSV: Recording Options set in Home, a motion clip appears in the Home app and Scrypted logs a recording session
- [x] Add UniFi Protect to HA (API key only); camera-offline alerting; update the HA System page (2026-10-20: Aaron added it from the discovery card because Claude's flow aborted `already_in_progress`; Alert2 generator `homelab_camera_offline`, commit ad7a6c6)

## Changes

![[Changes.base#For this project]]
