#!/usr/bin/env python3
"""为 4 个视频生成独立 HTML 报告 + 首页索引"""
import os, json, base64
from pathlib import Path

VIDEO_DIR = "/Users/cyh/Desktop/未命名文件夹 2"
WORK_DIR = f"{VIDEO_DIR}/.report_work"
OUT_DIR = f"{VIDEO_DIR}/视频拆分报告"
os.makedirs(OUT_DIR, exist_ok=True)

# 分类（哪些 shot 跳过重画）
classification = {}
cls_path = f"{WORK_DIR}/classification.json"
if os.path.exists(cls_path):
    with open(cls_path) as f:
        classification = json.load(f)

def get_shot_skip(alias, sid):
    """返回 (skip:bool, skip_type:str|None, reason:str|None)"""
    if alias not in classification:
        return (False, None, None)
    info = classification[alias].get(str(sid))
    if not info:
        return (False, None, None)
    t = info.get('type')
    if t in ('TEXT_ONLY', 'BG_ONLY'):
        return (True, t, info.get('reason', ''))
    return (False, None, None)


VIDEO_DIR = "/Users/cyh/Desktop/未命名文件夹 2"
WORK_DIR = f"{VIDEO_DIR}/.report_work"
OUT_DIR = f"{VIDEO_DIR}/视频拆分报告"
os.makedirs(OUT_DIR, exist_ok=True)

with open('/tmp/v4_style.css') as f:
    BASE_CSS = f.read()

EXTRA_CSS = """
.video-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(320px,1fr));gap:24px;margin-top:24px}
.video-card{background:#fff;border:0.5px solid rgba(0,0,0,.1);border-radius:14px;overflow:hidden;text-decoration:none;color:inherit;transition:transform .2s,box-shadow .2s;display:block}
.video-card:hover{transform:translateY(-2px);box-shadow:0 8px 24px rgba(0,0,0,.06)}
.video-cover{width:100%;aspect-ratio:16/9;background:#F1EFE8;object-fit:cover;display:block}
.video-info{padding:18px 20px}
.video-name{font-size:16px;font-weight:500;margin-bottom:6px;letter-spacing:-.01em}
.video-meta{font-size:12px;color:#7a7a78;display:flex;gap:14px}
.video-meta b{font-weight:500;color:#3A3A36;font-feature-settings:"tnum"}
.video-extras{margin-top:10px;font-size:11.5px;color:#7a7a78}
.video-extras .tag{display:inline-block;background:#F1EFE8;color:#3A3A36;padding:2px 8px;border-radius:8px;margin-right:4px;font-size:10.5px}
.lightbox{display:none;position:fixed;inset:0;background:rgba(0,0,0,.85);z-index:1000;align-items:center;justify-content:center;padding:40px}
.lightbox:target{display:flex}
.lightbox img{max-width:90vw;max-height:80vh;border-radius:8px}
.lightbox .close{position:absolute;inset:0;text-decoration:none}
.lightbox .label{position:absolute;bottom:20px;left:0;right:0;text-align:center;color:#fff;font-size:13px}
.metric-bar{display:flex;gap:24px;margin:16px 0;padding:14px 20px;background:#fff;border-radius:10px;border:0.5px solid rgba(0,0,0,.08);flex-wrap:wrap}
.metric{font-size:11.5px;color:#7a7a78}
.metric b{display:block;font-size:14px;color:#1F1E1B;font-weight:500;margin-bottom:2px}
.placeholder{color:#a0a09c;font-size:11.5px;font-style:italic;text-align:center;padding:8px}
.back-link{color:#185FA5;text-decoration:none;font-size:13px;margin-bottom:20px;display:inline-block}
"""

def img_to_b64(path):
    with open(path, 'rb') as f:
        ext = Path(path).suffix[1:]
        if ext == 'jpg': ext = 'jpeg'
        return f"data:image/{ext};base64,{base64.b64encode(f.read()).decode()}"

with open(f"{WORK_DIR}/videos.json") as f:
    videos = json.load(f)

analyses = {}
for alias in videos:
    apath = f"{WORK_DIR}/{alias}_analysis.json"
    if os.path.exists(apath):
        with open(apath) as f:
            analyses[alias] = {a['shot']: a for a in json.load(f)}

