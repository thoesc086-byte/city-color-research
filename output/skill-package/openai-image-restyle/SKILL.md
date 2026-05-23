---
name: openai-image-restyle
description: 使用 OpenAI GPT-Image API 进行图像风格迁移和重绘。核心原则是"只换风格，不动构图"——保持原图主体的位置、大小、比例、姿态完全不变，仅替换绘画风格。提供"极简线描签名风"等开箱即用的 prompt 模板。当用户需要"风格迁移"、"图像重绘"、"换风格"、"线描化"、"极简化"等场景时使用。需要用户提供 OpenAI API Key（通过 OPENAI_API_KEY 环境变量）。
metadata: { "openclaw": { "category": "image", "emoji": "🎨", "displayName": "OpenAI 图像重绘" } }
---

# OpenAI 图像风格迁移与重绘

通过 OpenAI 官方 GPT-Image API（`/v1/images/edits`）实现风格迁移。

## ⭐ 核心原则

### 1. 只换风格，不动构图

- ✅ 保持主体在画面中的**位置、大小占比、姿态、朝向、视角**与原图一致
- ❌ 不要让 AI 重新构图、放大主体、做特写裁切
- ❌ 不要主动在 prompt 中加入 `close-up`、`LARGE`、`60-70% of frame` 等改变构图的词
- 用户上传的原图就是**构图参考**；只有当用户明确要求才改变构图

### 2. 风格描述用 prompt，不用参考图（重要！）

⚠️ **不要传"风格参考图"作为第二张输入图**。OpenAI gpt-image API 会把参考图里的**内容**（比如里面有奔跑的人）当成需求，导致输出强行加入这些元素。

- ✅ 风格通过 **prompt 文字描述**实现（"minimalist line drawing", "watercolor style"等）
- ❌ 不要用 `bash restyle.sh "按图二风格" original.png style_ref.png` 这种用法
- 例外：仅当参考图风格非常独特、文字难以描述时才考虑，且要在 prompt 中明确"忽略参考图内容，只学风格"

### 3. 批量任务必须先单测

- 批量重绘前，**先跑 1 张让用户确认风格**
- 风格满意后再批量
- 否则可能批量产出几十张都有同样的诡异 bug（如奔跑人物幽灵）

## 使用方法

```bash
bash <skill_location>/scripts/restyle.sh "<提示词>" <原图> [更多原图...]
```

### 单图重绘

```bash
bash <location>/scripts/restyle.sh "极简线描风格" /path/to/photo.png
```

### 批量（推荐：循环单张调用）

```bash
for f in /path/to/originals/*.jpeg; do
  bash <location>/scripts/restyle.sh "$PROMPT" "$f"
done
```

OpenAI API 调用本身是无状态的，循环就够了，无需 spawn subagent。

## 前置条件

### API Key（必填）

```bash
export OPENAI_API_KEY="sk-proj-xxx..."
```

⚠️ **安全要求**：
- API Key 只通过环境变量传递，绝不写入文件、git 提交或日志
- 如果用户在对话中明文发送 key，立即提醒撤销重发
- 调用前检查 `OPENAI_API_KEY` 是否已设置

### 依赖

`curl`、`jq`、`base64`、`sips`（macOS 内置）

## 环境变量

| 变量 | 默认 | 说明 |
| - | - | - |
| `OPENAI_API_KEY` | 必填 | OpenAI API Key |
| `OPENAI_IMAGE_MODEL` | `gpt-image-1.5` | 默认 1.5（更稳定保持原构图）；2.0 倾向于重新构图 |
| `OPENAI_IMAGE_SIZE` | 自动 | 输出尺寸（见下方支持档位） |
| `OPENAI_IMAGE_QUALITY` | `high` | 质量（`low` / `medium` / `high`） |
| `KEEP_ORIGINAL_SIZE` | `1` | 是否缩放回原图尺寸 |
| `OUTPUT_DIR` | `~/.openclaw/workspace/output/images` | 输出目录 |

### 模型对比

| 模型 | 特点 | 估算费用/张 |
| - | - | - |
| `gpt-image-1.5` ⭐ | **默认推荐**：稳定保持原图构图 | ~$0.05-0.08 |
| `gpt-image-2` | 最新版，倾向重新构图（让主体变大），慎用 | ~$0.07-0.10 |
| `gpt-image-1` | 经典版本 | ~$0.04-0.06 |
| `gpt-image-1-mini` | 便宜，适合批量 | ~$0.02-0.03 |

