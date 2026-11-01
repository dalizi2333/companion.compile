#!/usr/bin/env python3
"""《庄颜协议》发布打包工具：正文 → EPUB + TXT + 许可，打成发布 zip。

用法：python3 tools/make_release.py <版本号>
示例：python3 tools/make_release.py 0.1.0
产物：dist/zhuangyan-part1-v<版本>.epub / .txt / .zip（仅标准库，无外部依赖）
"""
import html
import re
import sys
import uuid
import zipfile
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
SRC = BASE / "正文" / "第一部"
LICENSE = BASE / "LICENSE.md"
DIST = BASE / "dist"
LANG = "zh-CN"
AUTHOR = "dalizi2333"
BOOK_TITLE = "庄颜协议·第一部"
UUID = uuid.uuid5(uuid.NAMESPACE_URL, "https://github.com/dalizi2333/companion.compile")


def chapters():
    out = []
    for f in sorted(SRC.glob("*.md")):
        lines = f.read_text(encoding="utf-8").splitlines()
        title = lines[0].lstrip("# ").strip()
        body = [ln for ln in lines[1:]]
        out.append((f.stem, title, body))
    return out


def md_to_xhtml(lines):
    """极简 md→xhtml：段落、# 标题、*** 场景分隔、**粗体**。"""
    out = []
    for ln in lines:
        s = ln.strip()
        if not s:
            continue
        if s == "***":
            out.append('<p class="scene">◆</p>')
            continue
        m = re.match(r"^#{2,3}\s+(.*)$", s)
        if m:
            out.append(f"<h2>{inline(m.group(1))}</h2>")
            continue
        out.append(f"<p>{inline(s)}</p>")
    return "\n".join(out)


def inline(s):
    s = html.escape(s, quote=False)
    return re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", s)


def xhtml(title, body):
    return f"""<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops" xml:lang="{LANG}">
<head><meta charset="utf-8"/><title>{html.escape(title)}</title><link rel="stylesheet" type="text/css" href="style.css"/></head>
<body>
{body}
</body>
</html>
"""


CSS = """body{margin:5% 8%;line-height:1.8;font-family:serif}
h1{font-size:1.4em;margin:1.2em 0 1em;text-align:center}
h2{font-size:1.1em;margin:1.2em 0 .8em}
p{margin:.6em 0;text-indent:2em}
p.scene{text-align:center;text-indent:0;color:#888;margin:1.4em 0}
p.center{text-align:center;text-indent:0}
p.small{font-size:.85em;color:#555;text-indent:0}
strong{font-weight:bold}
"""


