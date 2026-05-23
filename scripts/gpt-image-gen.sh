#!/usr/bin/env bash
# GPT Image 文生图脚本
# 用法: ./gpt-image-gen.sh "提示词" [模型] [尺寸] [质量]
# 示例: ./gpt-image-gen.sh "一只可爱的小狗" gpt-image-2 1024x1024 high

set -euo pipefail

# ==================== 配置 ====================
# Venus Token - 从 https://venus.woa.com/#/openapi/accountManage/personalAccount 获取
VENUS_TOKEN="${VENUS_TOKEN:-}"
API_URL="http://v2.open.venus.oa.com/chatproxy/images/generations"
OUTPUT_DIR="$(cd "$(dirname "$0")/.." && pwd)/output/images"

# ==================== 参数 ====================
PROMPT="${1:-}"
MODEL="${2:-gpt-image-2}"   # gpt-image-1 / gpt-image-1.5 / gpt-image-2
SIZE="${3:-1024x1024}"      # 1024x1024 / 1536x1024 / 1024x1536
QUALITY="${4:-medium}"       # low / medium / high

# ==================== 校验 ====================
if [[ -z "$PROMPT" ]]; then
    echo "❌ 错误：请提供提示词"
    echo "用法: $0 \"提示词\" [模型] [尺寸] [质量]"
    echo ""
    echo "支持的模型: gpt-image-1, gpt-image-1.5, gpt-image-2"
    echo "支持的尺寸: 1024x1024, 1536x1024, 1024x1536"
    echo "支持的质量: low, medium, high"
    exit 1
fi

if [[ -z "$VENUS_TOKEN" ]]; then
    echo "❌ 错误：未设置 VENUS_TOKEN 环境变量"
    echo ""
    echo "请先获取 Token："
    echo "  https://venus.woa.com/#/openapi/accountManage/personalAccount"
    echo ""
    echo "然后设置环境变量："
    echo "  export VENUS_TOKEN=\"你的token\""
    exit 1
fi

# ==================== 执行 ====================
mkdir -p "$OUTPUT_DIR"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
OUTPUT_FILE="$OUTPUT_DIR/${MODEL}_${TIMESTAMP}.png"

echo "🎨 正在生成图片..."
echo "   模型: $MODEL"
echo "   尺寸: $SIZE"
echo "   质量: $QUALITY"
echo "   提示词: $PROMPT"
echo ""

RESPONSE=$(curl -sS -X POST "$API_URL" \
    -H "Content-Type: application/json" \
    -H "Authorization: Bearer $VENUS_TOKEN" \
    -d "$(jq -n \
        --arg model "$MODEL" \
        --arg prompt "$PROMPT" \
        --arg size "$SIZE" \
        --arg quality "$QUALITY" \
        '{model: $model, prompt: $prompt, size: $size, quality: $quality, n: 1}')")

# 检查错误
if echo "$RESPONSE" | jq -e '.error' > /dev/null 2>&1; then
    echo "❌ 调用失败:"
    echo "$RESPONSE" | jq '.error'
    exit 1
fi

# 解码并保存
if echo "$RESPONSE" | jq -e '.data[0].b64_json' > /dev/null 2>&1; then
    echo "$RESPONSE" | jq -r '.data[0].b64_json' | base64 --decode > "$OUTPUT_FILE"
    echo "✅ 图片已保存: $OUTPUT_FILE"
    echo ""
    echo "📂 完整路径: $(realpath "$OUTPUT_FILE")"
else
    echo "❌ 响应格式异常:"
    echo "$RESPONSE" | jq '.'
    exit 1
fi
