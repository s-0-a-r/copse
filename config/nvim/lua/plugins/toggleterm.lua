local copse_header = [[
 ██████╗ ██████╗ ██████╗ ███████╗███████╗
██╔════╝██╔═══██╗██╔══██╗██╔════╝██╔════╝
██║     ██║   ██║██████╔╝███████╗█████╗
██║     ██║   ██║██╔═══╝ ╚════██║██╔══╝
╚██████╗╚██████╔╝██║     ███████║███████╗
 ╚═════╝ ╚═════╝ ╚═╝     ╚══════╝╚══════╝]]

local neovim_header = [[
███╗   ██╗███████╗ ██████╗ ██╗   ██╗██╗███╗   ███╗
████╗  ██║██╔════╝██╔═══██╗██║   ██║██║████╗ ████║
██╔██╗ ██║█████╗  ██║   ██║██║   ██║██║██╔████╔██║
██║╚██╗██║██╔══╝  ██║   ██║╚██╗ ██╔╝██║██║╚██╔╝██║
██║ ╚████║███████╗╚██████╔╝ ╚████╔╝ ██║██║ ╚═╝ ██║
╚═╝  ╚═══╝╚══════╝ ╚═════╝   ╚═══╝  ╚═╝╚═╝     ╚═╝]]

return {
  {
    "folke/snacks.nvim",
    priority = 1000,
    lazy = false,
    opts = {
      terminal = {},
      dashboard = {
        enabled = true,
        preset = {
          header = vim.g.copse_nvim and copse_header or neovim_header,
          keys = {
            { icon = " ", key = "f", desc = "Find File", action = function() require("fzf-lua").files() end },
            { icon = " ", key = "r", desc = "Recent Files", action = function() require("fzf-lua").oldfiles() end },
            { icon = " ", key = "g", desc = "Find Text", action = function() require("fzf-lua").live_grep() end },
            { icon = " ", key = "q", desc = "Quit", action = ":qa" },
          },
        },
      },
    },
    -- Terminal panes are herdr panes (split by bin/ide on startup).
    -- Use herdr keybindings (prefix+v, prefix+-, etc.) to manage terminals.
    keys = {},
    config = function(_, opts)
      require("snacks").setup(opts)
    end,
  },
}
