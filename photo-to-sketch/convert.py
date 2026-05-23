#!/usr/bin/env python3
"""
照片转线稿工具
将真实照片转换为简约线稿风格
"""

import cv2
import numpy as np
from pathlib import Path
import sys

def photo_to_sketch(input_path, output_path, style='simple'):
    """
    将照片转换为线稿
    
    Args:
        input_path: 输入图片路径
        output_path: 输出图片路径
        style: 'simple' - 简单线稿, 'detailed' - 细节线稿
    """
    # 读取图片
    img = cv2.imread(str(input_path))
    if img is None:
        print(f"❌ 无法读取图片: {input_path}")
        return False
    
    # 转灰度
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    if style == 'simple':
        # 简单线稿风格 (类似第一张图的效果)
        # 1. 高斯模糊减少噪点
        blur = cv2.GaussianBlur(gray, (5, 5), 0)
        
        # 2. Canny边缘检测
        edges = cv2.Canny(blur, 30, 100)
        
        # 3. 反色（白底黑线）
        sketch = cv2.bitwise_not(edges)
        
    else:  # detailed
        # 细节线稿风格
        # 1. 双边滤波保留边缘
        bilateral = cv2.bilateralFilter(gray, 9, 75, 75)
        
        # 2. 中值滤波
        median = cv2.medianBlur(bilateral, 5)
        
        # 3. 边缘检测
        edges = cv2.adaptiveThreshold(
            median, 255, 
            cv2.ADAPTIVE_THRESH_MEAN_C, 
            cv2.THRESH_BINARY, 
            9, 2
        )
        
        sketch = edges
    
    # 保存结果
    cv2.imwrite(str(output_path), sketch)
    print(f"✅ 已转换: {input_path.name} -> {output_path.name}")
    return True


def batch_convert(input_dir, output_dir, style='simple'):
    """批量转换文件夹中的所有图片"""
    input_path = Path(input_dir)
    output_path = Path(output_dir)
    
    # 支持的图片格式
    image_extensions = {'.jpg', '.jpeg', '.png', '.bmp', '.webp'}
    
    # 查找所有图片
    images = [f for f in input_path.iterdir() 
              if f.suffix.lower() in image_extensions]
    
    if not images:
        print(f"❌ 在 {input_dir} 中未找到图片")
        return
    
    print(f"📁 找到 {len(images)} 张图片")
    print(f"🎨 线稿风格: {style}")
    print("=" * 50)
    
    success = 0
    for img_file in images:
        output_file = output_path / f"{img_file.stem}_sketch{img_file.suffix}"
        if photo_to_sketch(img_file, output_file, style):
            success += 1
    
    print("=" * 50)
    print(f"✨ 完成! 成功转换 {success}/{len(images)} 张图片")
    print(f"📂 输出位置: {output_path}")


if __name__ == "__main__":
    # 默认配置
    script_dir = Path(__file__).parent
    input_dir = script_dir / "input"
    output_dir = script_dir / "output"
    
    # 命令行参数
    style = 'simple'  # 或 'detailed'
    
    if len(sys.argv) > 1:
        if sys.argv[1] in ['simple', 'detailed']:
            style = sys.argv[1]
    
    print("=" * 50)
    print("📸 照片转线稿工具")
    print("=" * 50)
    
    # 检查输入目录
    if not input_dir.exists():
        print(f"❌ 输入目录不存在: {input_dir}")
        sys.exit(1)
    
    # 创建输出目录
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # 批量转换
    batch_convert(input_dir, output_dir, style)
