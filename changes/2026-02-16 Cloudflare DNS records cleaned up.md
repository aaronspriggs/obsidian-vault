---
date: 2026-02-16
type: doc
system:
- '[[UniFi (UDM Pro)]]'
notion_id: 30a7ae76-22ba-81c6-a933-fefd40d3bef9
---

# Cloudflare DNS records cleaned up

Deleted orphaned DNS records from pre-2022 GoDaddy hosting (email, imap, smtp, pop, mail, webmail, mobilemail, pda, ftp, www, _domainconnect CNAMEs, stale plex A record, two GoDaddy MX records). Domain was fully transferred to Cloudflare in 2022. Remaining records: [thespriggs.com](http://thespriggs.com/) A record (stale IP, harmless) and [vpn.thespriggs.com](http://vpn.thespriggs.com/) A record (DDNS).
