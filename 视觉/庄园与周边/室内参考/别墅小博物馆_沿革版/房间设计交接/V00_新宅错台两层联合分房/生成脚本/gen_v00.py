#!/usr/bin/env python3
# V00 新宅错台两层联合分房 · 参数化设计与出图 v2
import json, math

S = 22.0          # px per meter
GAP = 0.15        # 内隔墙厚

ROOMS = [
 # ---- 二层（x 切分：前室3.0|纵巷1.8|客房A4.0|客房B4.0|公卫2.65|过厅5.0，缝0.15） ----
 dict(id="U01", fl=2, name="签收前室", rect=[-21.6, 6.4, -18.6, 10.4], pid=None,
      note="西口进门(西南向)；东门进客廊纵巷；唯一馆务接口", fill="#e8eef2"),
 dict(id="U13a", fl=2, name="生活储藏A", rect=[-21.6, 10.55, -18.6, 17.9], pid=None,
      note="无窗；前室/纵巷后侧；收发+家庭储(分期)", fill="#eceff1"),
 dict(id="GB2", fl=2, name="客廊纵巷", rect=[-14.3, 6.4, -12.5, 17.9], kind="corr", pid=None,
      note="北端封端；南开口接主廊；西服务客房A、东服务客房B与储段", fill="#f1ede4"),
 dict(id="U05", fl=2, name="普通客房A", rect=[-18.45, 6.4, -14.45, 10.4], pid="G-A",
      note="G-A 16㎡；北墙窗(西北,朝向受限记录)；东门进客廊(反锁)", fill="#eef3e8"),
 dict(id="U05b", fl=2, name="客房A厕洗·收纳", rect=[-18.45, 10.55, -14.45, 13.9], pid="G-A",
      note="G-A套内段；门开寝南墙；机械排气", fill="#e7f0ee"),
 dict(id="U13b", fl=2, name="生活储藏B", rect=[-18.45, 14.05, -14.45, 17.9], pid=None,
      note="无窗；东门进客廊", fill="#eceff1"),
 dict(id="U07", fl=2, name="普通客房B", rect=[-12.35, 6.4, -8.35, 10.4], pid="G-B",
      note="G-B 16㎡；北墙窗(西北,朝向受限记录)；西门进客廊(反锁)", fill="#eef3e8"),
 dict(id="U07b", fl=2, name="客房B厕洗·收纳", rect=[-12.35, 10.55, -8.35, 13.9], pid="G-B",
      note="G-B套内段；门开寝南墙；机械排气", fill="#e7f0ee"),
 dict(id="U13c", fl=2, name="生活储藏C", rect=[-12.35, 14.05, -8.35, 17.9], pid=None,
      note="无窗；西门进客廊", fill="#eceff1"),
 dict(id="U06", fl=2, name="公卫·清洁", rect=[-8.2, 6.4, -5.55, 10.4], pid=None,
      note="北高窗；东门进过厅；服务全层", fill="#e7f0ee"),
 dict(id="U10", fl=2, name="家务·布草", rect=[-8.2, 10.55, -5.55, 17.9], pid=None,
      note="无窗辅助(机械排风)；南门进主廊；19.5㎡", fill="#ece9f2"),
 dict(id="U03", fl=2, name="过厅(北口)", rect=[-5.4, 6.4, -3.2, 17.9], pid=None,
      note="北口进门；内分门厅/前厅+衣帽储段(分期)；南端开口接主廊", fill="#f1ede4"),
 dict(id="U50", fl=2, name="活动·阅读", rect=[-3.05, 6.4, -0.4, 17.9], pid=None,
      note="东外墙窗(东北,漫射光记录)；南门进主廊；30.5㎡", fill="#f0ede9"),
 dict(id="U24", fl=2, name="画角·衣帽(庄颜套内)", rect=[-15.05, 20.15, -12.15, 23.6], pid="G-ZY",
      note="V01新增(V00缺口补全)；画桌/画架/画材柜；南窗东南向阳", fill="#f3ece7"),
 dict(id="U21", fl=2, name="庄颜普通客房", rect=[-21.6, 20.15, -17.4, 23.6], pid="G-ZY",
      note="G-ZY 14㎡级；西墙(西南向阳)+南墙(东南向阳)双向阳；壁炉芯VC3穿北角", fill="#f7ecec"),
 dict(id="U22", fl=2, name="客房门斗", rect=[-17.25, 20.15, -15.2, 21.55], pid="G-ZY",
      note="套间入口；V01细化反锁/放箱", fill="#f7ecec"),
 dict(id="U23", fl=2, name="客房厕洗", rect=[-17.25, 21.7, -15.2, 23.6], pid="G-ZY",
      note="G-ZY专用厕洗；南墙高窗", fill="#e7f0ee"),
 dict(id="U40", fl=2, name="小起居室(含水吧台)", rect=[-8.25, 18.05, -0.4, 23.6], pid=None,
      note="南墙(东南向阳)湖景；玻璃门EXT-U-S；水吧台家具级", fill="#fdf6e3"),
 dict(id="GA", fl=2, name="主廊(客廊)", rect=[-21.6, 18.05, -8.4, 20.0], kind="corr", pid=None,
      note="东西向；东端即起居室门与梯口", fill="#f1ede4"),
 # ---- 一层 ----
 dict(id="L02", fl=1, name="家务间(炊事炉VC3)", rect=[-26.6, 20.4, -19.5, 23.8], pid=None,
      note="北墙承土无窗；VC3炊事铁炉候选", fill="#ece9f2"),
 dict(id="L04", fl=1, name="储物间", rect=[-19.35, 20.4, -12.15, 23.8], pid=None,
      note="北墙承土；门开南墙进主廊", fill="#eceff1"),
 dict(id="L01", fl=1, name="梯间(主梯起步)", rect=[-12.0, 20.4, -8.4, 23.8], pid=None,
      note="主梯起步平台+梯下储柜；VC4采暖炉候选", fill="#f3ece7"),
 dict(id="L05", fl=1, name="设备·储物", rect=[-8.25, 20.4, -4.9, 23.8], pid=None,
      note="北墙承土；热泵分水器/管井端头", fill="#eceff1"),
 dict(id="L15", fl=1, name="公卫·清洁", rect=[-4.75, 20.4, -0.4, 23.8], pid=None,
      note="北墙承土无窗；机械排气", fill="#e7f0ee"),
 dict(id="L10", fl=1, name="门厅", rect=[-26.6, 25.9, -22.2, 30.4], pid=None,
      note="EXT-L-W进门(西南向)；北门进主廊", fill="#f3ece7"),
 dict(id="L16", fl=1, name="西储·衣帽", rect=[-26.6, 30.55, -22.2, 33.6], pid=None,
      note="门北进门厅；南墙窗(东南向)", fill="#eceff1"),
 dict(id="L12", fl=1, name="备餐间", rect=[-22.05, 25.9, -14.2, 27.25], pid=None,
      note="北门进主廊；南传菜口通餐厅；辅助无窗", fill="#e8eef2"),
 dict(id="L11", fl=1, name="家庭餐厅(V03)", rect=[-22.05, 27.4, -14.2, 33.6], pid=None,
      note="南墙2窗(东南向阳)；西墙南端壁炉VC5候选", fill="#fdf6e3"),
 dict(id="L13", fl=1, name="会客室(含南窗游坐区)", rect=[-14.05, 25.9, -8.0, 33.6], pid=None,
      note="北门进主廊；南墙2窗(东南向阳)", fill="#eef3e8"),
 dict(id="L14", fl=1, name="家庭起居", rect=[-7.85, 25.9, -4.3, 33.6], pid=None,
      note="北门进主廊；南墙2窗(东南向阳)", fill="#eef3e8"),
 dict(id="L19", fl=1, name="家庭书房", rect=[-4.15, 25.9, -0.4, 33.6], pid=None,
      note="南+东外墙；原家庭卧室改家庭阅读(签调令场景)", fill="#eef3e8"),
 dict(id="GA-L", fl=1, name="主廊", rect=[-26.6, 23.95, -0.4, 25.75], kind="corr", pid=None,
      note="东西贯通；西端短死端放伞柜", fill="#f1ede4"),
]

