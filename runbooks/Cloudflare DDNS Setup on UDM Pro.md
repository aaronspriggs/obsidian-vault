---
kind: setup
status: active
system:
- '[[UniFi (UDM Pro)]]'
notion_id: 30a7ae76-22ba-81b5-ae17-f63a362ea239
---

Configure the UDM Pro to automatically update a Cloudflare DNS A record ([vpn.thespriggs.com](http://vpn.thespriggs.com/)) whenever the CenturyLink WAN IP changes. Prerequisite for WireGuard VPN setup.

## Overview

The UDM Pro's built-in DDNS feature can update a Cloudflare DNS record automatically whenever the WAN IP changes. This is a prerequisite for WireGuard VPN, so the client config can use a stable hostname (`vpn.thespriggs.com`) instead of a raw IP that may change.
Cloudflare was added as a native DDNS provider in UniFi OS 4.3.6+. No scripts or external clients required.

## Prerequisites

- Active Cloudflare account with `thespriggs.com` using Cloudflare nameservers
- Access to UDM Pro controller at [https://192.168.1.1](https://192.168.1.1/)
- UniFi OS 4.3.6 or newer (currently on 5.0.12 ✓)

## Phase 1 — Create Cloudflare API Token

1. Go to [https://dash.cloudflare.com](https://dash.cloudflare.com/) and log in.
2. Click your **profile icon** (top-right) → **My Profile**.
3. In the left sidebar, click **API Tokens**.
4. Click **Create Token**.
5. Find the **"Edit zone DNS"** template → click **Use template**.
6. Rename the token to something descriptive: `UDM Pro DDNS – thespriggs.com`
7. Under **Zone Resources**, change from "All zones" to:
    - Include → Specific zone → [**thespriggs.com**](http://thespriggs.com/)
8. Leave TTL untouched (no expiration).
9. Click **Continue to summary** → review → **Create Token**.
10. **Copy the token immediately** — Cloudflare only shows it once. Store in password manager.
11. Verify the token works using the curl command Cloudflare provides on that screen. Expected response: `"status":"active"`

## Phase 2 — Configure DDNS on UDM Pro

1. Log into UniFi controller at [https://192.168.1.1](https://192.168.1.1/)
2. Go to **Settings → Internet**.
3. Click on **Internet 1 (WAN1 / CenturyLink)**.
4. Scroll to **Advanced** → switch from **Auto** to **Manual**.
5. Scroll to the **Dynamic DNS** section → click **Create New**.
6. Fill in the fields:
    - **Service:** Cloudflare
    - **Hostname:** `vpn.thespriggs.com`
    - **Zone Name:** `thespriggs.com`
    - **API Token:** *(paste token from Phase 1)*
7. Click **Save**.

## Verification

- Wait 10–15 minutes after saving.
- Log into [https://dash.cloudflare.com](https://dash.cloudflare.com/) → [thespriggs.com](http://thespriggs.com/) → **DNS → Records**.
- Confirm an A record for `vpn.thespriggs.com` exists pointing to the current WAN IP.
- Confirm the record shows **DNS only (grey cloud)** — not proxied. Proxied breaks WireGuard UDP traffic.
- Optionally set the record's TTL to **60 seconds** for faster propagation on future IP changes.

## Gotchas

- The A record does **not** need to be pre-created in Cloudflare — UDM Pro creates it automatically.
- Record **must not** be proxied (orange cloud) — WireGuard uses UDP which Cloudflare's proxy doesn't support.
- If the DDNS entry shows an error in UniFi, double-check the API token scope and that the zone name matches exactly.

## Next Step

Once verified, proceed to WireGuard VPN setup on UDM Pro using `vpn.thespriggs.com:51820` as the endpoint.
