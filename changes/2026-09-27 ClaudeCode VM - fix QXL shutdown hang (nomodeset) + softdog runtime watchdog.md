---
date: 2026-09-27
type: fix
system:
- '[[ClaudeCode (VM)]]'
notion_id: 3e87ae76-22ba-8127-99c6-e4ce4c9f0791
---

# ClaudeCode VM: fix QXL shutdown hang (nomodeset) + softdog runtime watchdog

First homelab-update run rebooted the VM at 10:30:45 (kernel 7.0.0-30 → -34). Shutdown hung ~9.5 h until Aaron hard-reset at ~20:10: PID 1 stuck in D state in drm_modeset_lock via fbcon on the qxl (SPICE) framebuffer; kernel had logged [TTM] Buffer eviction failed every 15 s since at least 2026-09-07. Fix: nomodeset on kernel cmdline, softdog + RuntimeWatchdogSec=2min. Commit 585a3f9.

## What happened

The first `homelab-update` run on 2026-09-27 installed updates including kernel 7.0.0-34, then ran `systemctl reboot` at 10:30:45 UTC. The shutdown hung at 10:30:46: PID 1 blocked in D state (hung-task trace: `drm_modeset_lock` ← `drm_fb_helper_pan_display` ← `fbcon_switch` ← tty write) on the `qxl` virtual GPU driver. It stayed there until Aaron hard-reset the VM at ~20:10 UTC, so the VM was down about 9.5 h. The underlying fault had been showing for weeks: the kernel logged `[TTM] Buffer eviction failed` every ~15 s since at least 2026-09-07. This was the first reboot since then.
Side effect: after the hard reset, `claude remote-control` registered a new environment (`env_01A53F5…` → `env_01VzTgq…`), so the Claude desktop app filed all earlier sessions under "Other" and made a new `homelab-agent` group. The transcripts are still on disk in `~/.claude/projects/-home-aspriggs-homelab-agent/`.

## Fix

Commit [585a3f9](https://github.com/aaronspriggs/spriggs-homelab/commit/585a3f9) in `claudecode-vm/`:
- `grub/99-nomodeset.cfg` → `/etc/default/grub.d/`: appends `nomodeset`, so the kernel never loads the qxl DRM framebuffer. The TrueNAS console still works in VGA text mode.
- `modules-load.d/softdog.conf` + `systemd/system.conf.d/watchdog.conf`: kernel software watchdog. `RuntimeWatchdogSec=2min` reboots the VM if PID 1 stops pinging for 2 min (any cause, including during shutdown). `RebootWatchdogSec=5min` covers the final shutdown stage.
The watchdog lives at the system level rather than in `homelab-update` because the hang happened after the script had exited and inside PID 1 itself, where a script-level or systemd-timer watchdog couldn't fire.

## Verification

Before the reboot: `wdctl` shows the softdog on `/dev/watchdog0` with a 120 s timeout; `RuntimeWatchdogUSec=2min`; the generated `grub.cfg` has `nomodeset`; `make check` is clean.
After the reboot, check that `/proc/cmdline` contains `nomodeset`, `lsmod | grep qxl` is empty, `wdctl` is armed, and `journalctl -k | grep TTM` is empty.
**Verified after the test reboot (2026-09-27):** `nomodeset` is on the cmdline, qxl isn't loaded, and there are 0 TTM errors. **But the watchdog wasn't armed**: Ubuntu's kernel package blacklists every watchdog driver (`/lib/modprobe.d/blacklist_linux_*.conf`: `blacklist softdog`), and `systemd-modules-load` honours the blacklist, so the `modules-load.d` entry was silently ignored. An explicit `modprobe` isn't blocked. Replaced it with `claudecode-vm/systemd/softdog.service` (early-boot oneshot, `modprobe softdog`), commit [147dd96](https://github.com/aaronspriggs/spriggs-homelab/commit/147dd96). Confirmed that PID 1 opens `/dev/watchdog0` on its own once the module appears, with no reexec needed. The watchdog is armed now; boot-time loading gets confirmed on the next reboot (the weekly update).
**Also affected:** the TrueNAS alert relay didn't run from 10:29:41 (last successful run) until 20:12:03 (first run after the hard reset), so TrueNAS alerts weren't forwarded to HA for about 9.5 h and the Kuma push monitor stayed down. It recovered on its own after the reboot; nothing wrong with the relay itself.
**Fully verified 2026-09-27 20:28 UTC** with a second test reboot: clean shutdown (took about 3 s, journal ends with `systemd-shutdown` syncing), `softdog.service` active 3 s into boot with no manual step, `wdctl` shows the Software Watchdog, `RuntimeWatchdogUSec=2min`, `nomodeset` on the cmdline, qxl not loaded.
