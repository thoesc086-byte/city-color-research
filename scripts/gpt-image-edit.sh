#!/usr/bin/env bash
# GPT Image 图片编辑脚本
# 用法: ./gpt-image-edit.sh "编辑提示词" 图片1.png [图片2.png ...]
# 示例: ./gpt-image-edit.sh "改成黑白色" /path/to/photo.png

set -euo pipefail

# ==================== 配置 ====================
VENUS_TOKEN="${VENUS_TOKEN:-}"
API_URL="http://v2.open.venus.oa.com/chatproxy/images/edits"
OUTPUT_DIR="$(cd "$(dirname "$0")/.." && pwd)/output/images"
MODEL="${MODEL:-gpt-image-2}"
SIZE="${SIZE:-1024x1024}"

# ==================== 参数 ====================
PROMPT="${1:-}"
shift || true
IMAGES=("$@")

# ==================== 校验 ====================
if [[ -z "$PROMPT" ]] || [[ ${#IMAGES[@]} -eq 0 ]]; then
    echo "❌ 错误：用法不正确"
    echo "用法: $0 \"编辑提示词\" 图片1.png [图片2.png ...]"
    echo "环境变量: MODEL=gpt-image-2 SIZE=1024x1024"
    exit 1
fi

if [[ -z "$VENUS_TOKEN" ]]; then
    echo "❌ 错误：未设置 VENUS_TOKEN 环境变量"
    echo "请先：export VENUS_TOKEN=\"你的token\""
    exit 1
fi

# 校验图片文件
for img in "${IMAGES[@]}"; do
    if [[ ! -f "$img" ]]; then
        echo "❌ 图片不存在: $img"
        exit 1
    fi
done

# ==================== 执行 ====================
mkdir -p "$OUTPUT_DIR"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
OUTPUT_FILE="$OUTPUT_DIR/edit_${MODEL}_${TIMESTAMP}.png"

echo "🎨 正在编辑图片..."
echo "   模型: $MODEL"
echo "   提示词: $PROMPT"
echo "   输入图片: ${IMAGES[*]}"
echo ""

# 构建 curl 参数
CURL_ARGS=(
    -sS -X POST "$API_URL"
    -H "Authorization: Bearer $VENUS_TOKEN"
    -F "model=$MODEL"
    -F "prompt=$PROMPT"
    -F "size=$SIZE"
    -F "n=1"
)

for img in "${IMAGES[@]}"; do
    CURL_ARGS+=(-F "image[]=@$img")
done

RESPONSE=$(curl "${CURL_ARGS[@]}")

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
    echo "📂 完整路径: $(realpath "$OUTPUT_FILE")"
else
    echo "❌ 响应格式异常:"
    echo "$RESPONSE" | jq '.'
    exit 1
fi
