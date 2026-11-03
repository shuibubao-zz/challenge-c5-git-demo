# 架构：一次转换里发生了什么

> 本文描述的是**代码实际执行顺序**，不是理想设计。每一步都标了「失败时怎么办」——
> 这个项目的稳定性主要来自这些失败路径，而不是主路径。

---

## 一、总览

```
输入（.md / .docx / .html）
   │
   ├─[1] 读取与元数据解析 ────────── front-matter / 首个 # 标题
   │
   ├─[2] 解析成中间表示 IR ───────── 两条引擎：markdown 库 ／ 自带 md_lite
   │
   ├─[3] 逐块渲染（带 inline CSS）─── 主题 + 中文排版 + callout + 目录
   │
   ├─[4] 内联清洗与加固 ──────────── 禁标签/禁属性 → <section> 化
   │
   ├─[5] 图片内嵌 ────────────────── 本地图 → base64
   │
   ├─[6] 合规自检 ────────────────── wechat_check.py
   │
   └─[7] 输出 HTML（+ JSON 报告）
```

代码位置：`scripts/convert_to_wechat.py` 的 `convert_one()` 串起 [1]–[7]，
`batch_convert()` 只是对目录里的每个文件循环调用它。

---

## 二、逐步说明

### [1] 读取与元数据（`read_markdown` / `read_docx`）

| 输入 | 处理 |
|---|---|
| `.md` | 读文本 → 切出 front-matter（`title/author/date/abstract/theme/toc/copyright`）→ 剩下的是正文 |
| `.docx` | `python-docx` 遍历段落与 run，保留加粗/斜体；**缺 python-docx 时直接报错并给出 `pip install python-docx`** |
| `.html` | 直接进 [4]，跳过 [2][3] 的 Markdown 路径 |

**失败路径**：非 UTF-8 → 按 UTF-8 容错读取并替换，不崩。空文件 → 空正文，自检通过，统计 0 字。

### [2] 解析成 IR（`read_markdown` → `md_lite` 或 `markdown`+`bs4`）

IR 只有一种节点形态：`{"type": ..., ...}`，`type` 取 `h2/h3/h4/p/quote/list/table/code/img/hr`。

| 引擎 | 何时用 |
|---|---|
| `markdown` + `beautifulsoup4` | 装了就走这条（CommonMark 更严谨） |
| `md_lite`（自研，394 行） | 没装就自动降级；`--engine lite` 可强制 |

**为什么要两套**：换台机器没库就跑不了，是这类工具最常见的死法。但"降级"不能是"差不多"——
`selftest.py` 里有一条断言要求两条路径对同一输入的输出**字节一致**，这条断言在 C4B 阶段抓出了 3 个真缺陷
（`nl2br` 换行数不一致、相邻引用块被合并、callout 标记不支持多行）。

`:::warning … :::` 围栏在进入引擎前被 `convert_callout_fences()` 改写成 `> [!WARNING]`，
因为围栏语法不是标准 Markdown，两条引擎都不认。

### [3] 渲染（`render_blocks` 及其分支）

- **主题**：`themes.py` 的 `BASE` 打底，主题覆盖层叠加，`--theme-file` 再叠加（三层合并，后层覆盖前层）
- **中文排版**（`typography.py`）：中英文之间插空格、标点挤压、省略号归一；`--no-typo` 关闭
- **callout**：`> [!NOTE|TIP|PRACTICE|WARNING]` → 带底色/左边框/图标的 `<section>`
- **目录**：从 h2/h3 列表生成**纯文本**目录——公众号不支持页内锚点，做成链接是骗人的
- **公式**：`$…$` / `$$…$$` 交给 `math_render.py` 渲染 PNG，**先用占位符替换**，
  等图片归一化处理完再插回，否则公式 `<img>` 的自定义样式会被覆盖

**失败路径**：matplotlib 缺失 → 公式降级为红字等宽文本 + 告警，**不假装渲染成功**。

### [4] 内联清洗（`sanitize_inline`）

这一步是"能不能在公众号里活下来"的关键。检查器的三张表都在 `wechat_check.py` 顶部：

1. **白名单标签** `ALLOWED_TAGS`：`p h2 h3 h4 ul ol li span img a table thead tbody tr th td br strong em b i`
   ——不在其中的要么是硬禁（见下），要么是"不保证保留"（`SOFT_TAGS`：`section/footer/header/nav/article/aside/main`，不算硬错误但也不承诺）
2. **硬禁标签** `FORBIDDEN_TAGS`：`script style iframe h1 div svg video audio form input button pre code blockquote …`
   ——其中 `h1` 会在渲染阶段先降级为 `h2`；`pre`/`code`/`blockquote` 在输出里被改写为带样式的 `section`/`span`
3. **禁用属性** `FORBIDDEN_ATTRS = {class, id}` + `on*` 事件属性；
   **禁用 CSS** `FORBIDDEN_CSS_HINT`：`position float flex grid animation transition transform z-index top left right bottom height`

**失败路径**：未知标签 → 降级为 `<span>` 保留文字，不丢弃内容。

### [5] 图片内嵌（`embed_images`）

本地图片 → base64 data URI。**SVG 直接拒绝并告警**——公众号保存时会丢 SVG，内嵌等于埋雷。

### [6] 合规自检（`wechat_check.py`）

转换结束自动跑一次，输出分两级：

| 级别 | 含义 | 处理 |
|---|---|---|
| `[错误]` | 硬违规（出现 `<style>`、`class`、外部资源等） | 必须修；`--strict` 下以非 0 退出 |
| `[提醒]` | 需人判断（正文外链、图片过大、SVG） | 作者决定 |

**这是本项目最有价值的一块**：C4B 阶段它抓到了我自己写的 `height:auto`，
`--strict` 让它可以接进 CI 当门禁。

### [7] 输出

```text
out.html              可直接粘贴的完整 HTML（含预览外壳）
out.html --fragment   只输出正文片段（嵌进别的页面时用）
--report x.json       解析引擎/主题/字数/图表统计/自检结果，供程序消费
```

---

## 三、数据流里三个容易踩的点

1. **顺序敏感**：公式替换必须在图片归一化**之前**用占位符挡一下，否则公式图的样式会被当成普通图片改写。
2. **两处都在改 HTML**：[4] 清洗和 [5] 内嵌都做正则替换。改动其中一处时，务必回归另一处——
   selftest 里"公式 + 图片同时存在"的用例就是为这个场景写的。
3. **统计口径**：`[6]` 的 h2/h3 计数只算开标签，早期版本把闭标签也算进去导致数字翻倍。

---

## 四、为什么不用模板引擎（Jinja 等）

三条理由，按重要性排序：

1. **零依赖**是主承诺，模板引擎是硬依赖
2. 输出需要精细控制到"每个 `<span>` 的 `style` 属性"，模板层的自动转义和空白处理会和这个目标打架
3. 这套 IR + 手写渲染不需要额外抽象层，`convert_to_wechat.py` 全文件 793 行（含 CLI、批量、docx 读取），
   比引入模板引擎后再想办法绕开它的自动转义要短

代价是新增块类型时要同时改 IR、渲染、白名单三处——见 `CONTRIBUTING.md` 的贡献路径。
