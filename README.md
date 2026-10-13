# Chinese Memoir Writing Skill

[中文说明](README.zh-CN.md) · [Skill](skills/chinese-memoir-writing/SKILL.md) · [Editorial guide](skills/chinese-memoir-writing/references/style-and-facts.md)

A general-purpose Codex / Claude Code skill for Chinese memoirs and narrative nonfiction: source-grounded scenes, coherent chapters, faithful quotations, factual queries and privacy-aware editing. A small Python helper compiles ordered Markdown chapters into printable, self-contained HTML.

**Version 1.0.0.** Public materials were rewritten as general editorial guidance. No real author's biography, family details, personal chronology, private manuscript, contact information or local project paths are included. The bundled example is entirely fictional.

## Install

```shell
git clone https://github.com/Y-123123/Chinese-Memoir-Writing-Skill.git
cd Chinese-Memoir-Writing-Skill
```

Copy the whole `skills/chinese-memoir-writing` folder to `~/.agents/skills/chinese-memoir-writing/` for Codex, or `~/.claude/skills/chinese-memoir-writing/` for Claude Code. Preserve scripts, references and examples; back up an existing same-name skill before replacing it. Restart the agent if its skill list has already been loaded.

Example: “Use chinese-memoir-writing to revise these interview notes into a chapter. Preserve known facts and quotations, use only my approved aliases, and list unresolved factual questions separately. Do not invent dialogue or events.”

The editorial guidance is configurable and does not imitate a named author's voice. The compiler has no AI dependency and does not call any external API.

## Compile a book

The helper uses the Python standard library (Python 3.10+ syntax); validation was performed on Windows with Python 3.14.3. No packages need to be installed.

```shell
python skills/chinese-memoir-writing/scripts/build_book.py --input skills/chinese-memoir-writing/examples/chapter-01.md --title "Fictional sample" --output output/sample.html
```

Pass your chapters in the intended order:

```shell
python skills/chinese-memoir-writing/scripts/build_book.py --input chapter-01.md chapter-02.md --title "Book title" --output output/book.html
```

Open the HTML in a browser, review it, then choose **Print → Save as PDF**. A5 print CSS is included; check browser paper-size/margin options. PDF export is manual and browser pagination may vary.

Supported Markdown: headings, paragraphs, single-level bullet lists, one-line block quotes, fenced code blocks and simple bold text. Raw HTML is escaped; links/images remain inert text. This is a limited compiler, not a full Markdown engine. Documents contain no external assets, scripts or network requests.

Sections headed exactly `待核实` or `Author queries` are removed until the next heading at the same or a higher level, including nested subsections. Headings inside code fences are preserved as literal text. Use these headings only for material you intend to exclude. Review the output: the helper neither anonymizes manuscripts nor verifies their factual accuracy.

Existing HTML is protected. `--force` explicitly replaces an existing output, but an input manuscript or symlink target is never accepted as output. The reported count is non-whitespace Markdown characters, not a linguistic word count. Original chapter files remain unchanged.

## Validation and privacy

```shell
python -m unittest discover -s tests -v
```

Seven checks cover editorial-query removal, nested headings, code-fence preservation, HTML escaping, inactive links/images, malformed fence rejection, chapter order, title escaping, UTF-8 output and overwrite protection. They validate compiler behavior; they do not establish literary quality, fact accuracy, browser PDF pagination, or agent behavior across models.

Only the generic skill, fictional example, compiler, tests and documentation are published. `.gitignore` excludes common manuscript and output folders, but it cannot remove identifying details from arbitrary content. Review and authorize disclosure before sharing a real manuscript.

MIT license applies to this repository. No third-party code is bundled and the compiler requires no additional dependencies.
