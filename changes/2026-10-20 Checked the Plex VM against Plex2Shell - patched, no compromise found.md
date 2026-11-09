---
date: 2026-10-20
type: research
system:
- '[[Plex Media Server]]'
---

# Checked the Plex VM against Plex2Shell: patched, no compromise found

## What changed

Nothing changed; this records a security check that was done on 2026-10-20 but only written to the KB on 2026-11-09, when its session was archived.

## Why

Plex2Shell (CVE-2026-96652, -96654, -96655, -96656) chains two SSRFs and a token leak into unauthenticated code execution. It writes a malicious `.so` into Plex's `Codecs` directory, and attackers used it to drop an XMRig miner (`mylovelyminer`, file `x12345`) and the `myawesomeproxy` reverse proxy (AISURU botnet). Fixed in Plex 1.43.3.10861 (about Sept 1, 2026); PoC public Oct 16, exploitation from Oct 17. It needs Plex reachable from the internet on 32400, which ours is (UDM Pro forwards TCP 32400 to 192.168.1.116).

## How

Over `ssh plex` on 2026-10-20: the server reported `1.43.4.10903` (past the fix, installed 2026-09-24); no IOC processes or files (`xmrig`, `mylovelyminer`, `myawesomeproxy`, `x12345`); nothing new in the `Codecs` directory since 2026-10-15; no unexpected outbound connections. Plex now runs 1.43.5 (2026-11-09) and homelab-update keeps it current weekly, which is the real mitigation while 32400 stays forwarded. Source: [The Hacker News](https://thehackernews.com/2026/10/hackers-exploit-plex2shell-flaws-to.html).
