---
kind: setup
status: deprecated
system:
- '[[ClaudeCode (VM)]]'
notion_id: 3217ae76-22ba-81a0-a62b-fa8c9f22e780
---

Step-by-step setup for a dual-mode AI workflow: [Claude.ai](http://claude.ai/) GUI for planning, VS Code + Claude Code on Mac for execution. Covers installation, Remote SSH, Notion MCP integration, and [CLAUDE.md](http://claude.md/) per-project context.

**Deprecated 2026-09-28:** Aaron uses Claude Code through the desktop and mobile apps (Remote Control to the ClaudeCode VM), not VS Code (KB governance decision 4). See [ClaudeCode (VM)](<../systems/ClaudeCode (VM).md>) and [Setting Up ha-mcp](<Setting Up ha-mcp (Home Assistant MCP Server) for Claude Code.md>).

## Overview

This runbook sets up a two-mode AI workflow:
- [**Claude.ai**](http://claude.ai/)** (GUI)** — planning, discussion, and high-level decisions
- **VS Code + Claude Code (Mac)** — executing changes, building projects, managing servers
Both share the same Notion KB as a single source of truth via MCP.

---

## Prerequisites

- Claude Pro (or Max) subscription — required for Claude Code access
- Mac with admin access
- SSH access to TrueNAS VMs and services
- Notion workspace connected to [Claude.ai](http://claude.ai/) (already done)

---

## Step 1 — Install VS Code

Download and install from [https://code.visualstudio.com](https://code.visualstudio.com/)
No special configuration needed at this stage.

---

## Step 2 — Add the Remote SSH Extension

1. Open VS Code
2. Go to Extensions (⇧⌘X)
3. Search for **Remote - SSH** (published by Microsoft)
4. Install it
This allows VS Code to connect directly to your TrueNAS VMs and edit files as if they were local.

---

## Step 3 — Install Claude Code on Mac

Claude Code runs locally on your Mac and SSHs out to your servers as needed. No VM required.
```bash
curl -fsSL https://claude.ai/install.sh | bash
```
Or via Homebrew:
```bash
brew install --cask claude-code
```
Authenticate with your [Claude.ai](http://claude.ai/) account when prompted.
> Verify install: open a terminal and type `claude` — it should start a session.

---

## Step 4 — Add Notion MCP to Claude Code

This connects Claude Code to the same Notion KB used by [Claude.ai](http://claude.ai/).
Create or edit `~/.claude/settings.json`:
```json
{
  "mcpServers": {
    "notion": {
      "type": "url",
      "url": "https://mcp.notion.com/mcp",
      "name": "notion"
    }
  }
}
```
Authenticate Notion when Claude Code prompts on first use.
> Reference: [https://docs.claude.com](https://docs.claude.com/) (search "MCP servers Claude Code")

---

## Step 5 — Set Up [CLAUDE.md](http://claude.md/) Per Project

Claude Code reads `CLAUDE.md` from the current working directory at the start of every session.

### File structure

```javascript
~/projects/
├── homelab/
│   └── CLAUDE.md       ← homelab context only
└── my-app/
    └── CLAUDE.md       ← app context only
```

### Global preferences (optional)

Create `~/.claude/CLAUDE.md` for things that apply across all projects (preferred coding style, general preferences, etc.)

### What to put in each [CLAUDE.md](http://claude.md/)

- What the project is and its goals
- Pointer to relevant Notion pages for live context
- Key constraints or preferences
- Any naming conventions or patterns to follow
> The homelab [CLAUDE.md](http://claude.md/) should reference the HomeLab KB in Notion so Claude Code pulls current system state before making changes.

---

## Day-to-Day Workflow

| Mode | Tool | Use for |
| --- | --- | --- |
| Planning | [Claude.ai](http://claude.ai/) GUI | Brainstorming, discussing approach, reviewing options |
| Execution | VS Code + Claude Code | Making changes, building, configuring servers |
| Documentation | Notion | Single source of truth, updated after changes |

### Switching from GUI → Claude Code

1. Finish planning conversation in [Claude.ai](http://claude.ai/)
2. Open VS Code → connect to relevant server via Remote SSH (or work locally for app projects)
3. Open integrated terminal → run `claude` in the project folder
4. Claude Code reads [CLAUDE.md](http://claude.md/) + Notion context automatically
5. Execute the work

---

## Project Isolation

Context never bleeds between projects because Claude Code only reads the `CLAUDE.md` in the current directory. Separate folders = separate context.
- Homelab work → open `~/projects/homelab/` in VS Code
- App projects → open `~/projects/my-app/` in VS Code

---

## Notes

- Claude Code and [Claude.ai](http://claude.ai/) have no shared memory between sessions — [CLAUDE.md](http://claude.md/) and Notion MCP bridge this gap
- Keep Notion as the source of truth; update it after significant changes
- Claude Pro limits apply to Claude Code sessions — heavy builds may warrant upgrading to Max
