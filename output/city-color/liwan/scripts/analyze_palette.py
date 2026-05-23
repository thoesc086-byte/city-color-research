"""
从 clusters.json 出发，做 5 色定调
策略：
1) 排除黑/灰/极暗色（saturation < 阈值 或 lightness 极端）
2) 在每个 hue family 内取最有代表性的色
3) 结合分类（民居/历史/自然/老字号/粤剧）做平衡
4) 输出 5 个特征色（NCS + HEX）
"""
import json, colorsys
from pathlib import Path
import numpy as np

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "3_color_data" / "clusters.json"

def rgb_to_hsv(rgb):
    return colorsys.rgb_to_hsv(rgb[0]/255, rgb[1]/255, rgb[2]/255)

def is_chromatic(rgb, sat_min=0.12, val_min=0.20, val_max=0.95):
    h, s, v = rgb_to_hsv(rgb)
    return s >= sat_min and val_min <= v <= val_max

def hue_family(rgb):
    h, s, v = rgb_to_hsv(rgb)
    if s < 0.10:
        if v < 0.30: return "black"
        elif v > 0.85: return "white"
        else: return "gray"
    h_deg = h * 360
    if h_deg < 15 or h_deg >= 345: return "red"
    elif h_deg < 45: return "orange"
    elif h_deg < 65: return "yellow"
    elif h_deg < 100: return "yellow-green"
    elif h_deg < 165: return "green"
    elif h_deg < 195: return "cyan"
    elif h_deg < 250: return "blue"
    elif h_deg < 285: return "purple"
    elif h_deg < 345: return "magenta"
    return "red"

def main():
    with open(DATA, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    main_p = data["main_palette_30"]
    
    # 分组
    by_family = {}
    for c in main_p:
        rgb = tuple(c["rgb"])
        fam = hue_family(rgb)
        h, s, v = rgb_to_hsv(rgb)
        c["hue"] = h*360
        c["sat"] = s
        c["val"] = v
        c["family"] = fam
        by_family.setdefault(fam, []).append(c)
    
    print("\n📊 30 个主色簇按色族分布：")
    for fam, items in sorted(by_family.items(), key=lambda x: -sum(c["weight"] for c in x[1])):
        total_w = sum(c["weight"] for c in items)
        items.sort(key=lambda x: -x["weight"])
        print(f"\n  [{fam}] 总权重 {total_w*100:.1f}%, {len(items)} 个色")
        for c in items[:5]:
            print(f"    {c['hex']} | weight {c['weight']*100:.1f}% | H={c['hue']:.0f}° S={c['sat']*100:.0f}% V={c['val']*100:.0f}%")
    
    # 按分类查看
    print("\n📦 按图像分类的代表色：")
    for cat, palette in data["by_category"].items():
        print(f"\n  [{cat}]")
        for c in palette[:5]:
            rgb = tuple(c["rgb"])
            h, s, v = rgb_to_hsv(rgb)
            mark = "⭐" if is_chromatic(rgb) else "  "
            print(f"    {mark} {c['hex']} | weight {c['weight']*100:.1f}% | H={h*360:.0f}° S={s*100:.0f}% V={v*100:.0f}%")

if __name__ == "__main__":
    main()
