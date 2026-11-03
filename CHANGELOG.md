# Changelog

本文件记录本项目的版本演进。格式参考 [Keep a Changelog](https://keepachangelog.com/zh-CN/1.1.0/)，
版本号遵循 [语义化版本](https://semver.org/lang/zh-CN/)。

> 说明：本项目先以「个人 AI 技能」形态存在（C4B），后仓库化（C5）。
> 因此 v1.x 的日期对应技能迭代，v1.3.0 是仓库化这一版。

## [1.3.0] — 2026-11-03

**仓库化：从"我电脑上的技能"变成"别人能用的项目"。**

### Added
- `README.md` 重写为完整项目说明（解决什么问题 / 快速开始 / 示例 / 项目结构 / 技术栈 / 质量保证 / 贡献）
- `LICENSE`（MIT）、`.gitignore`、`CONTRIBUTING.md`、本 CHANGELOG
- `AI_LOG.md`（AI 使用日志，含手写部分的反向举证与 5 次返工记录）
- `ATTRIBUTION.md`（拿来说明，按 L1–L4 标注每条规则的依据级别）
- `docs/architecture.md`（管线图：每一步的输入输出与失败路径）
- `docs/AAR.md`（复盘：这次仓库化做错了什么）
- `docs/official-evidence.md`（公众号限制规则的官方原文逐字摘录 + 4 处口径冲突裁定）
- `tests/test_smoke.py`（冒烟测试，不依赖 pytest）
- `tests/verify_official_quotes.py`（联网复核官方原文 + "100 张"断言回归护栏）
- `.github/workflows/ci.yml`（Windows / macOS / Linux × Python 3.9 / 3.11 / 3.13）
- `.github/ISSUE_TEMPLATE/`（bug / feature 模板）、`.github/PULL_REQUEST_TEMPLATE.md`
- `examples/sample_output.html`、`examples/sample_report.json` 作为可对照的真实产物

### Fixed
- **`tests/verify_official_quotes.py` 的假阴性**：官方文档站返回 gzip 压缩体，旧版直接 `decode("utf-8","ignore")`
  得到乱码，导致 10 条原文全部"找不到"。补上 gzip/deflate 解压后 10/10 全部复核通过。
  （这个 bug 在 C4B 阶段没暴露，因为当时用的是一次性脚本；仓库化后每次 CI 都跑才现形。）
- `docs/official-evidence.md` 里"100 张"勘误行的表述，加上"已删"标记，使回归护栏能正确区分
  "解释性提及"与"重新主张"。

### Changed
- 样例转换重新生成：补齐 `examples/img.png`，输出不再带「图片未找到」告警
- README 的「示例」段由**真实样例文件内容**替换初稿中凭印象写的假想文章

## [1.2.0] — 2026-10-07

**v2 加固轮：把"我觉得"换成"有出处"。**

### Added
- `references/` 每条规则标注依据级别（L1 官方明文 / L2 社区帖 / L3 实测 / L4 旁证）
- 3 张基于真实数据的示意图（流水线、7 坑速查表、依据分布）
- 官方原文核验脚本 + "100 张"回归护栏

### Fixed
- 删除「单篇不超过 100 张图片」——查无任何官方出处，属写作时把印象当事实
- 自检口径改为**双环境对照实验**（同一解释器，唯一变量=依赖是否可见）：满依赖 20/20、干净环境 18/20

### Removed
- starter 的首次运行静默 `pip install --break-system-packages`

## [1.1.0] — 2026-10-07

### Added
- `scripts/math_render.py`：LaTeX → PNG（matplotlib mathtext，不需要装 LaTeX）
- `md_lite.py` 支持 `$…$` / `$$…$$`；`--math auto|on|off`
- 代码区内的 `$` 不参与公式解析（避免 `$PATH`、`$5` 被误伤）
- selftest 从 16 项扩到 20 项

### Fixed
- 公式图由**透明底**改为**白底深字**——透明底在公众号深色模式下黑字隐形
- 自家合规检查器抓到自家输出：公式 `<img>` 上写了违规的 `height:auto`，已删除

## [1.0.0] — 2026-10-06

首个可用版本（C4B 交付版）。

### Added
- `scripts/convert_to_wechat.py`：Markdown / Word → 公众号 HTML 主流程
- `scripts/themes.py`：4 套主题（default / accent / warm / minimal）+ `--theme-file` 自定义
- `scripts/typography.py`：中文排版（中英文间距、标点、省略号）
- `scripts/md_lite.py`：零依赖 Markdown 解析引擎
- `scripts/wechat_check.py`：公众号合规检查器（禁用标签/属性/外部资源）
- `scripts/selftest.py`：16 项能力自检（后续扩到 20）
- callout 高亮框（`> [!NOTE]` 与 `:::warning` 两种写法）、自动目录、front-matter 元数据、页脚版权
- 本地图片自动转 base64 内嵌、批量转换 + 索引页、多格式输出（wechat / text / markdown）
- `SKILL.md`、4 份 `references/`、文章模板

### Known limitations
- 数学公式尚不支持（v1.1.0 补齐）
- 无 CI、无独立测试文件（v1.3.0 补齐）

## [0.1.0] — 2026-10-06

从官方 starter kit（`c4b-wechat-publisher-starter`）初始化骨架，删除三个模板占位文件。