# 门: wall 'h'(沿X,z=line)/'v'(沿Z,x=line); pos=[a1,a2]; hinge=轴端坐标; swing=开启方向
DOORS = [
 dict(id="D-EW",  fl=2, wall="v", line=-22.0,  pos=[7.25, 8.75],  w=1.5, hinge=7.25, swing="+x", name="EXT-U-W西口/签收(外门)"),
 dict(id="D-EN",  fl=2, wall="h", line=6.0,    pos=[-5.3, -3.7], w=1.6, hinge=-5.3, swing="+z", name="EXT-U-N北口/短廊(外门)"),
 dict(id="D-ES",  fl=2, wall="h", line=24.0,   pos=[-5.9, -4.1], w=1.8, hinge=-5.9, swing="+z", name="EXT-U-S露台玻璃门(外门,外开不占室内——V02变更R4.3)"),
 dict(id="D-U01a",fl=2, wall="v", line=-18.6,  pos=[8.0, 8.9],   w=0.9, hinge=8.0,  swing="+x", name="签收前室→客廊纵巷"),
 dict(id="D-U13a",fl=2, wall="h", line=17.9,   pos=[-21.0, -20.15],w=0.85,hinge=-21.0, swing="-z", name="生活储藏A←主廊"),
 dict(id="D-U05a",fl=2, wall="v", line=-14.45, pos=[8.0, 8.9],   w=0.9, hinge=8.0,  swing="-x", name="普通客房A←客廊(反锁)"),
 dict(id="D-U13b",fl=2, wall="v", line=-14.45, pos=[15.3, 16.15],w=0.85,hinge=15.3, swing="+x", name="生活储藏B←客廊"),
 dict(id="D-U07a",fl=2, wall="v", line=-12.5,  pos=[8.0, 8.9],   w=0.9, hinge=8.0,  swing="-x", name="普通客房B←客廊(反锁)"),
 dict(id="D-U13c",fl=2, wall="v", line=-12.5,  pos=[15.3, 16.15],w=0.85,hinge=15.3, swing="+x", name="生活储藏C←客廊"),
 dict(id="D-U06a",fl=2, wall="v", line=-5.55,  pos=[8.0, 8.85],  w=0.85,hinge=8.0,  swing="+x", name="公卫→过厅"),
 dict(id="D-U21a",fl=2, wall="h", line=20.15,  pos=[-16.9, -15.95],w=0.95,hinge=-16.9, swing="+z", name="庄颜客房套间入口(门斗)"),
 dict(id="D-U21b",fl=2, wall="v", line=-17.4,  pos=[20.6, 21.45],w=0.85,hinge=20.6, swing="-x", name="门斗→庄颜客房寝(反锁)"),
 dict(id="D-U23a",fl=2, wall="h", line=21.7,   pos=[-17.0, -16.25],w=0.75,hinge=-17.0, swing="+z", name="门斗→客房厕洗"),
 dict(id="D-U40a",fl=2, wall="v", line=-8.4,   pos=[18.4, 19.45],w=1.05,hinge=19.45, swing="+x", name="主廊→小起居室(1.05搀扶宽)"),
 dict(id="D-LW",  fl=1, wall="v", line=-27.0,  pos=[29.4, 30.6], w=1.2, hinge=29.4, swing="+x", name="EXT-L-W一楼西口(外门)"),
 dict(id="D-L10a",fl=1, wall="h", line=25.9,   pos=[-25.4, -24.5],w=0.9, hinge=-25.4, swing="+z", name="门厅→主廊"),
 dict(id="D-L11a",fl=1, wall="v", line=-22.2,  pos=[28.4, 29.3], w=0.9, hinge=29.3, swing="+x", name="门厅→餐厅"),
 dict(id="D-L12a",fl=1, wall="h", line=25.9,   pos=[-20.6, -19.7],w=0.9, hinge=-20.6, swing="-z", name="备餐间→主廊"),
 dict(id="D-L12b",fl=1, wall="h", line=27.4,   pos=[-19.2, -18.3],w=0.9, hinge=-19.2, swing="+z", name="备餐间→餐厅(传菜)"),
 dict(id="D-L13a",fl=1, wall="h", line=25.9,   pos=[-12.4, -11.5],w=0.9, hinge=-12.4, swing="+z", name="会客室→主廊"),
 dict(id="D-L14a",fl=1, wall="h", line=25.9,   pos=[-7.0, -6.1], w=0.9, hinge=-7.0, swing="+z", name="家庭起居→主廊"),
 dict(id="D-L19a",fl=1, wall="h", line=25.9,   pos=[-3.4, -2.55],w=0.9, hinge=-3.4, swing="+z", name="家庭书房→主廊"),
 dict(id="D-L02a",fl=1, wall="h", line=23.95,  pos=[-22.6, -21.7],w=0.9, hinge=-22.6, swing="-z", name="家务间→主廊"),
 dict(id="D-L04a",fl=1, wall="h", line=23.95,  pos=[-14.4, -13.5],w=0.9, hinge=-14.4, swing="-z", name="储物间→主廊"),
 dict(id="D-L15a",fl=1, wall="h", line=23.95,  pos=[-3.8, -2.9], w=0.9, hinge=-3.8, swing="-z", name="公卫→主廊"),
 dict(id="D-L16a",fl=1, wall="h", line=30.55,  pos=[-25.4, -24.55],w=0.85,hinge=-25.4, swing="+z", name="西储→门厅"),
 dict(id="D-L01w",fl=1, wall="v", line=-8.4,   pos=[21.2, 22.1], w=0.9, hinge=21.2, swing="+x", name="梯间→设备间(搬运)"),
]