# === 各视频独立报告 ===
for alias, meta in videos.items():
    shots = meta['shots']
    a = analyses.get(alias, {})
    # 优先用 GPT-Image 版本，没有则回退 DoG
    gpt_dir = f"{WORK_DIR}/{alias}_lines_gpt"
    dog_dir = f"{WORK_DIR}/{alias}_lines"
    if os.path.exists(gpt_dir):
        line_dir = gpt_dir
        line_engine = 'GPT-Image-1.5'
        has_line = True
    elif os.path.exists(dog_dir):
        line_dir = dog_dir
        line_engine = 'OpenCV DoG'
        has_line = True
    else:
        line_dir = None
        line_engine = None
        has_line = False
    
    rows = []
    lightboxes = []
    for s in shots:
        sid = s['shot_id']
        ana = a.get(sid, {})
        thumb_b64 = img_to_b64(s['frame_path'])
        
        # 检查是否应该跳过重画
        skip, skip_type, skip_reason = get_shot_skip(alias, sid)
        
        if skip:
            type_label = '仅文字' if skip_type == 'TEXT_ONLY' else '仅背景'
            line_cell = f'<div class="placeholder">— 略过重画 —<br/><span style="font-size:10px">({type_label})</span><br/><span style="font-size:10px;color:#c0c0bc">{skip_reason}</span></div>'
        elif has_line:
            line_path = f"{line_dir}/shot_{sid}.png"
            if os.path.exists(line_path):
                line_b64 = img_to_b64(line_path)
                line_cell = f'<a href="#lb-{alias}-{sid}-line"><img src="{line_b64}" alt="line {sid}"/></a>'
                lightboxes.append(f'<div id="lb-{alias}-{sid}-line" class="lightbox"><a class="close" href="#"></a><img src="{line_b64}"/><div class="label">构图 {sid} · 点击关闭</div></div>')
            else:
                line_cell = '<div class="placeholder">—</div>'
        else:
            line_cell = '<div class="placeholder">未生成<br/>(节省成本)</div>'
        
        lightboxes.append(f'<div id="lb-{alias}-{sid}" class="lightbox"><a class="close" href="#"></a><img src="{thumb_b64}"/><div class="label">画面 {sid} · 点击关闭</div></div>')
        
        rows.append(f'''
        <tr>
          <td class="num"><span class="dot" style="background:#185FA5"></span>{sid}</td>
          <td class="thumb"><a href="#lb-{alias}-{sid}"><img src="{thumb_b64}" alt="shot {sid}"/></a></td>
          <td class="thumb">{line_cell}</td>
          <td>
            <div class="content">{ana.get('content', '—')}</div>
            <div class="subj">{ana.get('subject', '')}</div>
          </td>
          <td class="dur"><span class="dur-num">{s['duration_s']:.1f}</span><span class="dur-unit">s</span><br/><span style="font-size:10px;color:#a0a09c">{s['start_s']:.1f}s 起</span></td>
          <td class="lang">{ana.get('lens_action', '—')}</td>
          <td class="analysis">{ana.get('analysis', '—')}</td>
          <td class="analysis">{ana.get('replicate_tips', '—')}</td>
        </tr>''')
    
    if has_line:
        line_status = f"✅ 已生成 ({line_engine})"
    else:
        line_status = "未生成"
    
    html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8"/>
<meta name="viewport" content="width=device-width,initial-scale=1"/>
<title>{alias} · 视频分镜分析</title>
<style>{BASE_CSS}{EXTRA_CSS}</style>
</head>
<body>
<div class="wrap">
  <header>
    <div class="kicker">VIDEO ANALYSIS<span class="pill-mode">{alias}</span></div>
    <h1>{alias} 分镜复刻分析</h1>
    <div class="sub">原视频文件: {meta["filename"]}</div>
    <div class="stats">
      <div class="stat"><b>{len(shots)}</b>个分镜</div>
      <div class="stat"><b>{meta["duration_s"]:.1f}s</b>视频时长</div>
      <div class="stat"><b>{line_status}</b>构图线描</div>
    </div>
  </header>
  <a href="index.html" class="back-link">← 返回首页</a>
  <table>
    <thead>
      <tr>
        <th>#</th>
        <th>画面</th>
        <th>构图</th>
        <th>镜头内容</th>
        <th>时长</th>
        <th>镜头语言/动作</th>
        <th>综合分析</th>
        <th>复刻要点</th>
      </tr>
    </thead>
    <tbody>{"".join(rows)}</tbody>
  </table>
