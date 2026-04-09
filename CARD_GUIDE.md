# 网页色卡制作指南 · Web Design Card Guide

> 通过分析各品牌 `DESIGN.md` 文档，提炼精华视觉要素，制作可横向比较的"网页色卡"。  
> 目标：一张色卡 = 一个品牌的设计基因速写。

---

## 一、色卡设计理念

### 类比游戏设计色卡
游戏美术用色卡（Color Card）定义角色、场景的视觉调性，方便团队选用风格。  
**网页色卡**在同样的框架下运作：

| 游戏色卡 | 网页色卡 |
|---------|---------|
| 角色主色 / 辅色 | 背景色 / 文字色 / 强调色 |
| 材质质感 | 阴影与边框样式 |
| 造型特征（圆润 / 尖锐） | 圆角程度 |
| 字体风格 | 字体族与字重 |
| 整体氛围 | 主题标签（极简 / 奢华 / 工程 …） |

### 关键平衡
- ✅ 展示：**配色 + 圆角 + 字体 + 阴影 + 按钮形态**（视觉基因）  
- ❌ 省略：高层次设计哲学、品牌叙事、布局网格细节（内容过密）

---

## 二、数据提取模板（从 DESIGN.md 中提炼）

分析每个品牌的 DESIGN.md，填写以下字段：

```yaml
# ── 品牌基础信息 ──────────────────────────────────────────────────────────
id:          cursor
name:        Cursor
category:    开发工具
filterGroup: dev

# ── 颜色 ──────────────────────────────────────────────────────────────────
# theme 决定卡片整体渲染逻辑（浅色/深色/特殊背景）
theme:    light       # light | dark | dual | special

bg:       "#f2f1ed"               # 页面主背景 → 色卡底色
text:     "#26251e"               # 主文字色   → 标题/正文渲染
accent:   "#f54e00"               # 强调色      → 主按钮背景、激活状态
surface:  "#e6e5e0"               # 表面色      → 次按钮背景、mini-card 背景
border:   "rgba(38,37,30,0.1)"   # 边框色      → 分割线、mini-card 边框、输入框轮廓
neutral:  "rgba(38,37,30,0.55)"  # 次要文字色  → body 文字、placeholder
accent2:  "#c08532"               # 第二强调色  → 仅色板展示（可选）

# 色板：6个代表色，依次排列（bg → text → accent → surface → neutral → accent2）
colors:
  - "#f2f1ed"
  - "#26251e"
  - "#f54e00"
  - "#e6e5e0"
  - "rgba(38,37,30,0.55)"
  - "#c08532"

# ── 字体 ──────────────────────────────────────────────────────────────────
font:           "CursorGothic + jjannon"  # 品牌字体名（仅文字展示）
fontProxy:      "system-ui"               # 卡片实际渲染用代理字体
headingWeight:  "400"                     # 标题字重 → 渲染预览标题
headingSpacing: "-0.5px"                  # 标题字间距 → 渲染预览标题

# ── 圆角（两种，分开记录）─────────────────────────────────────────────────
# 按钮/徽章圆角：体现 CTA 的形态感（pill / 方形 / 标准圆角）
btnRadius: "9999px"    # pill=9999px | 标准=8px | 精准=4px | 锐利=0px

# 容器/卡片/输入框圆角：体现整体界面的"温度"
boxRadius: "8px"       # 对于 MiniMax(20px)/Airbnb(20px) vs Tesla(4px) 差异显著

# ── 质感 ──────────────────────────────────────────────────────────────────
shadow:   "0 14px 32px rgba(0,0,0,0.1)"  # 主卡片阴影 → mini-card box-shadow
btnColor: "#ffffff"    # 主按钮文字色（亮色 accent 如黄/绿时改为深色）

# ── 高层次风格标签 ────────────────────────────────────────────────────────
# 原则：能被控件直接渲染体现的（圆角/颜色/阴影）不在此出现
# 这里只放：排版哲学、阴影哲学、情感基调、设计方法论等抽象层信息
# 建议 2-3 个，避免堆砌
tags:
  - "暖系工艺"      # 情感基调：暖系工艺 / 冷工程 / 奢华克制 / 开放社区 / 极简禅意
  - "三字体编排"    # 排版方法：三字体编排 / 可变字重 / 等宽展示 / 单字族纯粹 / 衬线主导
  - "大模糊阴影"    # 阴影哲学：无阴影 / 微阴影 / 大模糊阴影 / 品牌色阴影 / 多层叠影
```

