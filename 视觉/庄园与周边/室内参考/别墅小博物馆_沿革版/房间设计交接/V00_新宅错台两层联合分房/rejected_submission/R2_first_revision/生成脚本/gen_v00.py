#!/usr/bin/env python3
# V00 新宅错台两层联合分房 · 参数化设计与出图 v2
import json, math

S = 22.0          # px per meter
GAP = 0.15        # 内隔墙厚

ROOMS = [
 # ---- 二层 ----
 dict(id="U01", fl=2, name="签收前室", rect=[-21.6, 6.4, -18.6, 17.9],
      note="西口进门长条直通主廊；唯一馆务接口", fill="#e8eef2"),
 dict(id="U50", fl=2, name="家庭手作·活动", rect=[-18.45, 6.4, -13.55, 17.9],
      note="北墙2窗漫射光；内分手作区+材料储段(分期)", fill="#f0ede9"),
 dict(id="U10", fl=2, name="家务·布草", rect=[-13.4, 6.4, -9.9, 17.9],
      note="北窗；内分家务+储段(分期)", fill="#ece9f2"),
 dict(id="U06", fl=2, name="公卫·清洁", rect=[-9.75, 6.4, -7.35, 17.9],
      note="北高窗；内分卫+清洁段(分期)", fill="#e7f0ee"),
 dict(id="U03", fl=2, name="过厅(北口)", rect=[-7.2, 6.4, -3.65, 17.9],
      note="北口进门；内分门厅/前厅+衣帽储段(分期)", fill="#f1ede4"),
 dict(id="U04", fl=2, name="主卫·更衣", rect=[-3.35, 6.4, -0.4, 10.4],
      note="北高窗；主卧套内，门开寝", fill="#e7f0ee"),
 dict(id="U12", fl=2, name="主卧寝", rect=[-3.35, 10.55, -0.4, 17.9],
      note="东外墙2窗(上午阳)；南门进主廊", fill="#eef3e8"),
 dict(id="U21", fl=2, name="客房寝", rect=[-21.6, 20.15, -17.4, 23.6],
      note="V01细化；西+南外墙；壁炉芯VC3穿北角", fill="#f7ecec"),
 dict(id="U22", fl=2, name="客房门斗", rect=[-17.25, 20.15, -15.2, 21.55],
      note="套间入口；V01细化反锁/放箱", fill="#f7ecec"),
 dict(id="U23", fl=2, name="客房厕洗", rect=[-17.25, 21.7, -15.2, 23.6],
      note="南墙高窗", fill="#e7f0ee"),
 dict(id="U40", fl=2, name="小起居室(含水吧台)", rect=[-8.25, 18.05, -0.4, 23.6],
      note="V02细化；湖景窗W-S3+玻璃门EXT-U-S；水吧台家具级不设独立间", fill="#fdf6e3"),
 dict(id="GA", fl=2, name="主廊(客廊)", rect=[-21.6, 18.05, -8.4, 19.85], kind="corr",
      note="东西向；东端即起居室门与梯口", fill="#f1ede4"),
 # ---- 一层 ----
 dict(id="L02", fl=1, name="家务间(炊事炉VC3)", rect=[-26.6, 20.4, -19.5, 23.8],
      note="北墙承土无窗；VC3炊事铁炉", fill="#ece9f2"),
 dict(id="L04", fl=1, name="储物间", rect=[-19.35, 20.4, -12.15, 23.8],
      note="北墙承土；门开南墙进主廊", fill="#eceff1"),
 dict(id="L01", fl=1, name="梯间(主梯起步)", rect=[-12.0, 20.4, -8.4, 23.8],
      note="主梯起步平台+梯下储柜；VC4采暖炉候选", fill="#f3ece7"),
 dict(id="L05", fl=1, name="设备·储物", rect=[-8.25, 20.4, -4.9, 23.8],
      note="北墙承土；热泵分水器/管井端头", fill="#eceff1"),
 dict(id="L15", fl=1, name="公卫·清洁", rect=[-4.75, 20.4, -0.4, 23.8],
      note="北墙承土无窗；机械排气", fill="#e7f0ee"),
 dict(id="L10", fl=1, name="门厅", rect=[-26.6, 25.9, -22.2, 30.4],
      note="EXT-L-W进门；北门进主廊", fill="#f3ece7"),
 dict(id="L16", fl=1, name="西储·衣帽", rect=[-26.6, 30.55, -22.2, 33.6],
      note="门北进门厅；南墙窗", fill="#eceff1"),
 dict(id="L12", fl=1, name="备餐间", rect=[-22.05, 25.9, -14.2, 27.25],
      note="北门进主廊；南传菜口通餐厅；辅助无窗", fill="#e8eef2"),
 dict(id="L11", fl=1, name="家庭餐厅(V03)", rect=[-22.05, 27.4, -14.2, 33.6],
      note="南墙2窗向阳湖向；西墙南端壁炉VC5候选", fill="#fdf6e3"),
 dict(id="L13", fl=1, name="会客室", rect=[-14.05, 25.9, -8.0, 32.6],
      note="北门进主廊；南墙2窗向阳", fill="#eef3e8"),
 dict(id="L14", fl=1, name="家庭起居", rect=[-7.85, 25.9, -4.3, 33.6],
      note="北门进主廊；南墙2窗向阳", fill="#eef3e8"),
 dict(id="L19", fl=1, name="家庭卧室", rect=[-4.15, 25.9, -0.4, 33.6],
      note="南+东外墙均向阳；新宅第3卧(全组第3,老宅H9为第4)", fill="#eef3e8"),
 dict(id="GA-L", fl=1, name="主廊", rect=[-26.6, 23.95, -0.4, 25.75], kind="corr",
      note="东西贯通；西端短死端放伞柜", fill="#f1ede4"),
]

