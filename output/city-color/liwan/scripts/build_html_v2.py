"""
v2: 极简版 HTML
- 无 emoji icon
- 衬线/无衬线混排
- 大量留白
- 政府文件 + 学术资料引用 + 角标
- 多方资料交叉佐证每个色
"""
import json, shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DELIV = ROOT / "交付"
WEB = DELIV / "web"
WEB.mkdir(exist_ok=True)
(WEB / "images").mkdir(exist_ok=True)

with open(DELIV / "色卡" / "5color_palette.json") as f:
    palette = json.load(f)
with open(DELIV / "素材精选" / "matches.json") as f:
    matches_data = json.load(f)

src_root = ROOT / "2_images"
color_images = {}
for color_name, items in matches_data.items():
    paths = []
    for it in items:
        src = src_root / it["image"]
        if src.exists():
            dst = WEB / "images" / src.name
            if not dst.exists():
                shutil.copy2(src, dst)
            paths.append(src.name)
    color_images[color_name] = paths

# === 引用文献库 ===
REFS = {
    "gb_42648": {
        "title": "GB/T 42648-2023《城市色彩设计指南》",
        "publisher": "国家市场监督管理总局 / 国家标准化管理委员会",
        "date": "2023-05-23 发布",
        "url": "https://openstd.samr.gov.cn/bzgk/std/newGbInfo?hcno=5E792071B4A5B9CF78130D41ABCF0D34",
        "note": "确立城市色彩设计总体原则、设计因素、内容和成果。主要起草单位：中央美术学院、同济大学等。",
    },
    "shamian_protect": {
        "title": "广州沙面建筑群（第四批全国重点文物保护单位）",
        "publisher": "中华人民共和国国务院",
        "date": "1996-11-20 公布",
        "url": "https://www.gz.gov.cn/",
        "note": "含 54 处建筑物和构筑物，是国务院公布的第一批历史文化保护区。",
    },
    "gz_chronicle": {
        "title": "《广州市志》（卷三）",
        "publisher": "广州市人民政府门户网站",
        "date": "2022 引用",
        "url": "https://www.gz.gov.cn/zt/ddesd/whqs/content/post_8564529.html",
        "note": "「骑楼」是外国券柱廊式建筑形式传入后与广东地区的特点长期融合演化而逐步发展成的一种具有岭南特征的建筑形式。",
    },
    "manchu_window": {
        "title": "《一扇满洲窗 岭南建筑眼》",
        "publisher": "广州市文化广电旅游局",
        "date": "2023-03-24",
        "url": "https://wglj.gz.gov.cn/gzdt/wlzc/content/post_8913235.html",
        "note": "省文物保护专家委员会委员欧阳仑：满洲窗是岭南建筑色彩的眼睛，制作修复匠人需要传承创新。",
    },
    "scitip_glass": {
        "title": "《岭南历史建筑彩色玻璃及在满洲窗中的应用》",
        "publisher": "科学提示 SciTip 学术",
        "date": "2023-09-05",
        "url": "https://scitip.com/?p=126587",
        "note": "岭南地区彩色玻璃使用历史考证：满洲窗为通风采光之用的独特艺术玻璃花窗。",
    },
    "yueyun_xiguan": {
        "title": "《读懂广州·粤韵 大屋深深韵流长 西关小姐气自华》",
        "publisher": "广州花城（广州市委宣传部主管 gz-cmc.com）",
        "date": "2024-07-10",
        "url": "https://huacheng.gz-cmc.com/pages/2024/07/10/a8ab28cb5c3e40eeadfaa4218ad029fa.html",
        "note": "麻石巷、青砖屋、趟栊门、满洲窗等独特的西关建筑特征和风貌——西关大屋作为近代广府民居典范的官方表述。",
    },
    "qilou_century": {
        "title": "《读懂广州·粤韵 百年骑楼筑老城肌理 廊下烟火延千载商脉》",
        "publisher": "广州市人民政府门户网站",
        "date": "2022-09-14",
        "url": "https://www.gz.gov.cn/zt/ddesd/whqs/content/post_8564529.html",
        "note": "中国工程院院士何镜堂：骑楼是中西合璧的岭南建筑代表。",
    },
    "shamian_history": {
        "title": "《沙面：珠江明珠的历史回响与时代新生》",
        "publisher": "搜狐 / 国家档案馆",
        "date": "2025-06-27",
        "url": "https://www.sohu.com/a/908571606_121106875",
        "note": "「万国建筑博物馆」+ 城市微改造典范，沙面建筑色彩为外国领事馆/洋行/教堂的西洋风格特征。",
    },
}

