"""
生成单页 HTML 报告 + 把所有素材整理到 web/ 目录
"""
import json, shutil, base64
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DELIV = ROOT / "交付"
WEB = DELIV / "web"
WEB.mkdir(exist_ok=True)
(WEB / "images").mkdir(exist_ok=True)

# 复制全部代表图
matches_path = DELIV / "素材精选" / "matches.json"
with open(matches_path) as f:
    matches = json.load(f)

src_root = ROOT / "2_images"

# 收集每个色的 5 张代表图
color_images = {}
for color_name, items in matches.items():
    paths = []
    for it in items:
        src = src_root / it["image"]
        if src.exists():
            dst = WEB / "images" / src.name
            if not dst.exists():
                shutil.copy2(src, dst)
            paths.append(src.name)
    color_images[color_name] = paths

# 复制色卡海报
shutil.copy2(DELIV / "色卡" / "西关一图读懂.png", WEB / "西关一图读懂.png")
shutil.copy2(DELIV / "色卡" / "5color_palette.png", WEB / "5color_palette.png")

# 加载 5 色数据
with open(DELIV / "色卡" / "5color_palette.json") as f:
    palette = json.load(f)

# 详细文案
COLOR_DETAILS = {
    "麻石青": {
        "tag_line": "西关老城的视觉骨架",
        "ncs": "S 4502-Y50R",
        "extract_logic": "数据 48.6% 暖灰族 + 29.9% 中性灰 = 整个西关 4 张照片里有 3 张以它为主导色",
        "story": [
            "取自麻石巷的青石板，西关大屋的灰青砖外墙",
            "是骑楼内廊的阴影色、也是阴雨天的檐下色",
            "灰带一点暖（接近暖橄榄），不是北方那种冷青砖",
            "在数据里出现频率最高 —— 是西关的「沉默基底」",
        ],
        "reasons": [
            "✅ 客观性最强：数据中权重最高，代表整个老城真实视觉感受",
            "✅ 历史连续性：从清代麻石巷到民国骑楼到当代更新都用它",
            "✅ 不打架：作为主色不会抢戏，给其他色让出空间",
            "✅ 岭南特色：比北方青砖暖一档，带土黄底，符合岭南气候",
        ],
        "use_scene": "建筑外墙主色（70%以上面积）、街道铺装、公共构筑物、设施基础色",
        "ratio": "60%",
    },
    "骑楼米": {
        "tag_line": "100 年商埠的暖墙调",
        "ncs": "S 2010-Y20R",
        "extract_logic": "30°-50° 黄橙色族高权重簇，总占比 9.5%",
        "story": [
            "取自沙面欧式建筑外墙的水刷石仿石色",
            "也是恩宁路骑楼柱身、西关大屋墙面的暖底",
            "比江南粉墙黄一档、比北方土黄淡一档 —— 是「岭南专属」",
            "与英、法殖民建筑的米色形成历史对接",
        ],
        "reasons": [
            "✅ 商埠基因：是 100 年商埠贸易留下的视觉记忆",
            "✅ 历史接续：与英、法殖民建筑的米色形成对接（沙面）",
            "✅ 岭南专属：比江南粉墙黄一档，比北方土黄淡一档",
            "✅ 温度记忆：米黄是岭南「日落时的墙色」，是时间的颜色",
        ],
        "use_scene": "商铺立面、街墙辅色、灯柱栏杆、标识系统底色",
        "ratio": "20%",
    },
    "满洲窗红": {
        "tag_line": "西关大屋的色彩心跳",
        "ncs": "S 1080-Y90R",
        "extract_logic": "饱和度 84% + 明度 84% —— 整个色谱里最亮的色，9 张图里完全是文化语义",
        "story": [
            "取自西关大屋满洲窗的标志红玻璃 —— 中国民居最丰富彩色玻璃",
            "也是粤剧戏服、年节灯笼、老字号金匾红底",
            "在数据里 9 张图里有它（其中 8 张来自粤剧/永庆坊/民居）",
            "高纯度 + 高明度 → 适合做点缀，不可大面积铺",
        ],
        "reasons": [
            "✅ 教科书点睛色：低占比 + 高强度 = 经典「4+1」配比",
            "✅ 文化标志性：满洲窗是国内民居中唯一大规模使用彩色玻璃的传统",
            "✅ 跨场景共鸣：从居住到戏曲到商业 —— 红色在西关有最广的语义",
            "✅ 不可大面积：高强度色只能做点缀，否则视觉过载",
        ],
        "use_scene": "门窗装饰、招牌标识、节庆构筑物、灯笼旗帜（覆盖面积 ≤ 5%）",
        "ratio": "5%",
    },
    "沙面蓝": {
        "tag_line": "珠江与租界的对话",
        "ncs": "S 5030-R80B",
        "extract_logic": "195°-220° 蓝族色簇，总占比 5.1%，自然分类高权重",
        "story": [
            "取自沙面欧式建筑的百叶窗、拱券圳色",
            "也是白鹅潭江面、荔枝湾涌的复合蓝灰",
            "不是纯天蓝（北方天蓝过于明亮），是带灰的「岭南雨季蓝」",
            "与黄/红形成「朱红+靛蓝+米黄」经典三角",
        ],
        "reasons": [
            "✅ 滨水基因：荔湾区「湾」字本义就是水",
            "✅ 租界历史：沙面建筑特色配色 —— 中国少有的欧风蓝",
            "✅ 互补关系：与黄/红形成「朱红+靛蓝+米黄」经典三角",
            "✅ 岭南雨季蓝：带灰带绿，比北方天蓝更「潮湿」",
        ],
        "use_scene": "百叶窗门窗框、滨水栏杆桥梁、标识系统辅色、路灯座椅设施",
        "ratio": "10%",
    },
    "粤剧赭": {
        "tag_line": "岭南文化的暖底色",
        "ncs": "S 3050-Y50R",
        "extract_logic": "15°-35° 橙红色簇，平均饱和度 66% —— 岭南文化「暖底色」",
        "story": [
            "取自粤剧戏服中的赭红、广彩瓷器的胭脂红",
            "也是老字号木匾、祠堂木雕、屋檐木构件",
            "与金色形成「红金搭配」—— 岭南节庆审美的根",
            "比满洲窗红柔和，可大面积使用",
        ],
        "reasons": [
            "✅ 文化暖底：是岭南节庆审美的根（粤剧、广彩、广绣）",
            "✅ 可大面积：比满洲窗红柔和，可覆盖 15-20% 面积",
            "✅ 木质共鸣：与传统木构件天然契合",
            "✅ 金红搭配：与金色组合是岭南节庆审美",
        ],
        "use_scene": "木构件保护色、祠堂彩画修复色、节庆装饰、文化标识系统",
        "ratio": "5%",
    },
}