### 字段说明补充

**两种圆角的典型差异案例：**

| 品牌 | btnRadius | boxRadius | 说明 |
|------|-----------|-----------|------|
| MiniMax | 9999px (pill) | 20px | 导航用胶囊，卡片圆润 |
| Revolut | 9999px (pill) | 8px | 按钮全胶囊，容器标准 |
| Spotify | 9999px (pill) | 8px | 播放按钮圆形，卡片轻圆 |
| Tesla | 4px | 12px | 按钮精确，大图卡片柔和 |
| IBM | 0px | 0px | 全局锐利，Carbon 规范 |
| Apple | 8px | 8px | 小按钮/卡片一致，pill 仅用于链接 |

**tags 词库参考（按类别）：**

```
情感基调：暖系工艺 · 冷工程美学 · 奢华克制 · 开放社区感 · 极简禅意 · 戏剧张力
排版方法：三字体编排 · 可变字重 · 等宽字作展示 · 单字族纯粹 · 衬线主导 · 超大字号冲击
阴影哲学：无阴影 · 微边框阴影 · 大模糊氛围影 · 品牌色阴影 · 多层叠影
设计来源：摄影主导 · 印刷排版感 · 终端原生 · macOS 原生 · 游戏视觉 · 编辑杂志风
```

---

## 三、数据提取规则

### 3.1 从哪里找颜色？

| 字段 | DESIGN.md 对应位置 |
|------|-------------------|
| `bg` | Section 2 Primary → 页面背景色（Page background / Canvas） |
| `text` | Section 2 Primary / Text → 主文字色 |
| `accent` | Section 2 Interactive / Brand → 首个 CTA / 链接颜色 |
| `surface` | Section 2 Surface / 4. Buttons Primary Background → 按钮/卡片表面色 |
| `border` | Section 2 Border / Section 4 Cards → 默认边框色 |
| `neutral` | Section 2 Text → 次要文字色（Secondary / Body text） |

### 3.2 主题分类

| theme | 判断依据 | 典型品牌 |
|-------|---------|---------|
| `light` | 背景为白色或浅灰，文字为深色 | Cursor, Stripe, Notion, Tesla |
| `dark` | 背景为深色（#0a0a0a–#2a2a2a），文字为浅色 | Linear, Spotify, Supabase, xAI |
| `dual` | 页面交替出现深/浅区域作为核心设计特征 | Apple（黑白交替） |
| `special` | 品牌强调色作为页面背景 | Sanity（红底）、Wise（绿底） |

### 3.3 圆角感受标签

| 值范围 | 标签 | 代表品牌 |
|-------|------|---------|
| 0–2px | `r:0px` 锐利 | IBM, Ferrari, SpaceX |
| 3–6px | `r:4-6px` 精准 | Tesla, Stripe, Vercel |
| 8–12px | `r:8px` 标准 | 多数品牌（Notion, Claude, Linear） |
| 16–24px | `r:16-24px` 圆润 | MiniMax, Airbnb, Pinterest |
| 9999px | `r:pill` 胶囊 | Revolut, Spotify, Uber |

### 3.4 按钮文字颜色判断

强调色（accent）为**亮色/黄色/绿色**时，按钮文字须用深色：

```
需要 btnColor: "#000000"（或品牌深色）的品牌：
- ClickHouse (accent: #FAFF69)
- Miro (accent: #ffd02f)
- Lamborghini (accent: #e8b200)
- Renault (accent: #efda00)
- SpaceX / xAI (accent: rgba(255,255,255,...))
- Wise (accent: #23294e，但背景是绿色，不同场景)
```

---

## 四、色卡结构图解