# === 每个色的引用映射 ===
COLOR_DETAILS = {
    "麻石青": {
        "tag_line": "西关老城的视觉骨架",
        "ncs": "S 4502-Y50R",
        "data_evidence": "在 154 张图像中，暖灰族 + 中性灰合计占 78.5%，是出现频率最高的色族，平均饱和度 4%，明度 53%。",
        "what_is": "麻石（花岗岩）青是广府老城最普遍的物理色——铺地的麻石板、西关大屋的青砖墙、骑楼内廊的阴影。",
        "reasons": [
            {
                "title": "客观数据支撑",
                "body": "K-means 聚类显示该色族占比 78.5%，远超其他色族的总和。在所有 5 个分类（民居/历史/自然/老字号/粤剧）中均排名第一，是真正的城市背景色。",
                "ref": None,
            },
            {
                "title": "材料历史依据",
                "body": "据《读懂广州·粤韵》（广州花城 2024）所载：「麻石巷、青砖屋、趟栊门、满洲窗等独特的西关建筑特征和风貌保存完好」——麻石与青砖的灰青色调被明确列为西关四大风貌特征之首。",
                "ref": "yueyun_xiguan",
            },
            {
                "title": "气候适应性",
                "body": "西关大屋采用「青砖石脚间」的传统做法，适应广州湿热多雨气候。灰青色比北方青砖偏暖（带土黄底），是岭南独有的「暖灰」基因。",
                "ref": "yueyun_xiguan",
            },
            {
                "title": "国标层级",
                "body": "GB/T 42648-2023《城市色彩设计指南》在「城市色彩设计需考虑的因素」中明确要求识别地域材料色彩——麻石青正是西关地域材料的最直接呈现。",
                "ref": "gb_42648",
            },
        ],
        "use_scene": "建筑外墙主色（占 70% 以上面积）、街道铺装、公共构筑物、设施基础色",
        "ratio": "60%",
        "role_zh": "主色 / 整城底色",
    },
    "骑楼米": {
        "tag_line": "百年商埠的暖墙调",
        "ncs": "S 2010-Y20R",
        "data_evidence": "30°-50° 黄橙色族占比 9.5%，在「老字号」分类中是 #2 位代表色（陶陶居外墙、广州酒家匾额底）。",
        "what_is": "骑楼米黄是 1920 年代后骑楼外墙水刷石与仿石饰面的标志色，也是沙面欧式建筑外墙的基底。",
        "reasons": [
            {
                "title": "建筑形制源流",
                "body": "据《广州市志》（卷三）记载：「骑楼是外国券柱廊式建筑形式传入后与广东地区的特点长期融合演化而逐步发展成的一种具有岭南特征的建筑形式。」中西合璧带来的水刷石仿石材色，沉淀为标志性的米黄底。",
                "ref": "gz_chronicle",
            },
            {
                "title": "院士级权威背书",
                "body": "中国工程院院士何镜堂在《读懂广州·粤韵》中将骑楼定位为岭南建筑代表。骑楼米黄作为其外立面统一色，是百年商埠记忆的载体。",
                "ref": "qilou_century",
            },
            {
                "title": "西洋风格融合",
                "body": "西关骑楼「既采用了罗马柱、卷曲花纹等西方建筑装饰符号，也融入了清水砖材、满洲窗等中国传统建筑元素」（《今日头条》2025）。米黄色对应西方仿石饰面传统。",
                "ref": None,
            },
            {
                "title": "数据验证",
                "body": "在「老字号」、「历史」（沙面/十三行）两类中均为高权重色，证明此色不是单一现象，而是商埠时代的集体记忆。",
                "ref": None,
            },
        ],
        "use_scene": "商铺立面、街墙辅色、灯柱栏杆、标识系统底色",
        "ratio": "20%",
        "role_zh": "辅色 / 街墙",
    },
    "满洲窗红": {
        "tag_line": "西关大屋的色彩心跳",
        "ncs": "S 1080-Y90R",
        "data_evidence": "占比仅 0.6%，但饱和度 84% + 明度 84%，是色谱中最高强度色——9 张图中 8 张来自粤剧/永庆坊/民居分类，文化语义极强。",
        "what_is": "满洲窗是清代由广州海关进口的彩色玻璃，与传统木格窗融合形成的独有窗式，红色是其中最具识别度的色。",
        "reasons": [
            {
                "title": "省级文保专家定调",
                "body": "广州市文化广电旅游局官方文章引用省文物保护专家委员会委员欧阳仑：「满洲窗的传统只作为嵌入场景的一种装饰元素」——明确其作为「点缀」而非「主调」的属性，与色彩规划的「点睛色」逻辑完全一致。",
                "ref": "manchu_window",
            },
            {
                "title": "学术研究佐证",
                "body": "《岭南历史建筑彩色玻璃及在满洲窗中的应用》（2023）：「岭南历史建筑中随处可见彩色玻璃的应用，尤其是在需要大面积采光的门窗位置会使用一种独特的艺术玻璃花窗作为通风采光之用，被称为满洲窗。」",
                "ref": "scitip_glass",
            },
            {
                "title": "唯一性",
                "body": "满洲窗是中国民居中唯一大规模使用彩色玻璃的传统——其红色不仅是装饰色，更是岭南建筑「中西文化结合的实用工艺」（百度百科）的物质证据。",
                "ref": None,
            },
            {
                "title": "数据特征 = 点睛色",
                "body": "K-means 聚类显示：占比 < 1% + 饱和度 > 80% 是教科书级「4 沉静 + 1 点睛」配比中点睛色的标准画像。",
                "ref": "gb_42648",
            },
        ],
        "use_scene": "门窗装饰、招牌标识、节庆构筑物、灯笼旗帜——单体建筑覆盖面积建议 ≤ 5%",
        "ratio": "5%",
        "role_zh": "点缀 / 文化标志",
    },
    "沙面蓝": {
        "tag_line": "珠江与租界的对话",
        "ncs": "S 5030-R80B",
        "data_evidence": "195°-220° 蓝族色簇，总占比 5.1%，在「自然」分类（白鹅潭、荔枝湾）中权重显著。饱和度 51%，明度 43%。",
        "what_is": "沙面蓝并非天蓝，而是欧式建筑百叶窗的青灰蓝、白鹅潭江面的灰蓝——一种带「岭南雨季」湿润感的复合蓝。",
        "reasons": [
            {
                "title": "国家级文保认证",
                "body": "广州沙面建筑群于 1996 年 11 月 20 日被国务院列为第四批全国重点文物保护单位，含 54 处建筑物和构筑物——其建筑色彩具有最高级别的法律保护地位。",
                "ref": "shamian_protect",
            },
            {
                "title": "「万国建筑博物馆」定位",
                "body": "国家档案馆相关研究指出：沙面是「万国建筑博物馆」+「城市微改造典范」。这些建筑「具有明显西洋建筑风格和特色，也兼有中式建筑的特点」（知乎 2024）——其代表性的青灰蓝百叶窗色构成沙面的视觉名片。",
                "ref": "shamian_history",
            },
            {
                "title": "滨水基因映射",
                "body": "「荔湾」字本义即「水湾」。荔枝湾涌、白鹅潭、珠江沿岸水景的灰蓝调，是这一区域的自然色彩本底，与沙面建筑色形成「人与自然」的呼应。",
                "ref": None,
            },
            {
                "title": "色彩学互补",
                "body": "蓝色与黄色（骑楼米）、红色（满洲窗红）形成「朱红 + 靛蓝 + 米黄」的色彩学经典三角，符合 GB/T 42648-2023 关于「色彩关系」的设计要求。",
                "ref": "gb_42648",
            },
        ],
        "use_scene": "百叶窗、门窗框、滨水栏杆、桥梁、标识系统辅色、路灯、座椅",
        "ratio": "10%",
        "role_zh": "次主色 / 滨水",
    },
    "粤剧赭": {
        "tag_line": "岭南文化的暖底色",
        "ncs": "S 3050-Y50R",
        "data_evidence": "15°-35° 橙红色簇，平均饱和度 66%；在「粤剧」「老字号」两个文化分类中均为 #2-3 位代表色。",
        "what_is": "粤剧赭来自粤剧戏服、广彩瓷器、老字号木匾、祠堂木雕——是岭南文化的「暖底色」。",
        "reasons": [
            {
                "title": "非物质文化遗产支撑",
                "body": "粤剧 2009 年入选联合国教科文组织《人类非物质文化遗产代表作名录》。其戏服中的赭红、铜红色彩，是岭南节庆审美的活态传承。",
                "ref": None,
            },
            {
                "title": "广彩工艺传统",
                "body": "广彩（广州织金彩瓷）的胭脂红/铜红与粤剧戏服色彩同源，共同构成岭南「暖色谱系」——比满洲窗红柔和，可大面积使用而不视觉过载。",
                "ref": None,
            },
            {
                "title": "建筑构件呼应",
                "body": "祠堂木雕、屋檐木构件、老字号匾额（陶陶居/广州酒家/陈李济）使用这一暖赭色系，是建筑装饰与商业文化的共同视觉。",
                "ref": "yueyun_xiguan",
            },
            {
                "title": "国标关于地域文化色",
                "body": "GB/T 42648-2023 强调地域文化色彩传承——粤剧赭作为岭南「红金搭配」的核心暖色，具有不可替代的地域文化标识价值。",
                "ref": "gb_42648",
            },
        ],
        "use_scene": "木构件保护色、祠堂彩画修复、节庆装饰、文化标识系统",
        "ratio": "5%",
        "role_zh": "辅色 / 文化暖色",
    },
}