# 门: wall 'h'(沿X,z=line)/'v'(沿Z,x=line); pos=[a1,a2]; hinge=轴端坐标; swing=开启方向
DOORS = [
 dict(id="D-EW",  fl=2, wall="v", line=-22.0,  pos=[7.25, 8.75],  w=1.5, hinge=7.25, swing="+x", name="EXT-U-W西口/签收(外门)"),
 dict(id="D-EN",  fl=2, wall="h", line=6.0,    pos=[-5.3, -3.7], w=1.6, hinge=-5.3, swing="+z", name="EXT-U-N北口/短廊(外门)"),
 dict(id="D-ES",  fl=2, wall="h", line=24.0,   pos=[-5.9, -4.1], w=1.8, hinge=-5.9, swing="-z", name="EXT-U-S露台玻璃门(外门)"),
 dict(id="D-U01a",fl=2, wall="h", line=17.9,   pos=[-21.45, -20.55], w=0.95, hinge=-20.55, swing="-z", name="签收前室→主廊"),
 dict(id="D-U50a",fl=2, wall="h", line=17.9,   pos=[-16.6, -15.65], w=0.95, hinge=-15.65, swing="+z", name="家庭手作→主廊"),
 dict(id="D-U10a",fl=2, wall="h", line=17.9,   pos=[-12.3, -11.4], w=0.9, hinge=-12.3, swing="+z", name="家务间→主廊"),
 dict(id="D-U06a",fl=2, wall="h", line=17.9,   pos=[-9.2, -8.45], w=0.75, hinge=-9.2, swing="+z", name="公卫→主廊"),
 dict(id="D-U04a",fl=2, wall="h", line=10.55,  pos=[-3.0, -2.15], w=0.85, hinge=-3.0, swing="-z", name="主卫←主卧寝"),
 dict(id="D-U12a",fl=2, wall="h", line=17.9,   pos=[-2.9, -1.9], w=1.0, hinge=-2.9, swing="+z", name="主卧寝→主廊"),
 dict(id="D-U21a",fl=2, wall="h", line=20.15,  pos=[-16.9, -15.95],w=0.95,hinge=-16.9, swing="+z", name="客房套间入口(门斗)"),
 dict(id="D-U21b",fl=2, wall="v", line=-17.4,  pos=[20.6, 21.45],w=0.85,hinge=20.6, swing="-x", name="门斗→客房寝"),
 dict(id="D-U23a",fl=2, wall="h", line=21.7,   pos=[-17.0, -16.25],w=0.75,hinge=-17.0, swing="+z", name="门斗→客房厕洗"),
 dict(id="D-U40a",fl=2, wall="v", line=-8.4,   pos=[18.5, 19.45],w=0.95,hinge=19.45, swing="+x", name="主廊→小起居室"),
 dict(id="D-LW",  fl=1, wall="v", line=-27.0,  pos=[29.4, 30.6], w=1.2, hinge=29.4, swing="+x", name="EXT-L-W一楼西口(外门)"),
 dict(id="D-L10a",fl=1, wall="h", line=25.9,   pos=[-25.4, -24.5],w=0.9, hinge=-25.4, swing="+z", name="门厅→主廊"),
 dict(id="D-L11a",fl=1, wall="v", line=-22.2,  pos=[28.4, 29.3], w=0.9, hinge=29.3, swing="+x", name="门厅→餐厅"),
 dict(id="D-L12a",fl=1, wall="h", line=25.9,   pos=[-20.6, -19.7],w=0.9, hinge=-20.6, swing="-z", name="备餐间→主廊"),
 dict(id="D-L12b",fl=1, wall="h", line=27.4,   pos=[-19.2, -18.3],w=0.9, hinge=-19.2, swing="+z", name="备餐间→餐厅(传菜)"),
 dict(id="D-L13a",fl=1, wall="h", line=25.9,   pos=[-12.4, -11.5],w=0.9, hinge=-12.4, swing="+z", name="会客室→主廊"),
 dict(id="D-L14a",fl=1, wall="h", line=25.9,   pos=[-7.0, -6.1], w=0.9, hinge=-7.0, swing="+z", name="家庭起居→主廊"),
 dict(id="D-L19a",fl=1, wall="h", line=25.9,   pos=[-3.4, -2.55],w=0.9, hinge=-3.4, swing="+z", name="家庭卧室→主廊"),
 dict(id="D-L02a",fl=1, wall="h", line=23.95,  pos=[-22.6, -21.7],w=0.9, hinge=-22.6, swing="-z", name="家务间→主廊"),
 dict(id="D-L04a",fl=1, wall="h", line=23.95,  pos=[-14.4, -13.5],w=0.9, hinge=-14.4, swing="-z", name="储物间→主廊"),
 dict(id="D-L15a",fl=1, wall="h", line=23.95,  pos=[-3.8, -2.9], w=0.9, hinge=-3.8, swing="-z", name="公卫→主廊"),
 dict(id="D-L16a",fl=1, wall="h", line=30.55,  pos=[-25.4, -24.55],w=0.85,hinge=-25.4, swing="+z", name="西储→门厅"),
 dict(id="D-L01w",fl=1, wall="v", line=-8.4,   pos=[21.2, 22.1], w=0.9, hinge=21.2, swing="+x", name="梯间→设备间(搬运)"),
]

