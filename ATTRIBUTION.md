# ATTRIBUTION.md — 拿来说明

> 这个仓库里**没有一段代码是"看起来像"就抄进来的**。凡是借来的，下面都写了：从哪来、改了什么、为什么改。
>
> 依据分级（下文沿用这套标记）：
> **L1** = 微信官方接口文档原文（可联网复核）｜**L2** = 官方社区帖（需登录，未二次核验）｜
> **L3** = 本项目实测（脚本可复跑）｜**L4** = 第三方工具/博客（仅旁证，不作依据）

---

## 一、基座：WorkBuddy / Claude 官方 starter kit

`scripts/convert_to_wechat.py`、`references/wechat_restrictions.md`、`references/wechat_styles.md`
的**第一版**来自挑战提供的 `c4b-wechat-publisher-starter`（WorkBuddy skill-creator 生态的官方起步模板）。
starter 的原版输出我留了一份基线（`evidence/baseline_starter_output.html`，C4B 交付包内），用来量化"我改了什么"。

| starter 原样 | 我改成了 | 为什么 |
|---|---|---|
| 只在有 `markdown` 库时可用 | 加 `md_lite.py` 零依赖引擎，缺失时自动降级 | 换台机器就装不上库的人占多数；"能跑"不该依赖运气 |
| 首次运行静默 `pip install ... --break-system-packages` | **删掉**，改为"能降级就降级，不能降级给可操作提示" | 未经允许修改用户环境不是便利，是替用户做决定 |
| 用 `nl2br` 扩展 | 去掉，改在渲染层统一处理 | `nl2br` 让两条解析路径永远对不齐（详见 AAR） |
| 无主题、无 callout、无目录、无自检 | 4 套主题 / 5 种 callout / 自动目录 / 合规自检 | starter 的 `What This Starter Kit Does NOT Do (Yet)` 一节列出的空白 |
| `>` 折叠标量写 description | 改成 `|` 字面标量 | 官方打包器校验报错：`Description cannot contain angle brackets` |
| 无测试 | `selftest.py` 20 项 + `tests/test_smoke.py` | 没有断言就没有"等价"可言 |

**License 兼容性**：starter 随挑战资料分发，本项目在其基础上重写并采用 MIT。若上游对 starter 另有授权要求，以官方说明为准，本仓库的 MIT 仅覆盖我新写的部分。

---

## 二、公众号限制规则：出处逐条标注

这部分是本项目最容易被质疑的地方——**说"公众号会剥离 class"很容易，证明它很难**。
完整版见 [`docs/official-evidence.md`](./docs/official-evidence.md)（含逐字原文摘录、4 处官方口径冲突的裁定、诚实清单）。
核验脚本 [`tests/verify_official_quotes.py`](./tests/verify_official_quotes.py) 可联网复核这些原文是否还在页面上。

### 有官方明文依据的（L1）

| 结论 | 官方原文（逐字） | 出处 |
|---|---|---|
| `<script>` 被去除，所以 MathJax/KaTeX 一定失效 | "此处会去除JS" | [新增草稿接口](https://developers.weixin.qq.com/doc/service/api/draftbox/draftmanage/api_draft_add.html) `content` 字段 |
| 外部图片链接会被过滤，所以图片必须内嵌 | "外部图片url将被过滤" | 同上 |
| 正文有字数/体积上限 | "必须少于2万字符，小于1M" | 同上 |
| 图片格式仅 png/jpeg/jpg/gif，**不含 svg** | "图片（image）: 10M，支持bmp/png/jpeg/jpg/gif格式" | [上传永久素材](https://developers.weixin.qq.com/doc/service/api/material/permanent/api_addmaterial) |
| 单张图片 10MB（另有 2MB 说法，见冲突） | "文件大小限制：图片2MB/视频10MB" | [新增临时素材](https://developers.weixin.qq.com/doc/service/api/material/temporary/api_uploadtempmedia) |

> **一处必须说清的边界**：以上出自**服务端接口文档**，证明的是"通过 API 提交图文时平台怎么处理"，
> 与"编辑器里 Ctrl+V 粘贴 HTML 会怎样"**不是同一机制**。所以它只能作为强旁证，不能当作编辑器白名单。

### 查不到官方出处、明确标注为"未找到"的（L3 实测）

`<style>`/`class` 被剥离、`<h1>` 被征用、`<div>` 渲染不稳、`<pre>` 被压成一行——这 4 条
**我检索了开发者文档全站，没有找到任何官方条文**（微信从未公开编辑器 HTML 白名单）。
处理方式：在 `references/wechat_restrictions.md` 里逐条标明"未找到官方出处 + 实测"，并给出读者自己验证的步骤，
**不伪造出处**。

### 被自己证伪、已删除的一条

v1 曾写"单篇不超过 100 张图片"。**这个数字没有任何官方来源**，属我把印象当成了事实。
已从文档与检查器中删除，并在 `docs/official-evidence.md` 公开交代勘误；`tests/verify_official_quotes.py`
里加了回归护栏，该短语今后若不带"已删/查无出处"标记重新出现，脚本直接报错。

---

## 三、第三方思路与代码

| 来源 | 借了什么 | 怎么改的 | 级别 |
|---|---|---|---|
| `doocs/md`、`mdnice` 等 Markdown→公众号转换项目 | 「样式全部 inline、禁用 class」的思路 | 未复制代码，只借鉴思路；实现独立（本项目用 `<section>`，未沿用其模板） | L4 旁证 |
| matplotlib `mathtext` 官方文档 | 公式渲染方案（不需要本机装 LaTeX） | 直接调用其 API；**白底深字**是为公众号深色模式改的（原方案透明底在深色模式会隐形） | 官方文档 |
| Python 官方文档 `argparse` / `pathlib` / `base64` | CLI 与路径处理 | 标准库用法，未改写 | 官方文档 |
| `markdown`（Python-Markdown）+ `beautifulsoup4` | 可选解析路径 | 只作为**可替换引擎**，且要求与自研引擎产出字节一致（selftest 有断言） | 各自项目 License |
| Claude / WorkBuddy skill-creator | 技能目录约定（`SKILL.md` + `scripts/` + `references/` + `assets/`） | 遵循其约定，`SKILL.md` frontmatter 保留 `agent_created: true` | 官方文档 |

### 明确**没有**借用、但常被误认为同源的东西

- **微信官方 HTML 白名单**：不存在公开版本。任何声称"这就是官方白名单"的清单都不可信，包括本仓库的规则表——本仓库的每一条都标了依据级别，请你按级别自行判断。
- **公众号排版模板的 CSS 数值**：`references/wechat_styles.md` 的取值是我自己调的（正文 16px / 行高 1.75 / 段间距 12px / 图片 `max-width:100%` 等），不是从某个模板抄的。审美类选择无对错，欢迎改。

---

## 四、图标与素材

- `examples/img.png`：1×1 像素测试图，本项目自建，无版权问题。
- README 徽章：shields.io 动态徽章，文本自拟。
- 示意图（`docs/images/`）：用 matplotlib 由脚本生成，脚本随仓库提供，字体为系统微软雅黑（仅用于本地渲染，未打包字体文件）。

---

## 五、如果你认为这里漏了谁

开 Issue 告诉我具体是哪一段代码 / 哪一条规则，我会核对后补进本文件。
**拿来说明宁多勿少**——漏标的代价远大于多写一行。