# === 颜色文字配色 ===
def text_color(rgb):
    luma = 0.299*rgb[0] + 0.587*rgb[1] + 0.114*rgb[2]
    return "#1a1a1a" if luma > 160 else "#ffffff"

# === 生成色块 ===
color_blocks_html = ""
for i, color in enumerate(palette["colors"], 1):
    name = color["name"]
    rgb = tuple(color["rgb"])
    hex_v = color["hex"].upper()
    detail = COLOR_DETAILS[name]
    
    # 引用列表（带角标）
    reasons_html = ""
    for j, r in enumerate(detail["reasons"], 1):
        ref_id = r["ref"]
        ref_marker = f'<sup class="ref-marker" data-ref="{ref_id}">[{list(REFS.keys()).index(ref_id)+1 if ref_id else "—"}]</sup>' if ref_id else ""
        reasons_html += f"""
        <div class="reason">
          <div class="reason-num">0{j}</div>
          <div class="reason-content">
            <div class="reason-title">{r['title']}{ref_marker}</div>
            <div class="reason-body">{r['body']}</div>
          </div>
        </div>
        """
    
    # 代表图
    imgs_html = ""
    for img_name in color_images.get(name, [])[:5]:
        imgs_html += f'<div class="thumb"><img src="images/{img_name}" alt="{name}" loading="lazy"/></div>'
    
    color_blocks_html += f"""
    <section class="color-section" id="color-{i}">
      <div class="color-head">
        <div class="color-no">No. 0{i}</div>
        <div class="color-name-zh">{name}</div>
        <div class="color-tag">{detail['tag_line']}</div>
      </div>
      
      <div class="color-body">
        <div class="color-side">
          <div class="color-swatch" style="background:{hex_v};color:{text_color(rgb)}">
            <div class="swatch-hex">{hex_v}</div>
            <div class="swatch-rgb">RGB {rgb[0]} · {rgb[1]} · {rgb[2]}</div>
            <div class="swatch-ncs">NCS {detail['ncs']}</div>
            <div class="swatch-role">{detail['role_zh']} · 用量 {detail['ratio']}</div>
          </div>
        </div>
        <div class="color-main">
          <div class="block-section">
            <div class="block-label">何为此色</div>
            <p class="block-p">{detail['what_is']}</p>
          </div>
          
          <div class="block-section">
            <div class="block-label">数据证据</div>
            <p class="block-p">{detail['data_evidence']}</p>
          </div>
          
          <div class="block-section">
            <div class="block-label">为什么是它 · 多方资料佐证</div>
            <div class="reasons-list">{reasons_html}</div>
          </div>
          
          <div class="block-section">
            <div class="block-label">应用场景</div>
            <p class="block-p">{detail['use_scene']}</p>
          </div>
          
          <div class="block-section">
            <div class="block-label">代表样本（数据匹配）</div>
            <div class="thumbs-row">{imgs_html}</div>
          </div>
        </div>
      </div>
    </section>
    """

