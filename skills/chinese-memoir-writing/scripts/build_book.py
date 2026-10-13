"""Compile a safe, limited Markdown subset into self-contained printable HTML."""
from __future__ import annotations
import argparse
import html
from pathlib import Path
import re

QUERY_HEADINGS = {'待核实', 'Author queries'}


def strip_queries(text):
    lines, skip, fence = [], None, None
    for line in text.splitlines():
        marker = re.match(r'^\s*(`{3,}|~{3,})', line)
        if marker:
            char = marker.group(1)[0]
            fence = None if fence == char else char if fence is None else fence
        heading = re.match(r'^(#{1,6})\s+(.+?)\s*#*$', line) if fence is None else None
        if heading:
            level, title = len(heading[1]), heading[2].strip()
            if skip is not None and level <= skip:
                skip = None
            if title in QUERY_HEADINGS:
                skip = level
        if skip is None:
            lines.append(line)
    return '\n'.join(lines)


def inline(text):
    # Raw HTML and Markdown images/links remain escaped plain text: no active
    # content, remote requests, or filesystem resource resolution.
    escaped = html.escape(text)
    return re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', escaped)


def render(text):
    output, paragraph, code = [], [], None
    list_open = False

    def flush():
        if paragraph:
            output.append('<p>' + inline('\n'.join(paragraph)) + '</p>')
            paragraph.clear()

    for line in text.splitlines():
        if code is not None:
            if line.lstrip().startswith(code['marker']):
                output.append('<pre><code>' + html.escape('\n'.join(code['lines'])) + '</code></pre>')
                code = None
            else:
                code['lines'].append(line)
            continue
        marker = re.match(r'^\s*(`{3,}|~{3,})', line)
        heading = re.match(r'^(#{1,6})\s+(.+)$', line)
        bullet = re.match(r'^\s*[-*+]\s+(.+)$', line)
        if list_open and not bullet:
            output.append('</ul>'); list_open = False
        if marker:
            flush(); code = dict(marker=marker[1], lines=[])
        elif heading:
            flush(); level=len(heading[1]); output.append(f'<h{level}>'+inline(heading[2])+f'</h{level}>')
        elif bullet:
            flush()
            if not list_open:
                output.append('<ul>'); list_open=True
            output.append('<li>'+inline(bullet[1])+'</li>')
        elif line.startswith('> '):
            flush(); output.append('<blockquote>'+inline(line[2:])+'</blockquote>')
        elif not line.strip():
            flush()
        else:
            paragraph.append(line)
    if code is not None:
        raise ValueError('Unclosed Markdown code fence.')
    flush()
    if list_open:
        output.append('</ul>')
    return '\n'.join(output)


def compile_book(paths, title):
    chapters, count = [], 0
    for path in paths:
        text = strip_queries(Path(path).read_text(encoding='utf-8-sig'))
        count += len(re.sub(r'\s', '', text))
        chapters.append('<section class="chapter">' + render(text) + '</section>')
    css = '''@page{size:A5;margin:16mm 14mm}body{max-width:44rem;margin:2rem auto;padding:0 1rem;
font:18px/1.8 serif;color:#202020;background:white}h1,h2,h3{line-height:1.35;break-after:avoid}
.chapter{break-before:page}.chapter:first-of-type{break-before:auto}p{orphans:3;widows:3}
blockquote{margin-left:1rem;padding-left:1rem;border-left:2px solid #999}pre{white-space:pre-wrap}
@media print{body{margin:0;padding:0;font-size:11pt}header{break-after:page}}'''
    document = '<!doctype html><html lang="zh-CN"><meta charset="utf-8">' + \
        '<meta name="viewport" content="width=device-width,initial-scale=1">' + \
        '<meta http-equiv="Content-Security-Policy" content="default-src \'none\'; style-src \'unsafe-inline\'">' + \
        '<title>' + html.escape(title) + '</title><style>' + css + '</style><body><header><h1>' + \
        html.escape(title) + '</h1></header>' + '\n'.join(chapters) + '</body></html>'
    return document, count


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--input', nargs='+', required=True, type=Path)
    parser.add_argument('--title', default='Memoir')
    parser.add_argument('--output', required=True, type=Path)
    parser.add_argument('--force', action='store_true')
    args=parser.parse_args()
    if args.output.exists() and not args.force:
        parser.error('Output already exists; select another path or explicitly use --force.')
    if args.output.is_symlink() or args.output.resolve() in {p.resolve() for p in args.input}:
        parser.error('Output must not be a symlink or replace an input manuscript.')
    document,count=compile_book(args.input,args.title)
    args.output.parent.mkdir(parents=True,exist_ok=True)
    with args.output.open('w' if args.force else 'x',encoding='utf-8') as handle:
        handle.write(document)
    print(f'Wrote {args.output.name}; {count} non-whitespace Markdown characters (not a word count).')


if __name__=='__main__':
    main()
