#!/usr/bin/env python3
# V00 R2 提交：resubmission 写入边界门洞与炉位.json（schema 声明+逐室叙事+候选未接受标注）
import json, sys
sys.path.insert(0, '/tmp/v00_design')
import gen_v00 as G

BASE = "/mnt/Data/Program Files (x86)/ZhuangYanContract/companion.compile/视觉/庄园与周边/室内参考/别墅小博物馆_沿革版/房间设计交接/V00_新宅错台两层联合分房"
SRC = f"{BASE}/边界门洞与炉位.json"
d = json.load(open(SRC))

# ---- 逐室叙事（原用途→现代用途 / 所属 / 外墙朝向 / 入口与相邻） ----
ORIGIN = {
 "U01": dict(origin_use="西上门厅/门房", modern_use="签收·收发前室（新宅唯一馆务接口）",
             facade="西外墙(西南225°向)+北外墙(西北315°向)", entrance="EXT-U-W西口进门；东门D-U01a进客廊纵巷",
             adjacency="北：坡地平台/短廊方向；东：客廊纵巷；南：生活储藏A"),
 "U13a": dict(origin_use="门房储藏", modern_use="生活储藏A（收发暂存+家庭储，分期）",
             facade="无窗（辅助允许）", entrance="南门D-U13a进主廊", adjacency="北：签收前室；东：客房A套"),
 "GB2": dict(origin_use="走廊", modern_use="客廊纵巷（服务客房A/B与储段）", facade="无（交通）",
             entrance="南端开口接主廊；北端封端", adjacency="西：前室/客房A套；东：客房B套/储C"),
 "U05": dict(origin_use="原家庭卧室一", modern_use="普通客房A（G-A，留客可反锁）",
             facade="北外墙(西北315°，朝向受限记录：向阳墙带已让渡庄颜客房/起居)", entrance="东门D-U05a进客廊纵巷",
             adjacency="北：外墙；西：生活储藏A；东：客廊纵巷；南：套内厕洗收纳"),
 "U05b": dict(origin_use="原家庭卧室一附浴", modern_use="客房A厕洗·收纳（套内段）",
             facade="无窗（机械排气）", entrance="北门D-U05b开向寝", adjacency="北：客房A寝；南：生活储藏B"),
 "U13b": dict(origin_use="储物间", modern_use="生活储藏B", facade="无窗",
             entrance="东门D-U13b进客廊纵巷", adjacency="西：纵巷；北：客房A厕洗段"),
 "U07": dict(origin_use="原家庭卧室二", modern_use="普通客房B（G-B，留客可反锁）",
             facade="北外墙(西北315°，朝向受限记录同客房A)", entrance="西门D-U07a进客廊纵巷",
             adjacency="北：外墙；西：客廊纵巷；东：公卫；南：套内厕洗收纳"),
 "U07b": dict(origin_use="原家庭卧室二附浴", modern_use="客房B厕洗·收纳（套内段）",
             facade="无窗（机械排气）", entrance="北门开向寝", adjacency="北：客房B寝；东：家务·布草；南：生活储藏C"),
 "U13c": dict(origin_use="储物间", modern_use="生活储藏C", facade="无窗",
             entrance="西门D-U13c进客廊纵巷", adjacency="北：客房B厕洗段；西：纵巷"),
 "U06": dict(origin_use="厕浴/杂役间", modern_use="公卫·清洁（服务全层；VC6热水炉候选嵌北墙）",
             facade="北外墙(西北，高窗)", entrance="东门D-U06a进过厅", adjacency="西：客房B套；东：过厅"),
 "U10": dict(origin_use="家务房/布草间", modern_use="家务·布草（19.5㎡，机械排风）",
             facade="无窗（辅助允许）", entrance="南门D-U10a进主廊", adjacency="北：公卫；东：过厅"),
 "U03": dict(origin_use="后门厅/杂物间", modern_use="过厅（北口门厅+楼梯前厅，含衣帽储段，分期）",
             facade="北外墙(西北)+北口", entrance="EXT-U-N北口进门；南端开口2.2接主廊",
             adjacency="西：公卫/家务；东：活动·阅读"),
 "U50": dict(origin_use="家庭活动室/书房", modern_use="家庭活动·阅读（家庭阅读/手作功能落点之一）",
             facade="东外墙(东北45°，漫射光记录)", entrance="南门进主廊", adjacency="西：过厅；南：主廊"),
 "U21": dict(origin_use="原建普通客房", modern_use="庄颜普通客房（G-ZY，留客可反锁，由庄颜占用）",
             facade="西外墙(西南225°向阳)+南外墙(东南135°向阳)双向阳", entrance="经门斗D-U21a/D-U21b",
             adjacency="东：门斗；北：主廊西端与VC3芯角"),
 "U22": dict(origin_use="客房前室", modern_use="客房门斗（V01细化反锁/放箱组织）",
             facade="无外墙（套内缓冲，允许）", entrance="北门D-U21a进自主廊", adjacency="北：主廊；西/南：寝；南：厕洗"),
 "U23": dict(origin_use="客房厕浴", modern_use="庄颜客房专用厕洗",
             facade="南外墙(东南，高窗)", entrance="门D-U23a开向门斗", adjacency="北：门斗"),
 "U40": dict(origin_use="二楼家庭起居", modern_use="家庭小起居室（含水吧台，24-L剧情厅）",
             facade="南外墙(东南135°向阳，湖景)+东外墙(东北)", entrance="西门D-U40a进自主廊；玻璃门EXT-U-S出露台",
             adjacency="西：梯井栏板；南：露台/屋顶花园"),
 "GA": dict(origin_use="走廊", modern_use="主廊（客廊，净宽1.95；西端窗=42-L『西翼的窗前』位）", facade="西端外墙(西南向)窗W-GAw",
             entrance="连接纵巷/家务/过厅开口/客房套/起居室/梯口", adjacency="南缘贴梯井栏杆线即楼梯边缘"),
 "L02": dict(origin_use="灶间/家务房", modern_use="家务（炊事铁炉VC3候选）",
             facade="北墙承土无窗", entrance="南门D-L02a进主廊", adjacency="东：储物"),
 "L04": dict(origin_use="储物间", modern_use="生活储物",
             facade="北墙承土无窗", entrance="南门D-L04a进主廊", adjacency="西：家务；东：梯间"),
 "L01": dict(origin_use="楼梯间", modern_use="主梯起步厅+梯下储柜（VC4采暖炉候选）",
             facade="北墙承土", entrance="东门D-L01w通设备间；北端起步", adjacency="上：主梯洞口候选"),
 "L05": dict(origin_use="杂物/燃料间", modern_use="设备（热泵分水器/管井端头）+储物",
             facade="北墙承土无窗", entrance="西门D-L01w通梯间", adjacency="东：公卫"),
 "L15": dict(origin_use="厕浴", modern_use="公卫+清洁（机械排气）",
             facade="北墙承土无窗", entrance="南门D-L15a进主廊", adjacency="西：设备"),
 "L10": dict(origin_use="正门厅", modern_use="门厅",
             facade="西外墙(西南向，西门EXT-L-W+西窗)", entrance="西口进门；北门D-L10a进主廊", adjacency="南：西储"),
 "L16": dict(origin_use="门厅衣帽/储", modern_use="西储·衣帽",
             facade="南外墙(东南向阳)窗", entrance="北门D-L16a进门厅", adjacency="北：门厅"),
 "L12": dict(origin_use="备餐/传菜间", modern_use="备餐（辅助无窗）",
             facade="无外墙（服务过渡空间，允许）", entrance="北门D-L12a进主廊；传菜门D-L12b进餐厅", adjacency="南：餐厅"),
 "L11": dict(origin_use="家庭餐厅", modern_use="家庭餐厅（48㎡，VC5壁炉候选）",
             facade="南外墙(东南向阳湖向)2樘窗", entrance="西门D-L11a进门厅；传菜门D-L12b", adjacency="北：备餐"),
 "L13": dict(origin_use="客堂", modern_use="会客（日常接待）",
             facade="南外墙(东南向阳)2樘窗", entrance="北门D-L13a进主廊", adjacency="东：家庭起居"),
 "L14": dict(origin_use="家庭起居", modern_use="家庭起居",
             facade="南外墙(东南向阳)2樘窗", entrance="北门D-L14a进主廊", adjacency="东：家庭书房"),
 "L19": dict(origin_use="家庭卧室", modern_use="家庭书房/阅读（原家庭卧室改，签调令等文书场景落点）",
             facade="南外墙(东南向阳)+东外墙(东北)", entrance="北门D-L19a进主廊", adjacency="西：家庭起居"),
 "GA-L": dict(origin_use="走廊", modern_use="主廊", facade="无（交通）",
             entrance="连接门厅/各房间", adjacency="北带承土排/南带起居排"),
}