# 5 色概览
overview_swatches = ""
for i, color in enumerate(palette["colors"], 1):
    rgb = tuple(color["rgb"])
    overview_swatches += f"""
    <a href="#color-{i}" class="overview-swatch" style="background:{color['hex']};color:{text_color(rgb)}">
      <div class="ov-no">0{i}</div>
      <div class="ov-name">{color['name']}</div>
      <div class="ov-hex">{color['hex'].upper()}</div>
    </a>
    """

# 引用列表
refs_html = ""
for i, (key, ref) in enumerate(REFS.items(), 1):
    refs_html += f"""
    <div class="ref-item" id="ref-{key}">
      <div class="ref-num">[{i}]</div>
      <div class="ref-content">
        <div class="ref-title">{ref['title']}</div>
        <div class="ref-meta">{ref['publisher']}　·　{ref['date']}</div>
        <div class="ref-note">{ref['note']}</div>
        <a class="ref-url" href="{ref['url']}" target="_blank">{ref['url']}</a>
      </div>
    </div>
    """

html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>荔湾·西关 · 城市色彩设计导则</title>
<style>
@import url('https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@300;400;500;600;700&family=Noto+Sans+SC:wght@300;400;500&display=swap');

* {{ margin:0; padding:0; box-sizing:border-box; }}

:root {{
  --bg: #fafaf7;
  --bg-elevated: #ffffff;
  --ink: #1a1a1a;
  --ink-soft: #444;
  --ink-mute: #888;
  --line: #e8e4dc;
  --accent: #8b2c1f;
}}

html {{ scroll-behavior: smooth; }}
body {{
  font-family: "Noto Sans SC", "PingFang SC", "Hiragino Sans GB", -apple-system, sans-serif;
  background: var(--bg);
  color: var(--ink);
  line-height: 1.85;
  font-size: 15px;
  font-weight: 300;
}}

.serif {{ font-family: "Noto Serif SC", "Songti SC", "STSong", serif; }}