</div>
{"".join(lightboxes)}
</body>
</html>'''
    
    out_path = f"{OUT_DIR}/{alias}.html"
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f"✅ {alias}.html ({os.path.getsize(out_path)/1024:.1f} KB)")

# === 首页 ===
cards = []
for alias, meta in videos.items():
    shots = meta['shots']
    cover_b64 = img_to_b64(shots[0]['frame_path'])
    has_gpt = os.path.exists(f"{WORK_DIR}/{alias}_lines_gpt")
    has_dog = os.path.exists(f"{WORK_DIR}/{alias}_lines")
    if has_gpt:
        line_tag = '<span class="tag" style="background:#1F1E1B;color:#fff">含 GPT 线描</span>'
    elif has_dog:
        line_tag = '<span class="tag" style="background:#FFF3E0;color:#854F0B">含 DoG 线描</span>'
    else:
        line_tag = ''
    cards.append(f'''
    <a href="{alias}.html" class="video-card">
      <img class="video-cover" src="{cover_b64}" alt="{alias}"/>
      <div class="video-info">
        <div class="video-name">{alias}</div>
        <div class="video-meta">
          <span><b>{meta["duration_s"]:.1f}s</b> 时长</span>
          <span><b>{len(shots)}</b> 分镜</span>
        </div>
        <div class="video-extras">
          <span class="tag">{meta["filename"][:28]}...</span>
          {line_tag}
        </div>
      </div>
    </a>''')

timing_path = f"{WORK_DIR}/timing_test/timing_report.json"
gpt_timing_path = f"{WORK_DIR}/video_01_gpt_timing.json"
timing_html = ""
if os.path.exists(timing_path):
    with open(timing_path) as f:
        t = json.load(f)
    
    # GPT 版数据
    gpt_block = ""
    if os.path.exists(gpt_timing_path):
        with open(gpt_timing_path) as f:
            g = json.load(f)
        gpt_block = f'''
    <h3 style="margin-top:24px">🎨 GPT-Image-1.5 重画对比</h3>
    <div class="metric-bar">
      <div class="metric"><b>{g["total_duration_s"]}s</b>4 张总耗时</div>
      <div class="metric"><b>~{g["total_duration_s"]//4}s</b>单张平均</div>
      <div class="metric"><b>{g["total_tokens"]}</b>总 token</div>
      <div class="metric"><b>~${g["total_cost_usd_estimate"]}</b>实测成本</div>
      <div class="metric"><b>~¥{g["total_cost_cny_estimate"]}</b>折合人民币</div>
    </div>
    '''
    
    timing_html = f'''
    <h2>⏱️ video_01 处理性能基准</h2>
    <p style="color:#7a7a78;font-size:13px;margin-bottom:8px">9.17 秒视频 → 4 个分镜的完整流水线实测</p>
    
    <h3 style="margin-top:16px">📐 默认流水线（本地 DoG，已退役）</h3>
    <div class="metric-bar">
      <div class="metric"><b>{t.get("1_metadata", 0)}s</b>元信息读取</div>
      <div class="metric"><b>{t.get("2_scene_detect", 0)}s</b>镜头切换检测</div>
      <div class="metric"><b>{t.get("3_extract_frames", 0)}s</b>抽帧</div>
      <div class="metric"><b>{t.get("4_linedraw_dog", 0)}s</b>DoG 线描</div>
      <div class="metric"><b>~{t.get("5_vision_analysis", 0)}s</b>Vision 分析</div>
      <div class="metric"><b>¥0</b>总成本</div>
    </div>
    {gpt_block}
    <p style="color:#7a7a78;font-size:12px;line-height:1.6;margin-top:14px">
      ✓ 镜头检测/抽帧/Vision 分析全部本地或内网，无 API 成本<br/>
      ✓ 当前 video_01 表格使用 <b>GPT-Image-1.5</b> 重画版本（更优雅但需要外部 API）<br/>
      ✓ DoG 备选方案在 <code>.report_work/video_01_lines/</code> 备份保留
    </p>
    '''

total_shots = sum(len(v['shots']) for v in videos.values())
total_dur = sum(v['duration_s'] for v in videos.values())

home_html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8"/>
<meta name="viewport" content="width=device-width,initial-scale=1"/>
<title>视频拆分分析报告</title>
<style>{BASE_CSS}{EXTRA_CSS}</style>
</head>
<body>
<div class="wrap">
  <header>
    <div class="kicker">VIDEO ANALYSIS REPORT<span class="pill-mode">首页</span></div>
    <h1>视频拆分与分镜复刻分析</h1>
    <div class="sub">本报告对文件夹中 {len(videos)} 个视频进行自动镜头切换检测、分镜抽帧和文字分析。点击下方任一卡片查看详情。</div>
    <div class="stats">
      <div class="stat"><b>{len(videos)}</b>个视频</div>
      <div class="stat"><b>{total_dur:.1f}s</b>总时长</div>
      <div class="stat"><b>{total_shots}</b>个分镜</div>
      <div class="stat"><b>video_01</b>含线描</div>
    </div>
  </header>
  
  <h2>📁 视频列表</h2>
  <div class="video-grid">{"".join(cards)}</div>
  
  {timing_html}
</div>
</body>
</html>'''

with open(f"{OUT_DIR}/index.html", 'w', encoding='utf-8') as f:
    f.write(home_html)
print(f"✅ index.html ({os.path.getsize(f'{OUT_DIR}/index.html')/1024:.1f} KB)")

print(f"\n📂 全部文件: {OUT_DIR}/")
for fn in sorted(os.listdir(OUT_DIR)):
    p = f"{OUT_DIR}/{fn}"
    print(f"  {fn}: {os.path.getsize(p)/1024:.1f} KB")
