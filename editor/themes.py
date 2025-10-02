from PyQt6.QtGui import QColor

THEMES = {
    "Sn2 Dark": {
        "base": QColor("#1e1e1e"), "text": QColor("#d4d4d4"),
        "keyword": QColor("#c586c0"), "literal": QColor("#569cd6"),
        "string": QColor("#ce9178"), "number": QColor("#b5cea8"),
        "comment": QColor("#6a9955"),
        "app_window": QColor(53, 53, 53), "app_base": QColor(25, 25, 25),
        "app_highlight": QColor(42, 130, 218)
    },
    "Mariana": {
        "base": QColor("#263238"), "text": QColor("#EEFFFF"),
        "keyword": QColor("#C792EA"), "literal": QColor("#82AAFF"),
        "string": QColor("#C3E88D"), "number": QColor("#F78C6C"),
        "comment": QColor("#546E7A"),
        "app_window": QColor(38, 50, 56), "app_base": QColor(38, 50, 56),
        "app_highlight": QColor(0, 122, 204)
    },
    "Classic Light": {
        "base": QColor("#ffffff"), "text": QColor("#000000"),
        "keyword": QColor("#0000ff"), "literal": QColor("#00008b"),
        "string": QColor("#a31515"), "number": QColor("#098658"),
        "comment": QColor("#008000"),
        "app_window": QColor(240, 240, 240), "app_base": QColor(255, 255, 255), "app_text": QColor("#000000"),
        "app_highlight": QColor(0, 120, 215)
    },
    "Monokai": {
        "base": QColor("#272822"), "text": QColor("#F8F8F2"),
        "keyword": QColor("#F92672"), "literal": QColor("#66D9EF"),
        "string": QColor("#E6DB74"), "number": QColor("#AE81FF"),
        "comment": QColor("#75715E"),
        "app_window": QColor(39, 40, 34), "app_base": QColor(39, 40, 34),
        "app_highlight": QColor(253, 151, 31)
    },
    "Solarized Dark": {
        "base": QColor("#002b36"), "text": QColor("#839496"),
        "keyword": QColor("#859900"), "literal": QColor("#268bd2"),
        "string": QColor("#2aa198"), "number": QColor("#d33682"),
        "comment": QColor("#586e75"),
        "app_window": QColor(0, 43, 54), "app_base": QColor(7, 54, 66),
        "app_highlight": QColor(38, 139, 210)
    },
    "Solarized Light": {
        "base": QColor("#fdf6e3"), "text": QColor("#657b83"),
        "keyword": QColor("#859900"), "literal": QColor("#268bd2"),
        "string": QColor("#2aa198"), "number": QColor("#d33682"),
        "comment": QColor("#93a1a1"),
        "app_window": QColor(238, 232, 213), "app_base": QColor(253, 246, 227), "app_text": QColor("#002b36"),
        "app_highlight": QColor(38, 139, 210)
    },
    "Dracula": {
        "base": QColor("#282a36"), "text": QColor("#f8f8f2"),
        "keyword": QColor("#ff79c6"), "literal": QColor("#bd93f9"),
        "string": QColor("#f1fa8c"), "number": QColor("#bd93f9"),
        "comment": QColor("#6272a4"),
        "app_window": QColor(40, 42, 54), "app_base": QColor(40, 42, 54),
        "app_highlight": QColor(98, 114, 164)
    },
    "Nord": {
        "base": QColor("#2E3440"), "text": QColor("#D8DEE9"),
        "keyword": QColor("#81A1C1"), "literal": QColor("#81A1C1"),
        "string": QColor("#A3BE8C"), "number": QColor("#B48EAD"),
        "comment": QColor("#4C566A"),
        "app_window": QColor(46, 52, 64), "app_base": QColor(46, 52, 64),
        "app_highlight": QColor(129, 161, 193)
    },
    "Gruvbox Dark": {
        "base": QColor("#282828"), "text": QColor("#ebdbb2"),
        "keyword": QColor("#fe8019"), "literal": QColor("#83a598"),
        "string": QColor("#b8bb26"), "number": QColor("#d3869b"),
        "comment": QColor("#928374"),
        "app_window": QColor(40, 40, 40), "app_base": QColor(50, 48, 47),
        "app_highlight": QColor(254, 128, 25)
    },
    "Gruvbox Light": {
        "base": QColor("#fbf1c7"), "text": QColor("#3c3836"),
        "keyword": QColor("#9d0006"), "literal": QColor("#427b58"),
        "string": QColor("#79740e"), "number": QColor("#8f3f71"),
        "comment": QColor("#928374"),
        "app_window": QColor(249, 245, 215), "app_base": QColor(251, 241, 199), "app_text": QColor("#605c5a"),
        "app_highlight": QColor(204, 36, 29)
    },
    "One Dark Pro": {
        "base": QColor("#282c34"), "text": QColor("#abb2bf"),
        "keyword": QColor("#C678DD"), "literal": QColor("#56B6C2"),
        "string": QColor("#98C379"), "number": QColor("#D19A66"),
        "comment": QColor("#5c6370"),
        "app_window": QColor(33, 37, 43), "app_base": QColor(40, 44, 52),
        "app_highlight": QColor(97, 175, 239)
    },
    "Cobalt": {
        "base": QColor("#002240"), "text": QColor("#FFFFFF"),
        "keyword": QColor("#FF9D00"), "literal": QColor("#FF628C"),
        "string": QColor("#3AD900"), "number": QColor("#FF628C"),
        "comment": QColor("#0088FF"),
        "app_window": QColor(0, 34, 64), "app_base": QColor(0, 34, 64),
        "app_highlight": QColor(255, 157, 0)
    },
    "Tomorrow Night": {
        "base": QColor("#1d1f21"), "text": QColor("#c5c8c6"),
        "keyword": QColor("#b294bb"), "literal": QColor("#81a2be"),
        "string": QColor("#b5bd68"), "number": QColor("#de935f"),
        "comment": QColor("#969896"),
        "app_window": QColor(29, 31, 33), "app_base": QColor(29, 31, 33),
        "app_highlight": QColor(129, 162, 190)
    },
    "Tomorrow": {
        "base": QColor("#ffffff"), "text": QColor("#4d4d4c"),
        "keyword": QColor("#8e908c"), "literal": QColor("#3e999f"),
        "string": QColor("#718c00"), "number": QColor("#f5871f"),
        "comment": QColor("#8e908c"),
        "app_window": QColor(240, 240, 240), "app_base": QColor(255, 255, 255), "app_text": QColor("#4d4d4c"),
        "app_highlight": QColor(62, 153, 159)
    },
    "GitHub Dark": {
        "base": QColor("#0d1117"), "text": QColor("#c9d1d9"),
        "keyword": QColor("#ff7b72"), "literal": QColor("#79c0ff"),
        "string": QColor("#a5d6ff"), "number": QColor("#79c0ff"),
        "comment": QColor("#8b949e"),
        "app_window": QColor(13, 17, 23), "app_base": QColor(1, 4, 9),
        "app_highlight": QColor(35, 134, 255)
    },
    "GitHub Light": {
        "base": QColor("#ffffff"), "text": QColor("#24292e"),
        "keyword": QColor("#d73a49"), "literal": QColor("#005cc5"),
        "string": QColor("#032f62"), "number": QColor("#005cc5"),
        "comment": QColor("#6a737d"),
        "app_window": QColor(246, 248, 250), "app_base": QColor(255, 255, 255), "app_text": QColor("#24292e"),
        "app_highlight": QColor(3, 102, 214)
    },
    "Material Darker": {
        "base": QColor("#212121"), "text": QColor("#EEFFFF"),
        "keyword": QColor("#C792EA"), "literal": QColor("#82AAFF"),
        "string": QColor("#C3E88D"), "number": QColor("#F78C6C"),
        "comment": QColor("#546E7A"),
        "app_window": QColor(33, 33, 33), "app_base": QColor(33, 33, 33),
        "app_highlight": QColor(130, 170, 255)
    },
    "Material Lighter": {
        "base": QColor("#FAFAFA"), "text": QColor("#808080"),
        "keyword": QColor("#39ADB5"), "literal": QColor("#39ADB5"),
        "string": QColor("#91B859"), "number": QColor("#F76D47"),
        "comment": QColor("#90A4AE"),
        "app_window": QColor(250, 250, 250), "app_base": QColor(250, 250, 250), "app_text": QColor("#808080"),
        "app_highlight": QColor(57, 173, 181)
    },
    "Ayu Dark": {
        "base": QColor("#0A0E14"), "text": QColor("#B3B1AD"),
        "keyword": QColor("#FF7733"), "literal": QColor("#36A3D9"),
        "string": QColor("#C2D94C"), "number": QColor("#F29E74"),
        "comment": QColor("#5C6773"),
        "app_window": QColor(10, 14, 20), "app_base": QColor(10, 14, 20),
        "app_highlight": QColor(255, 119, 51)
    },
    "Ayu Light": {
        "base": QColor("#FAFAFA"), "text": QColor("#5C6773"),
        "keyword": QColor("#FA8D3E"), "literal": QColor("#36A3D9"),
        "string": QColor("#86B300"), "number": QColor("#F29E74"),
        "comment": QColor("#ABB0B6"),
        "app_window": QColor(250, 250, 250), "app_base": QColor(250, 250, 250), "app_text": QColor("#5C6773"),
        "app_highlight": QColor(250, 141, 62)
    },
    "Oceanic Next": {
        "base": QColor("#1B2B34"), "text": QColor("#CDD3DE"),
        "keyword": QColor("#C594C5"), "literal": QColor("#6699CC"),
        "string": QColor("#99C794"), "number": QColor("#F99157"),
        "comment": QColor("#65737E"),
        "app_window": QColor(27, 43, 52), "app_base": QColor(27, 43, 52),
        "app_highlight": QColor(102, 153, 204)
    },
    "Zenburn": {
        "base": QColor("#3f3f3f"), "text": QColor("#dcdccc"),
        "keyword": QColor("#f0dfaf"), "literal": QColor("#efef8f"),
        "string": QColor("#cc9393"), "number": QColor("#8cd0d3"),
        "comment": QColor("#7f9f7f"),
        "app_window": QColor(63, 63, 63), "app_base": QColor(63, 63, 63),
        "app_highlight": QColor(240, 223, 175)
    }
}

DEFAULT_THEME = "Sn2 Dark"