### 支持的尺寸档位

OpenAI API 仅支持：`1024x1024` / `1024x1536`（竖 2:3）/ `1536x1024`（横 3:2）。脚本自动选最接近档位，再用 `sips` 缩放到原图精确尺寸。

## 提示词构造规则

### 通用必备：构图锁定语

```
Preserve the EXACT composition, position, size, scale, and pose of the
subject(s) from the input image. Match the framing, viewing angle, and
proportions exactly. Do NOT zoom in, do NOT crop, do NOT enlarge or
shrink the subject. Only change the artistic style.
```

### 通用必备：内容锁定语

```
Do NOT add any new subjects, people, animals, or objects that are not
in the input image. Do NOT add running figures, do NOT add humans if
there are none in the input.
```

> 这条是关键。即使不传风格参考图，gpt-image-1.5 偶尔也会"创造性发挥"加人物。明确禁止能大幅降低概率。

### 禁用词（不要在提示词里出现）

- ❌ `close-up`, `portrait composition`
- ❌ `LARGE`, `prominent`, `dominant`
- ❌ `fills X% of frame`, `occupies most of`
- ❌ `centered`（除非原图主体本来就居中）
- ❌ `zoom in`, `crop tight`

## 提示词模板（开箱即用）

### 模板 A：极简单线签名风 ⭐⭐⭐ 推荐默认

适用：人物、动物、物品。**保留主体核心识别度（极简五官/小细节暗示）**，但去除所有杂线（毛发、衣服褶皱、阴影等）。

效果像设计师 10 秒画出的 logo / 概念草图。

```
Convert this single input image into a minimalist black line drawing on
pure white background, in the style of a master's quick contour sketch.

ABSOLUTE rules:
- Preserve the EXACT composition, position, size, and proportions from
  the input image.
- Do NOT add any new subjects, people, or animals.
- Do NOT zoom, crop, enlarge, or shrink anything.
- Do NOT add running figures or humans if not present in the input.

Style — like an elegant minimal pictogram with light hints of features:
- Draw the main body outline using clean confident lines (one outline,
  no double lines).
- Add ONLY the most essential feature hints — for example: a tiny simple
  eye shape (just a small curve or oval, no pupil), a simple nose contour
  (just a small triangle or curve, no nostrils), but NO mouth details,
  NO teeth, NO eyelashes.
- For fur: only 2-3 sparse short curved lines hinting fur direction at
  the neck or body edge — NEVER dense fur texture, NEVER hairy outline,
  NEVER fluffy strokes.
- NO clothing folds, NO clothing wrinkles, NO clothing patterns.
- NO shading, NO hatching, NO fill, NO color.
- The result should look like a quick elegant contour sketch a designer
  would draw in 10 seconds — minimalist but with light personality
  through 1-2 feature hints.

Background:
- Pure white. NO horizon line, NO ground line, NO structure lines, NO
  frame.
- Whitespace dominates.

Output: extremely clean, sparse, elegant single-line contour drawing.
Like a logo or a master designer's signature sketch.
```

### 模板 B：纯轮廓 silhouette（更极致）

适用：希望比模板 A 更彻底干净，**完全无五官、无毛发**，只有外轮廓。

```
Convert this single input image into an EXTREMELY simplified silhouette
line drawing on pure white background.

ABSOLUTE rules:
- Preserve the EXACT composition, position, size, and proportions from
  the input image.
- Do NOT add any new subjects.
- Do NOT zoom, crop, enlarge, or shrink anything.

CRITICAL — ULTRA SIMPLIFIED style:
- Draw ONLY the outermost silhouette / contour of each subject. ONE
  clean continuous outline per subject.
- ABSOLUTELY NO interior details: NO clothing folds, NO clothing
  wrinkles, NO clothing patterns, NO fur texture, NO hair strands, NO
  facial features, NO eyes, NO nose, NO mouth details, NO shading lines,
  NO hatching.
- The subject should look like a flat solid shape outlined by a single
  clean line — like a paper cutout.
- Treat clothing and body as one unified silhouette — do NOT separate
  clothing from body with extra lines.

Background:
- Pure white. Add ONLY 1 very thin subtle horizon line if there's a
  clear horizon in the input.
- No corner lines, no vertical edges, no construction lines.

Output: clean uniform black outline silhouettes on pure white.
Whitespace dominates. Like a logo or pictogram.
```

