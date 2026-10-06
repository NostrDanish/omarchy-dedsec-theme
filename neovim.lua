return {
  {
    "bjarneo/aether.nvim",
    branch = "v3",
    name = "aether",
    priority = 1000,
    opts = {
      colors = {
        bg = "#0a0a0a",
        dark_bg = "#050505",
        darker_bg = "#000000",
        lighter_bg = "#161616",

        fg = "#f2f2f2",
        dark_fg = "#6e6e6e",
        light_fg = "#c8c8c8",
        bright_fg = "#ffffff",
        muted = "#6e6e6e",

        red = "#EC008C",
        yellow = "#FDF001",
        orange = "#ff9900",
        green = "#7dff3a",
        cyan = "#00AEEF",
        blue = "#00AEEF",
        magenta = "#EC008C",
        brown = "#8a6b46",

        bright_red = "#ff33a8",
        bright_yellow = "#fff44f",
        bright_green = "#a6ff6a",
        bright_cyan = "#5cd6ff",
        bright_blue = "#33c4ff",
        bright_magenta = "#ff4db8",

        accent = "#FDF001",
        cursor = "#FDF001",
        foreground = "#f2f2f2",
        background = "#0a0a0a",
        selection = "#1f1f14",
        selection_foreground = "#0a0a0a",
        selection_background = "#FDF001",
      },
    },
  },
  {
    "LazyVim/LazyVim",
    opts = {
      colorscheme = "aether",
    },
  },
}
