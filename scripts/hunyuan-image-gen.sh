#!/usr/bin/env bash
# 腾讯混元 (Hunyuan) 文生图脚本 - 内网免费版
# 用法: ./hunyuan-image-gen.sh "提示词" [模型] [尺寸]
# 示例: ./hunyuan-image-gen.sh "一只在秋天森林中的红色狐狸"

set -euo pipefail

# ==================== 配置 ====================
# 混元 API Key - 从 https://hunyuan.woa.com/portal/userApi/applyList 申请
HUNYUAN_API_KEY="${HUNYUAN_API_KEY:-}"
API_URL="https://hunyuanapi.woa.com/openapi/v1/images/generations"
OUTPUT_DIR="$(cd "$(dirname "$0")/.." && pwd)/output/images"

# ==================== 参数 ====================
PROMPT="${1:-}"
MODEL="${2:-hunyuan-image}"   # 详见: https://iwiki.woa.com/p/4010715535
SIZE="${3:-1024x1024}"         # 1024x1024 / 1024x768 / 768x1024 / 1280x768 / 768x1280 / 1408x640

# ==================== 校验 ====================
if [[ -z "$PROMPT" ]]; then
    cat <<EOF
❌ 错误：请提供提示词

用法: $0 "提示词" [模型] [尺寸]

🤖 推荐模型:
  hunyuan-image           智能分发 (默认，推荐)
  hunyuan-image-general   通用场景
  hunyuan-image-portrait  人像
  hunyuan-image-game      游戏动漫
  hunyuan-image-text      文字海报
  hunyuan-image-fiction-ams 小说插画

📐 支持尺寸:
  1024x1024  方形 (默认)
  1024x768   横版 4:3
  768x1024   竖版 3:4
  1280x768   横版 16:9
  768x1280   竖版 9:16
  1408x640   电影宽屏 2.35:1

📚 完整模型列表:
  https://iwiki.woa.com/p/4010715535

💡 调用示例:
  $0 "一只可爱的小狐狸"
  $0 "未来城市夜景" hunyuan-image 1280x768
  $0 "古风美女" hunyuan-image-portrait 768x1280
EOF
    exit 1
fi

if [[ -z "$HUNYUAN_API_KEY" ]]; then
    cat <<EOF
❌ 错误：未设置 HUNYUAN_API_KEY 环境变量

🔑 获取 API Key（免费，2025 年底前不计费）:
  1. 访问: https://hunyuan.woa.com/portal/userApi/applyList
  2. 点击"API 接入" → 勾选"混元生图" → 申请
  3. 获取 token 后设置环境变量:
     export HUNYUAN_API_KEY="你的token"

  完整流程: https://iwiki.woa.com/p/4010848985
EOF
    exit 1
fi

# ==================== 执行 ====================
mkdir -p "$OUTPUT_DIR"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
OUTPUT_FILE="$OUTPUT_DIR/${MODEL}_${TIMESTAMP}.png"

echo "🎨 正在生成图片..."
echo "   模型: $MODEL"
echo "   尺寸: $SIZE"
echo "   提示词: $PROMPT"
echo ""

# 构建请求 body
REQUEST_BODY=$(jq -n \
    --arg model "$MODEL" \
    --arg prompt "$PROMPT" \
    --arg size "$SIZE" \
    '{model: $model, prompt: $prompt, size: $size}')

RESPONSE=$(curl -sS -X POST "$API_URL" \
    -H "Content-Type: application/json" \
    -H "Authorization: Bearer $HUNYUAN_API_KEY" \
    --max-time 60 \
    -d "$REQUEST_BODY")

# 检查错误
if echo "$RESPONSE" | jq -e '.error // .Error' > /dev/null 2>&1; then
    echo "❌ 调用失败:"
    echo "$RESPONSE" | jq '.'
    exit 1
fi

# 提取图片 URL
IMAGE_URL=$(echo "$RESPONSE" | jq -r '.data[0].url // empty')

if [[ -z "$IMAGE_URL" ]]; then
    echo "❌ 响应格式异常:"
    echo "$RESPONSE" | jq '.'
    exit 1
fi

echo "📥 下载图片中..."
curl -sS -o "$OUTPUT_FILE" "$IMAGE_URL"

if [[ -f "$OUTPUT_FILE" ]] && [[ -s "$OUTPUT_FILE" ]]; then
    echo ""
    echo "✅ 图片生成成功!"
    echo "📂 保存路径: $OUTPUT_FILE"
    echo "🌐 在线链接: $IMAGE_URL (有效期 24 小时)"
    echo ""
    # 自动用系统默认应用打开（macOS）
    if [[ "$(uname)" == "Darwin" ]]; then
        open "$OUTPUT_FILE" 2>/dev/null || true
    fi
else
    echo "❌ 下载失败"
    exit 1
fi
