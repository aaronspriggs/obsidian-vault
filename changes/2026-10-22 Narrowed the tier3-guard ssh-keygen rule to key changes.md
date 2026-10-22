---
date: 2026-10-22
type: config
system:
- '[[ClaudeCode (VM)]]'
project: '[[Build a Tier 3 guard mod for Claude Code]]'
commit: https://github.com/aaronspriggs/spriggs-homelab/commit/ce93d33
---

# Narrowed the tier3-guard ssh-keygen rule to key changes

## What changed

`tier3-guard` no longer holds every `ssh-keygen` call. Calls that only read run freely: `-l` (fingerprint), `-F` (known_hosts lookup) and usage (`--help`, `-?`), with `-f`, `-E` and `-v` allowed alongside them. A bare call, `-f` alone, `-t`, `-p`, `-R`, `-y` and any other flag are still held.

## Why

The first live test on 2026-10-22 held `ssh-keygen --help`, a harmless call. Aaron approved narrowing the rule the same day.

## How

Repo commit [ce93d33](https://github.com/aaronspriggs/spriggs-homelab/commit/ce93d33). `hooks/register.ts` was copied to `~/.claude/mods/tier3-guard/hooks/register.ts`, and `make check` came back clean. New sessions pick it up.

## How to verify / roll back

Verify: `claude plugin test ~/homelab/claudecode-vm/mods/tier3-guard` passes (53 tests). Roll back: revert ce93d33 and copy `register.ts` back. With the guard active, the copy into `~/.claude/mods` is held for Aaron's approval.
