#!/usr/bin/env python3
# V00 主梯纵剖面 A-A（沿西跑中线 x=-11.15 剖视，视线向东） v2
S = 62.0
def X(z): return 170 + (z - 19.6) * S
def Y(lv): return 620 - (lv - 19.0) * S

out = ['<svg xmlns="http://www.w3.org/2000/svg" width="980" height="700" viewBox="0 0 980 700">',
'<rect width="980" height="700" fill="#fafbfb"/>',
'<style>text{font-family:"Noto Sans CJK SC",sans-serif;fill:#263746;font-size:13px}'
'.s{font-size:11px;fill:#5a6b76}.dim{font-size:10.5px;fill:#a77643}</style>',
'<text x="30" y="34" font-size="21">V00R4 · 主梯纵剖面 A-A · 西跑中线（x=-11.15）剖视，视线向东</text>']

# 北侧承土示意（z<20.0，室外地面约21.4）
out.append(f'<line x1="{X(19.0):.0f}" y1="{Y(21.4):.0f}" x2="{X(20.0):.0f}" y2="{Y(21.4):.0f}" stroke="#8a7a5c" stroke-width="2.5"/>')
out.append(f'<text x="{X(19.0):.0f}" y="{Y(21.4)-8:.0f}" class="s">北侧承土（坡地，一楼北墙无窗）</text>')

# 一楼楼面（z 20.0~24.4）
out.append(f'<line x1="{X(20.0):.0f}" y1="{Y(20.8):.0f}" x2="{X(24.4):.0f}" y2="{Y(20.8):.0f}" stroke="#263746" stroke-width="2.5"/>')
out.append(f'<text x="{X(23.0):.0f}" y="{Y(20.8)+20:.0f}" class="s">一楼楼面 20.8m（梯间起步厅；起步点z≈20.1东跑）</text>')

# 二楼实楼板（z 19.6~20.0）：板顶24.0 板底23.7
out.append(f'<rect x="{X(19.6):.0f}" y="{Y(24.0):.0f}" width="{X(20.0)-X(19.6):.0f}" height="{Y(23.7)-Y(24.0):.0f}" fill="#b9c6cf" stroke="#263746" stroke-width="1.5"/>')
out.append(f'<text x="{X(19.55):.0f}" y="{Y(24.0)-8:.0f}" text-anchor="start" class="s">二楼实楼板（板底23.7）· 主廊侧</text>')

# 洞口两边界
out.append(f'<line x1="{X(20.0):.0f}" y1="{Y(24.0):.0f}" x2="{X(20.0):.0f}" y2="{Y(23.1):.0f}" stroke="#a77643" stroke-width="3.5"/>')
out.append(f'<text x="{X(20.35):.0f}" y="{Y(23.3):.0f}" class="dim">栏杆开口0.9高＝楼梯边缘(24-L)</text>')
out.append(f'<line x1="{X(24.0):.0f}" y1="{Y(27.2):.0f}" x2="{X(24.0):.0f}" y2="{Y(20.8):.0f}" stroke="#263746" stroke-width="3.5"/>')
out.append(f'<text x="{X(24.06):.0f}" y="{Y(25.9):.0f}" class="s">二楼南外墙 z=24.0（VC4二楼段栏板在其北）</text>')

# 屋面
out.append(f'<line x1="{X(19.6):.0f}" y1="{Y(26.8):.0f}" x2="{X(24.0):.0f}" y2="{Y(26.8):.0f}" stroke="#263746" stroke-width="2"/>')
out.append(f'<line x1="{X(19.6):.0f}" y1="{Y(27.2):.0f}" x2="{X(24.0):.0f}" y2="{Y(27.2):.0f}" stroke="#263746" stroke-width="3.5"/>')
out.append(f'<text x="{X(21.6):.0f}" y="{Y(27.2)-8:.0f}" text-anchor="middle" class="s">屋面（结构底≈26.8 工作值）· 洞口段贯通到屋面底</text>')