# === 生成 HTML ===
def text_color(rgb):
    luma = 0.299*rgb[0] + 0.587*rgb[1] + 0.114*rgb[2]
    return "#1a1a1a" if luma > 160 else "#ffffff"

color_blocks_html = ""
for i, color in enumerate(palette["colors"], 1):
    name = color["name"]
    rgb = tuple(color["rgb"])
    hex_v = color["hex"].upper()
    detail = COLOR_DETAILS[name]
    text_c = text_color(rgb)
    
    # 代表图
    imgs_html = ""
    for img_name in color_images.get(name, [])[:5]:
        imgs_html += f'<div class="thumb"><img src="images/{img_name}" alt="{name}" loading="lazy"/></div>'
    
    story_html = "".join(f"<li>{s}</li>" for s in detail["story"])
    reasons_html = "".join(f"<li>{r}</li>" for r in detail["reasons"])
    
    color_blocks_html += f"""
    <section class="color-block" id="color-{i}">
      <div class="color-hero" style="background:{hex_v};color:{text_c}">
        <div class="color-no">{i:02d}</div>
        <div class="color-name">{name}</div>
        <div class="color-tag">{detail['tag_line']}</div>
        <div class="color-meta">
          <div class="hex">{hex_v}</div>
          <div class="rgb">RGB({rgb[0]}, {rgb[1]}, {rgb[2]})</div>
          <div class="ncs">NCS {detail['ncs']}</div>
        </div>
        <div class="color-role">{color['role']} · 用量约 {detail['ratio']}</div>
      </div>
      <div class="color-detail">
        <div class="extract-logic">
          <div class="label">📊 数据驱动证据</div>
          <p>{detail['extract_logic']}</p>
        </div>
        <div class="story">
          <div class="label">📌 取色来源</div>
          <ul>{story_html}</ul>
        </div>
        <div class="reasons">
          <div class="label">✨ 提取理由</div>
          <ul class="reason-list">{reasons_html}</ul>
        </div>
        <div class="use-scene">
          <div class="label">🎯 设计应用</div>
          <p>{detail['use_scene']}</p>
        </div>
        <div class="thumbs">
          <div class="label">📷 代表图（数据匹配）</div>
          <div class="thumbs-row">{imgs_html}</div>
        </div>
      </div>
    </section>
    """