OPENINGS = [
 dict(fl=2, wall="h", line=17.9,  pos=[-14.3, -12.5], name="客廊纵巷→主廊 开口1.8"),
 dict(fl=2, wall="h", line=17.9,  pos=[-5.4, -3.2], name="过厅→主廊 开口2.2"),
]

WINDOWS = [
 dict(id="W-V04", fl=2, wall="v", line=-22.0, pos=[8.95, 9.75],  name="签收值班窗0.8(V04修正,原W-W1与西口重叠)"),
 dict(id="W-W3",  fl=2, wall="v", line=-22.0, pos=[21.2, 22.6],  name="庄颜客房西窗(西南向阳)"),
 dict(id="W-S1",  fl=2, wall="h", line=24.0,  pos=[-20.6, -19.2],name="庄颜客房南窗(东南向阳)"),
 dict(id="W-S2",  fl=2, wall="h", line=24.0,  pos=[-16.9, -16.3],name="客房厕洗高窗"),
 dict(id="W-S5",  fl=2, wall="h", line=24.0,  pos=[-14.3, -13.1],name="画角南窗(东南向阳,V01新增)"),
 dict(id="W-S3",  fl=2, wall="h", line=24.0,  pos=[-7.75, -6.25],name="起居湖景窗(对写生草地)"),
 dict(id="W-S4",  fl=2, wall="h", line=24.0,  pos=[-3.6, -1.2],  name="起居南大窗(东南向阳)"),
 dict(id="W-E1",  fl=2, wall="v", line=0.0,   pos=[20.4, 21.8],  name="起居东窗(东北)"),
 dict(id="W-E2",  fl=2, wall="v", line=0.0,   pos=[10.0, 11.4],  name="活动阅读东窗(东北,漫射光)"),
 dict(id="W-GAw", fl=2, wall="v", line=-22.0, pos=[18.75, 19.85],name="主廊西端窗(西南向阳,42-L窗前位)"),
 dict(id="W-N1",  fl=2, wall="h", line=6.0,   pos=[-20.9, -19.7],name="签收前室北窗(西北)"),
 dict(id="W-N2a", fl=2, wall="h", line=6.0,   pos=[-17.5, -16.1],name="客房A北窗(西北,朝向受限记录)"),
 dict(id="W-N2b", fl=2, wall="h", line=6.0,   pos=[-11.4, -10.0],name="客房B北窗(西北,朝向受限记录)"),
 dict(id="W-N4",  fl=2, wall="h", line=6.0,   pos=[-7.5, -6.6],  name="公卫北高窗"),
 dict(id="W-L10a",fl=1, wall="v", line=-27.0, pos=[27.0, 28.2],  name="门厅西窗(西南)"),
 dict(id="W-L16a",fl=1, wall="h", line=34.0,  pos=[-25.4, -24.2],name="西储南窗(东南)"),
 dict(id="W-L11a",fl=1, wall="h", line=34.0,  pos=[-20.3, -18.7],name="餐厅南窗a(东南向阳,避VC5)"),
 dict(id="W-L11b",fl=1, wall="h", line=34.0,  pos=[-17.8, -16.2],name="餐厅南窗b(东南向阳)"),
 dict(id="W-L13a",fl=1, wall="h", line=34.0,  pos=[-13.0, -11.4],name="会客南窗a(东南向阳)"),
 dict(id="W-L13b",fl=1, wall="h", line=34.0,  pos=[-10.4, -8.8], name="会客南窗b(东南向阳)"),
 dict(id="W-L14a",fl=1, wall="h", line=34.0,  pos=[-7.4, -5.8],  name="起居南窗a(东南向阳)"),
 dict(id="W-L14b",fl=1, wall="h", line=34.0,  pos=[-5.5, -4.7],  name="起居南窗b(东南向阳)"),
 dict(id="W-L19a",fl=1, wall="h", line=34.0,  pos=[-3.4, -2.2],  name="书房南窗(东南向阳)"),
 dict(id="W-L19b",fl=1, wall="v", line=0.0,   pos=[30.4, 31.6],  name="书房东窗(东北)"),
]

