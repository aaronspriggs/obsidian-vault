---
type: project
status: active
priority: high
system:
- '[[UniFi (UDM Pro)]]'
next_step: 2026-11-09 Aaron orders a UACC-CM-RJ45-MG and a Cat6a patch cable (must arrive before 2026-12-07) and decides where the Ting ONT goes; Claude verifies each UDM step with unifi-api on install day.
---

## Goal

Ting Fiber 2000 (2 Gbps symmetrical) installs **2026-12-07 at 3 pm**. Plug the Ting ONT straight into the UDM Pro, the same way CenturyLink bypasses its router today, with no Ting router in the path. Run both ISPs side by side, move primary to Ting once it's proven, and keep CenturyLink as failover until Aaron cancels it.

## Status / next step

2026-11-09: research done, plan below. Before install day, Aaron orders the hardware and decides where the ONT goes. Nothing on the UDM changes until 2026-12-07.

## Starting point (read live with unifi-api, 2026-11-09)

- **Internet 1** (CenturyLink): Port 9, the UDM Pro's only RJ45 WAN port (GbE). PPPoE on VLAN 201, IPv6 disabled, failover priority 1. The provider capabilities field says 723/539 Mbps.
- **Internet 2**: already exists. DHCP, no VLAN, IPv6 disabled, `failover-only`, priority 2, **no port assigned**.
- **SFP+ 1 (port 10)**: empty, link down. **SFP+ 2 (port 11)**: 10G DAC to the USW Pro Max 16.
- Plex port forward (32400), the WireGuard server (51820) and Cloudflare DDNS (`vpn.thespriggs.com`) are all tied to WAN1.
- IDS/IPS and Smart Queues are off. The UDM Pro is rated 3.5 Gbps IDS/IPS throughput, so 2 Gbps fits with headroom ([UDM Pro tech specs](https://techspecs.ui.com/unifi/cloud-gateways/udm-pro)). Smart Queues must stay off on this line: SQM on the UDM Pro caps throughput well below 2 Gbps.

## Hardware

Port 9 is taken by CenturyLink and is GbE anyway, so Ting goes into **SFP+ 1 (port 10)**. The UDM Pro's SFP+ ports only run at 1G or 10G, so it needs a copper module that negotiates multi-gig:

- **Ubiquiti UACC-CM-RJ45-MG** (SFP+ to RJ45, 1/2.5/5/10 Gbps, $65, [store](https://store.ui.com/us/en/category/accessories-transceivers/products/uacc-cm-rj45-mg), [tech specs](https://techspecs.ui.com/unifi/accessories/uacc-cm-rj45-mg)). It works whether the ONT's port turns out to be 2.5G or 10G. Don't buy the older UF-RJ45-10G: it only does 1G/10G and won't link to a 2.5G ONT port ([Wichita Computer Guy write-up](https://www.thewichitacomputerguy.com/blog/how-connect-10gbe-sfp-wan2-ubiquiti-unifi-udm-pro-se-1gbe-25gbe-5gbe-modem)).
- **Cat6a patch cable** from the ONT to the rack, long enough for wherever the ONT ends up.

The UniFi UI can show the port as 10G even when the copper side negotiated 2.5G ([same write-up](https://www.thewichitacomputerguy.com/blog/how-connect-10gbe-sfp-wan2-ubiquiti-unifi-udm-pro-se-1gbe-25gbe-5gbe-modem)). Judge the link by measured throughput, not the port badge. One reader comment there reports the module overheating and dropping; watch for WAN2 flaps in the first weeks.

## What Ting documents (and doesn't)

Ting supports bringing your own router and says the ONT hands off "standard Ethernet" ([BYOR article](https://help.ting.com/internet-articles/byor-to-your-ting-internet-service)). Its static-IP page says customer equipment just needs to "acquire an IP address through DHCP", and that IPv6 is available in some markets via "standard DHCPv6" alongside IPv4 ([static IP article](https://help.ting.com/internet-articles/ting-internet-static-ip-addresses)). So the WAN is plain DHCP with no PPPoE. That's simpler than CenturyLink, and the UDM's PPPoE single-thread limit doesn't apply. The ONT goes inside the house and is installed by the tech ([Getting Ting Fiber to your home](https://help.ting.com/internet-articles/getting-ting-fiber-to-your-home)).

Not documented anywhere I could read (two of Ting's 2 Gig help pages return 404): the ONT model and port speed, any VLAN tag, whether the ONT locks to the first MAC it sees, IPv6 prefix-delegation size, and whether residential IPv4 is public or CGNAT. 2026-11-10: a Ting installer working in the neighborhood told Aaron each house gets its own public IPv4 by DHCP and Ting doesn't use CGNAT.

## Plan

**Before 2026-12-07 (Aaron):**

1. Order the UACC-CM-RJ45-MG and a Cat6a patch cable.
2. Decide where the ONT goes and tell the tech on the day: as close to the rack as practical. If the UPS 2U has a free battery-backed outlet, plug the ONT into it. The CenturyLink ONT isn't on battery today, so internet drops on a power cut. All four battery outlets are believed to be in use (UPS note, 2026-09-29), so check first.
3. If the order includes Ting's eero rental (Whole Home Wi-Fi), decide whether to keep it. The UDM and U7 APs replace it.

**Install day, with the tech (2026-12-07):**

4. Let the tech bring the line up and test on their own equipment. Then ask: ONT model and port speed, any VLAN tag, whether the ONT needs a power-cycle (or a call to Ting) to hand a lease to a new router MAC, and whether IPv6/DHCPv6-PD is live in this market and at what prefix size.
5. Turn on `input_boolean.homelab_maintenance_mode`.
6. Module into SFP+ 1, Cat6a from the ONT. In UniFi Network → Settings → Internet → Internet 2: assign port **SFP+ 1**, DHCP, VLAN off, IPv6 off for now, set the advertised speed to 2000/2000. Keep it `failover-only`, priority 2, so CenturyLink still carries everything. If no lease arrives, power-cycle the ONT. Claude confirms with `unifi-api` that WAN2 is up with an address. The 10.6 menu labels may differ slightly from these, and the API read is the check.
7. **Public-IP check.** The installer said no CGNAT (2026-11-10), so this is a quick confirmation, not an expected blocker. Claude checks the WAN2 address: it must not be in 100.64.0.0/10 and must match what an external lookup sees when routed out WAN2. If it fails anyway, stop before step 10 and call Ting, because Plex remote access and WireGuard need a public IP.
8. Add a policy-based route (Settings → Routing → Policy-Based Routes, or Policy Table) sending one wired client out Internet 2. Test from a client faster than 1G: a 1G client tops out around 940 Mbps and would look like a fault. Use Big Boi (10G), e.g. a speedtest container, or the desk machine if its NIC is 2.5G (unknown, see the Workstation note). The UDM's built-in speed test isn't reliable at multi-gig.

**Cutover (same day if step 8 is clean, otherwise when Aaron chooses):**

9. Make Ting primary: Internet 2 priority 1, Internet 1 (CenturyLink) priority 2, both failover-only. No load balancing: it splits sessions across two public IPs and breaks sites that pin a session to an IP.
10. Move everything tied to WAN1 to Internet 2, in this order:
    - The Cloudflare DDNS entry for `vpn.thespriggs.com` (per the [DDNS runbook](<../runbooks/Cloudflare DDNS Setup on UDM Pro.md>)).
    - The WireGuard server's interface.
    - The Plex port forward's WAN interface: set it to Internet 2, or to both WANs if the UI offers that.
11. Verify: the DDNS record shows the Ting IP, a phone off Wi-Fi connects over WireGuard, and Plex reports remote access as reachable. Remove the test policy route and turn maintenance mode off.

**After CenturyLink is cancelled:**

12. Delete the Internet 1 PPPoE config and rename Internet 2 to "Ting". Ting stays on SFP+ 1; Port 9 becomes spare.
13. Optional: turn on IPv6 (DHCPv6, PD at the size Ting gives) once the flat LAN plan is decided.

## Decisions

- 2026-11-09: Ting goes on SFP+ 1 with a UACC-CM-RJ45-MG, not Port 9: Port 9 is GbE and taken by CenturyLink.
- 2026-11-10: no CGNAT expected (Ting installer to Aaron); the step 7 check stays as a quick confirmation.
- 2026-11-09: failover, not load balancing, while both lines run. Ting becomes primary only after the CGNAT gate and a multi-gig speed test.
- 2026-11-11 (Aaron): in the planned 30U floor rack both ONTs (CenturyLink and Ting) sit on a rack shelf, powered from a PDU Pro on the UPS, so internet stays up on battery. See the v3 layout in [Rebuild Big Boi into a new case with an HDD pool for bulk media](<Rebuild Big Boi into a new case with an HDD pool for bulk media.md>). Until that rack exists, step 2 still applies.
- 2026-11-09: Claude's UniFi account is read-only, so Aaron makes every UDM change in the UI and Claude verifies each one with `unifi-api`.

## Open questions

- Ting ONT model and port speed, VLAN, MAC behaviour, IPv6/PD size (ask the tech, step 4). Public IPv4 answered 2026-11-10 (yes, no CGNAT, per a Ting installer); confirmed live in step 7.
- Is a battery-backed UPS outlet free for the ONT?
- Alerting on WAN failover: a silent fail-back to CenturyLink would go unnoticed. Decide after cutover whether the HA UniFi integration or Uptime Kuma can see the active WAN.
