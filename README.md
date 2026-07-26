# copse

A terminal ADE (Agent Development Environment) built with Herdr + Neovim. A lightweight, CLI-native alternative to Orca for developers who prefer terminals over Electron.

The name comes from a *copse* — a small stand of trees. Each git worktree is a tree; copse manages them all.

## Requirements

- macOS
- [Homebrew](https://brew.sh)
- [Herdr](https://herdr.dev)
- A terminal emulator of your choice
- [PlemolJP Console NF](https://github.com/yuru7/PlemolJP) (or any other Nerd Font)

## Setup

```bash
git clone https://github.com/s-0-a-r/copse.git ~/copse
cd ~/copse
./setup.sh
```

If the tools are already installed:

```bash
./setup.sh --config-only
```

The setup script installs neovim, herdr, fzf, fd, ripgrep and deploys configs as symlinks.

After setup, Neovim auto-installs plugins on first launch. To pin to the exact versions in this repo:

```bash
nvim --headless "+Lazy! restore" +qa
```

## Configuration

Set `IDE_PROJECTS_DIR` to change the root directory scanned for projects (default: `~/projects`):

```bash
export IDE_PROJECTS_DIR="$HOME/work"
```

Worktrees are always placed under `$IDE_PROJECTS_DIR/.worktrees/<repo>/<branch>/`.

## Usage

```bash
copse                    # pick from ~/projects (includes worktrees) via fzf
copse .                  # open current directory
copse ~/my-app           # open a specific directory
copse ~/my-app --agent   # open with a Claude Code agent pane
```

### Agent Development (Orca-style)

```bash
# Open a branch as an isolated worktree workspace (agent starts by default)
copse worktree feature/my-branch --project ~/my-app
copse worktree feature/my-branch --project ~/my-app --no-agent  # editor only

# Fan out N parallel agents on the same task
copse fan "Add OAuth2 login" --count 3
copse fan "Refactor auth module" --count 2 --project ~/my-app
```

The `fan` command creates N isolated git worktrees, starts Neovim + Claude Code in each, and injects the task prompt automatically. Agents work in parallel; compare results with `git diff`.

> **Note:** copse requires the herdr TUI to be running before use. Start herdr first, then run copse from any terminal.

## Layout

| Mode | Panes | Description |
|---|---|---|
| No agent | nvim (65%) \| terminal (35%) + terminal below | VSCode-style: editor-first |
| With agent | nvim (35%) \| Claude Code (65%) | Orca-style: agent-first, 2 panes |

In agent mode, the agent pane is the primary actor and also serves as the terminal. No separate shell pane is created.

## Keybindings

### Neovim

| Key | Action |
|---|---|
| `Space` | Leader key |
| `Ctrl+h/j/k/l` | Move between windows |
| `Shift+H/L` | Previous / next tab |
| `Alt+J/K` | Move line up / down |
| `Space+ff` | Find file |
| `Space+fg` | Live grep |

### Herdr

| Key | Action |
|---|---|
| `Ctrl+B` | Prefix |
| `Prefix + c` | New tab |
| `Prefix + v` | Split right |
| `Prefix + -` | Split down |
| `Prefix + q` | Detach |

## Architecture

```
Terminal emulator (any)
  └─ Herdr (persistent workspaces / tabs / panes)
       ├─ Neovim pane      — file tree + editor
       ├─ Terminal pane    — shell
       └─ Agent pane       — Claude Code (with --agent or fan)
```

## Directory structure

```
copse/
├── setup.sh
├── config/
│   ├── herdr/
│   │   └── config.toml     # → ~/.config/herdr/config.toml
│   └── nvim/               # → ~/.config/nvim/
└── bin/
    └── copse               # → ~/.local/bin/copse
```

## License

MIT