def room_out(r):
    x1, z1, x2, z2 = r["rect"]
    o = ORIGIN[r["id"]]
    return dict(id=r["id"], program_id=r.get("pid"), floor=r["fl"], level=(24 if r["fl"]==2 else 20.8),
                name=r["name"], rect=[x1, z1, x2, z2],
                net_area=round((x2-x1)*(z2-z1), 1),
                origin_use=o["origin_use"], modern_use=o["modern_use"],
                facade=o["facade"], entrance=o["entrance"], adjacency=o["adjacency"],
                note=r.get("note", ""))

def door_out(dd):
    return dict(id=dd["id"], floor=dd["fl"], wall_axis=dd["wall"],
                wall_line=dd["line"], opening=[dd["pos"][0], dd["pos"][1]],
                width=dd["w"], hinge_at=dd["hinge"], swing=dd["swing"],
                name=dd["name"], sweep="90°内开(扇+扫掠见V00隔墙图R2)")

HEARTHS = [
 dict(id="H-V00-01", chimney="VC3", floor=1, level=20.8, center=[-20.0, 20.75], kind="炊事铁炉",
      room="L02家务间", candidate=True, accepted=False,
      note="北墙芯南侧炉体；独立烟道接VC3（旧铁炉期，改馆后冷态保留）"),
 dict(id="H-V00-02", chimney="VC3", floor=2, level=24.0, center=[-20.0, 20.4], kind="客房壁炉",
      room="U21客房寝北角", candidate=True, accepted=False,
      note="芯上半嵌寝室北角；与一楼炊事炉各自独立烟道汇入VC3砖芯"),
 dict(id="H-V00-03", chimney="VC4", floor=1, level=20.8, center=[-10.0, 20.75], kind="采暖铁炉",
      room="L01梯间北端", candidate=True, accepted=False,
      note="起步厅旁采暖炉；二楼段穿主梯洞口北栏板候选，需结构/烟道复核"),
 dict(id="H-V00-04", chimney="VC5", floor=1, level=20.8, center=[-21.6, 32.6], kind="餐厅壁炉",
      room="L11家庭餐厅西墙南端", candidate=True, accepted=False,
      note="芯贴西墙(上轮-21.3未接受，本稿修正贴墙)；top25.8穿一楼南带天面"),
 dict(id="H-V00-05", chimney="VC6", floor=2, level=24.0, center=[-11.6, 6.0], kind="热水/采暖铁炉",
      room="U10家务间北墙", candidate=True, accepted=False,
      note="芯半凸北墙外立24m坡地平台；供二楼热水（原(-6,12)在新布局落主卧套区，故调整候选）"),
]
HB = {}
for h in HEARTHS:
    HB.setdefault(h["chimney"], []).append(dict(id=h["id"], kind=h["kind"], floor=h["floor"]))