```
┌─────────────────────────────────┐  ← 卡片宽度 ~240px
│  Brand Name         [Category]  │  ← 品牌标题（以品牌字重/间距渲染）
├╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌┤  ← 分割线颜色 = border 字段（功能色直接体现）
│  ● ● ● ● ● ●                   │  ← 6个色板圆点（bg/text/accent/surface/neutral/accent2）
├╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌┤  ← 分割线
│  Display Text ←字重+字间距渲染   │  ← 标题：headingWeight + headingSpacing
│  Body text secondary            │  ← 正文：neutral 色
│                                 │
│  [  Primary  ]  [ Secondary ]   │  ← 主按钮：accent色+btnColor文字+btnRadius圆角
│                                 │     次按钮：surface色+text文字+btnRadius圆角
│  ┌──────────────────────────┐   │  ← mini-card：
│  │ Card Element             │   │     背景=surface / 边框=border+boxRadius / 阴影=shadow
│  │ Surface · Border · Shadow│   │     （三个功能色通过一个控件同时体现）
│  └──────────────────────────┘   │
├╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌┤  ← 分割线
│  font (monospace)               │  ← 字体名称
│  [高层次标签] [排版方法] [阴影]  │  ← 2-3个抽象风格标签（无法直接渲染的信息）
└─────────────────────────────────┘

控件 → 字段映射：
  分割线颜色    ← border
  色板圆点      ← colors[0..5]
  标题字重/间距 ← headingWeight + headingSpacing
  次要文字色    ← neutral
  主按钮        ← accent + btnColor + btnRadius
  次按钮        ← surface + text + btnRadius
  mini-card 背景 ← surface
  mini-card 边框 ← border + boxRadius
  mini-card 阴影 ← shadow
```

---

## 五、HTML 卡片模板

以下是单张色卡的 HTML 结构（使用 CSS Custom Properties 注入品牌样式）：

```html
<!-- 在 .card 上通过 data-* 属性支持过滤 -->
<div class="card"
     data-theme="light"
     data-group="dev"
     style="
       background: #f2f1ed;
       border: 1px solid rgba(0,0,0,0.08);
     ">
  
  <!-- 1. 品牌标题区 -->
  <div class="card-header">
    <span class="brand-name"
          style="color:#26251e; font-weight:400; letter-spacing:-0.5px;">
      Cursor
    </span>
    <span class="cat-badge"
          style="background:rgba(38,37,30,0.08); color:rgba(38,37,30,0.6);">
      开发工具
    </span>
  </div>
  
  <div class="divider" style="background:rgba(0,0,0,0.06);"></div>
  
  <!-- 2. 色板区 -->
  <div class="card-palette">
    <div class="swatch" style="background:#f2f1ed;" title="#f2f1ed 背景"></div>
    <div class="swatch" style="background:#26251e;" title="#26251e 主文字"></div>
    <div class="swatch" style="background:#f54e00;" title="#f54e00 强调色"></div>
    <div class="swatch" style="background:#e6e5e0;" title="#e6e5e0 表面色"></div>
    <div class="swatch" style="background:rgba(38,37,30,0.55);" title="次要文字"></div>
    <div class="swatch" style="background:#c08532;" title="#c08532 金色"></div>
  </div>
  
  <div class="divider" style="background:rgba(0,0,0,0.06);"></div>
  
  <!-- 3. 预览区 -->
  <div class="card-preview" style="background:#f2f1ed;">
    
    <!-- 标题样式展示 -->
    <div class="preview-heading"
         style="color:#26251e; font-weight:400; letter-spacing:-0.5px;">
      Display Text
    </div>
    
    <!-- 正文样式展示 -->
    <div class="preview-body"
         style="color:rgba(38,37,30,0.55);">
      Secondary body text sample
    </div>
    
    <!-- 按钮组 -->
    <div class="preview-buttons">
      <button class="preview-btn"
              style="background:#f54e00; color:#fff; border-radius:8px; border:none;">
        Primary
      </button>
      <button class="preview-btn"
              style="background:#e6e5e0; color:#26251e;
                     border-radius:8px; border:1px solid rgba(38,37,30,0.1);">
        Secondary
      </button>
    </div>
    
    <!-- 卡片元素 -->
    <div class="preview-card-inner"
         style="background:#e6e5e0;
                border:1px solid rgba(38,37,30,0.1);
                border-radius:8px;
                box-shadow:0 14px 32px rgba(0,0,0,0.1);">
      <div class="preview-card-title" style="color:#26251e;">Card Element</div>
      <div class="preview-card-body" style="color:rgba(38,37,30,0.55);">
        Surface · Border · Shadow
      </div>
    </div>
    
  </div>
  
  <div class="divider" style="background:rgba(0,0,0,0.06);"></div>
  
  <!-- 4. 规格说明区 -->
  <div class="card-footer" style="background:rgba(0,0,0,0.03);">
    <div class="font-label" style="color:rgba(38,37,30,0.5);">
      CursorGothic + jjannon + berkeleyMono
    </div>
    <div class="tags">
      <span class="tag" style="background:rgba(0,0,0,0.07); color:rgba(38,37,30,0.55);">Light</span>
      <span class="tag" style="background:rgba(0,0,0,0.07); color:rgba(38,37,30,0.55);">暖色</span>
      <span class="tag" style="background:rgba(0,0,0,0.07); color:rgba(38,37,30,0.55);">r:8px</span>
      <span class="tag" style="background:rgba(0,0,0,0.07); color:rgba(38,37,30,0.55);">编辑器</span>
    </div>
  </div>
  
</div>
```

