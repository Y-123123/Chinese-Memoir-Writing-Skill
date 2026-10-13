# 中文回忆录与纪实写作 Skill

[English](README.md) · [技能入口](skills/chinese-memoir-writing/SKILL.md) · [中文编辑规范](skills/chinese-memoir-writing/references/style-and-facts.md)

面向 Codex / Claude Code 的通用中文回忆录、纪实写作和章节修订技能。帮助整理有来源依据的场景、保持章节连贯、核实事实与引文、列出作者待确认事项，并使用简单脚本将 Markdown 章节编排为可打印的 HTML。

公开版本命名为 **chinese-memoir-writing**，内容重新编写为通用编辑规范，不包含真实作者经历、亲属信息、私人时间线、未公开稿件、联系方式或个人项目路径。示例全文为虚构，未改写任何私人故事。

## 安装

```shell
git clone https://github.com/Y-123123/Chinese-Memoir-Writing-Skill.git
cd Chinese-Memoir-Writing-Skill
```

将完整的 `skills/chinese-memoir-writing` 文件夹复制到个人技能目录：

| 软件 | 目录 |
| --- | --- |
| Codex | `~/.agents/skills/chinese-memoir-writing/` |
| Claude Code | `~/.claude/skills/chinese-memoir-writing/` |

Windows 的 `~` 指用户主目录。保留入口、参考资料、示例和脚本；替换同名技能前先备份。已加载技能列表的会话可重新启动后使用。

示例提问：“使用 chinese-memoir-writing，把下面的访谈笔记修订成章节。保留有依据的事实与引文，只使用我批准的化名。不要补写不存在的对话、细节或心理动机，把待核实事项单独列出。”

语句长短、幽默程度和叙述节奏按作者声音及场景调整，不强制模仿某位作家。技能不能代替作者核实事实、判断披露范围或获得引文使用授权。

## 编排 HTML 与 PDF

脚本只使用 Python 标准库，无需安装额外依赖或填写 API。语法需要 Python 3.10 及以上；本次测试使用 Windows + Python 3.14.3。

先尝试自带的虚构例文：

```shell
python skills/chinese-memoir-writing/scripts/build_book.py --input skills/chinese-memoir-writing/examples/chapter-01.md --title "虚构示例" --output output/sample.html
```

编排自己的稿件时，按预期次序传入章节：

```shell
python skills/chinese-memoir-writing/scripts/build_book.py --input chapter-01.md chapter-02.md --title "书名" --output output/book.html
```

在浏览器中打开 HTML，检查内容，再用“打印 → 另存为 PDF”。页面提供 A5 样式，但浏览器的纸张、边距和分页仍需检查；程序不会自动导出 PDF。

支持标题、段落、单层项目列表、单行引用、围栏代码块和简单粗体。原始 HTML 会被转义，链接与图片保留为普通文字；不嵌入外部资源，也不执行脚本。这是有限的 Markdown 子集，不是完整排版引擎。

恰好名为 `待核实` 或 `Author queries` 的标题及其内容会从成书稿删除，直到遇到同级或更高级标题；其下的小标题也会删除。代码块中的同名文字不触发删除。只把确实希望排除的编辑查询放在这些标题下，生成后仍须核对。

已有输出文件默认受到保护；明确添加 `--force` 才替换。不能以原稿或符号链接作为输出。字符计数统计去除空白后的 Markdown 字符，不是中文分词意义的词数。原章节文件不修改。编译器不会自动查证事实或匿名化稿件。

## 测试与公开范围

```shell
python -m unittest discover -s tests -v
```

7 项测试检查待核实段落删除、嵌套标题、代码块、HTML 转义、章节顺序、中文输出和防覆盖等行为。测试不证明文学质量、事实正确性、不同模型的代理行为或浏览器 PDF 分页效果。

公开内容仅包括通用规范、虚构示例、编排脚本、测试和中英文文档，采用 MIT 许可。默认忽略常见稿件与输出目录；它不能自动判断任意文件是否含私人信息。分享自己的真实稿件前，仍应检查姓名、日期、地址、关系组合及引文披露范围。