rooms = [room_out(r) for r in G.ROOMS]
doors = [door_out(x) for x in G.DOORS]
openings = [dict(floor=o["fl"], wall_axis=o["wall"], wall_line=o["line"],
                 opening=[o["pos"][0], o["pos"][1]], name=o["name"]) for o in G.OPENINGS]
windows = [dict(id=w["id"], floor=w["fl"], wall_axis=w["wall"], wall_line=w["line"],
                opening=[w["pos"][0], w["pos"][1]], name=w["name"],
                sill="高窗0.6" if "高窗" in w["name"] else "0.9")
           for w in G.WINDOWS]
chimneys = [dict(id=c["id"], center=c["center"], brick_half=c["half"], top=c["top"],
                 status=c["status"], candidate=True, accepted=False,
                 hearths_served=HB.get(c["id"], []), note=c["note"]) for c in G.CHIMNEYS]

stair = dict(G.STAIR)
stair["candidate"] = True
stair["accepted"] = False
stair["zone_original"] = [-8.0, 20.0, -4.4, 24.0]
stair["revisit"] = "西移4m为未接受候选：需结构（楼板开洞/栏板）、烟道（VC4穿栏板段耐火）与走位复核；未回写场地v13"

resub = dict(
    version="R4",
    r3_to_r4_changes=[
        "二楼重排为三客房硬清单落位：G-ZY庄颜客房(西南,双向阳)/G-A客房A(北带西,16.0㎡)/G-B客房B(北带中,16.0㎡)，均program_id标注、独立反锁门接同层客廊、套内厕洗·收纳",
        "删除主卧寝概念(罗辑住南岸主楼，原家庭主卧为G-A/G-B历史前身)；公卫·清洁服务全层",
        "取消二楼56㎡手作活动间(验收点名挤客房)：家庭阅读/手作由一楼家庭书房+小起居室+东带活动·阅读(30.5㎡)承担",
        "客廊纵巷居中回归(1.8×11.5)，服务客房A/B与储段；家务·布草压缩至19.5㎡、公卫10.6㎡、过厅25.3㎡",
        "真北换算纠正：+Z=东南135°(非正南)、+X=东北45°、−X=西南225°(向阳)、−Z=西北315°；窗位自校全部重做，客房A/B西北向受限已记录",
        "VC6候选随公卫落位调至(-6.85,6)公卫·清洁北墙；楼梯西移/VC5候选维持未接受",
    ],
    date="2026-11-07",
    response_to="功能边界与重做要求.md + R2退回与客房硬清单.md + 客房必备清单.json",
    schema={
        "coordinate": "房屋局部坐标X/Z，m。X轴指向真东北45°、Z轴指向真东南45°(heading=45°)；z-墙=朝真北、z+墙=朝真南、x-墙=朝真西、x+墙=朝真东",
        "rooms_rect": "四端点[x1,z1,x2,z2]=净空内缘（区别于场地包络的[X,Z,宽,深]）",
        "floor": "页面层号：1=一楼(楼面20.8m)、2=二楼(楼面24m)；对应场地输入层0/1",
        "walls": "相邻房间净空间距0.15=内隔墙；外墙厚0.4由场地层管理，图上外包络线即外墙面",
        "doors": "opening=[a1,a2]沿墙坐标；hinge_at=轴端；swing=门扇开启方向(+x/-x/+z/-z)；扫掠90°内开",
        "candidates": "stair/chimneys/hearths均标candidate=true且accepted=false，未回写场地v13"
    },
    functional_compliance={
        "new_house_use": "纯家庭居住与日常接待：卧室3+小起居室+家庭餐厅/会客/起居+家庭手作·阅读+家务+厕洗+交通",
        "no_exhibition": "无展厅/展室/检片/藏品库/馆务后台；家庭摆画陈设于起居与廊，不设独立展室",
        "bedrooms": {"new_house": 3, "new_house_floor": "全部二楼", "old_house_H9": 1, "whole_group": 4,
                     "guestrooms": [
                       {"program_id": "G-ZY", "room_id": "U21", "label": "庄颜普通客房", "sleep_net": 14.5, "door": "D-U21b内开反锁经门斗接主廊", "window": "西墙西南向阳+南墙东南向阳", "toilet": "U23专用厕洗"},
                       {"program_id": "G-A", "room_id": "U05", "label": "普通客房A", "sleep_net": 16.0, "door": "D-U05a内开反锁接客廊纵巷", "window": "北墙(西北,朝向受限记录)", "toilet": "U05b套内厕洗·收纳"},
                       {"program_id": "G-B", "room_id": "U07", "label": "普通客房B", "sleep_net": 16.0, "door": "D-U07a内开反锁接客廊纵巷", "window": "北墙(西北,朝向受限记录)", "toilet": "U07b套内厕洗·收纳"}
                     ],
                     "note": "三间客房全部二楼、独立反锁门接同层客廊、真实外墙窗、厕洗与收纳齐备；老宅H9另计；新宅不设现代主人套房，罗辑住南岸主楼"},
        "museum_interface": "仅二楼西口U01签收前室；后台移交经主廊→过厅→北口短廊去生产院，不穿居室",
        "fragmentation": "北带五间均贴北外墙大纵深完整房间；z14.05~17.9后段为各间附属储段(分期说明)，非独立碎房；无窗仅限储藏/清洁/备餐等辅助"
    },
    orientation_check={
        "conversion": "heading=45°真北换算(R3错误已纠正)：+X=东北45°、+Z=东南135°、−X=西南225°、−Z=西北315°；真南=局部(−0.707,+0.707)即−X+Z对角方向",
        "sunny_walls": "向阳外墙=z+(东南135°)与x−(西南225°)；背阳外墙=x+(东北45°)与z−(西北315°)；东南/西南均在向阳区间，无墙正对真南(45°偏差内)",
        "guestrooms": {
            "G-ZY庄颜客房": "西墙(西南225°向阳)+南墙(东南135°向阳)双向阳——全宅最优",
            "G-A客房A": "北墙(西北315°)——朝向受限记录：二楼向阳墙带(z+南带/x−西带)已分配给庄颜客房(剧情固定西翼)、小起居室(湖景窗/玻璃门固定位置)、客房A套内段，客房A取北带西北向，漫射光稳定",
            "G-B客房B": "北墙(西北315°)——同上记录"
        },
        "living_dining": "U40小起居室南墙(东南向阳)湖景、L11餐厅南墙2窗(东南向阳)、L13会客/L14起居/L19书房南墙(东南向阳)——全部向阳外墙",
        "north_rooms": "北带(西北)为客房A/B(受限记录)+储藏/公卫/家务/过厅辅助；活动·阅读东墙东北漫射光",
        "shading": "一楼北带承土无窗(坡地贴土)；二楼北窗外为24m坡地平台+短廊无高遮挡；西墙外为同标高侧廊+西花园；南墙外为屋顶花园/露台与湖景开阔"
    },
    phase_notes=[
        "北带大间(手作/家务/公卫/过厅)z14.05~17.9后段为附属储段：现代期生活储藏，历史期为杂物/燃料——内分虚线示意，分期说明",
        "旧铁炉期：VC3炊事/VC4采暖/VC5餐厅壁炉/VC6家务热水各炉独立烟道；现代热泵期炉冷态保留，热泵房远置(L05仅分水器/管井端头)",
        "备餐间无窗为服务过渡空间；清洁段无窗机械排气",
        "新宅不设现代主人套房：罗辑住南岸主楼；二楼三间均为普通留客房",
        "客房A/B套内厕洗·收纳段与储藏段为分期示意（寝区现代使用，储段历史杂物/现代生活储）",
        "主卧不设独立卫：公卫·清洁(U06)卫段服务全层(含主卧)，历史宅主卧附卫非必须，现代期可视需要分期加装",
        "水吧台为小起居室家具级配置(24-L茶水间口径)，不设独立茶水间"
    ],
    rooms=rooms, doors=doors, openings_internal=openings, windows=windows,
    chimneys=chimneys, hearths=HEARTHS, stair=stair,
    change_log_candidates=[
        dict(item="主梯工作区", original=[-8.0, 20.0, -4.4, 24.0], revised=[-12.0, 20.0, -8.4, 24.0],
             status="候选·未接受(需结构/烟道/走位复核)",
             reason="原位使z=24南墙玻璃门(x-5±0.9)与湖景窗(x-7)落入梯井，24-L『窗前→楼梯→沙发』动线无法同层连贯",
             impact="二楼洞口随移；一楼梯间L01与储物/设备间重排；重叠带(z20~24)内调整，未触碰包络与外门口；未回写场地v13"),
        dict(item="VC5烟囱芯", original=[-20.0, 30.0], revised=[-21.6, 32.6],
             status="候选·未接受(需烟道复核)",
             reason="原位悬于餐厅中部；本稿修正为贴餐厅西墙南端(上轮-21.3不贴墙)作壁炉，top25.8不变",
             impact="餐厅南墙窗西端起于x-20.3避让；一楼南带天面开孔随移；未回写场地v13"),
        dict(item="VC6烟囱芯", original=[-6.0, 12.0], revised=[-11.6, 6.0],
             status="候选·未接受(新增调整)",
             reason="原位在新布局落主卧套区成独立砖柱；移至二楼家务间北墙作热水炉，芯半凸北墙外立24m坡地平台",
             impact="二楼家务间北墙局部加厚；未回写场地v13"),
        dict(item="VC3/VC4维持", original="原位", revised="原位",
             status="候选·未接受(VC4穿栏板段需复核)",
             reason="与新隔墙相容", impact="VC4二楼段以栏板烟道形式穿主梯洞口北缘候选"),
    ],
    narrative_checks_note="以下为设计自校记录(真北换算已按+Z东南/+X东北/−X西南/−Z西北纠正)，供验收参考，不作为验收依据",
    narrative_checks=[
        dict(scene="20-L", check="『别墅西翼有间独立客房』+『可以自己锁门』",
             selfcheck="U21庄颜普通客房居二楼西南角(G-ZY)，西+南双向阳真实外墙；寝门D-U21b内开反锁，套间入口D-U21a接主廊"),
        dict(scene="24-L", check="搬箱两趟、门外放箱不挡门",
             selfcheck="西口1.5→签收前室(12㎡)→客廊纵巷/主廊1.8；放箱位[-16.9,19.25,-16.0,19.8]在D-U21a门前"),
        dict(scene="24-L", check="客房外门→走廊看湖窗→梯口→可躺沙发→小起居室→玻璃门→露台同层连贯",
             selfcheck="主廊净1.8东端即起居室门D-U40a；湖景窗W-S3(x-7.75~-6.25,z24)；栏杆开口[-12,-10.3]正对西跑顶端(楼梯西移候选)；沙发贴南墙(东南向阳,午后光落茶几)；玻璃门EXT-U-S出露台"),
        dict(scene="24-L", check="开门冲向梯口、撞怀、脚跟碰台阶、扶住扶手",
             selfcheck="下梯处=西跑顶端(z20.1,x-12~-10.3)；客房门前x≈-16.4至梯口约4.5m"),
        dict(scene="24-L", check="『我也知道茶水间在哪儿』",
             selfcheck="小起居室内水吧台(家具级)，不设独立茶水间"),
        dict(scene="05-L", check="西翼签收：门旁值班牌、合伞、玻璃窗望出",
             selfcheck="二楼西口进门即U01签收前室；后台移交经主廊→过厅→北口短廊去生产院，不穿居室、不作参观线"),
        dict(scene="20-L", check="靠湖小餐厅、上菜退出、离席拉腕让路",
             selfcheck="餐厅L11净48.7南墙(东南向阳)2窗；服务线=备餐L12北门+传菜门直入餐厅；桌西门间过道2.45m"),
        dict(scene="08-L", check="庄颜从西翼方向走到别墅门口",
             selfcheck="客房下西跑(候选)→一楼梯间L01→主廊→门厅L10→西口出园"),
        dict(scene="客房硬清单", check="G-ZY/G-A/G-B三间二楼、独立反锁门、真实外墙窗、厕洗收纳、不以沙发床凑数",
             selfcheck="三间全在二楼；G-ZY经门斗接主廊，G-A/G-B经客廊纵巷；窗与厕洗收纳逐间齐备；program_id已在图与JSON标注"),
        dict(scene="罗辑居所", check="罗辑住南岸主楼，新宅不设现代主人套房",
             selfcheck="R4已删除主卧寝；原家庭主卧为G-A/G-B历史前身；全组客房4=新宅3+老宅H9"),
        dict(scene="20-L", check="靠湖小餐厅/对面坐/上菜退出/离席拉腕让路/『西翼有间独立客房，一直空着』/『我可以自己锁门』",
             selfcheck="L11南墙东南向2窗+2.0×1.0对坐长桌；备餐间+传菜门服务线两门可关；桌西门过道2.45m；G-ZY原建普通客房空置即住，D-U21b内开反锁；南墙窗朝下坡湖向"),
        dict(scene="24-L", check="走廊尽头窗/扶人过门/沙发午后面/水吧/对面椅/墙屏",
             selfcheck="主廊东端即起居室门(1.05搀扶宽)，湖景窗紧贴『窗边的小起居室』口径；沙发贴南墙、茶几承午后光；水吧台家具级；扶手椅对面+墙屏北墙；42-L『西翼的窗前』=主廊西端窗W-GAw补位"),
        dict(scene="共同约束", check="普通客房非套房、功能规模不扩成酒店",
             selfcheck="庄颜客房套间含寝14.5+门斗+厕洗共21.6；G-A/G-B各16+套内厕洗收纳13.4；无套房化配置"),
    ],
)

d["resubmission"] = resub
d["design_status"] = dict(
    acceptance_status="R4_resubmitted_pending_review",
    approved=False,
    geometry_frozen=False,
    r4_date="2026-11-07",
    note="R4按《R2退回与客房硬清单》提交：三客房program_id落位二楼、真北换算纠正、无主卧；楼梯西移/VC5/VC6均为未接受候选，未回写场地v13；rejected_submission保留各版退回证据",
    next_tasks="验收通过前V01—V05不冻结门表；V06/V07工业组不受影响")

json.dump(d, open(SRC, "w"), ensure_ascii=False, indent=2)
print("R4 resubmission written. rooms:", len(rooms), "doors:", len(doors), "windows:", len(windows))
