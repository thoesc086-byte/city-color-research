
## 🗂️ 会话归档机制（2026-05-19 引入）

用户用 webchat，OpenClaw 默认单会话 UI（无 tab 切换）。
我们用文件归档来模拟"多会话"：
- 归档目录：`~/.openclaw/workspace/sessions_archive/`
- 索引文件：`sessions_archive/INDEX.md`（必读，列出所有别名+唤起关键词）
- 每个归档：`YYYY-MM-DD_<别名>.{jsonl,md}` 一对

**用户唤起方式**：直接说"回到XX窗口"或别名关键词
**当时立即应**：
1. 读 INDEX.md 找匹配的别名
2. 读对应 `.md` 摘要恢复上下文
3. 简短确认 + 等指令

已归档：
- `video-report-linedraw`（描线窗口） — 视频分镜线描化项目
