"""把 README.md 渲染成 GitHub 风格的静态 HTML，用于生成截图与本地预览。

用法（需要一个装了 markdown 库的解释器）：
    python tools/render_readme.py            # 输出到 docs/readme_preview.html

设计说明：
  - CSS 是 GitHub 浅色主题的近似值（字体、边框、代码块底色），不追求像素级一致。
  - 徽章图片指向 shields.io，无网络时会显示 alt 文本——这比"截图里没有徽章"更诚实。
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
README = ROOT / "README.md"
OUT = ROOT / "docs" / "readme_preview.html"

CSS = """
:root { color-scheme: light; }
* { box-sizing: border-box; }
body {
  margin: 0; padding: 32px 40px 48px;
  font-family: -apple-system, "Segoe UI", "Microsoft YaHei", Helvetica, Arial, sans-serif;
  font-size: 16px; line-height: 1.6; color: #1f2328; background: #fff;
  max-width: 980px;
}
h1 { font-size: 2em; font-weight: 600; padding-bottom: .3em; border-bottom: 1px solid #d1d9e0; margin: 24px 0 16px; }
h2 { font-size: 1.5em; font-weight: 600; padding-bottom: .3em; border-bottom: 1px solid #d1d9e0; margin: 24px 0 16px; }
h3 { font-size: 1.25em; font-weight: 600; margin: 24px 0 16px; }
p { margin: 0 0 16px; }
a { color: #0969da; text-decoration: none; }
a:hover { text-decoration: underline; }
code { background: #eff1f3; padding: .2em .4em; border-radius: 6px; font-size: 85%;
       font-family: ui-monospace, SFMono-Regular, "Segoe UI Mono", Consolas, monospace; }
pre { background: #f6f8fa; padding: 16px; border-radius: 6px; overflow: auto; margin: 0 0 16px; }
pre code { background: none; padding: 0; font-size: 85%; }
table { border-collapse: collapse; margin: 0 0 16px; }
th, td { border: 1px solid #d1d9e0; padding: 6px 13px; }
th { background: #f6f8fa; font-weight: 600; }
tr:nth-child(2n) td { background: #f6f8fa; }
blockquote { margin: 0 0 16px; padding: 0 1em; color: #59636e; border-left: .25em solid #d1d9e0; }
img { max-width: 100%; vertical-align: middle; }
hr { border: 0; border-top: 1px solid #d1d9e0; margin: 24px 0; }
ul, ol { padding-left: 2em; margin: 0 0 16px; }
li + li { margin-top: .25em; }
"""


def main() -> int:
    try:
        import markdown  # noqa: F401
    except ImportError:
        print("需要 markdown 库：pip install markdown")
        return 1

    import markdown

    text = README.read_text(encoding="utf-8")
    body = markdown.markdown(
        text,
        extensions=["tables", "fenced_code", "toc", "sane_lists", "md_in_html"],
        output_format="html5",
    )
    html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<title>README · wechat-publisher</title>
<style>{CSS}</style>
</head>
<body>
{body}
</body>
</html>
"""
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(html, encoding="utf-8")
    print(f"已生成：{OUT}")
    print("截图命令（Windows）：")
    print(
        '  msedge --headless=new --disable-gpu --hide-scrollbars '
        f'--window-size=1000,2600 --screenshot=docs/images/readme-preview.png "file:///{OUT.as_posix()}"'
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
