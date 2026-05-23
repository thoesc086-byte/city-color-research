# 📸 照片转线稿工具

自动将真实照片转换为简约线稿风格（类似分镜草图效果）

## 📁 目录结构

```
photo-to-sketch/
├── input/          # 放入要转换的照片
├── output/         # 转换后的线稿输出
├── convert.py      # 转换脚本
└── README.md       # 本文件
```

## 🚀 使用方法

### 1. 放入照片
将需要转换的照片放到 `input/` 文件夹

### 2. 运行转换
```bash
cd /Users/cyh/.openclaw/workspace/photo-to-sketch

# 简单线稿风格（推荐，类似分镜草图）
python3 convert.py simple

# 细节线稿风格（保留更多细节）
python3 convert.py detailed
```

### 3. 查看结果
转换后的线稿会保存在 `output/` 文件夹，文件名会自动添加 `_sketch` 后缀

## 🎨 风格说明

**simple 模式（推荐）**
- 极简的黑白线条
- 突出主要轮廓和结构
- 类似你提供的第一张分镜草图效果
- 适合：分镜设计、概念草图

**detailed 模式**
- 保留更多细节和纹理
- 适合需要较多信息的场景
- 适合：插画参考、详细草图

## 📋 支持格式

- JPG / JPEG
- PNG
- BMP
- WebP

## 💡 使用技巧

1. 输入照片分辨率越高，线稿质量越好
2. 光线对比明显的照片效果更好
3. 人物照片建议选择背景简洁的
4. 批量处理：直接把多张照片放入 input/ 即可

## 🔧 依赖

需要安装 OpenCV：
```bash
pip3 install opencv-python numpy
```

## 📝 示例

```bash
# 转换单批照片
python3 convert.py simple

# 输出示例：
# ✅ 已转换: photo1.jpg -> photo1_sketch.jpg
# ✅ 已转换: photo2.png -> photo2_sketch.png
# ✨ 完成! 成功转换 2/2 张图片
```
