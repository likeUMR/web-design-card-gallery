# 网页色卡库 · Web Design Card Gallery

> 58 个知名网站的设计 token 可视化色卡，支持一键复制 DESIGN.md、跳转官网、按主题/行业筛选。

**[在线预览 →](https://likeumr.github.io/web-design-card-gallery/)**

![gallery preview](https://img.shields.io/badge/brands-58-blue) ![license](https://img.shields.io/badge/license-MIT-green)

## 功能

- 🎨 **58 个品牌**色卡，覆盖 AI、开发工具、金融科技、汽车、SaaS、消费等行业
- 📋 **一键复制 DESIGN.md**：点击卡片右上角复制按钮，直接粘贴进项目使用
- 🔗 **跳转官网**：点击外链按钮访问品牌官方网站
- 🔍 **多维筛选**：按浅色/深色/特殊背景 + 行业分类筛选
- 🎯 **设计预览**：每张色卡展示配色、字体、圆角、阴影、按钮等核心 UI 元素

## 本地使用

直接用浏览器打开 `card-gallery.html` 即可，无需服务器。

## 重新生成（需要 LLM API）

```bash
# 安装依赖
pip install openai pyyaml

# 设置 API Key
set LLM_TOKEN=your_api_key_here   # Windows
export LLM_TOKEN=your_api_key_here  # macOS/Linux

# 提取所有品牌 YAML（支持断点续传）
python extract_yaml.py

# 根据 YAML 生成 HTML
python generate_gallery.py

# 或一键运行完整流程
python run_pipeline.py
```

## 文件结构

```
├── card-gallery.html        # 主画廊（可直接打开）
├── extract_yaml.py          # LLM 提取设计 token → YAML
├── generate_gallery.py      # YAML → HTML 生成器
├── run_pipeline.py          # 一键运行脚本
├── CARD_GUIDE.md            # 色卡设计规范与 YAML schema
├── brand_data/              # 58 个品牌的提取 YAML
└── design-md-download/      # 源 DESIGN.md 文件
```

## 数据来源

设计 token 数据来自 [VoltAgent/awesome-design-md](https://github.com/VoltAgent/awesome-design-md)（MIT License）。  
本项目仅对数据进行结构化提取和可视化展示，不主张对原始品牌视觉资产的任何所有权。

## License

MIT
