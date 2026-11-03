---
name: Bug 报告
about: 转换结果不对、崩溃、样式在公众号里丢了
title: "[bug] "
labels: ["bug"]
---

## 先做这三件事（能省一半来回）

1. 用样例文件复现一遍，确认不是你自己的文档特有问题：

   ```bash
   python scripts/convert_to_wechat.py examples/sample_article.md out.html
   ```

2. 跑一遍自检，把结果贴上来：

   ```bash
   python scripts/selftest.py
   ```

3. 告诉我你的环境：**操作系统 + Python 版本 + 装了哪些可选依赖**（`markdown` / `beautifulsoup4` / `python-docx` / `matplotlib`）。

> 为什么一定要环境信息：同一份代码在"装了 markdown 库"和"零依赖"两条路径下的行为本来就不同。
> 没有环境信息，我无法判断这是 bug 还是预期的降级行为。

## 问题描述

<!-- 一句话说清：你以为会发生什么，实际发生了什么 -->

## 复现步骤

```bash
# 1.
# 2.
```

## 最小复现输入

<!-- 请贴能触发问题的最小 Markdown 片段，不要贴整篇文章 -->

```markdown
（贴这里）
```

## 实际输出 / 报错

```text
（贴终端输出，或用 <details> 折叠长内容）
```

## 期望输出

<!-- 如果有参考截图，贴在这里 -->

---

## 自查（勾选后提交）

- [ ] 我已确认这不是「正文含外链」这类 `[提醒]`（提醒项是设计如此，不是 bug）
- [ ] 我已附上 Python 版本与依赖情况
- [ ] 我没有把整篇文章贴进来，而是给了最小复现片段
