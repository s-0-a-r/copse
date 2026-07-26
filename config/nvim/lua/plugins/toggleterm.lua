return {
  {
    "folke/snacks.nvim",
    priority = 1000,
    lazy = false,
    opts = {
      terminal = {},
      dashboard = {
        enabled = not vim.g.is_ide,
        preset = {
          header = [[
███╗   ██╗███████╗ ██████╗ ██╗   ██╗██╗███╗   ███╗
████╗  ██║██╔════╝██╔═══██╗██║   ██║██║████╗ ████║
██╔██╗ ██║█████╗  ██║   ██║██║   ██║██║██╔████╔██║
██║╚██╗██║██╔══╝  ██║   ██║╚██╗ ██╔╝██║██║╚██╔╝██║
██║ ╚████║███████╗╚██████╔╝ ╚████╔╝ ██║██║ ╚═╝ ██║
╚═╝  ╚═══╝╚══════╝ ╚═════╝   ╚═══╝  ╚═╝╚═╝     ╚═╝]],
          keys = {
            { icon = " ", key = "f", desc = "Find File", action = ":FzfLua files" },
            { icon = " ", key = "r", desc = "Recent Files", action = ":FzfLua oldfiles" },
            { icon = " ", key = "g", desc = "Find Text", action = ":FzfLua live_grep" },
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
      -- :q/:wq on last file buffer → :bd instead of quit (triggers BufDelete → dashboard)
      local function is_last_file_buf()
        local bufs = vim.tbl_filter(function(b)
          return vim.bo[b].buflisted and vim.bo[b].buftype == ""
        end, vim.api.nvim_list_bufs())
        return #bufs <= 1 and vim.bo.buflisted and vim.bo.buftype == ""
      end

      local function ide_close_buf(bang)
        local bufnr = vim.api.nvim_get_current_buf()
        local bufs = vim.tbl_filter(function(b)
          return b ~= bufnr and vim.api.nvim_buf_is_valid(b) and vim.bo[b].buflisted and vim.bo[b].buftype == ""
        end, vim.api.nvim_list_bufs())
        if #bufs > 0 then
          vim.cmd("buffer " .. bufs[#bufs])
        else
          vim.cmd("enew")
        end
        vim.cmd("bdelete" .. (bang and "!" or "") .. " " .. bufnr)
        if #bufs == 0 then
          Snacks.dashboard.open({ buf = 0, win = 0 })
        end
      end

      vim.api.nvim_create_user_command("SmartQ", function(o)
        if not vim.g.is_ide then
          vim.cmd("quit" .. (o.bang and "!" or ""))
        else
          ide_close_buf(o.bang)
        end
      end, { bang = true })

      vim.api.nvim_create_user_command("SmartWQ", function(o)
        vim.cmd("write")
        if not vim.g.is_ide then
          vim.cmd("quit" .. (o.bang and "!" or ""))
        else
          ide_close_buf(o.bang)
        end
      end, { bang = true })

      vim.cmd([[cnoreabbrev <expr> q getcmdtype() == ':' && getcmdline() ==# 'q' ? 'SmartQ' : 'q']])
      vim.cmd([[cnoreabbrev <expr> wq getcmdtype() == ':' && getcmdline() ==# 'wq' ? 'SmartWQ' : 'wq']])
    end,
  },
}