OPENINGS = [
 dict(fl=2, wall="h", line=17.9,  pos=[-6.9, -4.4], name="过厅→主廊 开口2.5"),
]

WINDOWS = [
 dict(id="W-N1",  fl=2, wall="h", line=6.0,   pos=[-21.0, -19.8],name="签收前室北窗"),
 dict(id="W-N2a", fl=2, wall="h", line=6.0,   pos=[-17.7, -16.5],name="手作北窗a"),
 dict(id="W-N2b", fl=2, wall="h", line=6.0,   pos=[-15.6, -14.4],name="手作北窗b"),
 dict(id="W-N3",  fl=2, wall="h", line=6.0,   pos=[-12.6, -11.4],name="家务北窗"),
 dict(id="W-N4",  fl=2, wall="h", line=6.0,   pos=[-9.3, -8.4],  name="公卫北高窗"),
 dict(id="W-N5",  fl=2, wall="h", line=6.0,   pos=[-7.0, -6.0],  name="过厅北窗"),
 dict(id="W-N6",  fl=2, wall="h", line=6.0,   pos=[-2.8, -1.8],  name="主卫北高窗"),
 dict(id="W-W3",  fl=2, wall="v", line=-22.0, pos=[21.2, 22.6],  name="客房寝西窗(下午晒)"),
 dict(id="W-S1",  fl=2, wall="h", line=24.0,  pos=[-20.6, -19.2],name="客房寝南窗(向阳)"),
 dict(id="W-S2",  fl=2, wall="h", line=24.0,  pos=[-16.9, -16.3],name="客房厕洗高窗"),
 dict(id="W-S3",  fl=2, wall="h", line=24.0,  pos=[-7.75, -6.25],name="起居湖景窗(对写生草地)"),
 dict(id="W-S4",  fl=2, wall="h", line=24.0,  pos=[-3.6, -1.2],  name="起居南大窗"),
 dict(id="W-E1",  fl=2, wall="v", line=0.0,   pos=[20.4, 21.8],  name="起居东窗"),
 dict(id="W-E2a", fl=2, wall="v", line=0.0,   pos=[14.5, 15.9],  name="主卧东窗a(上午阳)"),
 dict(id="W-E2b", fl=2, wall="v", line=0.0,   pos=[16.3, 17.7],  name="主卧东窗b(上午阳)"),
 dict(id="W-L10a",fl=1, wall="v", line=-27.0, pos=[27.0, 28.2],  name="门厅西窗"),
 dict(id="W-L16a",fl=1, wall="h", line=34.0,  pos=[-25.4, -24.2],name="西储南窗"),
 dict(id="W-L11a",fl=1, wall="h", line=34.0,  pos=[-20.3, -18.7],name="餐厅南窗a(避VC5)"),
 dict(id="W-L11b",fl=1, wall="h", line=34.0,  pos=[-17.8, -16.2],name="餐厅南窗b"),
 dict(id="W-L13a",fl=1, wall="h", line=34.0,  pos=[-13.0, -11.4],name="会客南窗a"),
 dict(id="W-L13b",fl=1, wall="h", line=34.0,  pos=[-10.4, -8.8], name="会客南窗b"),
 dict(id="W-L14a",fl=1, wall="h", line=34.0,  pos=[-7.4, -5.8],  name="起居南窗a"),
 dict(id="W-L14b",fl=1, wall="h", line=34.0,  pos=[-5.5, -4.7],  name="起居南窗b"),
 dict(id="W-L19a",fl=1, wall="h", line=34.0,  pos=[-3.4, -2.2],  name="卧室南窗(向阳)"),
 dict(id="W-L19b",fl=1, wall="v", line=0.0,   pos=[30.4, 31.6],  name="卧室东窗(上午阳)"),
]

