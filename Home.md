The knowledge base for the Spriggs homelab: every system, service and network device, runbooks for procedures, the change history, and open and future work. Claude Code on the ClaudeCode VM writes it; Aaron reads it in Obsidian. Rules for writing here: [STANDARDS](<STANDARDS.md>). Code lives in the [spriggs-homelab repo](<systems/spriggs-homelab repo.md>). Moved here from Notion on 2026-10-22.

**ISP:** CenturyLink | **Domain:** thespriggs.com (Cloudflare, DDNS active) | **VPN:** WireGuard on UDM Pro, endpoint `vpn.thespriggs.com`, UDP 51820 | **Location:** Adams County, Colorado

## Infrastructure overview

A UniFi network (UDM Pro, USW Pro Max 16 PoE, three U7 APs) and a TrueNAS SCALE server, **Big Boi** (i9-9900, 64 GB, RAIDZ1 of 5× 4 TB SSD), that is both the NAS and the hypervisor. Big Boi runs three VMs, **Plex**, **Home Assistant** and **ClaudeCode** (Claude Code's LAN foothold), plus **Dockhand**, which runs the **servarr** media stack and **Uptime Kuma**. HA is the automation hub and the single alert endpoint: Kuma, TrueNAS alerts and the weekly VM update jobs all report into it, and it pushes to Aaron's iPhone only when something needs attention. **Home Health** is the HA dashboard for leaks, batteries and sensors. A Raspberry Pi wall panel shows an HA kiosk dashboard. A **UniFi UPS 2U** is installed but graceful shutdown isn't configured yet.

**Flat network:** 192.168.1.0/24, no VLANs, one SSID. DHCP-reserved: TrueNAS .248, HA .218, Plex .116, ClaudeCode .156, wall panel .84, HDHomeRun .106.

### How each system is reached

| System | Aaron | Claude (from the ClaudeCode VM) |
| --- | --- | --- |
| [TrueNAS](<systems/TrueNAS SCALE (Big Boi).md>) (192.168.1.248) | Web UI :9443 as `truenas_admin` (1Password "TrueNAS - Admin"); SSH `aspriggs` | Read-only API user `claude` via `truenas-api` (no writes). No SSH (never set up; checked 2026-09-29) |
| [Home Assistant](<systems/Home Assistant OS (VM).md>) (192.168.1.218) | UI :8123 as `aaronspriggs` (MFA); shell via the Terminal & SSH app's web terminal (no network SSH port) | ha-mcp (full control through HA's API). No SSH |
| [Plex VM](<systems/Plex Media Server.md>) (192.168.1.116) | SSH `plexadmin` | SSH `ssh plex` as `claude`; root only through `claude-maint` |
| [ClaudeCode VM](<systems/ClaudeCode (VM).md>) (192.168.1.156) | SSH `aspriggs` (key only); Claude Remote Control from claude.ai/code or the app | Local |
| [UniFi](<systems/UniFi (UDM Pro).md>) (UDM Pro, 192.168.1.1) | UniFi UI | Read-only local account `claude-readonly` via `unifi-api` (Network View Only) |
| [Dockhand](<systems/Dockhand.md>) (:3001) / [Uptime Kuma](<systems/Uptime Kuma.md>) (:3002) | Web UIs on 192.168.1.248 | No direct access; state via the TrueNAS API and HA's Kuma integration |
| [Wall panel Pi](<systems/Raspberry Pi Wall Panel.md>) (192.168.1.84) | SSH `raspberrypidashboard` | None yet (backlog task) |
| [Repo](<systems/spriggs-homelab repo.md>) (GitHub, private) | Owner | Push via a repo-only deploy key; clone at `~/homelab` |

Secrets are never stored here; each note names the 1Password item (TOTP codes are in Proton Authenticator). The access details above came from the Notion homepage (last reviewed there 2026-09-29); each System note's Access section is the authority.

## Open work

![[Projects.base#Open]]

## Recent changes

![[Changes.base#Recent]]

## Systems

![[Systems.base#All]]

## Runbooks

![[Runbooks.base#By kind]]
