"""
Bing 图像搜索抓取脚本
- 按关键词搜索图像
- 解析缩略图 URL
- 下载到指定目录
"""
import os
import re
import sys
import json
import time
import hashlib
import urllib.parse
import requests
from pathlib import Path

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
}

def search_bing_images(query, count=30, retries=2):
    """Bing image search; returns list of image urls."""
    url = "https://www.bing.com/images/async"
    params = {
        "q": query,
        "first": 0,
        "count": count,
        "relp": count,
        "scenario": "ImageBasicHover",
        "datsrc": "I",
        "layout": "RowBased",
        "mmasync": 1,
    }
    for attempt in range(retries+1):
        try:
            r = requests.get(url, params=params, headers=HEADERS, timeout=15)
            if r.status_code != 200:
                print(f"  [warn] http {r.status_code}, retry {attempt}")
                time.sleep(2)
                continue
            html = r.text
            # m[*?murl="...
            urls = re.findall(r'murl&quot;:&quot;(.*?)&quot;', html)
            if not urls:
                urls = re.findall(r'"murl":"(.*?)"', html)
            urls = [u.replace("\\u002f","/") for u in urls]
            return urls
        except Exception as e:
            print(f"  [err] {e}, retry {attempt}")
            time.sleep(2)
    return []

def download_image(url, save_dir, prefix=""):
    """Download single image; returns filepath or None."""
    try:
        # Hash url for deduplication
        h = hashlib.md5(url.encode()).hexdigest()[:10]
        # Decide ext
        ext = ".jpg"
        for e in [".jpg", ".jpeg", ".png", ".webp"]:
            if e in url.lower():
                ext = e; break
        fp = Path(save_dir) / f"{prefix}_{h}{ext}"
        if fp.exists() and fp.stat().st_size > 1000:
            return str(fp)
        r = requests.get(url, headers=HEADERS, timeout=15, stream=True)
        if r.status_code != 200:
            return None
        ct = r.headers.get("content-type","").lower()
        if "image" not in ct:
            return None
        size = 0
        with open(fp, "wb") as f:
            for chunk in r.iter_content(8192):
                f.write(chunk)
                size += len(chunk)
                if size > 5_000_000:  # 5MB cap
                    break
        if size < 5000:  # too small probably bad
            fp.unlink(missing_ok=True)
            return None
        return str(fp)
    except Exception as e:
        return None

def fetch_for_query(query, save_dir, prefix, target_count=15):
    """Fetch images for one query into save_dir."""
    Path(save_dir).mkdir(parents=True, exist_ok=True)
    print(f"\n🔍 搜索: {query}")
    urls = search_bing_images(query, count=40)
    print(f"  找到 {len(urls)} 个候选 URL")
    saved = []
    for u in urls:
        if len(saved) >= target_count:
            break
        if not u.startswith("http"):
            continue
        fp = download_image(u, save_dir, prefix)
        if fp:
            saved.append(fp)
            print(f"  [{len(saved)}/{target_count}] {Path(fp).name}")
    return saved

if __name__ == "__main__":
    base = Path(__file__).resolve().parent.parent / "2_images"

    # 抓取计划：每个关键词 15 张
    PLAN = [
        # 民居
        ("西关大屋 老建筑",       "民居", "xiguan_dawu", 15),
        ("满洲窗 彩色玻璃 西关",   "民居", "manzhou_chuang", 12),
        ("骑楼 广州 恩宁路",       "民居", "qilou", 15),
        ("广州 麻石巷 西关",       "民居", "mashi", 8),
        ("泮塘五约",              "民居", "pantang", 10),

        # 历史建筑
        ("沙面 广州 建筑群",      "历史", "shamian", 15),
        ("陈家祠 广州",           "历史", "chenjiaci", 12),
        ("永庆坊 广州",           "历史", "yongqingfang", 15),
        ("十三行 博物馆",         "历史", "shisanhang", 8),

        # 自然
        ("荔枝湾 广州",           "自然", "lizhiwan", 12),
        ("白鹅潭 广州 江景",      "自然", "baietan", 8),

        # 老字号
        ("陶陶居 广州",           "老字号", "taotaoju", 8),
        ("广州酒家",              "老字号", "guangzhoujiujia", 8),

        # 粤剧
        ("粤剧 戏服 广州",        "粤剧", "yueju", 8),
    ]

    summary = {}
    for query, category, prefix, count in PLAN:
        save_dir = base / category
        results = fetch_for_query(query, save_dir, prefix, target_count=count)
        summary[query] = {"category": category, "count": len(results), "files": results}
        time.sleep(1.5)  # be polite

    # 输出 manifest
    out_file = base.parent / "1_research" / "manifest.json"
    out_file.parent.mkdir(parents=True, exist_ok=True)
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)
    
    total = sum(v["count"] for v in summary.values())
    print(f"\n✅ 共下载 {total} 张图片到 {base}")
    print(f"📋 manifest: {out_file}")