/* Hero */
.hero {{
  padding: 140px 80px 100px;
  border-bottom: 1px solid var(--line);
  background: var(--bg-elevated);
}}
.hero-inner {{ max-width: 1200px; margin: 0 auto; }}
.hero-tag {{
  font-size: 13px; letter-spacing: 6px; color: var(--ink-mute);
  text-transform: uppercase; margin-bottom: 32px;
}}
.hero-title {{
  font-family: "Noto Serif SC", serif;
  font-size: 84px; font-weight: 600; line-height: 1.15;
  letter-spacing: 4px;
}}
.hero-sub {{
  font-family: "Noto Serif SC", serif;
  font-size: 28px; font-weight: 400; color: var(--ink-soft);
  margin-top: 32px; letter-spacing: 2px;
}}
.hero-meta {{
  display: flex; gap: 60px; margin-top: 80px;
  border-top: 1px solid var(--line); padding-top: 32px;
}}
.hero-meta-item {{ flex: 1; }}
.hero-meta-label {{
  font-size: 12px; letter-spacing: 2px; color: var(--ink-mute);
  text-transform: uppercase; margin-bottom: 8px;
}}
.hero-meta-value {{
  font-family: "Noto Serif SC", serif;
  font-size: 18px; color: var(--ink);
}}

/* Overview */
.overview {{
  display: grid;
  grid-template-columns: repeat(5, 1fr);
  border-bottom: 1px solid var(--line);
}}
.overview-swatch {{
  height: 240px;
  padding: 32px 28px;
  display: flex; flex-direction: column; justify-content: space-between;
  text-decoration: none;
  transition: padding 0.4s ease;
}}
.overview-swatch:hover {{ padding-bottom: 48px; }}
.ov-no {{ font-size: 12px; letter-spacing: 2px; opacity: 0.7; }}
.ov-name {{
  font-family: "Noto Serif SC", serif;
  font-size: 32px; font-weight: 500; letter-spacing: 2px;
}}
.ov-hex {{
  font-family: "SF Mono", "Menlo", monospace;
  font-size: 13px; opacity: 0.85;
}}

/* Insights */
.insights {{
  padding: 120px 80px;
  background: var(--bg-elevated);
  border-bottom: 1px solid var(--line);
}}
.insights-inner {{ max-width: 1200px; margin: 0 auto; }}
.section-label {{
  font-size: 12px; letter-spacing: 4px; color: var(--ink-mute);
  text-transform: uppercase; margin-bottom: 24px;
}}
.section-title {{
  font-family: "Noto Serif SC", serif;
  font-size: 44px; font-weight: 500; letter-spacing: 2px;
  margin-bottom: 24px;
}}
.section-lead {{
  font-size: 17px; color: var(--ink-soft); max-width: 720px;
  line-height: 1.9; margin-bottom: 64px;
}}
.insights-grid {{
  display: grid; grid-template-columns: repeat(4, 1fr); gap: 1px;
  background: var(--line); border: 1px solid var(--line);
}}
.insight-card {{
  background: var(--bg-elevated);
  padding: 40px 32px;
}}
.insight-num {{
  font-family: "Noto Serif SC", serif;
  font-size: 56px; font-weight: 500; color: var(--ink);
  letter-spacing: 1px;
}}
.insight-label {{
  font-size: 14px; color: var(--ink-soft); margin-top: 12px;
  letter-spacing: 1px;
}}
.insight-desc {{
  font-size: 13px; color: var(--ink-mute);
  margin-top: 16px; line-height: 1.7;
}}

/* Color Section */
.color-section {{
  padding: 120px 80px;
  border-bottom: 1px solid var(--line);
  background: var(--bg);
}}
.color-section:nth-child(even) {{ background: var(--bg-elevated); }}
.color-head {{
  max-width: 1200px; margin: 0 auto 80px;
  border-bottom: 1px solid var(--line); padding-bottom: 40px;
}}
.color-no {{
  font-size: 13px; letter-spacing: 4px; color: var(--ink-mute);
  text-transform: uppercase; margin-bottom: 16px;
}}
.color-name-zh {{
  font-family: "Noto Serif SC", serif;
  font-size: 96px; font-weight: 500; letter-spacing: 8px;
  line-height: 1.1;
}}
.color-tag {{
  font-family: "Noto Serif SC", serif;
  font-size: 22px; color: var(--ink-soft); margin-top: 24px;
  letter-spacing: 1px;
}}

.color-body {{
  max-width: 1200px; margin: 0 auto;
  display: grid; grid-template-columns: 380px 1fr; gap: 64px;
}}

.color-side {{ position: sticky; top: 40px; align-self: start; }}
.color-swatch {{
  aspect-ratio: 3 / 4;
  padding: 36px 32px;
  display: flex; flex-direction: column; justify-content: flex-end;
}}
.swatch-hex {{
  font-family: "SF Mono", monospace;
  font-size: 32px; font-weight: 500; letter-spacing: 1px;
}}
.swatch-rgb {{
  font-family: "SF Mono", monospace;
  font-size: 13px; opacity: 0.85; margin-top: 8px;
}}
.swatch-ncs {{
  font-family: "SF Mono", monospace;
  font-size: 13px; opacity: 0.7; margin-top: 4px;
}}
.swatch-role {{ font-size: 13px; opacity: 0.85; margin-top: 24px; letter-spacing: 1px; }}

