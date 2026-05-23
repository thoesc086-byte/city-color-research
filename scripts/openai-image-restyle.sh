#!/usr/bin/env bash
# OpenAI GPT-Image 图像重绘脚本
# 用法:
#   1. 单图编辑（按提示词改风格）：
#      ./openai-image-restyle.sh "改成赛博朋克风格" 原图.png
#   2. 多图参考重绘（把第一张图按其他参考图的风格重绘）：
#      ./openai-image-restyle.sh "保持人物不变，应用参考图的风格" 原图.png 参考图.png
#
# 模型选择: gpt-image-2 (最强) / gpt-image-1.5 / gpt-image-1-mini (便宜)

set -euo pipefail

# ==================== 配置 ====================
# 通过环境变量传入，不写入文件
OPENAI_API_KEY="${OPENAI_API_KEY:-}"
API_URL="https://api.openai.com/v1/images/edits"
OUTPUT_DIR="$(cd "$(dirname "$0")/.." && pwd)/output/images"
MODEL="${OPENAI_IMAGE_MODEL:-gpt-image-2}"
SIZE="${OPENAI_IMAGE_SIZE:-1024x1024}"
QUALITY="${OPENAI_IMAGE_QUALITY:-high}"

# ==================== 参数 ====================
PROMPT="${1:-}"
shift || true
IMAGES=("$@")

# ==================== 校验 ====================
if [[ -z "$PROMPT" ]] || [[ ${#IMAGES[@]} -eq 0 ]]; then
    cat <<EOF
❌ 用法错误

用法:
  $0 "提示词" 原图.png [参考图.png ...]

环境变量:
  OPENAI_API_KEY        必填，你的 OpenAI key
  OPENAI_IMAGE_MODEL    可选，默认 gpt-image-2
  OPENAI_IMAGE_SIZE     可选，默认 1024x1024
  OPENAI_IMAGE_QUALITY  可选，默认 high (low/medium/high)

示例:
  # 单图改风格
  $0 "改成水彩画风格" /Users/me/photo.png

  # 多图参考（第一张是要改的，后面是风格参考）
  $0 "把人物画成参考图的风格" /Users/me/me.png /Users/me/anime_style.png

  # 用便宜模型
  OPENAI_IMAGE_MODEL=gpt-image-1-mini $0 "提示词" 图.png
EOF
    exit 1
fi

if [[ -z "$OPENAI_API_KEY" ]]; then
    cat <<EOF
❌ 未设置 OPENAI_API_KEY

设置方法（仅当前 shell 生效，不写入文件）:
  export OPENAI_API_KEY="sk-proj-xxx..."

然后再运行此脚本。
EOF
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
OUTPUT_FILE="$OUTPUT_DIR/restyle_${MODEL}_${TIMESTAMP}.png"

echo "🎨 正在用 OpenAI 重绘图片..."
echo "   模型: $MODEL"
echo "   质量: $QUALITY"
echo "   尺寸: $SIZE"
echo "   提示词: $PROMPT"
echo "   输入图片数: ${#IMAGES[@]}"
for i in "${!IMAGES[@]}"; do
    echo "   图片[$i]: ${IMAGES[$i]}"
done
echo ""

# 构建 curl 参数
CURL_ARGS=(
    -sS -X POST "$API_URL"
    --max-time 180
    -H "Authorization: Bearer $OPENAI_API_KEY"
    -F "model=$MODEL"
    -F "prompt=$PROMPT"
    -F "size=$SIZE"
    -F "quality=$QUALITY"
    -F "n=1"
)

# 添加图片（image[] 形式支持多图）
for img in "${IMAGES[@]}"; do
    CURL_ARGS+=(-F "image[]=@$img")
done

echo "⏳ 调用中（可能需要 30-90 秒）..."
RESPONSE=$(curl "${CURL_ARGS[@]}")

# 检查错误
if echo "$RESPONSE" | jq -e '.error' > /dev/null 2>&1; then
    echo "❌ API 调用失败:"
    echo "$RESPONSE" | jq '.error'
    exit 1
fi

# 提取并保存图片
if echo "$RESPONSE" | jq -e '.data[0].b64_json' > /dev/null 2>&1; then
    echo "$RESPONSE" | jq -r '.data[0].b64_json' | base64 --decode > "$OUTPUT_FILE"

    if [[ -s "$OUTPUT_FILE" ]]; then
        echo ""
        echo "✅ 重绘完成！"
        echo "📂 保存路径: $OUTPUT_FILE"
        echo "📐 文件大小: $(ls -lh "$OUTPUT_FILE" | awk '{print $5}')"

        # 显示用量信息
        if echo "$RESPONSE" | jq -e '.usage' > /dev/null 2>&1; then
            echo ""
            echo "💰 Token 用量:"
            echo "$RESPONSE" | jq '.usage'
        fi

        # macOS 自动打开
        if [[ "$(uname)" == "Darwin" ]]; then
            open "$OUTPUT_FILE" 2>/dev/null || true
        fi
    else
        echo "❌ 文件保存失败"
        exit 1
    fi
else
    echo "❌ 响应格式异常:"
    echo "$RESPONSE" | jq '.' | head -50
    exit 1
fi