FURN = [
 dict(fl=2, kind="bed",   rect=[-21.45, 20.6, -19.45, 21.8], label="床2.0×1.2"),
 dict(fl=2, kind="desk",  rect=[-19.0, 23.0, -17.7, 23.5],   label="写字台"),
 dict(fl=2, kind="ward",  rect=[-21.45, 22.75, -20.25, 23.45],label="衣柜"),
 dict(fl=2, kind="bench", rect=[-16.9, 20.3, -16.0, 20.6],   label="换鞋凳"),
 dict(fl=2, kind="sofa",  rect=[-7.7, 22.5, -5.9, 23.4],     label="沙发(可躺)"),
 dict(fl=2, kind="chair", rect=[-7.2, 20.5, -6.4, 21.3],     label="扶手椅"),
 dict(fl=2, kind="table", rect=[-7.0, 21.7, -6.0, 22.3],     label="茶几(水杯)"),
 dict(fl=2, kind="screen",rect=[-5.6, 18.15, -5.45, 19.35],  label="墙屏"),
 dict(fl=2, kind="counter",rect=[-8.2, 20.6, -7.8, 21.8],    label="水吧台"),
 dict(fl=2, kind="bed",   rect=[-18.2, 6.7, -17.0, 8.7],     label="床1.2×2.0"),
 dict(fl=2, kind="ward",  rect=[-15.0, 6.7, -14.55, 7.9],    label="衣柜"),
 dict(fl=2, kind="bed",   rect=[-12.1, 6.7, -10.9, 8.7],     label="床1.2×2.0"),
 dict(fl=2, kind="ward",  rect=[-8.8, 6.7, -8.35, 7.9],      label="衣柜"),
 dict(fl=2, kind="desk",  rect=[-2.8, 7.2, -1.8, 8.8],       label="阅读桌"),
 dict(fl=2, kind="box",   rect=[-16.9, 19.25, -16.0, 19.8],  label="放箱位(24-L)"),
 dict(fl=1, kind="dtable",rect=[-19.6, 29.4, -16.6, 31.4],   label="餐桌2.0×1.0"),
 dict(fl=1, kind="sideb", rect=[-21.8, 33.0, -19.0, 33.45],  label="餐边柜"),
 dict(fl=1, kind="sofa",  rect=[-13.9, 30.0, -12.1, 30.9],   label="三人沙发"),
 dict(fl=1, kind="table", rect=[-13.0, 28.8, -12.0, 29.4],   label="茶几"),
 dict(fl=1, kind="chair", rect=[-13.3, 27.4, -12.5, 28.2],   label="单椅"),
 dict(fl=1, kind="chair", rect=[-11.2, 27.4, -10.4, 28.2],   label="单椅"),
 dict(fl=1, kind="sofa",  rect=[-7.7, 28.2, -6.8, 30.0],     label="沙发"),
 dict(fl=1, kind="table", rect=[-6.4, 28.6, -5.4, 29.2],     label="茶几"),
 dict(fl=1, kind="desk",  rect=[-3.9, 31.8, -2.7, 33.4],     label="书桌"),
 dict(fl=1, kind="ward",  rect=[-0.95, 26.3, -0.5, 28.7],    label="书架墙"),
]

CHIMNEYS = [
 dict(id="VC3", fl=1, draw_fls=(1,2), center=[-20.0, 20.0], half=0.45, top=30.8, status="候选·维持原位(未接受)",
      note="一楼家务间炊事铁炉；穿二楼客房寝北角(壁炉候选)"),
 dict(id="VC4", fl=1, draw_fls=(1,), center=[-10.0, 20.0], half=0.45, top=30.8, status="候选·维持原位(未接受)",
      note="一楼梯间北端采暖炉候选；二楼段穿主梯洞口北栏板候选(X -10.45~-9.55)，需结构/烟道复核"),
 dict(id="VC5", fl=1, draw_fls=(1,), center=[-21.6, 32.6], half=0.45, top=25.8,
      status="候选·调整(原(-20,30)；上轮(-21.3,32.6)未接受)",
      note="餐厅西墙南端壁炉候选；top25.8穿一楼南带天面"),
 dict(id="VC6", fl=2, draw_fls=(2,), center=[-6.85, 6.0], half=0.45, top=30.8,
      status="候选·调整(原(-6,12))",
      note="二楼公卫·清洁北墙热水炉候选(供全层热水)；芯半凸北墙外立24m坡地平台"),
]

