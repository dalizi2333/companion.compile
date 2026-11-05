# Førde 小镇真实参考

整理日期：2026-11-02。地域方向：挪威 Jølster—Førde；具体店铺可架空，真实地形与街区需核对。

## 当前落地状态

**11 张参考照片已全部下载并逐张目视验收（2026-11-02）**：3 张 Førde 城区 + 8 张补录（Førde 广场/桥、Jølster 湖谷/雪季/谷地全景/湖岸农庄、Vassenden 村口/1880年代历史照）。其中 2 张大图受 Wikimedia 429 限流改存缩略图（Jolster-谷地全景 2560px、Astruptunet-湖岸农庄 1280px），如需原图后续重试。

**图像两级分级（2026-11-02）**：8 张超限大图已分级——高清原图移入 `原图/` 子目录（本地保留、git 忽略），原位替换为长边 2560 的入库版推远程。3 张未超限的本身就是入库版。分级脚本 `toolchain/image_tier.py`（根目录本地驻留）；`.metadata.json` 留原位随清单。sources.json 各条 `tier` 字段记录原图与入库版尺寸。

脚本 `download_references.py` 使用 Python 标准库，以自身目录为输出位置，通过 Commons API 取得原图地址及元数据；不会覆盖已有同名图片。运行环境若为 Python 沙箱需注意网络权限，或改在普通终端运行；urllib 需补 `http_proxy/https_proxy` 环境变量。下载记录字节数与 SHA-256，`.metadata.json` 保留 API 元数据。缩略图补取逻辑见 sources.json 各条 `thumbnail_url`。

已知小瑕疵：`Jolstravatnet-雪季-20160326.jpg` 原文件名含 mars2011，与 EXIF 2016-03-26 不符，拍摄时间存疑；`Vassenden-历史-1880年代.jpg` 为 7216×5412 大图，部分查看器打不开（文件完好，ImageMagick 可解）。

## 已核实的照片来源

| 文件 | 作者 | 时间 | 许可 | 用途 |
|---|---|---|---|---|
| Forde-市中心-20070617.jpg | Arild Nybø | 2007-06-17 | CC BY-SA 2.0 | 市中心、河流环境 |
| Forde-街景-2009年前.jpg | Olavfin | 拍摄日期未注明，2009-03-29已上传 | 作者释出公有领域 | 街景与背景山体；冬景可喂38章雪天进城 |
| Forde-城区与Vie-20070617.jpg | Arild Nybø | 2007-06-17 | CC BY-SA 2.0 | 谷地、城区和周边聚落尺度 |
| Forde-广场Elvegaarden-20061029.jpg | Michael Shanks | 2006-10-29 | CC BY-SA 2.5 | Førde 广场与 Elvetorget 外部（集市广场场景） |
| Forde-Jolstra桥-20170704.jpg | Vinguru | 2017-07-04 | CC BY-SA 4.0 | 桥边与河岸（29章桥边场景） |
| Jolstravatnet-湖景-200808.jpg | Ximonic | 2008-08-08 | CC BY-SA 3.0 | 湖面、山体、林线与小船 |
| Jolstravatnet-雪季-20160326.jpg | Cool guy | EXIF 2016-03-26（存疑） | CC BY-SA 4.0 | 湖区雪季（38章雪天进城氛围） |
| Vassenden-村落路口-20170704.jpg | Vinguru | 2017-07-04 | CC BY-SA 4.0 | 村落路口与木构建筑（Jølster Hotel） |
| Jolster-谷地全景-20170803.jpg | SinWin | 2017-08-03 | CC BY-SA 4.0 | 谷地全景、山体轮廓（缩略图2560px） |
| Astruptunet-湖岸农庄-20150506.jpg | Wolfmann | 2015-05-06 | CC BY-SA 4.0 | 湖岸草皮顶农庄（庄园选址气质；缩略图1280px） |
| Vassenden-历史-1880年代.jpg | Axel Lindahl（挪威国家图书馆数字化） | 1880-1890拍摄，2016-01-04上传 | Public domain | 19世纪末谷地与建筑（19世纪中叶老别墅气质） |

逐图来源见 `sources.json`。CC BY-SA 许可：https://creativecommons.org/licenses/by-sa/2.0/ （4.0/3.0/2.5 各依其版本）。第三方照片保留其原许可，不适用本仓原创素材许可。采用原图或改编图片时保留署名、来源、许可及修改说明。

## 街区与集市补充参考入口

- Elvetorget集市地点：https://bondensmarked.no/markedsplasser/elvetorget-i-foerde
- Elvetorget商业中心：https://www.elvetorget.no/
- 官方摄影散步路线：https://www.fjordnorway.com/en/inspiration/day-trips/forde/photo-walk-in-forde
- Hafstadvegen改造资料：https://www.fordepakken.no/kva-er-fordepakken/delprosjekt/tiltak-14-e39-fjellvegen/

上述为来源入口，不代表已下载或已获得照片再利用许可。集市是有日期的活动，具体规模和摊主构成随场次变化。新街道铺装与设施不能自动视为2012—2013年原貌。**缺口**：Elvetorget 农夫集市布置（现场摊位）、Hafstadvegen 沿街店面、Langebrua 桥侧视角在 Commons 无可下载实拍，已存的 Fordetorg 广场照 + Jølstra 桥照可作部分替代，其余按许可优先原则后续补。

## 同时供庄园地形设计使用

可共享：山体轮廓、森林与裸岩的分布、谷地宽度、坡地聚落与河流的空间关系；Astruptunet/1880年代历史照的草皮顶、木构+石基为 19 世纪中叶老别墅风格锚点。

不可直接套用：Førde城区的河岸不等于Jølster庄园湖岸；不能把城区视角中的山体当作庄园固定背景，也不能擅自加出该视角看不到的冰川。庄园湖岸、草地台地和积雪山峰另补Jølster实景参考，再组合设计架空地块。
