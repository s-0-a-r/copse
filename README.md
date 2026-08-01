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

## Scope

copse manages the lifecycle of parallel AI agent worktrees: provisioning, observation, and cleanup.
It deliberately stops at notifying humans; it does not orchestrate agents autonomously.

| Phase | Commands |
|---|---|
| Provision | `copse`, `copse new`, `copse worktree`, `copse fan` |
| Observe | `copse ls`, `copse watch` |
| Act | `copse diff`, `copse clean` |

## Usage

```bash
copse                    # pick from ~/projects (includes worktrees) via fzf
copse .                  # open current directory
copse ~/my-app           # open a project
copse new ~/my-app       # force-create a new workspace for project
```

### Agent Development

```bash
# Open a branch as an isolated worktree workspace
copse worktree feature/my-branch --project ~/my-app

# Fan out N parallel agents on the same task
copse fan "Add OAuth2 login" --count 3
copse fan "Refactor auth module" --count 2 --project ~/my-app

# Observe fan worktrees and agent status
copse ls
copse watch

# Compare fan worktree outputs
copse diff               # select slots interactively via fzf
copse diff 1 2           # compare slot 1 vs slot 2
copse diff 1             # compare default branch vs slot 1

# Clean up idle fan worktrees
copse clean              # remove idle worktrees (interactive confirmation)
copse clean --force      # remove all fan worktrees regardless of status
```

The `fan` command creates N isolated git worktrees, starts Claude Code + broot in each, and injects the task prompt automatically. Agents work in parallel; compare results with `git diff`.

To open a file from broot in a new herdr tab, press `Enter` — this runs `copse-open` which creates a new tab with nvim.

> **Note:** copse requires the herdr TUI to be running before use. Start herdr first, then run copse from any terminal.

## Layout

| Tab | Panes | Purpose |
|---|---|---|
| Tab 1 | Claude Code (80%) \| broot (20%) | Agent + file tree |
| Tab 2 (on demand) | nvim (100%) | File viewing — opens automatically from broot |

Select a file in broot and press `Enter` to open it in nvim on Tab 2. Close Tab 2 with `:q`.

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
       ├─ Tab 1
       │    ├─ Claude Code pane  — agent (large, ~80%)
       │    └─ broot pane         — file tree (~20%)
       └─ Tab 2 (on demand)
            └─ nvim pane         — file viewer (opened from broot)
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
