"""
取色 + 聚类管线
1) 每张图取主导色（K-means n=5）
2) 全集再聚类（K-means n=20-30）
3) 输出色彩分布、热力图、聚类结果
"""
import os, json, sys
from pathlib import Path
import numpy as np
from PIL import Image
from sklearn.cluster import KMeans
from collections import Counter

ROOT = Path(__file__).resolve().parent.parent
IMG_DIR = ROOT / "2_images"
OUT_DIR = ROOT / "3_color_data"
OUT_DIR.mkdir(parents=True, exist_ok=True)
(OUT_DIR / "per_image").mkdir(exist_ok=True)

def extract_dominant(image_path, n_colors=5, max_dim=300):
    """Return list of (rgb tuple, weight 0-1)."""
    try:
        img = Image.open(image_path).convert("RGB")
        w, h = img.size
        # downscale
        scale = max_dim / max(w, h)
        if scale < 1:
            img = img.resize((int(w*scale), int(h*scale)))
        arr = np.array(img).reshape(-1, 3)
        # remove near-white & near-black backgrounds (border 5% rule)
        # only keep pixels with reasonable saturation
        mask = ~((arr[:,0]>240) & (arr[:,1]>240) & (arr[:,2]>240))
        mask &= ~((arr[:,0]<15) & (arr[:,1]<15) & (arr[:,2]<15))
        if mask.sum() < 100:
            mask = np.ones(len(arr), dtype=bool)
        arr = arr[mask]
        # subsample if huge
        if len(arr) > 20000:
            idx = np.random.choice(len(arr), 20000, replace=False)
            arr = arr[idx]
        km = KMeans(n_clusters=n_colors, n_init=5, random_state=42)
        km.fit(arr)
        labels, counts = np.unique(km.labels_, return_counts=True)
        total = counts.sum()
        result = []
        for i, c in zip(labels, counts):
            rgb = tuple(int(x) for x in km.cluster_centers_[i])
            result.append({"rgb": rgb, "weight": float(c/total)})
        result.sort(key=lambda x: -x["weight"])
        return result
    except Exception as e:
        print(f"  [err] {image_path.name}: {e}")
        return []

def main():
    images = []
    for cat_dir in sorted(IMG_DIR.iterdir()):
        if not cat_dir.is_dir():
            continue
        for img in sorted(cat_dir.iterdir()):
            if img.suffix.lower() in {".jpg",".jpeg",".png",".webp"}:
                images.append((cat_dir.name, img))
    
    print(f"\n📷 处理 {len(images)} 张图片...\n")
    
    per_image_results = {}
    all_colors = []  # list of (rgb, weight, category)

    for i, (cat, img_path) in enumerate(images, 1):
        if i % 10 == 0 or i == 1:
            print(f"  [{i}/{len(images)}] {cat}/{img_path.name}")
        result = extract_dominant(img_path, n_colors=5)
        per_image_results[f"{cat}/{img_path.name}"] = result
        for c in result:
            all_colors.append((c["rgb"], c["weight"], cat))
    
    # 保存每张图结果
    with open(OUT_DIR / "per_image" / "all.json", "w", encoding="utf-8") as f:
        json.dump(per_image_results, f, ensure_ascii=False, indent=2)
    
    # 全集聚类（按 weight 加权采样）
    print(f"\n🎯 全集聚类...")
    rgbs = np.array([c[0] for c in all_colors])
    weights = np.array([c[1] for c in all_colors])
    
    # 按权重重复（每个色按权重 *100 取整作为采样次数）
    sample_counts = (weights * 100).astype(int).clip(min=1)
    sampled = np.repeat(rgbs, sample_counts, axis=0)
    
    print(f"  采样后 {len(sampled)} 个像素点参与全集聚类")
    
    # 主色谱：30 个簇
    K = 30
    km = KMeans(n_clusters=K, n_init=10, random_state=42)
    km.fit(sampled)
    labels, counts = np.unique(km.labels_, return_counts=True)
    total = counts.sum()
    
    main_palette = []
    for i, c in zip(labels, counts):
        rgb = tuple(int(x) for x in km.cluster_centers_[i])
        weight = float(c/total)
        main_palette.append({"rgb": rgb, "weight": weight, "hex": "#{:02x}{:02x}{:02x}".format(*rgb)})
    main_palette.sort(key=lambda x: -x["weight"])
    
    # 按类别聚类
    by_category = {}
    for cat in sorted(set(c[2] for c in all_colors)):
        cat_colors = [(c[0], c[1]) for c in all_colors if c[2] == cat]
        rgbs_c = np.array([c[0] for c in cat_colors])
        weights_c = np.array([c[1] for c in cat_colors])
        sample_c = (weights_c * 100).astype(int).clip(min=1)
        sampled_c = np.repeat(rgbs_c, sample_c, axis=0)
        if len(sampled_c) < 8:
            continue
        K_c = min(8, len(sampled_c) // 5)
        km_c = KMeans(n_clusters=K_c, n_init=5, random_state=42)
        km_c.fit(sampled_c)
        labels_c, counts_c = np.unique(km_c.labels_, return_counts=True)
        cat_palette = []
        for i, c in zip(labels_c, counts_c):
            rgb = tuple(int(x) for x in km_c.cluster_centers_[i])
            cat_palette.append({"rgb": rgb, "weight": float(c/counts_c.sum()), "hex": "#{:02x}{:02x}{:02x}".format(*rgb)})
        cat_palette.sort(key=lambda x: -x["weight"])
        by_category[cat] = cat_palette
    
    output = {
        "summary": {
            "total_images": len(images),
            "categories": {cat: sum(1 for x,_ in images if x==cat) for cat in set(x for x,_ in images)},
        },
        "main_palette_30": main_palette,
        "by_category": by_category,
    }
    
    with open(OUT_DIR / "clusters.json", "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    
    print(f"\n✅ 完成。结果：")
    print(f"   {OUT_DIR / 'per_image' / 'all.json'}")
    print(f"   {OUT_DIR / 'clusters.json'}")
    print(f"\n📊 主色谱前 10 个：")
    for c in main_palette[:10]:
        print(f"   {c['hex']} (权重 {c['weight']*100:.1f}%)")

if __name__ == "__main__":
    main()
