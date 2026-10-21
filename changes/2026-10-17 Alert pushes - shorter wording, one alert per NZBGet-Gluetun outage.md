---
date: 2026-10-17
type: config
system:
- '[[Home Assistant OS (VM)]]'
- '[[Uptime Kuma]]'
project:
- '[[Claude access model - more admin access, secrets management, account hardening]]'
commit: https://github.com/aaronspriggs/spriggs-homelab/commit/7ac2d66
notion_id: 3fc7ae76-22ba-810e-8a8a-c1ac1137b28e
---

# Alert pushes: shorter wording, one alert per NZBGet/Gluetun outage, Restart on Kuma down alerts

Found in the fix-run tap test: one NZBGet outage pushed three time-sensitive alerts (nzbget_down, sonarr_health, radarr_health), and Aaron found the pushes wordy. ha/alert2.yaml: arr health alerts skip while sensor.nzbget_status is down or Gluetun is down/unhealthy; Kuma *_down alerts get a Restart button when a Big Boi container restart button exists (sonarr, radarr, prowlarr, nzbget, seerr); every title/message/done_message shortened (rule in the defaults comment and the alerting runbook). Applied with ha_config_set_yaml, alert2.reload, no alert2_error. Automations (UI, not in repo) shortened: homelab_alert_ack_snooze_on_tap (Ack/Snooze confirmations), homelab_claude_fix_run_on_tap, homelab_claude_fix_run_result (cost as ' · $0.47', fixed a missing space HA strips from rendered variables), homelab_container_restart_on_approval. Test push through the result automation rendered correctly. Reports (09:00, Sunday, maintenance summary) not reworded.