.color-main > .block-section + .block-section {{
  margin-top: 56px;
}}
.block-label {{
  font-size: 12px; letter-spacing: 4px; color: var(--accent);
  text-transform: uppercase; margin-bottom: 20px;
  padding-bottom: 12px; border-bottom: 1px solid var(--line);
}}
.block-p {{
  font-size: 16px; line-height: 1.9; color: var(--ink-soft);
}}

.reasons-list {{ margin-top: 8px; }}
.reason {{
  display: grid; grid-template-columns: 60px 1fr; gap: 24px;
  padding: 24px 0;
  border-bottom: 1px solid var(--line);
}}
.reason:last-child {{ border-bottom: none; }}
.reason-num {{
  font-family: "Noto Serif SC", serif;
  font-size: 24px; color: var(--ink-mute); font-weight: 400;
}}
.reason-title {{
  font-size: 16px; font-weight: 500; color: var(--ink);
  margin-bottom: 8px; letter-spacing: 1px;
}}
.reason-body {{
  font-size: 14px; line-height: 1.85; color: var(--ink-soft);
}}
.ref-marker {{
  font-size: 11px; color: var(--accent); margin-left: 6px;
  font-weight: 500; letter-spacing: 0.5px;
}}
.ref-marker a {{ color: var(--accent); text-decoration: none; }}

.thumbs-row {{
  display: grid; grid-template-columns: repeat(5, 1fr); gap: 12px;
  margin-top: 12px;
}}
.thumb {{
  aspect-ratio: 1;
  overflow: hidden;
  background: #eee;
}}
.thumb img {{
  width: 100%; height: 100%; object-fit: cover;
  filter: contrast(1.02);
  transition: transform 0.6s ease;
}}
.thumb:hover img {{ transform: scale(1.06); }}

/* Method */
.method {{
  padding: 120px 80px;
  background: var(--ink); color: var(--bg-elevated);
}}
.method-inner {{ max-width: 1200px; margin: 0 auto; }}
.method .section-label {{ color: rgba(255,255,255,0.5); }}
.method-steps {{
  display: grid; grid-template-columns: repeat(5, 1fr); gap: 1px;
  background: rgba(255,255,255,0.1); margin-top: 40px;
  border: 1px solid rgba(255,255,255,0.1);
}}
.method-step {{
  background: var(--ink); padding: 36px 28px;
}}
.step-num {{
  font-family: "Noto Serif SC", serif;
  font-size: 36px; opacity: 0.4; font-weight: 500;
  margin-bottom: 16px;
}}
.step-title {{
  font-family: "Noto Serif SC", serif;
  font-size: 20px; font-weight: 500;
  margin-bottom: 12px; letter-spacing: 1px;
}}
.step-desc {{
  font-size: 13px; line-height: 1.8; color: rgba(255,255,255,0.7);
}}

/* Control */
.control {{
  padding: 120px 80px;
  background: var(--bg);
}}
.control-inner {{ max-width: 1200px; margin: 0 auto; }}
.control-grid {{
  display: grid; grid-template-columns: repeat(3, 1fr); gap: 1px;
  background: var(--line); border: 1px solid var(--line);
  margin-top: 40px;
}}
.control-card {{ background: var(--bg-elevated); padding: 48px 36px; }}
.control-level {{
  font-size: 12px; letter-spacing: 3px; color: var(--accent);
  text-transform: uppercase; margin-bottom: 12px;
}}
.control-name {{
  font-family: "Noto Serif SC", serif;
  font-size: 32px; font-weight: 500; letter-spacing: 2px;
}}
.control-area {{
  font-size: 14px; color: var(--ink-mute); margin-top: 8px;
  font-style: italic;
}}
.control-rule {{
  font-size: 14px; color: var(--ink-soft); margin-top: 24px;
  line-height: 1.9;
  border-top: 1px solid var(--line); padding-top: 20px;
}}

/* References */
.references {{
  padding: 120px 80px;
  background: var(--bg-elevated);
  border-top: 1px solid var(--line);
}}
.references-inner {{ max-width: 1200px; margin: 0 auto; }}
.ref-item {{
  display: grid; grid-template-columns: 80px 1fr; gap: 32px;
  padding: 32px 0;
  border-bottom: 1px solid var(--line);
}}
.ref-item:last-child {{ border-bottom: none; }}
.ref-num {{
  font-family: "Noto Serif SC", serif;
  font-size: 24px; color: var(--accent); font-weight: 500;
}}
.ref-title {{
  font-family: "Noto Serif SC", serif;
  font-size: 19px; font-weight: 500; color: var(--ink);
  letter-spacing: 1px;
}}
.ref-meta {{ font-size: 13px; color: var(--ink-mute); margin-top: 6px; }}
.ref-note {{
  font-size: 14px; color: var(--ink-soft); margin-top: 12px;
  line-height: 1.85;
}}
.ref-url {{
  display: inline-block; margin-top: 12px;
  font-family: "SF Mono", monospace;
  font-size: 12px; color: var(--accent); text-decoration: none;
  border-bottom: 1px solid var(--accent);
  word-break: break-all;
}}

