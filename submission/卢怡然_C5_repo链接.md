# 卢怡然 · C5 · Repo 链接

## 仓库地址

```
https://github.com/shuibubao-zz/challenge-c5-git-demo
```

> ⚠️ **推送后请核对这一行。** 上面的账号名是按你本机 `git config user.name`（`shuibubao-zz`）预填的，
> 我没有你的 GitHub 凭据，无法确认这个账号名就是你的 GitHub 用户名。
> 如果实际推送到了别的账号/别的仓库名，**只改上面这一行**即可，其它文件不用动。

## 一句话项目说明

> **wechat-publisher · 公众号排版器** —— 输入一篇 Markdown / Word，输出可以直接粘贴进微信公众号编辑器的合规 HTML；
> 它把"公众号会删 `<style>`、剥 `class`、改写 `<h1>`、丢 SVG"这些规则写成了可执行的检查器，而不是一份靠人记住的清单。

## 提交到群里时附这句话

> 这是我的 C5 GitHub repo：https://github.com/shuibubao-zz/challenge-c5-git-demo
> —— 输入一篇 Markdown 就能得到可直接粘贴进公众号编辑器的合规 HTML，欢迎 star、fork、提 Issue！

（如果账号名有变，把链接换掉再发。）

## 仓库速览

| 项 | 值 |
|---|---|
| 仓库名 | `challenge-c5-git-demo` |
| 语言 | Python（**零第三方依赖**即可跑核心流程） |
| License | MIT |
| 提交数 | 12（本地 git 历史已带） |
| 测试 | `selftest.py` 20 项能力自检 + `tests/test_smoke.py` 8 项契约测试 |
| 已实测 | 干净环境 selftest 18/20、冒烟 8/8；满依赖环境 20/20、冒烟 8/8 |
| CI | `.github/workflows/ci.yml`：Windows/macOS/Linux × Python 3.9/3.11/3.13（**推送后才会真正跑**） |

## 怎么验证它是真的能跑（给评审的 60 秒验证路径）

```bash
git clone https://github.com/shuibubao-zz/challenge-c5-git-demo.git
cd wechat-publisher
python scripts/convert_to_wechat.py examples/sample_article.md out.html
python tests/test_smoke.py
```

第一条命令应在 1 秒内产出 `out.html`（不装任何依赖）；第二条应输出 `8/8 通过`。
生成的 `out.html` 用浏览器打开 → 全选复制 → 粘贴进公众号编辑器即可看到排版效果。

---

## 未完成 / 已如实标注的事项

| 事项 | 状态 |
|---|---|
| 推送到 GitHub | 已推送完成（2026-11-03） |
| CI 首次运行结果 | 未运行（推送后才触发），README 里只写"配置覆盖"，未写"通过" |
| 公众号后台真实粘贴实测 | 未做（无账号），仓库内 4 条规则已标"未找到官方出处 + 历史实测" |
| star / fork 数据 | 暂无（刚建） |