STAIR = dict(
    zone=[-12.0, 20.0, -8.4, 24.0],
    west_run=[-12.0, 20.1, -10.3, 22.35],
    east_run=[-10.3, 20.1, -8.6, 22.35],
    mid_land=[-12.0, 22.35, -8.4, 23.9],
    steps_per_run=9, riser=0.178, tread=0.25, run_w=1.7,
    level_lo=20.8, level_hi=24.0,
    opening2=[-12.0, 20.0, -8.4, 24.0],
    note="U形双跑18级；西移4m为未接受候选，需结构/烟道/走位复核")

FURN = [
 dict(fl=2, kind="bed",   rect=[-21.45, 20.6, -19.45, 21.8], label="床2.0×1.2"),
 dict(fl=2, kind="desk",  rect=[-19.0, 23.0, -17.7, 23.5],   label="写字台"),
 dict(fl=2, kind="ward",  rect=[-21.45, 22.75, -20.25, 23.45],label="衣柜"),
 dict(fl=2, kind="bench", rect=[-16.9, 20.3, -16.0, 20.6],   label="换鞋凳"),
 dict(fl=2, kind="sofa",  rect=[-7.7, 22.5, -5.9, 23.4],     label="沙发(可躺)"),
 dict(fl=2, kind="chair", rect=[-7.2, 20.5, -6.4, 21.3],     label="扶手椅"),
 dict(fl=2, kind="table", rect=[-7.0, 21.7, -6.0, 22.3],     label="茶几(水杯)"),
 dict(fl=2, kind="screen",rect=[-5.6, 18.15, -5.45, 19.35],  label="墙屏"),
 dict(fl=2, kind="counter",rect=[-8.2, 20.6, -7.8, 21.8],    label="水吧台"),
 dict(fl=2, kind="box",   rect=[-16.9, 19.25, -16.0, 19.8],  label="放箱位(24-L)"),
 dict(fl=1, kind="dtable",rect=[-19.6, 29.4, -16.6, 31.4],   label="餐桌2.0×1.0"),
 dict(fl=1, kind="sideb", rect=[-21.8, 33.0, -19.0, 33.45],  label="餐边柜"),
 dict(fl=1, kind="sofa",  rect=[-13.9, 30.0, -12.1, 30.9],   label="三人沙发"),
 dict(fl=1, kind="table", rect=[-13.0, 28.8, -12.0, 29.4],   label="茶几"),
 dict(fl=1, kind="chair", rect=[-13.3, 27.4, -12.5, 28.2],   label="单椅"),
 dict(fl=1, kind="chair", rect=[-11.2, 27.4, -10.4, 28.2],   label="单椅"),
 dict(fl=1, kind="sofa",  rect=[-7.7, 28.2, -6.8, 30.0],     label="沙发"),
 dict(fl=1, kind="table", rect=[-6.4, 28.6, -5.4, 29.2],     label="茶几"),
 dict(fl=1, kind="desk",  rect=[-3.9, 31.8, -2.7, 33.4],     label="书桌"),
 dict(fl=1, kind="ward",  rect=[-0.95, 26.3, -0.5, 28.7],    label="书架墙"),
]

# ---------------- 校验 ----------------
def rects_overlap(a, b, tol=0.001):
    return not (a[2] <= b[0]+tol or b[2] <= a[0]+tol or a[3] <= b[1]+tol or b[3] <= a[1]+tol)

def check():
    errs = []
    for fl in (1, 2):
        rs = [r for r in ROOMS if r["fl"]==fl]
        for i in range(len(rs)):
            for j in range(i+1, len(rs)):
                if rects_overlap(rs[i]["rect"], rs[j]["rect"]):
                    errs.append(f"[{fl}层] 重叠: {rs[i]['id']} × {rs[j]['id']}")
        area = sum((r["rect"][2]-r["rect"][0])*(r["rect"][3]-r["rect"][1]) for r in rs)
        env = 345.8 if fl==1 else 364.6
        print(f"  {fl}层 净面积 {area:.1f} / 净区 {env:.1f}（墙缝 {env-area:.1f}）")
    # 家具不压门扫掠粗查：家具不越房间界
    for f in FURN:
        for r in ROOMS:
            if r["fl"]==f["fl"]:
                a, b = f["rect"], r["rect"]
                if a[0]>=b[0]-0.01 and a[1]>=b[1]-0.01 and a[2]<=b[2]+0.01 and a[3]<=b[3]+0.01:
                    break
        else:
            errs.append(f"家具越界: {f['label']} {f['rect']} fl{f['fl']}")
    # 家具不重叠
    for i in range(len(FURN)):
        for j in range(i+1, len(FURN)):
            if FURN[i]["fl"]==FURN[j]["fl"] and rects_overlap(FURN[i]["rect"], FURN[j]["rect"]):
                errs.append(f"家具重叠: {FURN[i]['label']} × {FURN[j]['label']}")
    return errs

# ---------------- 渲染 ----------------
BASE = {2: dict(x0=258, z0=118, ox=-22.0, oz=6.0),
        1: dict(x0=203, z0=118, ox=-27.0, oz=20.0)}
def px(fl, x, z):
    b = BASE[fl]
    return b["x0"] + (x-b["ox"])*S, b["z0"] + (z-b["oz"])*S