### 配套 CSS

```css
/* 卡片容器 */
.card {
  border-radius: 12px;
  overflow: hidden;
  transition: transform 0.18s ease, box-shadow 0.18s ease;
}
.card:hover { transform: translateY(-3px); }

/* 内部分区 */
.card-header  { padding: 12px 14px 10px; display: flex; align-items: center; justify-content: space-between; }
.card-palette { padding: 8px 14px; display: flex; gap: 5px; align-items: center; }
.card-preview { padding: 12px 14px; }
.card-footer  { padding: 8px 14px 12px; }
.divider      { height: 1px; margin: 0 14px; }

/* 色块 */
.swatch {
  width: 22px; height: 22px; border-radius: 50%; flex-shrink: 0;
  box-shadow: inset 0 0 0 1px rgba(0,0,0,0.1), inset 0 0 0 1px rgba(255,255,255,0.15);
}

/* 预览内容 */
.brand-name      { font-size: 14px; }
.cat-badge       { font-size: 9px; padding: 2px 7px; border-radius: 9999px; font-weight:600; text-transform:uppercase; letter-spacing:0.5px; }
.preview-heading { font-size: 17px; line-height: 1.1; margin-bottom: 4px; }
.preview-body    { font-size: 10px; line-height: 1.5; margin-bottom: 10px; }
.preview-buttons { display: flex; gap: 6px; margin-bottom: 10px; }
.preview-btn     { font-size: 10px; padding: 4px 10px; cursor: default; font-family: inherit; line-height: 1; }
.preview-card-inner { padding: 7px 9px; }
.preview-card-title { font-size: 9px; font-weight: 700; margin-bottom: 2px; }
.preview-card-body  { font-size: 8px; }

/* 规格区 */
.font-label { font-size: 9px; font-family: monospace; margin-bottom: 6px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.tags       { display: flex; gap: 4px; flex-wrap: wrap; }
.tag        { font-size: 8px; padding: 2px 6px; border-radius: 4px; font-weight: 600; text-transform: uppercase; letter-spacing: 0.3px; }
```

---

## 六、品牌数据速查表（58 个品牌）

