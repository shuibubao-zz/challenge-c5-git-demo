# 贡献指南

先说清楚：这个项目**接受任何规模的贡献**，包括"只提一个 Issue 说文档看不懂"。文档看不懂是文档的问题，不是你的问题。

---

## 一、30 秒判断你该做什么

| 你想做的事 | 去哪 |
|---|---|
| 报告 bug（转换结果不对、崩溃、样式丢了） | [开 Bug Issue](.github/ISSUE_TEMPLATE/bug_report.md)（请附最小复现输入） |
| 想要新功能（新主题、新语法、新输出格式） | [开 Feature Issue](.github/ISSUE_TEMPLATE/feature_request.md) |
| 改了代码想合并 | 提 PR，见下文第四节 |
| 只是想说"这个规则我不同意" | 开 Issue，**带上你的实测证据**，这个项目的规则是按证据级别说话的 |

> ⚠️ 提交前请先看 [`ATTRIBUTION.md`](./ATTRIBUTION.md) 的分级约定：这个项目里"我觉得公众号会这样"和"官方文档明这样"是两种不同强度的主张，Issue 里请说明你属于哪种。

---

## 二、本地开发

```bash
git clone https://github.com/<your-name>/wechat-publisher.git
cd wechat-publisher

python scripts/selftest.py            # 20 项能力自检（干净环境应为 18/20，见 README）
python tests/test_smoke.py            # 冒烟测试，两种环境都应通过
```

**没有 `requirements.txt`，这是故意的。** 项目只用标准库，可选依赖见 README「技术栈」。

如果你要改 `.docx` 或公式相关代码，本地装一下可选依赖便于测试：

```bash
pip install python-docx matplotlib    # 仅测试用，项目运行时不强依赖
```

### 改动前请先跑一遍基线

```bash
python scripts/selftest.py > /tmp/before.txt 2>&1
# 改代码
python scripts/selftest.py > /tmp/after.txt 2>&1
diff /tmp/before.txt /tmp/after.txt
```

**没有变化**是好事；**通过了项目数变多**是好事；**某项从 ✅ 变 ❌** 说明你引入了退化。

---

## 三、动手示例：加一套新主题（最典型的第一个 PR）

假设你想要一套「墨绿」主题。

**Step 1** — 在 `scripts/themes.py` 的 `THEMES` 字典里加一个键（只写和 `BASE` 不同的值，没写的自动继承）：

```python
"forest": {
    "h2": (
        "font-size: 22px; font-weight: bold; line-height: 1.6; "
        "color: #1b5e20; margin: 26px 0 12px 0;"
    ),
    "h3": (
        "font-size: 18px; font-weight: bold; line-height: 1.6; "
        "color: #1b5e20; margin: 18px 0 8px 0;"
    ),
    "blockquote": (
        "background-color: #f1f8e9; color: #555; padding: 10px 15px; "
        "margin: 14px 0; border-left: 4px solid #2e7d32;"
    ),
    "a": "color: #2e7d32; text-decoration: underline;",
},
```

**Step 2** — 不需要改命令行。`--theme` 的取值来自 `themes.py` 里的 `THEME_NAMES = list(THEMES.keys())`，
所以加完键就能用：

```bash
python scripts/convert_to_wechat.py --list-themes     # 应能看到 forest
```

**Step 3** — 跑自检。`selftest.py` 会遍历**所有**主题做合规检查（禁用标签、`class`/`id`、外部资源），
所以新主题如果用了 `height` / `position` / `flex` 之类的属性，会在这一步被抓出来。

```bash
python scripts/selftest.py
python scripts/convert_to_wechat.py examples/sample_article.md out.html --theme forest
```

**Step 4** — 在 `references/wechat_styles.md` 的「主题差异」表里补一行，在 `CHANGELOG.md` 的
`[Unreleased]` 下写一条。

**Step 5** — 提 PR，并在描述里附上 `out.html` 的截图（浏览器打开截一张，手机宽度 375px 最好）。

> 只用一套配色、不想提 PR？用 `--theme-file my.json` 传一个 JSON 覆盖任意样式键，不需要改代码。
> 键名见 `references/wechat_styles.md`。

---

## 四、PR 约定

### 提交信息

用「类型: 一句话」的格式，类型取 `feat` / `fix` / `docs` / `test` / `refactor` / `chore`：

```
feat: 新增 forest 主题
fix: 代码块里的 $ 被误判为公式
docs: 补充粘贴后排版丢失的排查顺序
```

### PR 之前自查（复制到 PR 描述里打勾）

```
□ python scripts/selftest.py 通过项数没有减少（干净环境基线 18/20）
□ python tests/test_smoke.py 通过
□ 改了输出格式的地方，附了 before/after 的 HTML 片段对比
□ 新增的规则/数字，标了依据级别（L1 官方 / L3 实测 / L4 旁证）
□ 不需要新增第三方依赖（如果需要，请在 PR 里说明为什么不能降级实现）
```

### 会被拒绝的 PR（提前说清楚，省得你白写）

| 情况 | 原因 |
|---|---|
| 引入 `pip install` 式的必装依赖 | 与"零依赖也能跑"的主承诺冲突 |
| 在运行时自动安装依赖 | 未经允许修改用户环境 |
| 新增"公众号一定会剥离 X"这类断言但拿不出依据 | 本项目按证据级别说话，见 ATTRIBUTION |
| 重排整个文件的格式（纯格式化 PR） | 会让 `git blame` 失效，请单独提且先说明 |
| 把输出改成 `class` 方案"更优雅" | 公众号会剥掉 `class`，这是本项目的存在理由 |

---

## 五、文档贡献同样重要

以下这些改动**不需要写一行代码**，但价值很高：

- `references/troubleshooting.md` 补一条你实际遇到的粘贴失败现象和解法
- 在 Issue 里报告"某条规则我实测不成立"（带截图或复现步骤）
- 修正 README 里任何与 `--help` 输出不一致的地方——**文档与代码不符时，文档错了**

---

## 六、行为准则

- 对事不对人。指出问题时给复现步骤，而不是给结论。
- **不许伪造实测**。写"我测过"就必须真的测过；没测过就写"我没测过，只是推测"。这个项目所有的信任都建立在这一条上。
- 新手问题不嘲笑。你曾经也不知道 `<h1>` 会被公众号改写。

---

有问题？开 Issue，标题写清楚就行，不用纠结格式。
