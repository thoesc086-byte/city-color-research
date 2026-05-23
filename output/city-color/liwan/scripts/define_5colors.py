"""
5 色定调：从聚类结果选出代表
策略：
- 1 个"骨架色"（灰族，最高权重）
- 4 个"色相色"（不同 hue family，高权重 + 高饱和度）
- 输出色卡 PNG/SVG/JSON
"""
import json, colorsys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "3_color_data" / "clusters.json"
OUT = ROOT / "4_outputs"
OUT.mkdir(parents=True, exist_ok=True)

def rgb_to_hsv(rgb):
    return colorsys.rgb_to_hsv(rgb[0]/255, rgb[1]/255, rgb[2]/255)

def hex_of(rgb):
    return "#{:02x}{:02x}{:02x}".format(*rgb)

def luminance(rgb):
    return 0.299*rgb[0] + 0.587*rgb[1] + 0.114*rgb[2]

def main():
    with open(DATA, "r", encoding="utf-8") as f:
        data = json.load(f)
    main_p = data["main_palette_30"]
    by_cat = data["by_category"]
    
    # 给每个色加 HSV
    for c in main_p:
        h, s, v = rgb_to_hsv(c["rgb"])
        c["hue"] = h*360; c["sat"] = s; c["val"] = v
    
    # 1) 选骨架色（灰族，最高权重，且 V 在 0.4-0.7 间）
    grays = [c for c in main_p if c["sat"] < 0.10 and 0.35 < c["val"] < 0.75]
    grays.sort(key=lambda x: -x["weight"])
    # 西关青砖灰
    skeleton = grays[0] if grays else main_p[0]
    
    # 2) 米黄（暖中性）—— 30-50° hue，sat 0.10-0.30，val > 0.6
    yellows = [c for c in main_p if 25 < c["hue"] < 50 and 0.10 < c["sat"] < 0.35 and c["val"] > 0.55]
    yellows.sort(key=lambda x: -x["weight"])
    
    # 3) 满洲窗红 —— 从 by_cat 和 main_p 中查鲜红
    red_candidates = []
    for cat, palette in by_cat.items():
        for c in palette:
            rgb = tuple(c["rgb"])
            h, s, v = rgb_to_hsv(rgb)
            if (h*360 < 30 or h*360 > 340) and s > 0.50 and 0.35 < v < 0.95:
                red_candidates.append({"rgb": rgb, "hex": hex_of(rgb), "weight": c["weight"], "category": cat, "hue":h*360, "sat":s, "val":v})
    # 从 main_p 中也拾鲜红
    for c in main_p:
        if (c["hue"] < 30 or c["hue"] > 340) and c["sat"] > 0.50 and 0.35 < c["val"] < 0.95:
            red_candidates.append({"rgb": tuple(c["rgb"]), "hex": hex_of(c["rgb"]), "weight": c["weight"], "category": "main", "hue":c["hue"], "sat":c["sat"], "val":c["val"]})
    red_candidates.sort(key=lambda x: -x["weight"])
    
    # 4) 蓝（沙面）—— 195-220° hue，饱和度中等
    blue_candidates = [c for c in main_p if 195 < c["hue"] < 220 and c["sat"] > 0.20]
    blue_candidates.sort(key=lambda x: -x["weight"])
    if not blue_candidates:
        # fallback：从 by_cat 自然分类找
        for c in by_cat.get("自然", []) + by_cat.get("历史", []):
            rgb = tuple(c["rgb"])
            h, s, v = rgb_to_hsv(rgb)
            if 195 < h*360 < 220 and s > 0.15:
                blue_candidates.append({"rgb": rgb, "hex": hex_of(rgb), "weight": c["weight"], "hue":h*360, "sat":s, "val":v})
        blue_candidates.sort(key=lambda x: -x["weight"])
    
    # 5) 木色/暖橙（粤剧暖橙、骑楼装饰）—— 15-30° hue，sat 0.40-0.70，val 0.4-0.7
    orange_candidates = []
    for cat, palette in by_cat.items():
        for c in palette:
            rgb = tuple(c["rgb"])
            h, s, v = rgb_to_hsv(rgb)
            if 15 < h*360 < 35 and 0.30 < s < 0.75 and 0.40 < v < 0.80:
                orange_candidates.append({"rgb": rgb, "hex": hex_of(rgb), "weight": c["weight"], "category": cat, "hue":h*360, "sat":s, "val":v})
    orange_candidates.sort(key=lambda x: -x["weight"])
    
    # 装配 5 色（按"骨架灰 + 米黄 + 满洲窗红 + 沙面蓝 + 粤剧赭"）
    final5 = []
    
    if skeleton:
        c = skeleton
        final5.append({
            "name": "麻石青",
            "story": "西关麻石巷与青砖墙的中性灰，是整个老城的视觉骨架",
            "source": "data-driven (gray family, weight {:.1f}%)".format(c["weight"]*100),
            "rgb": list(c["rgb"]),
            "hex": hex_of(c["rgb"]),
            "role": "主色 / 骨架"
        })
    
    if yellows:
        c = yellows[0]
        final5.append({
            "name": "骑楼米",
            "story": "沙面欧式建筑、恩宁路骑楼、西关大屋外墙的暖米黄基调",
            "source": "data-driven (warm neutral 30-50°, weight {:.1f}%)".format(c["weight"]*100),
            "rgb": list(c["rgb"]),
            "hex": hex_of(c["rgb"]),
            "role": "辅色 / 街墙"
        })
    
    # 满洲窗红 优先取鲜红（高饱和高明度）
    if red_candidates:
        # 优先 saturation > 0.75 + value > 0.65 的鲜红
        bright_reds = [c for c in red_candidates if c["sat"] > 0.70 and c["val"] > 0.60]
        if bright_reds:
            bright_reds.sort(key=lambda x: -(x["sat"]*x["val"]))
            c = bright_reds[0]
        else:
            # 降级选饰莽红赭
            c = red_candidates[0]
        final5.append({
            "name": "满洲窗红",
            "story": "西关大屋满洲窗彩色玻璃中的标志红，也呼应粤剧戏服与老字号金匾",
            "source": f"data-driven (red family, from category {c.get('category','main')})",
            "rgb": list(c["rgb"]),
            "hex": hex_of(c["rgb"]),
            "role": "点缀色 / 文化符号"
        })
    
    # 沙面蓝：优先选中饱和度、中明度的（避免选出极淺天空色）
    if blue_candidates:
        # 过滤出 V<0.85 的（不是高光天空）
        deep_blues = [c for c in blue_candidates if c.get("val", c.get("sat",0))<0.80 and c.get("sat",0)>0.30]
        c = deep_blues[0] if deep_blues else blue_candidates[0]
        if isinstance(c.get("rgb"), tuple):
            c["rgb"] = list(c["rgb"])
        final5.append({
            "name": "沙面蓝",
            "story": "沙面欧式建筑的百叶窗与拱券圳色、白鹅潭江面复合蓝",
            "source": "data-driven (blue 195-220°)",
            "rgb": list(c["rgb"]),
            "hex": hex_of(c["rgb"]),
            "role": "次主色 / 滨水"
        })
    
    if orange_candidates:
        # 选 saturation 最高的
        orange_candidates.sort(key=lambda x: -x["sat"])
        c = orange_candidates[0]
        final5.append({
            "name": "粤剧赭",
            "story": "粤剧戏服、广彩瓷器、老字号木匾的暖赭色，岭南文化的暖底色",
            "source": f"data-driven (orange-red 15-35°, sat {c['sat']*100:.0f}%)",
            "rgb": list(c["rgb"]),
            "hex": hex_of(c["rgb"]),
            "role": "辅色 / 文化暖色"
        })
    
    # ===== 输出 JSON =====
    out_json = {
        "name": "荔湾·西关 5 色色谱",
        "method": "在线远程取色：154 张图像 → 5 色 K-means → 三元映射 → 5 色定调",
        "source_count": 154,
        "colors": final5
    }
    with open(OUT / "5color_palette.json", "w", encoding="utf-8") as f:
        json.dump(out_json, f, ensure_ascii=False, indent=2)
    
    # ===== 输出色卡 PNG =====
    n = len(final5)
    W = 1500
    H = 600
    sw = W // n
    img = Image.new("RGB", (W, H), "white")
    draw = ImageDraw.Draw(img)
    try:
        font_t = ImageFont.truetype("/System/Library/Fonts/PingFang.ttc", 32)
        font_role = ImageFont.truetype("/System/Library/Fonts/PingFang.ttc", 18)
        font_h = ImageFont.truetype("/System/Library/Fonts/Menlo.ttc", 22)
        font_d = ImageFont.truetype("/System/Library/Fonts/PingFang.ttc", 14)
    except:
        font_t = ImageFont.load_default()
        font_role = font_h = font_d = font_t
    
    for i, c in enumerate(final5):
        x = i * sw
        rgb = tuple(c["rgb"])
        draw.rectangle([x, 0, x+sw, 380], fill=rgb)
        text_color = "#1a1a1a" if luminance(rgb) > 160 else "#ffffff"
        draw.text((x+24, 20), c["name"], fill=text_color, font=font_t)
        draw.text((x+24, 60), c["role"], fill=text_color, font=font_role)
        draw.text((x+sw-160, 340), c["hex"].upper(), fill=text_color, font=font_h)
        # 下方说明
        draw.text((x+24, 400), c["story"][:18]+("..." if len(c["story"])>18 else ""), fill="#1a1a1a", font=font_d)
        draw.text((x+24, 422), c["story"][18:36]+("..." if len(c["story"])>36 else ""), fill="#444", font=font_d)
        draw.text((x+24, 460), f"RGB({rgb[0]},{rgb[1]},{rgb[2]})", fill="#666", font=font_d)
        draw.text((x+24, 480), c["source"][:30], fill="#888", font=font_d)
    
    # 标题
    draw.text((24, 540), "荔湾·西关 5 色色谱  ·  数据驱动 154 张在线图像", fill="#1a1a1a", font=font_t)
    
    img.save(OUT / "5color_palette.png", optimize=True)
    
    print(f"\n🎨 5 色定调完成！")
    for c in final5:
        print(f"  {c['name']:6s} {c['hex']}  RGB{tuple(c['rgb'])}  | {c['role']}")
        print(f"         {c['story']}")
    print(f"\n📁 输出：")
    print(f"   {OUT / '5color_palette.json'}")
    print(f"   {OUT / '5color_palette.png'}")

if __name__ == "__main__":
    main()
