#!/usr/bin/env bash
# OpenAI GPT-Image 图像重绘脚本（skill 版本）
#
# 功能：
#   - 单图风格化或多图参考重绘
#   - 自动选择最接近的官方尺寸档位
#   - 默认缩放回原图精确尺寸
#
# 用法：
#   bash restyle.sh "提示词" 原图.png [参考图.png ...]

set -euo pipefail

# ==================== 配置 ====================
OPENAI_API_KEY="${OPENAI_API_KEY:-}"
API_URL="https://api.openai.com/v1/images/edits"
MODEL="${OPENAI_IMAGE_MODEL:-gpt-image-1.5}"
QUALITY="${OPENAI_IMAGE_QUALITY:-high}"
KEEP_ORIGINAL_SIZE="${KEEP_ORIGINAL_SIZE:-1}"

# 默认输出到 OpenClaw 工作区
DEFAULT_OUTPUT_DIR="$HOME/.openclaw/workspace/output/images"
OUTPUT_DIR="${OUTPUT_DIR:-$DEFAULT_OUTPUT_DIR}"

# ==================== 参数 ====================
PROMPT="${1:-}"
shift || true
IMAGES=("$@")

# ==================== 校验 ====================
if [[ -z "$PROMPT" ]] || [[ ${#IMAGES[@]} -eq 0 ]]; then
    cat <<EOF
❌ 用法错误

用法:
  bash restyle.sh "提示词" 原图.png [参考图.png ...]

环境变量:
  OPENAI_API_KEY        必填，你的 OpenAI key
  OPENAI_IMAGE_MODEL    可选，默认 gpt-image-1.5（推荐，更稳定保持原图构图）
  OPENAI_IMAGE_SIZE     可选，自动选择（1024x1024 / 1024x1536 / 1536x1024）
  OPENAI_IMAGE_QUALITY  可选，默认 high
  KEEP_ORIGINAL_SIZE    可选，默认 1（缩放回原图尺寸）
  OUTPUT_DIR            可选，默认 ~/.openclaw/workspace/output/images
EOF
    exit 1
fi

if [[ -z "$OPENAI_API_KEY" ]]; then
    echo "❌ 未设置 OPENAI_API_KEY 环境变量"
    echo "   export OPENAI_API_KEY=\"sk-proj-xxx\""
    exit 1
fi

# 校验依赖
for cmd in curl jq base64; do
    if ! command -v "$cmd" >/dev/null 2>&1; then
        echo "❌ 缺少依赖: $cmd"
        exit 1
    fi
done

# 校验图片
for img in "${IMAGES[@]}"; do
    if [[ ! -f "$img" ]]; then
        echo "❌ 图片不存在: $img"
        exit 1
    fi
done

# ==================== 自动选择尺寸 ====================
ORIGINAL_W=""
ORIGINAL_H=""

if command -v sips >/dev/null 2>&1; then
    ORIGINAL_W=$(sips -g pixelWidth "${IMAGES[0]}" 2>/dev/null | awk '/pixelWidth/ {print $2}')
    ORIGINAL_H=$(sips -g pixelHeight "${IMAGES[0]}" 2>/dev/null | awk '/pixelHeight/ {print $2}')
fi

# 如果用户没指定 size，根据原图比例自动选档
if [[ -z "${OPENAI_IMAGE_SIZE:-}" ]]; then
    if [[ -n "$ORIGINAL_W" ]] && [[ -n "$ORIGINAL_H" ]]; then
        # 计算宽高比 *100 取整
        RATIO=$(awk -v w="$ORIGINAL_W" -v h="$ORIGINAL_H" 'BEGIN {printf "%d", (w/h)*100}')
        if [[ $RATIO -ge 130 ]]; then
            SIZE="1536x1024"   # 横版
        elif [[ $RATIO -le 76 ]]; then
            SIZE="1024x1536"   # 竖版
        else
            SIZE="1024x1024"   # 方形
        fi
    else
        SIZE="1024x1024"
    fi
else
    SIZE="$OPENAI_IMAGE_SIZE"
fi

# ==================== 执行 ====================
mkdir -p "$OUTPUT_DIR"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
RAW_OUTPUT="$OUTPUT_DIR/restyle_${MODEL}_${TIMESTAMP}.png"
FINAL_OUTPUT="$RAW_OUTPUT"

echo "🎨 OpenAI 图像重绘"
echo "   模型: $MODEL"
echo "   质量: $QUALITY"
echo "   API 尺寸: $SIZE"
if [[ -n "$ORIGINAL_W" ]] && [[ "$KEEP_ORIGINAL_SIZE" == "1" ]]; then
    echo "   原图尺寸: ${ORIGINAL_W}x${ORIGINAL_H} (将自动缩放)"
fi
echo "   输入图片数: ${#IMAGES[@]}"
for i in "${!IMAGES[@]}"; do
    echo "   图片[$i]: ${IMAGES[$i]}"
done
echo ""

# 构建 curl 参数
CURL_ARGS=(
    -sS -X POST "$API_URL"
    --max-time 240
    -H "Authorization: Bearer $OPENAI_API_KEY"
    -F "model=$MODEL"
    -F "prompt=$PROMPT"
    -F "size=$SIZE"
    -F "quality=$QUALITY"
    -F "n=1"
)

for img in "${IMAGES[@]}"; do
    CURL_ARGS+=(-F "image[]=@$img")
done

echo "⏳ 调用中（30-90 秒）..."
RESPONSE=$(curl "${CURL_ARGS[@]}")

# 检查错误
if echo "$RESPONSE" | jq -e '.error' >/dev/null 2>&1; then
    echo "❌ API 调用失败:"
    echo "$RESPONSE" | jq '.error'
    exit 1
fi

# 提取并保存图片
if ! echo "$RESPONSE" | jq -e '.data[0].b64_json' >/dev/null 2>&1; then
    echo "❌ 响应格式异常:"
    echo "$RESPONSE" | jq '.' | head -50
    exit 1
fi

echo "$RESPONSE" | jq -r '.data[0].b64_json' | base64 --decode > "$RAW_OUTPUT"

if [[ ! -s "$RAW_OUTPUT" ]]; then
    echo "❌ 文件保存失败"
    exit 1
fi

# 缩放回原图尺寸
if [[ "$KEEP_ORIGINAL_SIZE" == "1" ]] && [[ -n "$ORIGINAL_W" ]] && [[ -n "$ORIGINAL_H" ]] && command -v sips >/dev/null 2>&1; then
    FINAL_OUTPUT="$OUTPUT_DIR/restyle_${MODEL}_${TIMESTAMP}_${ORIGINAL_W}x${ORIGINAL_H}.png"
    cp "$RAW_OUTPUT" "$FINAL_OUTPUT"
    sips --resampleHeightWidth "$ORIGINAL_H" "$ORIGINAL_W" "$FINAL_OUTPUT" >/dev/null 2>&1
fi

# ==================== 输出 ====================
echo ""
echo "✅ 重绘完成！"
echo "📂 文件: $FINAL_OUTPUT"
echo "📐 大小: $(ls -lh "$FINAL_OUTPUT" | awk '{print $5}')"

if [[ "$FINAL_OUTPUT" != "$RAW_OUTPUT" ]]; then
    echo "📦 原始: $RAW_OUTPUT"
fi

if echo "$RESPONSE" | jq -e '.usage' >/dev/null 2>&1; then
    TOTAL=$(echo "$RESPONSE" | jq -r '.usage.total_tokens')
    echo "💰 Token: $TOTAL"
fi

# macOS 自动打开
if [[ "$(uname)" == "Darwin" ]]; then
    open "$FINAL_OUTPUT" 2>/dev/null || true
fi
