#!/usr/bin/env python3
# V00 交付：回写 边界门洞与炉位.json（rooms/doors/windows/chimneys/hearths/stair/变更清单）
import json, sys, copy
sys.path.insert(0, '/tmp/v00_design')
import gen_v00 as G

BASE = "/mnt/Data/Program Files (x86)/ZhuangYanContract/companion.compile/视觉/庄园与周边/室内参考/别墅小博物馆_沿革版/房间设计交接/V00_新宅错台两层联合分房"
SRC = f"{BASE}/边界门洞与炉位.json"

d = json.load(open(SRC))
# 输入备份
json.dump(d, open(f"{BASE}/边界门洞与炉位.v13输入备份.json", "w"), ensure_ascii=False, indent=2)

def room_out(r):
    x1, z1, x2, z2 = r["rect"]
    return dict(id=r["id"], floor=r["fl"], level=(24 if r["fl"]==2 else 20.8),
                name=r["name"], rect=[x1, z1, x2, z2],
                net_area=round((x2-x1)*(z2-z1), 1), note=r.get("note", ""))

def door_out(dd):
    return dict(id=dd["id"], floor=dd["fl"], wall_axis=dd["wall"],
                wall_line=dd["line"], opening=[dd["pos"][0], dd["pos"][1]],
                width=dd["w"], hinge_at=dd["hinge"], swing=dd["swing"],
                name=dd["name"], sweep="90°内开(扇+扫掠见V00隔墙图)")

rooms = [room_out(r) for r in G.ROOMS]
doors = [door_out(x) for x in G.DOORS]
openings = [dict(floor=o["fl"], wall_axis=o["wall"], wall_line=o["line"],
                 opening=[o["pos"][0], o["pos"][1]], name=o["name"]) for o in G.OPENINGS]
windows = [dict(id=w["id"], floor=w["fl"], wall_axis=w["wall"], wall_line=w["line"],
                opening=[w["pos"][0], w["pos"][1]], name=w["name"],
                sill="高窗0.6" if "高窗" in w["name"] else "0.9", note="详见V00隔墙图窗符号")
           for w in G.WINDOWS]

HEARTHS_BY_VC = {}
HEARTHS = [
 dict(id="H-V00-01", chimney="VC3", floor=1, level=20.8, center=[-20.0, 20.75], kind="炊事铁炉",
      room="L02家务间", note="北墙芯南侧炉体；独立烟道接VC3（旧铁炉期用，改馆后可冷态保留）"),
 dict(id="H-V00-02", chimney="VC3", floor=2, level=24.0, center=[-20.0, 20.4], kind="客房壁炉",
      room="U21客房寝东北角", note="芯上半嵌寝室东北角壁炉；与一楼炊事炉各自独立烟道汇入VC3砖芯"),
 dict(id="H-V00-03", chimney="VC4", floor=1, level=20.8, center=[-10.0, 20.75], kind="采暖铁炉",
      room="L01梯间北端", note="起步厅旁采暖炉；烟道沿芯上行，二楼段穿主梯洞口北栏板(X -10.45~-9.55)"),
 dict(id="H-V00-04", chimney="VC5", floor=1, level=20.8, center=[-21.3, 32.6], kind="餐厅壁炉",
      room="L11家庭餐厅西南角", note="芯嵌餐厅西南角；top25.8穿一楼南带天面"),
 dict(id="H-V00-05", chimney="VC6", floor=2, level=24.0, center=[-6.0, 12.0], kind="热水/采暖铁炉",
      room="U11茶水间西隔墙", note="供二楼热水与北翼采暖；芯嵌茶水间/纵廊隔墙"),
]
for h in HEARTHS:
    HEARTHS_BY_VC.setdefault(h["chimney"], []).append(dict(id=h["id"], kind=h["kind"], floor=h["floor"]))

chimneys = []
for c in G.CHIMNEYS:
    chimneys.append(dict(id=c["id"], center=c["center"], brick_half=c["half"], top=c["top"],
                         status=c["status"], hearths_served=HEARTHS_BY_VC.get(c["id"], []),
                         note=c["note"]))

stair = dict(
    id="ST-MAIN", type="U形双跑",
    zone=[-12.0, 20.0, -8.4, 24.0],
    zone_original=[-8.0, 20.0, -4.4, 24.0],
    zone_change="工作区调整候选：西移4m，仍在上下层重叠带(z20~24)内；原因见change_log",
    west_run=[-12.0, 20.1, -10.3, 22.35],
    east_run=[-10.3, 20.1, -8.6, 22.35],
    mid_landing=[-12.0, 22.35, -8.4, 23.9],
    steps=18, steps_per_run=9, riser=0.178, tread=0.25, run_width=1.7,
    level_low=20.8, level_high=24.0,
    opening_floor2=[-12.0, 20.0, -8.4, 24.0],
    railing_open_north=[-12.0, -10.3],
    railing_solid_north=[-10.3, -8.4],
    railing_solid_north_note="北栏板实段含VC4二楼段烟道",
    mid_landing_headroom="上方开洞贯通至屋面结构底(≈26.8)，净高≈4.4",
    arrival="二楼到达点z=20.1北缘(西跑顶)，跨入主廊GA；一楼起步点z=20.1(东跑底)，起步厅L01")

