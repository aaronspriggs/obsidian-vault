---
type: task
status: backlog
priority: low
system:
- '[[ClaudeCode (VM)]]'
- '[[Claude Code (Remote Control service)]]'
parent: '[[Build a Tier 3 guard mod for Claude Code]]'
---

Follow-up from the [setup review](<Review and tune the Claude Code setup on the ClaudeCode VM.md>), closed out on 2026-11-15.

## Goal

Stop tier3-guard holding commands that only mention `ssh-keygen` or the SSH authorized-keys file. Four false holds on 2026-11-15: the `keygenChangesKeys` rule matches `ssh-keygen` anywhere in a command (a `cat` of a change note, a heredoc editing a project note), and the rule on the authorized-keys file does the same (a read-only check, a heredoc editing a project note).

## Plan

1. Match both only where a simple command starts with `ssh-keygen`, or names the authorized-keys file as the target of a write (the same shape step 3 of the review gave the guarded-path rule).
2. Add the four false holds and the true cases to the guard's tests, and replay the recorded Bash commands as in step 3.
3. Claude writes and tests it in the repo; Aaron commits, pushes and deploys with one SSH line (guard changes go through his hands).

## Decisions

- **2026-11-15: bundle with the next guard change, not a deploy of its own.** A false hold costs one retry, and each guard deploy is a Tier 3 step for Aaron. The natural partner is [Let tier3-guard skip deletes of items Claude created in the same session](<Let tier3-guard skip deletes of items Claude created in the same session.md>). Aaron can ask for it sooner.
