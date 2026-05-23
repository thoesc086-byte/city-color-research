"""
仿亦庄"一图读懂"风格的长图海报
- 标题区
- 5 色色卡区
- 每个色一个详细板块（来源 + 提取理由 + 代表图缩略）
- 数据驱动说明
- 导则总结
"""
import json
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent.parent
PALETTE = ROOT / "4_outputs" / "5color_palette.json"
MATCHES = ROOT / "交付" / "素材精选" / "matches.json"
IMG_DIR = ROOT / "2_images"
OUT = ROOT / "交付" / "色卡" / "西关一图读懂.png"
OUT.parent.mkdir(parents=True, exist_ok=True)

with open(PALETTE) as f: palette = json.load(f)
with open(MATCHES) as f: matches = json.load(f)

# 详细的"为什么选这个色"理由（手工编写，仿亦庄文案风格）
COLOR_DETAILS = {
    "麻石青": {
        "tag_line": "西关老城的视觉骨架",
        "extract_logic": "🎯 数据 48.6% 暖灰族 + 29.9% 中性灰 = 整个西关 4 张照片里有 3 张是它",
        "story": [
            "📌 取自麻石巷的青石板，西关大屋的灰青砖外墙",
            "📌 是骑楼内廊的阴影色、也是阴雨天的檐下色",
            "📌 灰带一点暖（接近暖橄榄），不是北方那种冷青砖",
            "📌 在数据里出现频率最高 —— 是西关的「沉默基底」",
        ],
        "role": "主色 / 整城底色",
        "use_scene": "建筑外墙主色、铺地、构筑物",
        "ncs_approx": "S 4502-Y50R",
    },
    "骑楼米": {
        "tag_line": "100 年商埠的暖墙调",
        "extract_logic": "🎯 数据：30°-50° 黄橙族高权重簇，9.5% 占比",
        "story": [
            "📌 取自沙面欧式建筑外墙的水刷石仿石色",
            "📌 也是恩宁路骑楼柱身、西关大屋墙面的暖底",
            "📌 比江南粉墙黄一档、比北方土黄淡一档 —— 是「岭南专属」",
            "📌 与英、法殖民建筑的米色形成历史对接",
        ],
        "role": "辅色 / 街墙",
        "use_scene": "建筑外墙辅色、商铺立面、灯柱",
        "ncs_approx": "S 2010-Y20R",
    },
    "满洲窗红": {
        "tag_line": "西关大屋的色彩心跳",
        "extract_logic": "🎯 数据：饱和度 84% + 权重 0.6% —— 占比小但视觉冲击大，标准点睛色",
        "story": [
            "📌 取自西关大屋满洲窗的标志红玻璃 —— 中国民居中最丰富的彩色玻璃",
            "📌 也是粤剧戏服、年节灯笼、老字号金匾红底",
            "📌 在数据里 9 张图里有它（其中 8 张是粤剧/永庆坊/民居）",
            "📌 高纯度 + 高明度 → 适合做点缀，不可大面积铺",
        ],
        "role": "点缀色 / 文化标志",
        "use_scene": "门窗装饰、招牌、标识、灯笼、节庆构筑物",
        "ncs_approx": "S 1080-Y90R",
    },
    "沙面蓝": {
        "tag_line": "珠江与租界的对话",
        "extract_logic": "🎯 数据：195°-220° 蓝族 + 自然分类高权重",
        "story": [
            "📌 取自沙面欧式建筑的百叶窗、拱券圳色",
            "📌 也是白鹅潭江面、荔枝湾涌的复合蓝灰",
            "📌 不是纯天蓝（北方天蓝过于明亮），是带灰的「岭南雨季蓝」",
            "📌 与黄色/红色形成完美互补 —— 经典「朱红+靛蓝+米黄」三角",
        ],
        "role": "次主色 / 滨水",
        "use_scene": "百叶窗、构筑物、标识、滨水设施",
        "ncs_approx": "S 5030-R80B",
    },
    "粤剧赭": {
        "tag_line": "岭南文化的暖底色",
        "extract_logic": "🎯 数据：15°-35° 橙红，平均饱和度 66%",
        "story": [
            "📌 取自粤剧戏服中的赭红、广彩瓷器的胭脂红",
            "📌 也是老字号木匾、祠堂木雕、屋檐木构件的色彩",
            "📌 与金色形成「红金搭配」—— 岭南节庆审美的根",
            "📌 比满洲窗红柔和，可大面积使用",
        ],
        "role": "辅色 / 文化暖色",
        "use_scene": "木构件、祠堂彩画、节庆装饰、文化标识",
        "ncs_approx": "S 3050-Y50R",
    },
}

# === 海报参数 ===
W = 1600
PAD = 60
COLOR_BLOCK_H = 600  # 每个色块高度
HEAD_H = 280
FOOT_H = 280
H = HEAD_H + COLOR_BLOCK_H * 5 + FOOT_H

img = Image.new("RGB", (W, H), "#f7f4ee")  # 米白底
draw = ImageDraw.Draw(img)

# 字体
def F(size, bold=False):
    name = "/System/Library/Fonts/Hiragino Sans GB.ttc"
    return ImageFont.truetype(name, size)

font_xlg = F(56, True)
font_lg = F(36, True)
font_md = F(28)
font_sm = F(22)
font_xs = F(18)
font_mono = ImageFont.truetype("/System/Library/Fonts/Menlo.ttc", 32)
font_mono_sm = ImageFont.truetype("/System/Library/Fonts/Menlo.ttc", 20)