# 5 色概览条 HTML
overview_swatches = ""
for color in palette["colors"]:
    rgb = tuple(color["rgb"])
    overview_swatches += f"""
    <a href="#color-{palette['colors'].index(color)+1}" class="swatch-item" style="background:{color['hex']};color:{text_color(rgb)}">
      <div class="sw-name">{color['name']}</div>
      <div class="sw-hex">{color['hex'].upper()}</div>
    </a>
    """

html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<title>荔湾·西关 城市色彩设计导则</title>
<style>
* {{ margin:0; padding:0; box-sizing:border-box; }}
body {{
  font-family: -apple-system, "PingFang SC", "Hiragino Sans GB", "Microsoft YaHei", sans-serif;
  background: #f7f4ee;
  color: #1a1a1a;
  line-height: 1.7;
}}
.hero {{
  background: linear-gradient(135deg, #868580 0%, #b39f8a 100%);
  color: #fff;
  padding: 80px 60px 100px;
  text-align: center;
  position: relative;
  overflow: hidden;
}}
.hero::before {{
  content: "";
  position: absolute;
  top: -50%; right: -20%;
  width: 600px; height: 600px;
  background: radial-gradient(circle, rgba(216,30,32,0.3) 0%, transparent 70%);
  border-radius: 50%;
}}
.hero h1 {{ font-size: 64px; font-weight: 700; letter-spacing: 2px; position: relative; z-index: 1; }}
.hero .subtitle {{ font-size: 24px; margin-top: 24px; opacity: 0.95; position: relative; z-index: 1; }}
.hero .meta {{ font-size: 16px; margin-top: 32px; opacity: 0.85; position: relative; z-index: 1; }}
.hero .badge {{
  display: inline-block;
  padding: 6px 18px;
  background: rgba(255,255,255,0.2);
  border-radius: 30px;
  margin: 0 6px;
  font-size: 14px;
}}

/* 5 色概览条 */
.swatches-bar {{
  display: grid;
  grid-template-columns: repeat(5, 1fr);
  height: 200px;
  margin: 0;
}}
.swatch-item {{
  display: flex;
  flex-direction: column;
  justify-content: flex-end;
  align-items: flex-start;
  padding: 20px 24px;
  text-decoration: none;
  transition: transform 0.3s;
  cursor: pointer;
}}
.swatch-item:hover {{
  transform: translateY(-8px);
}}
.sw-name {{ font-size: 24px; font-weight: 600; }}
.sw-hex {{ font-family: "SF Mono", Menlo, monospace; font-size: 16px; opacity: 0.85; margin-top: 4px; }}

/* 数据洞察 */
.insights {{
  background: #fff;
  padding: 60px;
  margin: 0;
}}
.insights h2 {{ font-size: 36px; margin-bottom: 24px; color: #9a3a1f; }}
.insights-grid {{
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 24px;
  margin-top: 32px;
}}
.insight-card {{
  background: #faf6ee;
  padding: 28px 24px;
  border-radius: 16px;
  border-left: 4px solid #9a3a1f;
}}
.insight-num {{ font-size: 42px; font-weight: 700; color: #9a3a1f; }}
.insight-label {{ font-size: 14px; color: #666; margin-top: 6px; }}
.insight-desc {{ font-size: 13px; color: #888; margin-top: 8px; }}

/* 色块详细 */
.color-block {{
  display: grid;
  grid-template-columns: 480px 1fr;
  min-height: 600px;
  background: #fff;
  margin-top: 1px;
  position: relative;
}}
.color-hero {{
  padding: 48px 40px;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  position: sticky;
  top: 0;
  height: 600px;
}}
.color-no {{
  font-family: "SF Mono", Menlo, monospace;
  font-size: 24px;
  opacity: 0.4;
}}
.color-name {{ font-size: 64px; font-weight: 700; margin-top: -12px; }}
.color-tag {{ font-size: 22px; opacity: 0.85; margin-top: 8px; }}
.color-meta {{ margin-top: auto; }}
.color-meta .hex {{ font-family: Menlo, monospace; font-size: 36px; font-weight: 600; }}
.color-meta .rgb {{ font-family: Menlo, monospace; font-size: 16px; opacity: 0.85; margin-top: 6px; }}
.color-meta .ncs {{ font-family: Menlo, monospace; font-size: 14px; opacity: 0.7; margin-top: 4px; }}
.color-role {{ margin-top: 16px; font-size: 14px; opacity: 0.75; }}
.color-detail {{
  padding: 48px 60px;
  background: #fff;
}}
.color-detail .label {{
  font-size: 14px;
  color: #9a3a1f;
  font-weight: 600;
  letter-spacing: 1px;
  margin-bottom: 12px;
  text-transform: uppercase;
}}
.color-detail > div {{ margin-bottom: 28px; }}
.color-detail p {{ font-size: 16px; color: #333; }}
.color-detail ul {{ list-style: none; padding-left: 0; }}
.color-detail ul li {{
  padding: 8px 0 8px 24px;
  position: relative;
  font-size: 15px;
  color: #444;
}}
.color-detail .story ul li::before {{
  content: "•";
  position: absolute; left: 8px;
  color: #9a3a1f;
  font-weight: bold;
}}
.reason-list li {{ padding-left: 0 !important; }}
.reason-list li::before {{ display: none; }}

.thumbs-row {{
  display: grid;
  grid-template-columns: repeat(5, 1fr);
  gap: 8px;
  margin-top: 8px;
}}
.thumb {{
  aspect-ratio: 1;
  overflow: hidden;
  border-radius: 8px;
  background: #eee;
}}
.thumb img {{ width:100%; height:100%; object-fit:cover; transition: transform 0.4s; }}
.thumb:hover img {{ transform: scale(1.1); }}

/* 方法论 */
.method {{
  background: #1a1a1a;
  color: #f7f4ee;
  padding: 80px 60px;
}}
.method h2 {{ font-size: 42px; margin-bottom: 32px; color: #ffeb99; }}
.method-steps {{
  display: grid;
  grid-template-columns: repeat(5, 1fr);
  gap: 16px;
  margin-top: 32px;
}}
.method-step {{
  background: rgba(255,255,255,0.05);
  border: 1px solid rgba(255,235,153,0.2);
  padding: 24px;
  border-radius: 12px;
}}
.step-num {{ font-size: 36px; color: #ffeb99; font-weight: 700; }}
.step-title {{ font-size: 18px; font-weight: 600; margin-top: 8px; }}
.step-desc {{ font-size: 13px; opacity: 0.8; margin-top: 8px; line-height: 1.6; }}

/* 三级管控 */
.control {{
  background: #f7f4ee;
  padding: 80px 60px;
}}
.control h2 {{ font-size: 42px; margin-bottom: 32px; color: #9a3a1f; }}
.control-grid {{
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 24px;
}}
.control-card {{
  background: #fff;
  padding: 32px;
  border-radius: 16px;
  box-shadow: 0 4px 20px rgba(0,0,0,0.06);
}}
.control-level {{ font-size: 14px; color: #9a3a1f; font-weight: 600; }}
.control-name {{ font-size: 24px; font-weight: 700; margin-top: 6px; }}
.control-area {{ font-size: 14px; color: #666; margin-top: 8px; }}
.control-rule {{ font-size: 14px; color: #444; margin-top: 16px; line-height: 1.7; }}

/* 海报 */
.poster {{
  padding: 60px;
  background: #fff;
  text-align: center;
}}
.poster h2 {{ font-size: 36px; margin-bottom: 24px; color: #9a3a1f; }}
.poster img {{ max-width: 800px; width: 100%; box-shadow: 0 8px 32px rgba(0,0,0,0.12); border-radius: 8px; }}

/* footer */
footer {{
  padding: 40px 60px;
  background: #1a1a1a;
  color: rgba(255,255,255,0.6);
  text-align: center;
  font-size: 14px;
}}

/* 响应式 */
@media (max-width: 1024px) {{
  .color-block {{ grid-template-columns: 1fr; }}
  .color-hero {{ height: auto; min-height: 360px; position: relative; }}
  .insights-grid {{ grid-template-columns: repeat(2, 1fr); }}
  .method-steps {{ grid-template-columns: repeat(2, 1fr); }}
  .control-grid {{ grid-template-columns: 1fr; }}
  .swatches-bar {{ height: 140px; }}
  .sw-name {{ font-size: 16px; }}
  .sw-hex {{ font-size: 12px; }}
  .hero h1 {{ font-size: 40px; }}
  .hero .subtitle {{ font-size: 18px; }}
  .color-name {{ font-size: 40px; }}
  .color-tag {{ font-size: 16px; }}
  .insights, .method, .control, .poster {{ padding: 40px 24px; }}
  .color-detail {{ padding: 32px 24px; }}
}}
</style>
</head>
<body>

<header class="hero">
  <h1>🎨 荔湾·西关</h1>
  <div class="subtitle">城市色彩设计导则</div>
  <div class="meta">
    <span class="badge">📍 约 12 km²</span>
    <span class="badge">🖼️ 154 张图像</span>
    <span class="badge">🎨 5 色定调</span>
    <span class="badge">📊 数据驱动</span>
  </div>
  <div class="meta" style="margin-top:16px; font-size:14px;">
    范围：恩宁路 · 永庆坊 · 沙面 · 荔枝湾 · 陈家祠 · 泮塘五约
  </div>
</header>

<div class="swatches-bar">
{overview_swatches}
</div>

<section class="insights">
  <h2>📊 数据洞察</h2>
  <p style="font-size:18px; color:#666; max-width:900px;">
    基于 154 张在线图像 K-means 聚类分析，西关老城的真实色彩分布与"刻板印象"很不一样：
  </p>
  <div class="insights-grid">
    <div class="insight-card">
      <div class="insight-num">48.6%</div>
      <div class="insight-label">暖灰族占比</div>
      <div class="insight-desc">青砖+老木+阴影构成的温暖灰，是真正的"底色"</div>
    </div>
    <div class="insight-card">
      <div class="insight-num">29.9%</div>
      <div class="insight-label">中性灰占比</div>
      <div class="insight-desc">麻石巷、青砖墙的标志色</div>
    </div>
    <div class="insight-card">
      <div class="insight-num">9.5%</div>
      <div class="insight-label">米黄占比</div>
      <div class="insight-desc">骑楼、沙面外墙的暖墙调</div>
    </div>
    <div class="insight-card">
      <div class="insight-num">2.0%</div>
      <div class="insight-label">鲜红占比</div>
      <div class="insight-desc">满洲窗、灯笼、戏服 — 占比小但视觉冲击大</div>
    </div>
  </div>
  <p style="margin-top:24px; color:#9a3a1f; font-size:16px; font-weight:600;">
    💡 完全符合"4 沉静 + 1 点睛"的色彩规划经典配比！
  </p>
</section>

{color_blocks_html}

<section class="method">
  <h2>📐 提取方法（5 步法）</h2>
  <p style="font-size:16px; opacity:0.85; max-width:900px;">
    从原始图像到 5 色色谱，全流程数据驱动 + 三元映射。
  </p>
  <div class="method-steps">
    <div class="method-step">
      <div class="step-num">1️⃣</div>
      <div class="step-title">关键词搜索</div>
      <div class="step-desc">14 类素材：西关大屋、满洲窗、骑楼、麻石巷、泮塘五约、沙面、陈家祠、永庆坊、十三行、荔枝湾、白鹅潭、陶陶居、广州酒家、粤剧</div>
    </div>
    <div class="method-step">
      <div class="step-num">2️⃣</div>
      <div class="step-title">每张图取主导色</div>
      <div class="step-desc">154 张 → K-means n=5 → 共 770 个色点</div>
    </div>
    <div class="method-step">
      <div class="step-num">3️⃣</div>
      <div class="step-title">全集 + 分类聚类</div>
      <div class="step-desc">30 个主簇 + 5 类各 8 簇 = 70 个候选色</div>
    </div>
    <div class="method-step">
      <div class="step-num">4️⃣</div>
      <div class="step-title">三元映射</div>
      <div class="step-desc">自然(沙面蓝/江景) + 人文(满洲窗红/粤剧赭) + 商埠(骑楼米/麻石青)</div>
    </div>
    <div class="method-step">
      <div class="step-num">5️⃣</div>
      <div class="step-title">综合定调</div>
      <div class="step-desc">4 沉静色 + 1 点睛色 = 经典 4+1 配比</div>
    </div>
  </div>
</section>

<section class="control">
  <h2>🛡️ 三级管控建议</h2>
  <div class="control-grid">
    <div class="control-card">
      <div class="control-level">一级管控 · 重点营造</div>
      <div class="control-name">核心片区</div>
      <div class="control-area">永庆坊、沙面、陈家祠、泮塘五约</div>
      <div class="control-rule">
        5 色全用，严格按比例：<br>
        🌫️ 麻石青 60% &nbsp;&nbsp; ☕ 骑楼米 20%<br>
        💙 沙面蓝 10% &nbsp;&nbsp; 🟫 粤剧赭 5%<br>
        ❤️ 满洲窗红 5%
      </div>
    </div>
    <div class="control-card">
      <div class="control-level">二级管控 · 一般控制</div>
      <div class="control-name">沿线片区</div>
      <div class="control-area">恩宁路、龙津西路、荔枝湾涌沿线</div>
      <div class="control-rule">
        主色 + 辅色为主<br>
        点缀色限节庆使用<br>
        允许传统材料原色
      </div>
    </div>
    <div class="control-card">
      <div class="control-level">三级管控 · 一般引导</div>
      <div class="control-name">其他片区</div>
      <div class="control-area">荔湾区其他西关片区</div>
      <div class="control-rule">
        负面清单：<br>
        ❌ 高彩度蓝绿/紫红/荧光色<br>
        ✅ 鼓励使用 5 色谱<br>
        ✅ 自由度更大
      </div>
    </div>
  </div>
</section>

<section class="poster">
  <h2>🖼️ 一图读懂海报</h2>
  <img src="西关一图读懂.png" alt="一图读懂"/>
</section>

<footer>
  <p>📁 数据驱动 · 在线远程取色 · 154 张图像 · 制作于 2026-05-22</p>
  <p style="margin-top:8px;">荔湾·西关城市色彩设计导则（数据驱动初版）</p>
</footer>

</body>
</html>
"""

out_html = WEB / "index.html"
with open(out_html, "w", encoding="utf-8") as f:
    f.write(html)

print(f"✅ HTML 生成: {out_html}")
print(f"📁 web 目录: {WEB}")
import os
total_size = sum(os.path.getsize(p) for p in WEB.rglob("*") if p.is_file())
print(f"📊 总大小: {total_size//1024} KB")
print(f"📷 图片: {len(list((WEB/'images').iterdir()))} 张")
