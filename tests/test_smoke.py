#!/usr/bin/env python3
"""冒烟测试：不依赖 pytest，直接 `python tests/test_smoke.py` 就能跑。

设计原则（和 selftest.py 的分工）：
  - selftest.py 测「能力」：20 项功能断言，属于开发者改代码时的回归网。
  - 本文件测「契约」：一个陌生人按 README 操作时，最少应该得到什么。
    所以这里的断言都很粗——粗到即使你大改实现，只要没破坏对外承诺，它们就该继续通过。

覆盖：
  T1  CLI 能跑起来（--list-themes 退出码 0，且至少 4 套主题）
  T2  样例转换成功，产出文件非空
  T3  产物不含公众号禁用项（<style> / class= / id= / <h1> / <script>）
  T4  产物里样式是 inline 的（存在 style=" 属性）
  T5  合规检查器对产物无硬错误
  T6  --fragment 只出正文片段（不含预览外壳）
  T7  批量转换能生成索引页
  T8  坏 HTML 会被检查器抓到（反向断言，防止检查器变成永远通过的摆设）

用法：
    python tests/test_smoke.py          # 全部跑
    python tests/test_smoke.py -v       # 打印每条断言细节
"""

from __future__ import annotations

import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCRIPTS = ROOT / "scripts"
CONVERT = SCRIPTS / "convert_to_wechat.py"
CHECK = SCRIPTS / "wechat_check.py"
SAMPLE = ROOT / "examples" / "sample_article.md"

VERBOSE = "-v" in sys.argv
results: list[tuple[str, bool, str]] = []


def record(name: str, ok: bool, detail: str = "") -> None:
    results.append((name, ok, detail))
    mark = "PASS" if ok else "FAIL"
    print(f"  [{mark}] {name}" + (f" —— {detail}" if detail and (VERBOSE or not ok) else ""))


def run(args: list[str], timeout: int = 120) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, *args],
        cwd=str(ROOT),
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        timeout=timeout,
    )


def main() -> int:
    print("=" * 68)
    print("wechat-publisher 冒烟测试（契约级）")
    print(f"解释器：{sys.executable}")
    print(f"版本  ：{sys.version.split()[0]}")
    print(f"仓库  ：{ROOT}")
    print("=" * 68)

    if not SAMPLE.exists():
        print(f"❌ 样例文件不存在：{SAMPLE}")
        return 2

    workdir = Path(tempfile.mkdtemp(prefix="wxp-smoke-"))
    try:
        # ---------------- T1 CLI 可用 ----------------
        p = run([str(CONVERT), "--list-themes"])
        # 实际输出形如：可用主题：default / accent / warm / minimal
        m = re.search(r"可用主题[：:]\s*(.+)", p.stdout or "")
        names = [t.strip() for t in re.split(r"[/,、]", m.group(1))] if m else []
        names = [n for n in names if n]
        record(
            "T1 CLI 可运行且主题 >= 4",
            p.returncode == 0 and len(names) >= 4,
            f"exit={p.returncode}, 解析到主题 {len(names)} 个: {'/'.join(names)}",
        )

        # ---------------- T2 样例转换 ----------------
        out = workdir / "sample_output.html"
        p = run([str(CONVERT), str(SAMPLE), str(out)])
        ok2 = p.returncode == 0 and out.exists() and out.stat().st_size > 1000
        record("T2 样例转换产出非空 HTML", ok2, f"exit={p.returncode}, size={out.stat().st_size if out.exists() else 0}")
        if not ok2:
            print("\n转换失败，stderr 摘要：")
            print((p.stderr or p.stdout)[-800:])
            return 1

        html = out.read_text(encoding="utf-8", errors="replace")

        # ---------------- T3 禁用项 ----------------
        forbidden = {
            "<style": r"<style",
            "<script": r"<script",
            "<h1": r"<h1\b",
            "class=": r"\bclass\s*=",
            "id=": r"\bid\s*=",
        }
        found = [name for name, pat in forbidden.items() if re.search(pat, html, re.I)]
        record("T3 产物无禁用标签/属性", not found, ("命中: " + ", ".join(found)) if found else "五项均未出现")

        # ---------------- T4 样式内联 ----------------
        inline_cnt = len(re.findall(r'\bstyle\s*=\s*"', html))
        record("T4 样式以 inline style 存在", inline_cnt >= 10, f"style= 出现 {inline_cnt} 次")

        # ---------------- T5 合规检查器 ----------------
        p = run([str(CHECK), str(out)])
        combined = (p.stdout or "") + (p.stderr or "")
        no_hard_error = ("[错误]" not in combined) and p.returncode == 0
        record("T5 合规检查器对产物无硬错误", no_hard_error, f"exit={p.returncode}")

        # ---------------- T6 fragment ----------------
        frag = workdir / "frag.html"
        p = run([str(CONVERT), str(SAMPLE), str(frag), "--fragment"])
        frag_txt = frag.read_text(encoding="utf-8", errors="replace") if frag.exists() else ""
        record(
            "T6 --fragment 只出正文片段",
            p.returncode == 0 and "<!DOCTYPE" not in frag_txt.upper() and len(frag_txt) > 100,
            f"exit={p.returncode}, size={len(frag_txt)}",
        )

        # ---------------- T7 批量 ----------------
        batch_src = workdir / "articles"
        batch_src.mkdir()
        shutil.copy(SAMPLE, batch_src / "a.md")
        shutil.copy(SAMPLE, batch_src / "b.md")
        batch_out = workdir / "batch_out"
        p = run([str(CONVERT), str(batch_src), str(batch_out), "--batch"])
        produced = list(batch_out.glob("*.html")) if batch_out.exists() else []
        record(
            "T7 批量转换 + 索引页",
            p.returncode == 0 and len(produced) >= 3,  # 2 篇 + index.html
            f"exit={p.returncode}, 产出 {len(produced)} 个 html",
        )

        # ---------------- T8 检查器能抓到坏 HTML（反向断言）----------------
        bad = workdir / "bad.html"
        bad.write_text(
            '<html><head><style>p{color:red}</style></head>'
            '<body><h1>标题</h1><div class="x">正文</div>'
            '<script>alert(1)</script></body></html>',
            encoding="utf-8",
        )
        p = run([str(CHECK), str(bad)])
        combined = (p.stdout or "") + (p.stderr or "")
        caught = ("[错误]" in combined) or p.returncode != 0
        record("T8 检查器能抓到故意写坏的 HTML", caught, f"exit={p.returncode}（此处 exit!=0 或报 [错误] 才算对）")

    finally:
        shutil.rmtree(workdir, ignore_errors=True)

    passed = sum(1 for _, ok, _ in results if ok)
    total = len(results)
    print("-" * 68)
    print(f"冒烟测试结果：{passed}/{total} 通过")
    if passed != total:
        print("失败项：")
        for name, ok, detail in results:
            if not ok:
                print(f"  - {name}（{detail}）")
    print("-" * 68)
    return 0 if passed == total else 1


if __name__ == "__main__":
    sys.exit(main())
