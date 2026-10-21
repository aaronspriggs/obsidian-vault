---
type: project
status: done
priority: high
system:
- '[[ClaudeCode (VM)]]'
- '[[TrueNAS SCALE (Big Boi)]]'
- '[[Plex Media Server]]'
- '[[spriggs-homelab repo]]'
completed: 2026-09-27
notion_id: 3e77ae76-22ba-81d1-8da1-d9dc35a65d3b
---

# Homelab foundation: version-controlled repo for code & config (Notion = why, Git = how)

Done 2026-09-27: private GitHub repo spriggs-homelab holds all homelab code/config; Notion stays the why, runbooks link to the repo; make check catches drift. Page collapsed 2026-09-29.

## Outcome

Done 2026-09-27. Homelab code and config now live in the private GitHub repo [aaronspriggs/spriggs-homelab](https://github.com/aaronspriggs/spriggs-homelab), cloned at `~/homelab` on the ClaudeCode VM, and runbooks link to repo files instead of pasting source. The problem it fixed (seen 2026-09-24 to 2026-09-26): scripts existed only on hosts, with copies pasted into Notion that drifted, and nothing had history or rollback.
What was delivered: README with layout, secrets policy and the `<area>: <summary>` commit convention; pre-commit hook running gitleaks (plus custom rules for HA webhook IDs and Kuma push tokens) and shellcheck; `deployed.tsv` + `make check` comparing sha256 of every deployed file against the repo (all 8 matched at import); imports of `homelab-update/`, `truenas/`, `plex-vm/`, `claudecode-vm/` and `stacks/`. `CLAUDE.md` gained the repo rule. Current state and layout: [spriggs-homelab repo](<../systems/spriggs-homelab repo.md>).

## Decisions

- **2026-09-26: Notion = what and why, Git = how.** Notion stays the source of truth (Projects, Systems, Changes, Runbooks) because both Claudes can read and write it; one private repo holds code and config. No Jira: team-workflow overhead for one person.
- **2026-09-26: GitHub, not self-hosted Gitea/Forgejo,** so the code has an offsite copy and doesn't die with Big Boi.
- **2026-09-26: Claude's access is a write deploy key scoped to this repo** (`~/.ssh/id_ed25519_github_spriggs_homelab`, never leaves the VM; no expiry). GitHub App rejected for now: it still needs a long-lived private key on the VM, so no gain for one VM and one repo. No `gh` CLI or PR/issue API; Claude commits directly to `main`.
- **2026-09-26: deploy model is "repo is the source, copy to hosts",** with `make check` for drift. Hosts don't pull from the repo.
- **2026-09-26: out of scope:** Home Assistant config (storage-mode; HA backups cover it, and a config repo must never hold `.storage`/`secrets.yaml`). `sops`/`age` not adopted: hosts keep real values and the repo holds `*.example` templates.
- **2026-09-26: deferred** Ansible, Renovate and a docs site until the host/container count makes per-host work a burden.
- `stacks/` needs Aaron to copy files (the read-only TrueNAS API can't read files; the VM only accepts SSH keys). Procedure in `stacks/README.md`.

## Links

Commits: scaffold `0eb8016`, imports `619b974`, gitleaks rules `3b633ac`, stacks `2dd54a6`. Follow-ups split out 2026-09-29: "Evaluate Renovate for container image and dependency updates" (Idea, Deferred) and "Check whether Cowork can read the spriggs-homelab repo" (Task, Backlog). Full pre-collapse text: KB export commit 4ac914e.