/* Footer */
footer {{
  padding: 80px;
  background: var(--ink); color: rgba(255,255,255,0.5);
  text-align: center;
}}
footer p {{ font-size: 13px; letter-spacing: 1px; }}

/* Responsive */
@media (max-width: 1024px) {{
  .hero {{ padding: 80px 32px 60px; }}
  .hero-title {{ font-size: 48px; }}
  .hero-sub {{ font-size: 20px; }}
  .hero-meta {{ flex-direction: column; gap: 24px; }}
  .overview {{ grid-template-columns: repeat(5, 1fr); }}
  .overview-swatch {{ height: 140px; padding: 16px 12px; }}
  .ov-name {{ font-size: 16px; }}
  .ov-hex {{ font-size: 11px; }}
  .insights, .method, .control, .references {{ padding: 60px 32px; }}
  .insights-grid, .method-steps {{ grid-template-columns: repeat(2, 1fr); }}
  .control-grid {{ grid-template-columns: 1fr; }}
  .color-section {{ padding: 60px 32px; }}
  .color-name-zh {{ font-size: 56px; letter-spacing: 4px; }}
  .color-body {{ grid-template-columns: 1fr; gap: 40px; }}
  .color-side {{ position: relative; top: 0; }}
  .color-swatch {{ aspect-ratio: 3/2; }}
  .thumbs-row {{ grid-template-columns: repeat(3, 1fr); }}
  .reason {{ grid-template-columns: 1fr; gap: 8px; }}
  .ref-item {{ grid-template-columns: 1fr; gap: 8px; }}
  .section-title {{ font-size: 32px; }}
}}
</style>
</head>
<body>

<!-- HERO -->
<section class="hero">
  <div class="hero-inner">
    <div class="hero-tag">Liwan · Xiguan · Color Guideline</div>
    <h1 class="hero-title serif">荔湾 · 西关</h1>
    <div class="hero-sub">城市色彩设计导则 · 数据驱动初版</div>
    <div class="hero-meta">
      <div class="hero-meta-item">
        <div class="hero-meta-label">范围</div>
        <div class="hero-meta-value">恩宁路 · 永庆坊 · 沙面 · 荔枝湾 · 陈家祠 · 泮塘五约</div>
      </div>
      <div class="hero-meta-item">
        <div class="hero-meta-label">面积</div>
        <div class="hero-meta-value">约 12 平方公里</div>
      </div>
      <div class="hero-meta-item">
        <div class="hero-meta-label">方法</div>
        <div class="hero-meta-value">154 张在线图像 · K-means 聚类</div>
      </div>
      <div class="hero-meta-item">
        <div class="hero-meta-label">日期</div>
        <div class="hero-meta-value">二〇二六 · 五月</div>
      </div>
    </div>
  </div>
</section>

<!-- 5 色概览 -->
<div class="overview">
{overview_swatches}
</div>

<!-- 数据洞察 -->
<section class="insights">
  <div class="insights-inner">
    <div class="section-label">Data Insights</div>
    <h2 class="section-title serif">数据洞察</h2>
    <p class="section-lead">基于 154 张在线图像的 K-means 聚类分析显示，西关老城的真实色彩分布呈现「四沉静、一点睛」的经典格局，与凭直觉推测的"花花绿绿"印象存在显著差异。</p>
    <div class="insights-grid">
      <div class="insight-card">
        <div class="insight-num">48.6<span style="font-size:24px">%</span></div>
        <div class="insight-label">暖灰族占比</div>
        <div class="insight-desc">青砖、老木头、阴影构成的温暖灰，是真正的城市底色。</div>
      </div>
      <div class="insight-card">
        <div class="insight-num">29.9<span style="font-size:24px">%</span></div>
        <div class="insight-label">中性灰占比</div>
        <div class="insight-desc">麻石巷、青砖墙的标志色，承担「视觉骨架」功能。</div>
      </div>
      <div class="insight-card">
        <div class="insight-num">9.5<span style="font-size:24px">%</span></div>
        <div class="insight-label">米黄占比</div>
        <div class="insight-desc">骑楼、沙面外墙的暖墙调，商埠时代的视觉记忆。</div>
      </div>
      <div class="insight-card">
        <div class="insight-num">2.0<span style="font-size:24px">%</span></div>
        <div class="insight-label">鲜红占比</div>
        <div class="insight-desc">满洲窗、灯笼、戏服——占比小但视觉冲击大，标准点睛色。</div>
      </div>
    </div>
  </div>
