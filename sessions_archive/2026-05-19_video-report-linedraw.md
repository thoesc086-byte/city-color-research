# 📁 会话归档：视频报告线描图（描线窗口）

**归档日期**：2026-05-19 15:05 GMT+8
**会话别名**：`描线窗口` / `video-report-linedraw`
**Transcript**：`./2026-05-19_video-report-linedraw.jsonl`（1.6 MB，含完整对话历史）

---

## 🎯 主题

把 `/Users/cyh/WorkBuddy/20260518161442/video_report/index_v3.html` 中 15+ 张分镜画面，批量转成**极简黑白线描风格**（"大师签名速写"），生成新的 `index_v4.html` 视频报告，包含「构图」列。

---

## 📂 关键文件

### 报告 HTML
- **当前最终版**：`/Users/cyh/WorkBuddy/20260518161442/video_report/index_v4.html`（约 3.8 MB，16 行表格，全部点击放大）
- **原始保留**：`/Users/cyh/WorkBuddy/20260518161442/video_report/index_v3.html`（不要动）

### 线描图素材
- **原图**：`shots_linedraw/originals/shot_N.jpeg`（视频原画面截图）
- **线描成品**：`shots_linedraw_final/shot_N.png`（共 16 张：1, 2, 3, 4, 6, 7, 8, 10-17, 19）
  - shot_4 是合并行（5+9）的山脉云朵线描，由用户手动提供
  - shot_3 用 Template A v3（signature-sketch）
  - shot_19 用 Template B v2（silhouette）
  - 其余用原 v3 prompt
- **历史备份**：`shot_3_v1.png` / `shot_3_v2.png` / `shot_19_v1.png` / `shot_19_v2.png`

### Skill
- `~/.openclaw/skills/openai-image-restyle/SKILL.md`（12.3 KB，5 个模板：A/B/C/D/E）
- `~/.openclaw/skills/openai-image-restyle/scripts/restyle.sh`

---

## 🔑 重要决策与经验

1. **核心原则**：风格描述用 prompt，不传第二张参考图（否则 AI 会把参考图内容当主体）
2. **构图锁定关键词**：`"preserve EXACT composition"`、`"do NOT add"`
3. **禁用词**：`LARGE` / `close-up` / `X% of frame`（会让 AI 重构图）
4. **批量任务先单测**：1-3 张验证后才批量
5. **细节判断**：clean 输出 ≈ 16-24K；细节过多/jagged ≈ 30-50K
6. **默认模型**：`gpt-image-1.5`（gpt-image-2 会重构图）
7. **API key**：通过 `OPENAI_API_KEY` 环境变量传，不写文件
8. **GPT-Image 仅支持固定尺寸**：1024×1024 / 1024×1536 / 1536×1024，非标尺寸用 `sips` 后处理
9. **`image()` 工具限制**：路径必须在 `~/.openclaw/workspace/` 内

---

## 📐 表格结构（最终）

```
# | 画面 | 构图 | 镜头内容 | 时长 | 镜头语言/动作 | 综合分析 | 复刻要点
```

16 行连续编号 1-16；其中第 4 行是 "5+9 合并" 镜头：
- 画面列：合并缩略图，链接 `#lb-5_9`
- 构图列：山脉云朵线描（用户提供），链接 `#lb-4-line`

之前删除的：
- 顶部 `<div class="stat"><b>7</b>段落</div>`
- 「段落分布」区块（h3 + sec-bar 7 个色卡）
- 表头 `<th>段落</th>` + 16 个 `<td class="sec">`

---

## 🎨 Template A（生产默认 prompt）

```
minimalist black line drawing on pure white background,
in the style of a master's quick contour sketch.
Preserve EXACT composition, position, scale, posture, and proportions.
Outline + tiny eye/nose hint + 2-3 sparse fur strokes max.
Do NOT add interior folds, fur texture, or shading.
Pure white background.
```

---

## 🚧 未完成 / 阻塞项

- ❌ 企微 mobile 配对仍未完成（缺 corpId/agentId）
- ⚠️ 用户的 OpenAI key 前缀 `sk-proj-zVo2Pf...` 还在使用，建议尽快 revoke

---

## 🔄 切回此对话的方式

> 用户说："**回到描线窗口**" / "回到那个视频报告的对话" / "切回 video-report-linedraw"

我（助手）应该执行：
1. `read /Users/cyh/.openclaw/workspace/sessions_archive/2026-05-19_video-report-linedraw.md`（本文件）
2. 必要时 `read jsonl` 查找具体历史细节
3. 在新对话中明确告知用户："已加载描线窗口上下文" + 简要回顾上次进度
4. 等待用户的新指令
