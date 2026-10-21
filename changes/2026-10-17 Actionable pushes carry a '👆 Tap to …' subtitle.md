---
date: 2026-10-17
type: config
system:
- '[[Home Assistant OS (VM)]]'
- '[[Uptime Kuma]]'
project:
- '[[Claude access model - more admin access, secrets management, account hardening]]'
commit: https://github.com/aaronspriggs/spriggs-homelab/commit/3e1ae09
notion_id: 3fc7ae76-22ba-81f5-8a63-c1717c3246a5
---

# Actionable pushes carry a '👆 Tap to …' subtitle; Snooze re-push keeps Fix with Claude

Aaron wanted to tell from the banner which pushes need his action. iOS subtitle '👆 Tap to <button> or <button>' on every push with a real action button (Restart, Fix with Claude, Install, Update all), built from the same list as the buttons; none on FYI or Ack/Snooze-only pushes. ha/alert2.yaml: service_down, arr health, gluetun_down/unhealthy, container_down/unhealthy data templates rebuilt as fix-list + dict(); container update alert has a literal subtitle. Automations (UI): homelab_alert_ack_snooze_on_tap re-push now builds its data as one template with the subtitle, and adds Fix with Claude when action_data has a fix_id (the re-push used to drop it); 09:00 report Install push and Sunday report Update all get the subtitle. All templates render-tested (Restart, Fix with Claude, both, none); alert2.reload with no alert2_error; a passive test push sent to Aaron's phone to check the subtitle renders.