| 品牌 | 主题 | 背景色 | 强调色 | 圆角 | 字体 | 类别 |
|------|------|-------|-------|------|------|------|
| Airbnb | Light | #ffffff | #ff385c 红 | 8px | Airbnb Cereal VF | 市场 |
| Airtable | Light | #ffffff | #2D7FF9 蓝 | 6px | Inter | 生产力 |
| Apple | Dual | #f5f5f7/black | #0071e3 蓝 | 8px/pill | SF Pro | 消费科技 |
| BMW | Light | #ffffff | #1c69d4 蓝 | 4px | BMW Helvetica | 汽车 |
| Cal | Light | #ffffff | #101010 黑 | 8px | Cal Sans/Inter | 调度 |
| Claude | Light | #f5f4ed 羊皮纸 | #c96442 陶土 | 8px | Anthropic Serif | AI对话 |
| Clay | Dark | #0f172a | #7c3aed 紫 | 12px | Geist/Inter | CRM |
| ClickHouse | Light | #ffffff | #FAFF69 黄 | 4px | Inter | 数据库 |
| Cohere | Light | #f8f7f6 暖白 | #39594d 深绿 | 8px | Inter | 企业AI |
| Coinbase | Light | #ffffff | #0052FF 蓝 | 8px | Coinbase Display | 加密 |
| Composio | Dark | #0a0a0a | #7c3aed 紫 | 8px | Inter | 开发工具 |
| Cursor | Light | #f2f1ed 奶油 | #f54e00 橙 | 8px | CursorGothic+jjannon | 开发工具 |
| ElevenLabs | Dark | #111111 | #ff9f43 橙 | 8px | Inter | AI语音 |
| Expo | Light | #ffffff | #4630eb 紫 | 8px | Inter | 移动开发 |
| Ferrari | Dark | #000000 | #DA291C 红 | 2px | FerrariSans | 超跑 |
| Figma | Light | #ffffff | #000000 黑白 | pill(50px) | figmaSans Variable | 设计工具 |
| Framer | Dark | #0a0a0a | #0099ff 蓝 | 12px | Inter | 设计工具 |
| HashiCorp | Dark | #000000 | #6b3ccc 紫 | 6px | Inter | 企业DevOps |
| IBM | Light | #ffffff | #0f62fe 蓝 | **0px** | IBM Plex Sans | 企业 |
| Intercom | Light | #ffffff | #1f8eed 蓝 | 8px | Inter | 客服SaaS |
| Kraken | Dark | #1a0533 深紫 | #5741d9 紫 | 8px | Inter | 加密交易 |
| Lamborghini | Dark | #000000 | #e8b200 金 | **0px** | Lato | 超跑 |
| Linear | Dark | #08090a | #5e6ad2 靛蓝 | 6px | Inter Variable | 项目管理 |
| Lovable | Light | #ffffff | #ff6b6b 粉红 | 12px | Inter | AI开发 |
| MiniMax | Light | #ffffff | #1456f0+#ea5ec1 | 20px | DM Sans+Outfit | AI平台 |
| Mintlify | Dark | #0a0a0a | #16b364 绿 | 8px | Inter | 文档平台 |
| Miro | Light | #ffffff | #ffd02f 黄 | 12px | Inter | 协作白板 |
| Mistral AI | Dark | #0d0d0d | #ff7000 橙 | 8px | Inter | AI模型 |
| MongoDB | Dark | #001e2b 深蓝 | #00ed64 绿 | 8px | Euclid Circular B | 数据库 |
| Notion | Light | #ffffff | #0075de 蓝 | 8px | NotionInter | 生产力 |
| NVIDIA | Dark | #000000 | #76b900 绿 | 4px | Inter | AI芯片 |
| Ollama | Light | #f6f6f4 暖灰 | #ff6b35 橙 | 6px | Inter | 本地LLM |
| OpenCode | Dark | #0a0a0a | #0070f3 蓝 | 8px | Geist | AI编码 |
| Pinterest | Light | #ffffff | #e60023 红 | 16px | Helvetica Neue | 视觉社交 |
| PostHog | Dark | #1d1d1d | #ff7b3e 橙 | 8px | Matter/Inter | 分析 |
| Raycast | Dark | #07080a 蓝黑 | #FF6363 红 | 8px | Inter | 开发工具 |
| Renault | Dark | #000000 | #efda00 黄 | **0px** | Inter | 汽车 |
| Replicate | Dark | #000000 | #047857 绿 | 6px | Söhne/Inter | ML平台 |
| Resend | Dark | #000000 | #0070f3 蓝 | 6px | Geist | 邮件API |
| Revolut | Dark | #191c1f | #494fdf 蓝 | **pill** | Aeonik Pro | 金融科技 |
| Runway ML | Dark | #0a0a0a | #00ff87 绿 | 8px | Agrandir/Inter | 创意AI |
| Sanity | Special | #f03e2f 红底 | #ffffff 白 | 4px | Inter | CMS |
| Sentry | Dark | #1d1127 深紫 | #6c5fc7 紫 | 8px | Rubik/Inter | 监控 |
| SpaceX | Dark | #000000 | #ffffff 白 | **0px** | Helvetica Neue | 航天 |
| Spotify | Dark | #121212 | #1ed760 绿 | **pill** | Circular | 音乐 |
| Stripe | Light | #ffffff | #533afd 紫 | 6px | Söhne (Weight 300) | 支付 |
| Supabase | Dark | #171717 | #3ecf8e 绿 | 6px | Circular | 开源数据库 |
| Superhuman | Dark | #0a0a0a | #8b5cf6 紫 | 8px | Inter | 邮件 |
| Tesla | Light | #FFFFFF | #3E6AE1 蓝 | **4px** | Universal Sans | 汽车 |
| Together AI | Dark | #0a0a0a | #3d5afe 蓝 | 8px | Inter | AI推理 |
| Uber | Light | #ffffff | #000000 黑 | **pill** | UberMove | 出行 |
| Vercel | Light | #ffffff | #0072f5 蓝 | 6px | Geist Sans+Mono | 部署 |
| VoltAgent | Dark | #0a0a0a | #ff6b00 橙 | 8px | Inter | AI Agent |
| Warp | Dark | #1b1b2f 深蓝 | #00b4d8 青 | 8px | Inter | 终端 |
| Webflow | Light | #ffffff | #146ef5 蓝 | 12px | Inter | NoCode |
| Wise | Special | #9fe870 绿底 | #23294e 深蓝 | 8px | Inter | 国际汇款 |
| xAI (Grok) | Dark | #1f2228 | 纯白 | **2px** | GeistMono+universalSans | AI模型 |
| Zapier | Light | #ffffff | #ff4a00 橙 | 8px | Circular/Inter | 自动化 |