def render(fl):
    W, H = 1000, 660
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">',
           f'<rect width="{W}" height="{H}" fill="#fafbfb"/>',
           '<style>text{font-family:"Noto Sans CJK SC",sans-serif;fill:#263746}'
           '.t{font-size:12px}.s{font-size:10px;fill:#5a6b76}.dim{font-size:10px;fill:#a77643}</style>']
    title = "场地v13 · V00分房R4.1(冻结+细化变更) · 新宅2层 · 楼面24m" if fl==2 else "场地v13 · V00分房R4.1(冻结+细化变更) · 新宅1层 · 楼面20.8m"
    out.append(f'<text x="30" y="34" font-size="21">{title}</text>')
    env = (-22.0, 6.0, 0.0, 24.0) if fl==2 else (-27.0, 20.0, 0.0, 34.0)
    ex1, ez1 = px(fl, env[0], env[1]); ex2, ez2 = px(fl, env[2], env[3])
    out.append(f'<rect x="{ex1}" y="{ez1}" width="{ex2-ex1}" height="{ez2-ez1}" fill="#ffffff" stroke="#263746" stroke-width="3.2"/>')
    for r in ROOMS:
        if r["fl"] != fl: continue
        x1, z1, x2, z2 = r["rect"]
        ax1, az1 = px(fl, x1, z1); ax2, az2 = px(fl, x2, z2)
        out.append(f'<rect x="{ax1:.1f}" y="{az1:.1f}" width="{ax2-ax1:.1f}" height="{az2-az1:.1f}" fill="{r.get("fill","#fff")}" stroke="#8ea0ab" stroke-width="0.8"/>')
        cx, cz = (x1+x2)/2, (z1+z2)/2
        if r["id"] == "GA": cx = -20.3
        if r["id"] == "U11": cz += 0.9
        tx, tz = px(fl, cx, cz)
        nm = r["name"] + (f'[{r["pid"]}]' if r.get("pid") else "")
        fs = 11 if len(nm) <= 9 else 10
        out.append(f'<text x="{tx:.0f}" y="{tz-2:.0f}" text-anchor="middle" font-size="{fs}" fill="#3a4c58">{nm}</text>')
        sfs = 8.5 if (x2-x1)*(z2-z1) < 9 else 10
        out.append(f'<text x="{tx:.0f}" y="{tz+12:.0f}" text-anchor="middle" font-size="{sfs}" fill="#5a6b76">{r["id"]} {(x2-x1)*(z2-z1):.1f}㎡</text>')
    # 内墙缝
    rs = [r for r in ROOMS if r["fl"]==fl]
    for i in range(len(rs)):
        for j in range(i+1, len(rs)):
            a, b = rs[i]["rect"], rs[j]["rect"]
            for (ea, eb) in [(a,b),(b,a)]:
                if abs(ea[2]-eb[0]) < 0.02 and eb[1] < ea[3]-0.05 and ea[1] < eb[3]-0.05:
                    za, zb = max(ea[1], eb[1]), min(ea[3], eb[3])
                    p1 = px(fl, ea[2], za); p2 = px(fl, eb[0], zb)
                    out.append(f'<rect x="{p1[0]-1.5:.1f}" y="{p1[1]:.1f}" width="{(p2[0]-p1[0])+3:.1f}" height="{p2[1]-p1[1]:.1f}" fill="#607787"/>')
                if abs(ea[3]-eb[1]) < 0.02 and eb[0] < ea[2]-0.05 and ea[0] < eb[2]-0.05:
                    xa, xb = max(ea[0], eb[0]), min(ea[2], eb[2])
                    p1 = px(fl, xa, ea[3]); p2 = px(fl, xb, eb[1])
                    out.append(f'<rect x="{p1[0]:.1f}" y="{p1[1]-1.5:.1f}" width="{p2[0]-p1[0]:.1f}" height="{(p2[1]-p1[1])+3:.1f}" fill="#607787"/>')
    # 开口
    for op in OPENINGS:
        if op["fl"] != fl: continue
        if op["wall"]=="h":
            a1, b1 = px(fl, op["pos"][0], op["line"]); a2, b2 = px(fl, op["pos"][1], op["line"])
            out.append(f'<rect x="{a1:.1f}" y="{b1-1.6:.1f}" width="{a2-a1:.1f}" height="3.2" fill="#fafbfb"/>')
            out.append(f'<text x="{(a1+a2)/2:.0f}" y="{b1-5:.0f}" text-anchor="middle" font-size="8.5" fill="#286b88">{op["name"]}</text>')
    # 门（swing 显式）
    for d in DOORS:
        if d["fl"] != fl: continue
        w = d["w"]; pos = d["pos"]; sw = d["swing"]; hg = d["hinge"]
        if d["wall"]=="h":
            a1, b1 = px(fl, pos[0], d["line"]); a2, b2 = px(fl, pos[1], d["line"])
            out.append(f'<rect x="{a1:.1f}" y="{b1-2.2:.1f}" width="{a2-a1:.1f}" height="4.4" fill="#fafbfb"/>')
            # 轴点
            hx, hy = px(fl, hg, d["line"])
            # 闭位端(另一端)
            cx_ = pos[1] if hg == pos[0] else pos[0]
            clx, cly = px(fl, cx_, d["line"])
            # 开位端: 沿 swing 沿墙垂向
            dz = w if sw=="+z" else -w
            opx, opy = px(fl, hg, d["line"]+dz)
            out.append(f'<line x1="{hx:.1f}" y1="{hy:.1f}" x2="{opx:.1f}" y2="{opy:.1f}" stroke="#3593a0" stroke-width="2.4"/>')
            rr = abs(cly-hy)
            # 弧方向: 从闭位端到开位端
            flg = 0 if (sw=="+z") == (hg==pos[0]) else 1
            out.append(f'<path d="M {clx:.1f} {cly:.1f} A {rr:.1f} {rr:.1f} 0 0 {flg} {opx:.1f} {opy:.1f}" fill="none" stroke="#3593a0" stroke-width="0.8" stroke-dasharray="3 2.5"/>')
            out.append(f'<text x="{(a1+a2)/2:.0f}" y="{b1-5:.0f}" text-anchor="middle" font-size="8.5" fill="#3593a0">{d["id"]}</text>')
        else:
            a1, b1 = px(fl, d["line"], pos[0]); a2, b2 = px(fl, d["line"], pos[1])
            out.append(f'<rect x="{a1-2.2:.1f}" y="{b1:.1f}" width="4.4" height="{b2-b1:.1f}" fill="#fafbfb"/>')
            hx, hy = px(fl, d["line"], hg)
            cy_ = pos[1] if hg == pos[0] else pos[0]
            clx, cly = px(fl, d["line"], cy_)
            dx = w if sw=="+x" else -w
            opx, opy = px(fl, d["line"]+dx, hg)
            out.append(f'<line x1="{hx:.1f}" y1="{hy:.1f}" x2="{opx:.1f}" y2="{opy:.1f}" stroke="#3593a0" stroke-width="2.4"/>')
            rr = abs(clx-hx)
            flg = 0 if (sw=="+x") == (hg==pos[0]) else 1
            out.append(f'<path d="M {clx:.1f} {cly:.1f} A {rr:.1f} {rr:.1f} 0 0 {flg} {opx:.1f} {opy:.1f}" fill="none" stroke="#3593a0" stroke-width="0.8" stroke-dasharray="3 2.5"/>')
            out.append(f'<text x="{a1+6:.0f}" y="{(b1+b2)/2+3:.0f}" font-size="8.5" fill="#3593a0">{d["id"]}</text>')
    # 窗
    for wd in WINDOWS:
        if wd["fl"] != fl: continue
        pos = wd["pos"]
        if wd["wall"]=="h":
            a1, b1 = px(fl, pos[0], wd["line"]); a2, b2 = px(fl, pos[1], wd["line"])
            out.append(f'<rect x="{a1:.1f}" y="{b1-3:.1f}" width="{a2-a1:.1f}" height="6" fill="#cfe3ea" stroke="#3593a0" stroke-width="1.2"/>')
            out.append(f'<line x1="{a1:.1f}" y1="{b1:.1f}" x2="{a2:.1f}" y2="{b2:.1f}" stroke="#3593a0" stroke-width="0.7"/>')
        else:
            a1, b1 = px(fl, wd["line"], pos[0]); a2, b2 = px(fl, wd["line"], pos[1])
            out.append(f'<rect x="{a1-3:.1f}" y="{b1:.1f}" width="6" height="{b2-b1:.1f}" fill="#cfe3ea" stroke="#3593a0" stroke-width="1.2"/>')
            out.append(f'<line x1="{a1:.1f}" y1="{b1:.1f}" x2="{a2:.1f}" y2="{b2:.1f}" stroke="#3593a0" stroke-width="0.7"/>')
    # 烟囱
    for c in CHIMNEYS:
        if fl not in c["draw_fls"]: continue
        cx, cz = c["center"]; h = c["half"]
        p1 = px(fl, cx-h, cz-h); p2 = px(fl, cx+h, cz+h)
        out.append(f'<rect x="{p1[0]:.1f}" y="{p1[1]:.1f}" width="{p2[0]-p1[0]:.1f}" height="{p2[1]-p1[1]:.1f}" fill="#b8946a" stroke="#607787" stroke-width="1.6"/>')
        ly_ = p1[1]-4 if c["id"] in ("VC4","VC5") else p2[1]+11
        out.append(f'<text x="{(p1[0]+p2[0])/2:.0f}" y="{ly_:.0f}" text-anchor="middle" class="dim">{c["id"]}</text>')
    # 主梯
    if fl == 2:
        z = STAIR["zone"]
        p1 = px(fl, z[0], z[1]); p2 = px(fl, z[2], z[3])
        out.append(f'<rect x="{p1[0]:.1f}" y="{p1[1]:.1f}" width="{p2[0]-p1[0]:.1f}" height="{p2[1]-p1[1]:.1f}" fill="none" stroke="#a77643" stroke-width="2" stroke-dasharray="6 4"/>')
        ml = STAIR["mid_land"]
        p1 = px(fl, ml[0], ml[1]); p2 = px(fl, ml[2], ml[3])
        out.append(f'<rect x="{p1[0]:.1f}" y="{p1[1]:.1f}" width="{p2[0]-p1[0]:.1f}" height="{p2[1]-p1[1]:.1f}" fill="#e8dfd0" stroke="#8a7a5c" stroke-width="1"/>')
        tx_, ty_ = px(fl, -10.2, 23.35)
        out.append(f'<text x="{tx_:.0f}" y="{ty_:.0f}" text-anchor="middle" font-size="9" fill="#7a6a4c">中间平台 22.4m</text>')
        for run, base_z, n, up in [(STAIR["west_run"], 22.35, 9, True), (STAIR["east_run"], 20.1, 9, False)]:
            t = STAIR["tread"]
            for k in range(1, n+1):
                zz = base_z - k*t if up else base_z + k*t
                a1, b1 = px(fl, run[0], zz); a2, b2 = px(fl, run[2], zz)
                out.append(f'<line x1="{a1:.1f}" y1="{b1:.1f}" x2="{a2:.1f}" y2="{b2:.1f}" stroke="#8a7a5c" stroke-width="0.8"/>')
            mx = (run[0]+run[2])/2
            ax_, ay_ = px(fl, mx, base_z - 0.35 if up else base_z + 0.35)
            bx_, by_ = px(fl, mx, base_z - 1.15 if up else base_z + 1.15)
            out.append(f'<line x1="{ax_:.1f}" y1="{ay_:.1f}" x2="{bx_:.1f}" y2="{by_:.1f}" stroke="#a77643" stroke-width="1.2"/>')
            tx_, ty_ = px(fl, mx, 21.5 if up else 21.5)
            out.append(f'<text x="{tx_:.0f}" y="{ty_+8:.0f}" text-anchor="middle" font-size="9" fill="#7a6a4c">{"西跑↑" if up else "东跑↓"}</text>')
        a1, b1 = px(fl, -12.0, 20.0); a2, b2 = px(fl, -8.4, 20.0)
        out.append(f'<line x1="{a1:.1f}" y1="{b1:.1f}" x2="{a2:.1f}" y2="{b2:.1f}" stroke="#a77643" stroke-width="3"/>')
        tx_, ty_ = px(fl, -13.1, 19.35)
        out.append(f'<text x="{tx_:.0f}" y="{ty_:.0f}" font-size="9" fill="#a77643">梯口栏杆＝楼梯边缘(24-L)</text>')
        # VC4二楼段栏板
        a1, b1 = px(fl, -10.45, 20.0); a2, b2 = px(fl, -9.55, 20.0)
        out.append(f'<rect x="{a1:.1f}" y="{b1-3:.1f}" width="{a2-a1:.1f}" height="10" fill="#b8946a" stroke="#607787" stroke-width="1.2"/>')
        out.append(f'<text x="{(a1+a2)/2:.0f}" y="{b1-6:.0f}" text-anchor="middle" class="dim">VC4二楼段(栏板含烟道)</text>')
    if fl == 1:
        z = STAIR["zone"]
        p1 = px(fl, z[0], z[1]); p2 = px(fl, z[2], z[3])
        out.append(f'<rect x="{p1[0]:.1f}" y="{p1[1]:.1f}" width="{p2[0]-p1[0]:.1f}" height="{p2[1]-p1[1]:.1f}" fill="#efe8da" stroke="#8a7a5c" stroke-width="1.4"/>')
        tx_, ty_ = px(fl, -10.2, 22.2)
        out.append(f'<text x="{tx_:.0f}" y="{ty_:.0f}" text-anchor="middle" font-size="9.5" fill="#7a6a4c">主梯体</text>')
        tx_, ty_ = px(fl, -10.2, 23.1)
        out.append(f'<text x="{tx_:.0f}" y="{ty_:.0f}" text-anchor="middle" font-size="9" fill="#7a6a4c">(上方为洞口)</text>')
        for run, base_z, n, up in [(STAIR["west_run"], 22.35, 9, True), (STAIR["east_run"], 20.1, 9, False)]:
            t = STAIR["tread"]
            for k in range(1, n+1):
                zz = base_z - k*t if up else base_z + k*t
                a1, b1 = px(fl, run[0], zz); a2, b2 = px(fl, run[2], zz)
                out.append(f'<line x1="{a1:.1f}" y1="{b1:.1f}" x2="{a2:.1f}" y2="{b2:.1f}" stroke="#b0a284" stroke-width="0.6"/>')
    # 家具
    for f in FURN:
        if f["fl"] != fl: continue
        x1, z1, x2, z2 = f["rect"]
        ax1, az1 = px(fl, x1, z1); ax2, az2 = px(fl, x2, z2)
        col = {"bed":"#d9c9e8","desk":"#c9d7e8","ward":"#c9d7e8","sofa":"#c9e8d1","chair":"#c9e8d1",
               "table":"#e8d9c9","dtable":"#e8c9a9","screen":"#aab6bf","hearth":"#b8946a","bench":"#e0d9c9",
               "sideb":"#e0d9c9","box":"#f0d9a0","counter":"#d8cfc0"}.get(f["kind"], "#dddddd")
        out.append(f'<rect x="{ax1:.1f}" y="{az1:.1f}" width="{ax2-ax1:.1f}" height="{az2-az1:.1f}" fill="{col}" stroke="#7d8b94" stroke-width="0.8" rx="2"/>')
        lx, lz = (ax1+ax2)/2, (az1+az2)/2
        vertical = (ax2-ax1) < (az2-az1)*0.75 and (az2-az1) > 30
        tr = f'transform="rotate(-90 {lx:.0f} {lz:.0f})"' if vertical else ''
        out.append(f'<text x="{lx:.0f}" y="{lz+3:.0f}" text-anchor="middle" font-size="8.5" fill="#4a5a66" {tr}>{f["label"]}</text>')
    ly = ez2 + 46
    out.append(f'<text x="30" y="{ly}" class="s">房间色块＝净空（缝0.15＝内隔墙）；蓝＝门扇+扫掠/窗；棕＝烟囱芯0.9×0.9；家具＝剧情硬性示意。</text>')
    out.append(f'<text x="30" y="{ly+20}" class="s">X向右/Z向下；heading=45°非正东西南。北带(一层z20.4-23.8)承土无窗。{"" if fl==1 else "橙虚线＝主梯工作区调整候选原[-8,20,3.6,4]→[-12,20,3.6,4]。"}</text>')
    out.append('</svg>')
    return "\n".join(out)

if __name__ == "__main__":
    print("== 校验 ==")
    errs = check()
    for e in errs: print("  ERROR:", e)
    print("== 出图 ==")
    for fl in (2, 1):
        open(f"/tmp/v00_design/out/v00_draft_{fl}f.svg", "w").write(render(fl))
    print("  done")