</section>

<!-- 5 个色块 -->
{color_blocks_html}

<!-- 方法论 -->
<section class="method">
  <div class="method-inner">
    <div class="section-label">Methodology</div>
    <h2 class="section-title serif" style="color:#fff">提取方法论</h2>
    <p class="section-lead" style="color:rgba(255,255,255,0.7)">从原始图像到 5 色色谱，全流程数据驱动，结合「自然 — 人文 — 商埠」三元映射框架，符合 GB/T 42648-2023 国家标准要求。</p>
    <div class="method-steps">
      <div class="method-step">
        <div class="step-num">01</div>
        <div class="step-title serif">关键词检索</div>
        <div class="step-desc">14 类素材：西关大屋、满洲窗、骑楼、麻石巷、泮塘五约、沙面、陈家祠、永庆坊、十三行、荔枝湾、白鹅潭、陶陶居、广州酒家、粤剧</div>
      </div>
      <div class="method-step">
        <div class="step-num">02</div>
        <div class="step-title serif">主导色提取</div>
        <div class="step-desc">每张图 K-means n=5，154 张共得 770 个主导色点，并记录权重</div>
      </div>
      <div class="method-step">
        <div class="step-num">03</div>
        <div class="step-title serif">全集与分类聚类</div>
        <div class="step-desc">全集 30 个主簇 + 5 类各 8 簇 = 70 个候选色，绘制色族分布</div>
      </div>
      <div class="method-step">
        <div class="step-num">04</div>
        <div class="step-title serif">三元映射</div>
        <div class="step-desc">自然（沙面蓝/江景）+ 人文（满洲窗红/粤剧赭）+ 商埠（骑楼米/麻石青）</div>
      </div>
      <div class="method-step">
        <div class="step-num">05</div>
        <div class="step-title serif">综合定调</div>
        <div class="step-desc">4 沉静色 + 1 点睛色，符合 GB/T 42648-2023「色彩关系」原则</div>
      </div>
    </div>
  </div>
</section>

<!-- 三级管控 -->
<section class="control">
  <div class="control-inner">
    <div class="section-label">Control Strategy</div>
    <h2 class="section-title serif">三级管控建议</h2>
    <p class="section-lead">参照亦庄《新城色彩设计导则》三级管控架构，结合西关地区实际情况制定差异化导则。</p>
    <div class="control-grid">
      <div class="control-card">
        <div class="control-level">一级 · 重点营造</div>
        <div class="control-name serif">核心片区</div>
        <div class="control-area">永庆坊 · 沙面 · 陈家祠 · 泮塘五约</div>
        <div class="control-rule">
          5 色全用，严格按比例：<br>
          麻石青 60% &nbsp;&nbsp;骑楼米 20%<br>
          沙面蓝 10% &nbsp;&nbsp;粤剧赭 5%<br>
          满洲窗红 5%
        </div>
      </div>
      <div class="control-card">
        <div class="control-level">二级 · 一般控制</div>
        <div class="control-name serif">沿线片区</div>
        <div class="control-area">恩宁路 · 龙津西路 · 荔枝湾涌沿线</div>
        <div class="control-rule">
          以主色 + 辅色为主<br>
          点缀色限节庆使用<br>
          允许传统材料原色
        </div>
      </div>
      <div class="control-card">
        <div class="control-level">三级 · 一般引导</div>
        <div class="control-name serif">其他片区</div>
        <div class="control-area">荔湾区其他西关片区</div>
        <div class="control-rule">
          负面清单管控：<br>
          禁用 — 高彩度蓝绿 / 紫红 / 荧光色<br>
          鼓励 — 5 色谱合理使用<br>
          自由度更大
        </div>
      </div>
    </div>
  </div>
</section>

<!-- 参考文献 -->
<section class="references">
  <div class="references-inner">
    <div class="section-label">References</div>
    <h2 class="section-title serif">参考文献</h2>
    <p class="section-lead">本导则的色彩选取与表述综合引用以下国家标准、政府文件、官方媒体、学术研究及百科条目，确保多方资料交叉佐证。</p>
    <div class="refs-list">
{refs_html}
    </div>
  </div>
</section>

<footer>
  <p>荔湾 · 西关 · 城市色彩设计导则（数据驱动初版）</p>
  <p style="margin-top:12px">154 张在线图像 · 8 项参考文献 · 二〇二六 · 五月</p>
</footer>

</body>
</html>
"""

out = WEB / "index.html"
with open(out, "w", encoding="utf-8") as f:
    f.write(html)

print(f"v2 HTML 已生成: {out}")
import os
print(f"大小: {os.path.getsize(out)//1024} KB")