# === 标题区 ===
y = 50
draw.text((PAD, y), "🎨 一图读懂", fill="#9a3a1f", font=font_lg)
y += 50
draw.text((PAD, y), "荔湾·西关 城市色彩设计导则", fill="#1a1a1a", font=font_xlg)
y += 80
draw.text((PAD, y), "—— 数据驱动 · 5 色定调 · 5 个文化基因  ·  154 张在线图像分析", fill="#444", font=font_md)
y += 50
draw.text((PAD, y), "范围：恩宁路·永庆坊·沙面·荔枝湾·陈家祠·泮塘五约（约 12 km²）", fill="#666", font=font_sm)

# === 5 色概览条 ===
y = HEAD_H - 80
sw = (W - 2*PAD) // 5
for i, color in enumerate(palette["colors"]):
    x = PAD + i * sw
    rgb = tuple(color["rgb"])
    draw.rectangle([x, y, x+sw-8, y+50], fill=rgb)

# === 每个色的详细板块 ===
y = HEAD_H
for color in palette["colors"]:
    name = color["name"]
    rgb = tuple(color["rgb"])
    hex_v = color["hex"].upper()
    detail = COLOR_DETAILS.get(name, {})
    
    block_top = y
    
    # 左侧色块（占 40%）
    color_w = int((W - 2*PAD) * 0.40)
    draw.rectangle([PAD, y+20, PAD+color_w, y+COLOR_BLOCK_H-20], fill=rgb)
    
    # 色块上写名字+HEX
    luma = 0.299*rgb[0]+0.587*rgb[1]+0.114*rgb[2]
    text_c = "#1a1a1a" if luma > 160 else "#ffffff"
    draw.text((PAD+30, y+50), name, fill=text_c, font=font_xlg)
    draw.text((PAD+30, y+130), detail.get("tag_line",""), fill=text_c, font=font_md)
    draw.text((PAD+30, y+COLOR_BLOCK_H-90), hex_v, fill=text_c, font=font_mono)
    draw.text((PAD+30, y+COLOR_BLOCK_H-55), f"RGB({rgb[0]}, {rgb[1]}, {rgb[2]})", fill=text_c, font=font_mono_sm)
    
    # 右侧文字（占 60%）
    text_x = PAD + color_w + 40
    text_y = y + 30
    
    # NCS 编号
    draw.text((text_x, text_y), f"NCS  {detail.get('ncs_approx','')}    |    角色  {detail.get('role','')}", fill="#9a3a1f", font=font_sm)
    text_y += 50
    
    # extract logic
    draw.text((text_x, text_y), detail.get("extract_logic",""), fill="#1a1a1a", font=font_sm)
    text_y += 45
    
    # 故事点
    for line in detail.get("story", []):
        draw.text((text_x, text_y), line, fill="#333", font=font_sm)
        text_y += 35
    
    text_y += 15
    draw.text((text_x, text_y), "🎯 适用场景：" + detail.get("use_scene", ""), fill="#0a4a4a", font=font_sm)
    text_y += 40
    
    # 代表图缩略图（4 张）
    rep_imgs = matches.get(name, [])[:4]
    thumb_w = 110
    thumb_h = 110
    gap = 12
    tx = text_x
    ty = y + COLOR_BLOCK_H - thumb_h - 30
    draw.text((text_x, ty - 30), "📷 代表图（数据匹配）：", fill="#666", font=font_xs)
    for j, ri in enumerate(rep_imgs):
        src = IMG_DIR / ri["image"]
        if not src.exists(): continue
        try:
            thumb = Image.open(src).convert("RGB")
            tw, th = thumb.size
            scale = thumb_w / tw
            new_h = int(th * scale)
            thumb = thumb.resize((thumb_w, new_h))
            # crop to square
            if new_h > thumb_h:
                top = (new_h - thumb_h) // 2
                thumb = thumb.crop((0, top, thumb_w, top+thumb_h))
            elif new_h < thumb_h:
                # paste on white
                bg = Image.new("RGB", (thumb_w, thumb_h), "#fff")
                bg.paste(thumb, (0, (thumb_h-new_h)//2))
                thumb = bg
            img.paste(thumb, (tx + j*(thumb_w+gap), ty))
        except Exception as e:
            pass
    
    # 板块分割线
    y += COLOR_BLOCK_H
    draw.line([(PAD, y-5), (W-PAD, y-5)], fill="#d0c8b8", width=1)

# === 底部总结 ===
y = HEAD_H + COLOR_BLOCK_H * 5 + 30
draw.text((PAD, y), "📐 提取方法（5 步法）", fill="#9a3a1f", font=font_lg)
y += 60

steps = [
    "1️⃣  关键词搜索 14 类素材   →  154 张在线图像",
    "2️⃣  每张图 K-means 取主导色  →  共 770 个色点",
    "3️⃣  全集再聚类成 30 个色簇   +   按 5 类（民居/历史/自然/老字号/粤剧）各取 8 簇",
    "4️⃣  三元映射：自然(沙面蓝/江景) + 人文(满洲窗红/粤剧赭) + 商埠(骑楼米/麻石青)",
    "5️⃣  综合定调：4 沉静色（麻石青/骑楼米/沙面蓝/粤剧赭）  +  1 点睛色（满洲窗红）",
]
for s in steps:
    draw.text((PAD, y), s, fill="#333", font=font_sm)
    y += 38

y += 20
draw.text((PAD, y), "⚠️ 这是数据驱动的「初版」，正式导则需补充：实地比色、季节加权、专家评审、专用色卡制作", fill="#888", font=font_xs)

img.save(OUT, optimize=True)
print(f"✅ 一图读懂海报：{OUT}")
print(f"   尺寸：{img.size}")
import os
print(f"   大小：{os.path.getsize(OUT)//1024} KB")