# 中间平台（z 22.35~23.9 顶22.4 板底22.15）
out.append(f'<rect x="{X(22.35):.0f}" y="{Y(22.4):.0f}" width="{X(23.9)-X(22.35):.0f}" height="{Y(22.15)-Y(22.4):.0f}" fill="#e8dfd0" stroke="#8a7a5c" stroke-width="1.5"/>')
out.append(f'<text x="{X(23.12):.0f}" y="{Y(22.4)-6:.0f}" text-anchor="middle" class="s">中间平台 22.4m</text>')
out.append(f'<line x1="{X(23.9):.0f}" y1="{Y(22.15):.0f}" x2="{X(23.9):.0f}" y2="{Y(20.8):.0f}" stroke="#8a7a5c" stroke-width="1.2" stroke-dasharray="4 3"/>')
out.append(f'<text x="{X(23.96):.0f}" y="{Y(21.5):.0f}" class="dim">平台支承墙(示意)</text>')

# 西跑踏步：从(z 20.1, 24.0)向南下行至(z 22.35, 22.4)  9级 riser0.178 tread0.25
riser, tread, n = 0.178, 0.25, 9
segs = []
for k in range(n):
    z1 = 20.1 + k*tread; l1 = 24.0 - k*riser
    z2 = z1 + tread;    l2 = l1 - riser
    segs.append((z1, l1, z2, l2))
d = f'M {X(20.1):.0f} {Y(24.0):.0f} '
for (z1, l1, z2, l2) in segs:
    d += f'L {X(z2):.0f} {Y(l2):.0f} L {X(z2):.0f} {Y(l1):.0f} '  # 竖板向上回到上级踏面高度
out.append(f'<path d="{d}" fill="none" stroke="#8a7a5c" stroke-width="2"/>')
out.append(f'<line x1="{X(20.1):.0f}" y1="{Y(24.0):.0f}" x2="{X(22.35):.0f}" y2="{Y(22.4):.0f}" stroke="#b0a284" stroke-width="1" stroke-dasharray="5 4"/>')
out.append(f'<text x="{X(20.35):.0f}" y="{Y(23.85):.0f}" class="dim">西跑9级↓ 踏面0.25×竖板0.178</text>')

# 头部净空线（梯段法线上方1.9，检查与板底/栏板）
out.append(f'<line x1="{X(20.1):.0f}" y1="{Y(24.0-1.9):.0f}" x2="{X(22.35):.0f}" y2="{Y(22.4-1.9):.0f}" stroke="#c2504a" stroke-width="1.2" stroke-dasharray="6 4"/>')
out.append(f'<text x="{X(20.75):.0f}" y="{Y(22.02):.0f}" class="s" fill="#c2504a">头部净空检查线1.9m：下行至z≈22.1后触二楼板底→</text>')
out.append(f'<text x="{X(20.75):.0f}" y="{Y(21.7):.0f}" class="s" fill="#c2504a">该段上方必须开洞（本方案洞口已全覆盖z20.0~24.0）</text>')

# 平台上方净高标注
out.append(f'<line x1="{X(23.0):.0f}" y1="{Y(22.4):.0f}" x2="{X(23.0):.0f}" y2="{Y(26.8):.0f}" stroke="#a77643" stroke-width="1" stroke-dasharray="4 3"/>')
out.append(f'<text x="{X(23.08):.0f}" y="{Y(25.4):.0f}" class="dim">平台上方净高≈4.4（转体无压头）</text>')

# 标高引线
for lv, lab in [(20.8, "20.8"), (22.4, "22.4"), (24.0, "24.0"), (26.8, "26.8")]:
    out.append(f'<line x1="112" y1="{Y(lv):.0f}" x2="{X(19.6):.0f}" y2="{Y(lv):.0f}" stroke="#a77643" stroke-width="0.8"/>')
    out.append(f'<text x="106" y="{Y(lv)+4:.0f}" text-anchor="end" class="dim">{lab}m</text>')

out.append('<text x="30" y="672" class="s">Z（南→）· 洞口3.6×4m于z20.0~24.0全开 · 东跑（未剖到）自一楼20.8在z20.1起步升至平台22.4 · 西跑自平台升至二楼24.0在z20.1跨出</text>')
out.append('</svg>')
open('/tmp/v00_design/out/v00_section.svg','w').write("\n".join(out))
print("section v2 done")