def build_epub(ver, chs, out):
    title_page = xhtml("书名页", f"""
<h1>庄颜协议</h1>
<p class="center">第一部</p>
<p class="center">　</p>
<p class="center">{AUTHOR} 著</p>
<p class="center">　</p>
<p class="small center">基于刘慈欣《三体》的同人衍生作品（非官方）</p>
<p class="small center">原作元素版权归刘慈欣及三体宇宙等权利方；原创内容以 CC BY-NC-SA 4.0 授权</p>
<p class="small center">详见文末“版权与许可”</p>
""")

    lic = LICENSE.read_text(encoding="utf-8")
    lic_body = "\n".join(
        f"<p>{inline(ln.strip())}</p>" if ln.strip() else ""
        for ln in lic.splitlines()).replace("<p></p>", "")
    license_page = xhtml("版权与许可", f"<h1>版权与许可</h1>\n{lic_body}")

    manifest, spine, files = [], [], [("title", title_page), ("license", license_page)]
    manifest.append('<item id="nav" href="nav.xhtml" media-type="application/xhtml+xml" properties="nav"/>')
    manifest.append('<item id="ncx" href="toc.ncx" media-type="application/x-dtbncx+xml"/>')
    manifest.append('<item id="css" href="style.css" media-type="text/css"/>')
    manifest.append('<item id="title" href="title.xhtml" media-type="application/xhtml+xml"/>')
    manifest.append('<item id="license" href="license.xhtml" media-type="application/xhtml+xml"/>')
    spine.append('<itemref idref="title"/>')
    navs, ncx = [], []
    for i, (sid, title, body) in enumerate(chs, 1):
        fid = f"c{i:02d}"
        href = f"{fid}.xhtml"
        files.append((fid, xhtml(title, md_to_xhtml(body))))
        manifest.append(f'<item id="{fid}" href="{href}" media-type="application/xhtml+xml"/>')
        spine.append(f'<itemref idref="{fid}"/>')
        navs.append(f'<li><a href="{href}">{html.escape(title)}</a></li>')
        ncx.append(f'<navPoint id="n{i}" playOrder="{i + 1}"><navLabel><text>{html.escape(title)}</text></navLabel><content src="{href}"/></navPoint>')
    spine.append('<itemref idref="license"/>')
    files.append(("nav", xhtml("目录", f'<nav epub:type="toc" id="toc"><h1>目录</h1><ol>{"".join(navs)}</ol></nav>')))
    nav_xhtml = files.pop()[1]
    toc_ncx = f"""<?xml version="1.0" encoding="utf-8"?>
<ncx xmlns="http://www.daisy.org/z3986/2005/ncx/" version="2005-1">
<head><meta name="dtb:uid" content="urn:uuid:{UUID}"/></head>
<docTitle><text>{html.escape(BOOK_TITLE)}</text></docTitle>
<navMap><navPoint id="n0" playOrder="1"><navLabel><text>书名页</text></navLabel><content src="title.xhtml"/></navPoint>{"".join(ncx)}<navPoint id="nL" playOrder="{len(ncx) + 2}"><navLabel><text>版权与许可</text></navLabel><content src="license.xhtml"/></navPoint></navMap>
</ncx>
"""
    opf = f"""<?xml version="1.0" encoding="utf-8"?>
<package xmlns="http://www.idpf.org/2007/opf" version="3.0" unique-identifier="pub-id" xml:lang="{LANG}">
<metadata xmlns:dc="http://purl.org/dc/elements/1.1/">
<dc:identifier id="pub-id">urn:uuid:{UUID}</dc:identifier>
<dc:title>{html.escape(BOOK_TITLE)}</dc:title>
<dc:creator>{AUTHOR}</dc:creator>
<dc:language>{LANG}</dc:language>
<dc:description>基于《三体》的同人衍生作品：AGI 庄颜主视角。原作元素版权归原权利方；原创内容以 CC BY-NC-SA 4.0 授权。</dc:description>
<meta property="dcterms:modified">{ver}T00:00:00Z</meta>
</metadata>
<manifest>{"".join(manifest)}</manifest>
<spine toc="ncx">{"".join(spine)}</spine>
</package>
"""
    with zipfile.ZipFile(out, "w") as z:
        z.writestr(zipfile.ZipInfo("mimetype"), "application/epub+zip", zipfile.ZIP_STORED)
        z.writestr("META-INF/container.xml", """<?xml version="1.0" encoding="utf-8"?>
<container version="1.0" xmlns="urn:oasis:names:tc:opendocument:xmlns:container">
<rootfiles><rootfile full-path="OEBPS/content.opf" media-type="application/oebps-package+xml"/></rootfiles>
</container>
""", zipfile.ZIP_DEFLATED)
        z.writestr("OEBPS/content.opf", opf, zipfile.ZIP_DEFLATED)
        z.writestr("OEBPS/nav.xhtml", nav_xhtml, zipfile.ZIP_DEFLATED)
        z.writestr("OEBPS/toc.ncx", toc_ncx, zipfile.ZIP_DEFLATED)
        z.writestr("OEBPS/style.css", CSS, zipfile.ZIP_DEFLATED)
        for fid, content in files:
            z.writestr(f"OEBPS/{fid}.xhtml", content, zipfile.ZIP_DEFLATED)


def build_txt(chs, out):
    lines = [
        f"《{BOOK_TITLE}》",
        f"作者：{AUTHOR}（三体同人衍生作品，非官方）",
        "原创内容以 CC BY-NC-SA 4.0 授权；原作元素版权归刘慈欣及三体宇宙等权利方。",
        "",
    ]
    for _, title, body in chs:
        lines.append(title.lstrip("# ").strip())
        lines.append("")
        for ln in body:
            s = ln.strip()
            if not s:
                lines.append("")
                continue
            if s == "***":
                continue
            lines.append(re.sub(r"\*\*(.+?)\*\*", r"\1", s))
        lines.append("")
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    ver = sys.argv[1].lstrip("v")
    DIST.mkdir(exist_ok=True)
    chs = chapters()
    epub = DIST / f"zhuangyan-part1-v{ver}.epub"
    txt = DIST / f"zhuangyan-part1-v{ver}.txt"
    z = DIST / f"zhuangyan-part1-v{ver}.zip"
    build_epub(ver, chs, epub)
    build_txt(chs, txt)
    with zipfile.ZipFile(z, "w", zipfile.ZIP_DEFLATED) as zf:
        zf.write(epub, f"zhuangyan-part1-v{ver}.epub")
        zf.write(txt, f"zhuangyan-part1-v{ver}.txt")
        zf.write(LICENSE, "LICENSE.md")
    with zipfile.ZipFile(epub) as zf:
        first = zf.infolist()[0]
        assert first.filename == "mimetype" and first.compress_type == 0, "EPUB mimetype 规范错误"
    print(f"章节 {len(chs)} | {epub.name} {epub.stat().st_size // 1024}KB | {txt.name} {txt.stat().st_size // 1024}KB | {z.name} {z.stat().st_size // 1024}KB")


if __name__ == "__main__":
    main()