CHIMNEYS = [
 dict(id="VC3", fl=1, draw_fls=(1,2), center=[-20.0, 20.0], half=0.45, top=30.8, status="候选·维持原位(未接受)",
      note="一楼家务间炊事铁炉；穿二楼客房寝北角(壁炉候选)"),
 dict(id="VC4", fl=1, draw_fls=(1,2), center=[-10.0, 20.0], half=0.45, top=30.8, status="候选·维持原位(未接受)",
      note="一楼梯间北端采暖炉候选；二楼段穿主梯洞口北栏板候选(X -10.45~-9.55)，需结构/烟道复核"),
 dict(id="VC5", fl=1, draw_fls=(1,), center=[-21.6, 32.6], half=0.45, top=25.8,
      status="候选·调整(原(-20,30)；上轮(-21.3,32.6)未接受)",
      note="餐厅西墙南端壁炉候选；top25.8穿一楼南带天面"),
 dict(id="VC6", fl=2, draw_fls=(2,), center=[-11.6, 6.0], half=0.45, top=30.8,
      status="候选·调整(原(-6,12)落主卧套区)",
      note="二楼家务间北墙热水炉候选；芯半凸北墙外立24m坡地平台"),
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
 dict(fl=2, kind="desk",  rect=[-18.2, 7.0, -14.0, 8.0],     label="手作大台"),
 dict(fl=2, kind="bed",   rect=[-3.1, 14.0, -1.9, 16.0],     label="床1.2×2.0"),
 dict(fl=2, kind="desk",  rect=[-1.0, 16.6, -0.5, 17.7],     label="书写角"),
 dict(fl=2, kind="box",   rect=[-16.9, 19.25, -16.0, 19.8],  label="放箱位(24-L)"),
 dict(fl=1, kind="dtable",rect=[-19.6, 29.4, -16.6, 31.4],   label="餐桌2.0×1.0"),
 dict(fl=1, kind="sideb", rect=[-21.8, 33.0, -19.0, 33.45],  label="餐边柜"),
 dict(fl=1, kind="sofa",  rect=[-13.9, 30.0, -12.1, 30.9],   label="三人沙发"),
 dict(fl=1, kind="table", rect=[-13.0, 28.8, -12.0, 29.4],   label="茶几"),
 dict(fl=1, kind="chair", rect=[-13.3, 27.4, -12.5, 28.2],   label="单椅"),
 dict(fl=1, kind="chair", rect=[-11.2, 27.4, -10.4, 28.2],   label="单椅"),
 dict(fl=1, kind="sofa",  rect=[-7.7, 28.2, -6.8, 30.0],     label="沙发"),
 dict(fl=1, kind="table", rect=[-6.4, 28.6, -5.4, 29.2],     label="茶几"),
 dict(fl=1, kind="bed",   rect=[-1.9, 30.8, -0.7, 32.8],     label="床1.2×2.0"),
 dict(fl=1, kind="ward",  rect=[-4.0, 26.2, -2.8, 26.8],     label="衣柜"),
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
    title = "场地v13 · V00分房R2(重做) · 新宅2层 · 楼面24m" if fl==2 else "场地v13 · V00分房R2(重做) · 新宅1层 · 楼面20.8m"
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
        nm = r["name"]
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
