"""在可联网的普通终端运行；图片下载到脚本所在目录。"""
import hashlib
import json
from pathlib import Path
from urllib.parse import urlencode
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parent
items = json.loads((ROOT / "sources.json").read_text())
for item in items:
    target = ROOT / item["local"]
    if target.exists():
        print("已有，跳过：", target.name)
        continue
    try:
        params = dict(action="query", titles="File:" + item["file"], prop="imageinfo", iiprop="url|extmetadata", format="json")
        request = Request("https://commons.wikimedia.org/w/api.php?" + urlencode(params), headers={"User-Agent": "ZhuangYanContract-Reference/1.0"})
        with urlopen(request, timeout=30) as response:
            pages = json.load(response)["query"]["pages"]
        info = next(iter(pages.values()))["imageinfo"][0]
        request = Request(info["url"], headers={"User-Agent": "ZhuangYanContract-Reference/1.0"})
        with urlopen(request, timeout=60) as response:
            data = response.read()
        if not data.startswith(bytes([255, 216, 255])):
            raise ValueError("返回内容不是JPEG")
        temporary = target.with_suffix(".jpg.part")
        temporary.write_bytes(data)
        temporary.replace(target)
        item.update(status="已下载，待目视验收", bytes=len(data), sha256=hashlib.sha256(data).hexdigest(), original_url=info["url"])
        target.with_suffix(".metadata.json").write_text(json.dumps(info, ensure_ascii=False, indent=2))
        print("已下载：", target.name)
    except Exception as error:
        print("下载失败：", item["file"], str(error))
(ROOT / "sources.json").write_text(json.dumps(items, ensure_ascii=False, indent=2) + "\n")
