# 分镜草图生成提示词

## 核心要求
将真实照片转换为电影分镜/漫画分镜风格的线稿草图

## 详细描述

**主体处理：**
- 清晰勾勒人物的轮廓线条
- 保留关键姿态和动态特征
- 简化细节但保持可识别性
- 人物用实线描绘

**背景处理：**
- 将所有建筑/环境元素转换为透视引导线
- 创建明确的消失点（vanishing point）
- 用简化的几何线条表现空间深度
- 背景线条引导视线到画面纵深处

**整体风格：**
- 黑白线稿，白色背景
- 极简主义，只保留结构性线条
- 类似电影分镜草图（storyboard sketch）
- 强调构图和空间关系，而非细节

**参考风格关键词：**
- Storyboard sketch
- Architectural line drawing
- Perspective guide lines
- Minimalist manga panel
- Film composition draft

---

## ChatGPT / DALL-E 提示词（英文）

```
Convert this photo into a minimalist storyboard sketch style:

SUBJECT (person):
- Clear, bold outline of the figure
- Capture the pose and gesture dynamics
- Simplified but recognizable features
- Solid contour lines

BACKGROUND (environment):
- Transform all architecture into perspective guide lines
- Create strong vanishing point convergence
- Use geometric lines to show spatial depth
- Minimal details, focus on spatial structure

STYLE:
- Black lines on white background
- Film storyboard / manga panel aesthetic
- Extremely simplified, structural only
- Emphasize composition and spatial relationships
```

---

## ChatGPT / DALL-E 提示词（中文）

```
将这张照片转换为极简的分镜草图风格：

人物主体：
- 清晰的轮廓线条
- 捕捉姿态和动态
- 简化但可识别
- 实线勾勒

背景环境：
- 所有建筑转换为透视引导线
- 创建明确的消失点
- 用几何线条表现空间深度
- 极简，只保留结构

整体风格：
- 白底黑线线稿
- 电影分镜/漫画分镜美学
- 极度简化，只保留结构性信息
- 强调构图和空间关系
```

---

## Midjourney 提示词

```
[upload photo] 

convert to minimalist storyboard sketch, black line art on white background, clear subject outline, background as perspective guide lines with vanishing point, film composition draft style, architectural line drawing aesthetic --style raw --stylize 50
```

---

## Stable Diffusion ControlNet 方案

**模型：**
- ControlNet Lineart
- 或 ControlNet Scribble

**提示词：**
```
masterpiece, storyboard sketch, architectural line drawing, minimalist black line art, white background, subject clear outline, perspective guide lines, vanishing point composition, film storyboard aesthetic, clean geometric lines
```

**负面提示词：**
```
detailed, shading, texture, complex, realistic, photo, color
```

**参数：**
- ControlNet 权重: 0.8-1.0
- CFG Scale: 7-9
- Steps: 25-35