d["geometry_status"] = "V00已联合分房：rooms/doors/windows/hearths/stair为V00设计值；外门口扫掠已试排"
d["design_status"] = dict(
    v00_delivered="2026-11-07",
    deliverables=["V00隔墙图_一层.svg", "V00隔墙图_二层.svg", "V00主梯纵剖面.svg",
                  "V00房间与门窗表.json(本文件)", "V00交付说明.md"],
    next_tasks="V01—V05按本JSON房间ID与门表细化；V06/V07工业组不受影响")
d["rooms"] = rooms
d["doors"] = doors
d["openings_internal"] = openings
d["windows"] = windows
d["chimneys"] = chimneys
d["hearths"] = HEARTHS
d["stair"] = stair
d["change_log"] = [
 dict(item="主梯工作区", original=[-8.0, 20.0, -4.4, 24.0], revised=[-12.0, 20.0, -8.4, 24.0],
      reason="原位使z=24南墙x-5±0.9玻璃门与x-7湖景窗落入梯井，24-L『窗前→楼梯→沙发』动线无法同层连贯；西移后窗/门/梯口/沙发全部就位",
      impact="二楼洞口随之西移；一楼梯间移至x-12~-8.4，起步厅L01与两侧储物/设备间重排；重叠带(z20~24)内调整，未触碰包络与外门口"),
 dict(item="VC5烟囱芯", original=[-20.0, 30.0], revised=[-21.3, 32.6],
      reason="原位悬于餐厅中部天井；移至餐厅西南角嵌墙作壁炉，top25.8不变",
      impact="餐厅南墙窗位避让(西窗起于x-20.3)；一楼南带天面开孔随移"),
 dict(item="VC3/VC4/VC6", original="维持原位", revised="维持原位",
      reason="与新隔墙相容", impact="VC4二楼段以栏板烟道形式穿主梯洞口北缘(x-10.45~-9.55段加厚)"),
]

d["narrative_checks"] = [
 dict(scene="20-L", check="『别墅西翼有间独立客房』+『可以自己锁门』",
      verdict="通过", note="客房套间U21-U23居二楼西南角，西+南双向真实外墙（旧A6/A14无外墙缺陷不复现）；寝门D-U21b内开可反锁，套间入口D-U21a在主廊南墙"),
 dict(scene="24-L", check="搬箱两趟：门外放箱、箱子不挡门",
      verdict="通过", note="西口1.5→前室U01→西次廊1.8m→主廊1.8m；放箱位[-16.9,19.25,-16.0,19.8]在D-U21a门前，门扇内开不扫箱"),
 dict(scene="24-L", check="客房外门→走廊看湖窗→梯口→可躺沙发→小起居室→玻璃门→露台同层连贯",
      verdict="通过", note="主廊GA(净1.8m)东端即起居室门D-U40a；湖景窗W-S3(x-7.75~-6.25,z24)对写生草地；梯口栏杆开口正对西跑顶端；沙发[-7.7,22.5,-5.9,23.4]贴南窗（24-L232午后光落茶几）；玻璃门EXT-U-S接露台"),
 dict(scene="24-L", check="开门冲向梯口、撞怀、脚跟碰台阶、扶住扶手",
      verdict="通过", note="罗辑下梯处=西跑顶端(z20.1,x-12~-10.3)；栏杆开口[-12,-10.3]正对该处；客房门前x≈-16.4至梯口约5.4m，『这么长一段路』成立"),
 dict(scene="24-L", check="起居室和放映室共用片库、个人Agent接管播放设备；墙屏",
      verdict="通过", note="墙屏示意贴小起居室北墙(x-5.6)；放映室在旧版功能清单，V02细化口径"),
 dict(scene="24-L", check="『我也知道茶水间在哪儿』",
      verdict="通过", note="二楼茶水间U11在纵廊西邻，起居室经主廊-纵廊可达；水杯动线成立"),
 dict(scene="05-L", check="西翼归档室签收：门旁值班牌、合伞、玻璃窗望出",
      verdict="通过", note="二楼西口EXT-U-W进门即签收前室U01；值班窗/值班牌细节V04细化；后台移交经主廊-过厅-北口短廊至生产院，不穿居室"),
 dict(scene="20-L", check="靠湖的小餐厅、上菜后退出、离席拉腕让路",
      verdict="通过", note="餐厅L11净48.7㎡朝南两窗湖向；服务线=备餐间L12北门进主廊+传菜门D-L12b直入餐厅，不经主客动线；桌西门间过道2.45m，让路净空成立"),
 dict(scene="08-L", check="庄颜从西翼方向走到别墅门口",
      verdict="通过", note="客房下西跑→一楼梯间L01→主廊→门厅L10→西口EXT-L-W出园"),
 dict(scene="共同约束", check="四间可住卧室、庄颜普通客房非套房",
      verdict="通过", note="主卧U12(22.1)+客房寝U21(14.5)+客卧A U05(19.7)+客卧L19(16.1)=4间；客房套间含门斗厕洗共21.6㎡，未扩成套房"),
 dict(scene="共同约束", check="北侧承土不开景观窗；厕洗/旧铁炉/热泵分期保留",
      verdict="通过", note="一楼北带(z20.4~23.8)六间均无窗；VC3-VC6四芯各炉独立烟道；热泵房远置，宅内L05仅分水器/管井端头"),
]

json.dump(d, open(SRC, "w"), ensure_ascii=False, indent=2)
print("JSON written:", SRC)
print("rooms:", len(rooms), "doors:", len(doors), "windows:", len(windows), "hearths:", len(HEARTHS))
