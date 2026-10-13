from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT=Path(__file__).resolve().parents[1]
SCRIPTS=ROOT/'skills'/'chinese-memoir-writing'/'scripts'
sys.path.insert(0,str(SCRIPTS))
from build_book import strip_queries, render, compile_book


class BookTests(unittest.TestCase):
    def test_remove_queries_including_nested_sections(self):
        text='# Chapter\nKeep.\n## 待核实\nPrivate query.\n### Nested\nMore.\n## Next\nRetain.'
        out=strip_queries(text)
        self.assertNotIn('Private query',out)
        self.assertNotIn('More.',out)
        self.assertIn('Retain.',out)

    def test_code_fence_heading_is_not_an_editorial_section(self):
        text='# Chapter\n```text\n## 待核实\nLiteral.\n```\nRetain.'
        self.assertEqual(strip_queries(text),text)

    def test_author_queries_english(self):
        out=strip_queries('# Title\nText.\n## Author queries\nQuestion?\n# Chapter 2\nNext.')
        self.assertNotIn('Question?',out)
        self.assertIn('Next.',out)

    def test_escape_html_and_keep_links_inert(self):
        out=render('<script>alert(1)</script>\n\n![x](https://example.test/track)\n\n**中文**')
        self.assertNotIn('<script>',out)
        self.assertNotIn('<img',out)
        self.assertIn('&lt;script&gt;',out)
        self.assertIn('<strong>中文</strong>',out)

    def test_reject_unclosed_code_fence(self):
        with self.assertRaises(ValueError):
            render('```python\nprint(1)')

    def test_order_title_and_self_contained_output(self):
        with tempfile.TemporaryDirectory() as tmp:
            a,b=Path(tmp)/'a.md',Path(tmp)/'b.md'
            a.write_text('# First\n甲。',encoding='utf-8')
            b.write_text('# Second\n乙。',encoding='utf-8')
            output,count=compile_book([b,a],'<unsafe>')
            self.assertLess(output.index('Second'),output.index('First'))
            self.assertIn('<title>&lt;unsafe&gt;</title>',output)
            self.assertIn('default-src',output)
            self.assertNotIn('src=',output)
            self.assertGreater(count,0)

    def test_cli_protects_existing_output_and_input(self):
        with tempfile.TemporaryDirectory() as tmp:
            a,out=Path(tmp)/'chapter.md',Path(tmp)/'book.html'
            a.write_text('# 虚构示例\n一盏灯。\n## 待核实\n查询。',encoding='utf-8')
            cmd=[sys.executable,'-X','utf8',str(SCRIPTS/'build_book.py'),
                 '--input',str(a),'--output',str(out)]
            run=subprocess.run(cmd,capture_output=True,text=True,encoding='utf-8',timeout=15)
            self.assertEqual(run.returncode,0,run.stderr)
            first=out.read_bytes()
            self.assertNotIn('查询',first.decode('utf-8'))
            self.assertNotEqual(subprocess.run(cmd,capture_output=True,timeout=15).returncode,0)
            self.assertEqual(out.read_bytes(),first)
            same=cmd[:-1]+[str(a),'--force']
            self.assertNotEqual(subprocess.run(same,capture_output=True,timeout=15).returncode,0)
            self.assertIn('查询',a.read_text(encoding='utf-8'))


if __name__=='__main__':
    unittest.main()
