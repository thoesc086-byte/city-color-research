"""
为每个特征色挑选 3-5 张最能体现该色的代表图片
基于 per_image/all.json 找到含有该色的高权重图片
"""
import json, colorsys, shutil
from pathlib import Path
import numpy as np

ROOT = Path(__file__).resolve().parent.parent
PER_IMAGE = ROOT / "3_color_data" / "per_image" / "all.json"
PALETTE = ROOT / "4_outputs" / "5color_palette.json"
IMG_DIR = ROOT / "2_images"
OUT = ROOT / "交付" / "素材精选"
OUT.mkdir(parents=True, exist_ok=True)

def color_dist(rgb1, rgb2):
    """RGB 距离"""
    return ((rgb1[0]-rgb2[0])**2 + (rgb1[1]-rgb2[1])**2 + (rgb1[2]-rgb2[2])**2) ** 0.5

with open(PER_IMAGE, "r", encoding="utf-8") as f:
    per_img = json.load(f)
with open(PALETTE, "r", encoding="utf-8") as f:
    palette = json.load(f)

print("\n📸 为每个特征色匹配代表图片：\n")

result = {}
for color in palette["colors"]:
    target = tuple(color["rgb"])
    matches = []
    for img_path, dom_colors in per_img.items():
        for c in dom_colors[:5]:  # 取每张图前 5 个主导色
            d = color_dist(c["rgb"], target)
            if d < 60:  # 距离阈值
                # score = weight - distance penalty
                score = c["weight"] * 100 - d
                matches.append((img_path, c["rgb"], c["weight"], d, score))
                break
    matches.sort(key=lambda x: -x[4])
    
    selected = matches[:5]
    print(f"  [{color['name']}] {color['hex']} → 找到 {len(matches)} 张匹配，取前 5：")
    color_dir = OUT / color["name"]
    color_dir.mkdir(exist_ok=True)
    
    img_list = []
    for img_path, rgb, weight, dist, score in selected:
        src = IMG_DIR / img_path
        if not src.exists():
            continue
        dst = color_dir / src.name
        shutil.copy2(src, dst)
        img_list.append({
            "image": img_path,
            "matched_rgb": list(rgb),
            "weight_in_image": float(weight),
            "distance": float(dist),
        })
        print(f"    {img_path}  匹配 RGB{rgb}  权重 {weight*100:.0f}%  距离 {dist:.0f}")
    result[color["name"]] = img_list

with open(OUT / "matches.json", "w", encoding="utf-8") as f:
    json.dump(result, f, ensure_ascii=False, indent=2)

print(f"\n✅ 完成。代表图分别在 {OUT}/")