---

## 七、品牌分类参考

用于画廊页面的过滤功能：

```
AI / ML:      minimax, claude, xai, cohere, elevenlabs, mistral, nvidia, ollama,
              opencode, replicate, runwayml, together, voltagent, lovable, composio

开发工具:     cursor, linear, vercel, supabase, raycast, warp, expo, posthog,
              hashicorp, mintlify, resend, sentry, figma, framer, webflow,
              figma, clickhouse, mongodb, airtable, intercom

金融科技:     stripe, revolut, coinbase, wise, kraken, airbnb (marketplace)

汽车:         tesla, ferrari, bmw, lamborghini, renault, spacex

SaaS 生产力:  notion, miro, zapier, cal, sanity, superhuman

消费 / 媒体:  airbnb, uber, spotify, pinterest, apple
```

---

## 八、制作流程（Step by Step）

1. **提取数据**：按第二节模板，从 DESIGN.md 的 Section 1-4 中提取关键值  
2. **填写色卡**：将数据填入 HTML 模板的 `style=""` 内联属性  
3. **调整预览**：确认按钮文字色（亮色系 accent 用深色文字）  
4. **添加标签**：基于主题 / 圆角值 / 风格感受选取 3-4 个标签  
5. **加入画廊**：将卡片对象添加到 `card-gallery.html` 的 `brands` 数组  

---

## 九、扩展思路

- **悬停展开**：鼠标悬停时显示更多字段（阴影样式、字号规格）  
- **颜色值复制**：点击色块自动复制 HEX 到剪贴板  
- **导出功能**：将卡片渲染为 PNG / SVG 图片（可用 `html2canvas`）  
- **对比模式**：选择多张色卡并排对比  
- **CSV 导入**：从 CSV 批量导入品牌数据，无需修改 JS  