### 模板 C：极简线描 + 轻微背景结构线

适用：希望保留一点点空间感（地平线、山脊轮廓等），但不要太多。

> 慎用：实测 AI 容易把"结构线"画成奇怪的角落硬线（像房间墙角），效果不稳定。优先用模板 A 或 B。

```
Convert this single input image into an extremely minimalist black line
drawing on pure white background.

ABSOLUTE rules:
- Preserve the EXACT composition, position, size, and proportions from
  the input image.
- Do NOT add any new subjects, people, or animals.
- Do NOT zoom, crop, enlarge, or shrink anything.
- Only change the artistic style — content stays identical to the input.

Subject style (priority — keep it elegant):
- Draw the main subject(s) with clean simple outline lines.
- No facial features, no fur texture, no shading, no fill, no color.
- Subject should look like a confident single-line contour drawing.

Background structure (very subtle, secondary):
- Add ONLY 1 to 2 soft thin lines that hint at the natural scene
  division — for example a horizon line, a mountain ridge silhouette
  curve, or a slight ground/sky boundary.
- DO NOT draw walls, room corners, vertical boundary lines, framing
  borders, helper lines, or any architectural construction marks.
- DO NOT add geometric shapes that aren't in the original.
- These structural hints must be barely visible, much thinner/lighter
  than the subject lines.
- Most of the canvas should remain pure white empty space.

Output: clean uniform black line drawing on pure white, conceptual
sketch style, white space dominates.
```

### 模板 D：水彩画风

```
Repaint this image in soft watercolor style. Preserve the EXACT
composition, position, size, and pose of the subject from the input
image. Match the framing exactly. Do NOT add any new subjects.

Gentle brush strokes, muted pastel palette, paper texture visible.
Wet-on-wet technique with subtle color bleeding. Dreamy atmospheric mood.
```

### 模板 E：日系胶片摄影

```
Restyle this image in Japanese film photography aesthetic. Preserve the
EXACT composition, position, size, and pose of the subject from the
input image. Match the framing exactly. Do NOT add any new subjects.

Warm vintage tones, slight grain texture, soft natural lighting, muted
color palette with warm browns and yellows. Nostalgic serene atmosphere.
```

## 工作流建议

### 单张重绘
1. 用户给原图 → 询问目标风格（除非明显）
2. 选模板 → 单次调用 → 给用户预览
3. 根据反馈调整 prompt 或换模板

### 批量重绘
1. **先跑 1 张试样**（重要！）
2. 用户确认风格 → 选定 prompt
3. 循环跑剩余的，每张耗时 30-60 秒
4. 全部完成后整理到独立目录（建议不要混在 `output/images/` 里）
5. 如果某张效果不好，单独重跑那一张

### 风格不满意时的迭代顺序
1. **杂线太多** → 换模板 B（silhouette）
2. **太空洞** → 换模板 A（保留五官暗示）
3. **结构线乱** → 移除模板 C 中的结构线段，改用 A 或 B
4. **加了不该有的人物** → 强化"内容锁定语"中的 `Do NOT add` 部分

## 重要经验教训

1. **不传风格参考图** —— 内容会被 AI 当成需求强加到输出
2. **批量前单测** —— 哪怕 prompt 写得再好，也先跑 1 张确认
3. **构图锁定语 + 内容锁定语都要有** —— 各自防不同问题
4. **不要试图"反向纠正"** —— 生成的主体偏小不要加 `LARGE`，会让 AI 失控；换模型或换措辞
5. **gpt-image-1.5 比 2.0 稳定** —— 2.0 更倾向于"创造性发挥"重新构图

## 输出

脚本会输出：
- 📂 文件路径（默认 `output/images/`）
- 📐 文件大小
- 💰 Token 用量
- 自动在 macOS 上 `open` 打开预览

## 失败排查

| 错误 | 解决 |
| - | - |
| `401 Unauthorized` | 检查 `OPENAI_API_KEY` |
| `429 Rate Limit` | 等待 1-2 分钟，或换便宜模型 |
| `400 size` | 检查 `OPENAI_IMAGE_SIZE` 是否在支持档位 |
| 图片下载失败 | 检查网络（需访问 OpenAI API） |
| 输出加了不该有的元素 | 在 prompt 中明确 `Do NOT add ...` |
| 输出主体太大/被裁切 | 换 `gpt-image-1.5`，加构图锁定语，去掉所有"放大"相关词 |
