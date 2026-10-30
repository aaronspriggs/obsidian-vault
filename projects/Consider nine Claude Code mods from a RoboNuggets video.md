---
type: idea
status: backlog
priority: low
system:
- '[[ClaudeCode (VM)]]'
---

# Consider nine Claude Code mods from a RoboNuggets video

Aaron liked some of the mods in [9 NEW Claude Mods that can truly change how you work](https://www.youtube.com/watch?v=lDrAZ1wAyVs) (Jay E, RoboNuggets, 2026-10-08) and wants them kept as possible additions (2026-10-30). The list and links below come from the video's description and each mod's README, read 2026-10-30. The video's captions couldn't be fetched, so what the video itself says about each mod isn't captured here. None of these are installed or tested yet.

Two limits decide most of the fit. First, over Remote Control only mod hooks work; panes, bands, buttons, toasts and status lines don't render (see [Use mod UI once Remote Control clients draw it](<Use mod UI once Remote Control clients draw it.md>)). Second, the token budget rules out anything that makes model calls on its own. The VM runs Claude Code 2.1.286; Skins, Cache Tax and Filetree need 2.1.287 or newer (Filetree needs 2.1.306).

## The nine mods and how they'd fit here

- **Blast Radius** ([Anthropic sample](https://github.com/anthropics/claude-code-playground/tree/main/claude-code/mods/blast-radius)): holds `rm -r`, `git reset --hard`, `git clean`, `git push --force` and migrations, works out what they'd touch (files and sizes, uncommitted changes, commits a force push would drop) and asks Proceed or Cancel. The buttons won't show over Remote Control, but the measuring code is the useful part: tier3-guard could print the same impact report in its hold message. Best fit of the nine.
- **Cache Tax** ([karanb192/cache-tax](https://github.com/karanb192/cache-tax)): before a message that would rewrite a cold cache in a 50k+ token session, it drops the send once and shows the estimated cost, and the README says this guard covers Remote Control messages. Only the guard fits; its `/keepwarm` pings spend tokens on a timer, which the token budget rules out. A settings-hook version that only warns is in [karanb192/claude-code-hooks](https://github.com/karanb192/claude-code-hooks/tree/main/plugins/cache-tax).
- **Reflect** ([BayramAnnakov/claude-reflect](https://github.com/BayramAnnakov/claude-reflect)): turns Aaron's corrections into saved rules. The Python plugin queues corrections from a hook and `/reflect` reviews them later by text, which works over Remote Control. The mod version runs a Haiku call on every short prompt and saves through buttons, so it doesn't fit. Either version writes to CLAUDE.md, while here corrections belong in the versioned memory directory, so it would need pointing there.
- **You Should Know** (built into Claude Code, no repo; turned on with `/plugin enable cc-plugin-you-should-know@builtin`): a side agent forks the model during a turn and flags things Aaron might miss, in a band above the prompt. It's present in 2.1.286 on the VM. Each check is a model fork and the output is UI, so it fails both limits for now.
- **Savvy Progress** ([JohnnyVizz/claude-kit](https://github.com/JohnnyVizz/claude-kit/tree/main/plugins/savvy-progress)): progress bar and live subagent panel with cost estimates. UI only, and subagents are rare here.
- **Replay Theater** ([Anthropic sample](https://github.com/anthropics/claude-code-playground/tree/main/claude-code/mods/replay-theater)): steps through the last turn's file edits one diff at a time in a pane. UI only.
- **Filetree** ([data-goblin/claude-code-filetree](https://github.com/data-goblin/claude-code-filetree)): IDE-style file tree that lights up the files Claude reads and writes, in a sidebar that needs the fullscreen terminal layout. UI only.
- **Claude Skins** ([hellosverre/claude-skins](https://github.com/hellosverre/claude-skins)): restyles tool calls, diffs, tables and Mermaid charts, plus a usage band and themes. UI only. Its marketplace also has a `mod-store` mod for browsing about 2,700 mods.
- **Terminal Browser** ([zenbu-labs/terminal-browser](https://github.com/zenbu-labs/terminal-browser)): a real browser inside a terminal with kitty graphics, which Claude can drive. It needs a graphics terminal, so it does nothing over Remote Control, and the VM already has WebFetch for reading pages.

## When to pick this up

Aaron hasn't said yet which mods he liked; ask before starting. Blast Radius' impact report (folded into tier3-guard) and the Cache Tax guard without keepwarm are worth doing now, since they work by text. The UI-only mods wait on the mod UI project above. Install third-party mods only after reading their source, since a mod's hooks see every tool call.
