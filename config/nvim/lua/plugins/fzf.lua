return {
  {
    "ibhagwan/fzf-lua",
    dependencies = { "nvim-tree/nvim-web-devicons" },
    keys = {
      { "<leader>ff", "<cmd>FzfLua files<cr>", desc = "Find files" },
      { "<leader>fg", "<cmd>FzfLua live_grep<cr>", desc = "Live grep" },
      { "<leader>fb", "<cmd>FzfLua buffers<cr>", desc = "Buffers" },
      { "<leader>fh", "<cmd>FzfLua help_tags<cr>", desc = "Help tags" },
      { "<leader>fr", "<cmd>FzfLua oldfiles<cr>", desc = "Recent files" },
      { "<leader>fd", "<cmd>FzfLua diagnostics_document<cr>", desc = "Diagnostics" },
    },
    opts = {
      winopts = {
        height = 0.85,
        width = 0.80,
        preview = { layout = "vertical", vertical = "up:40%" },
      },
      files = { fd_opts = "--type f --hidden --exclude .git" },
    },
  },
}
