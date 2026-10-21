---
date: 2026-10-17
type: config
system:
- '[[ClaudeCode (VM)]]'
project:
- '[[Claude access model - more admin access, secrets management, account hardening]]'
commit: https://github.com/aaronspriggs/spriggs-homelab/commit/7cff08d
notion_id: 3fc7ae76-22ba-81ea-93ec-e737dba25765
---

# claude-fix: shorter result push (one line for FIXED)

Aaron found the first real result push wordy (about 430 characters, truncated in the iOS banner). The wrapper now strips the FIXED:/NEEDS YOU:/NOT FIXED: prefix (the push title already says it). A FIXED push carries only the summary sentence; other outcomes keep up to three detail lines. The run prompt asks for a summary sentence under 100 characters. Tested outcome() against the real run's JSON; deployed, listener restarted, make check ok.
