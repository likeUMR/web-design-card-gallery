# coding=utf-8
"""
generate_gallery.py
───────────────────
读取 brand_data/*.yaml，生成 card-gallery.html。

用法:
    python generate_gallery.py              # 输出到 card-gallery.html
    python generate_gallery.py out.html     # 自定义输出路径
"""

import sys
import json
import yaml
from pathlib import Path

# Windows GBK 控制台 UTF-8 兼容
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

BRAND_DATA_DIR = Path(__file__).parent / "brand_data"
DESIGN_ROOT    = Path(__file__).parent / "design-md-download"
OUTPUT_HTML    = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).parent / "card-gallery.html"

# 官方网站映射（用于"查看源站"按钮）
BRAND_URLS: dict = {
    "airbnb":      "https://www.airbnb.com",
    "airtable":    "https://www.airtable.com",
    "apple":       "https://www.apple.com",
    "bmw":         "https://www.bmw.com",
    "cal":         "https://cal.com",
    "claude":      "https://claude.ai",
    "clay":        "https://clay.com",
    "clickhouse":  "https://clickhouse.com",
    "cohere":      "https://cohere.com",
    "coinbase":    "https://www.coinbase.com",
    "composio":    "https://composio.io",
    "cursor":      "https://www.cursor.com",
    "elevenlabs":  "https://elevenlabs.io",
    "expo":        "https://expo.dev",
    "ferrari":     "https://www.ferrari.com",
    "figma":       "https://www.figma.com",
    "framer":      "https://www.framer.com",
    "hashicorp":   "https://www.hashicorp.com",
    "ibm":         "https://www.ibm.com",
    "intercom":    "https://www.intercom.com",
    "kraken":      "https://www.kraken.com",
    "lamborghini": "https://www.lamborghini.com",
    "linear.app":  "https://linear.app",
    "lovable":     "https://lovable.dev",
    "minimax":     "https://www.minimaxi.com",
    "mintlify":    "https://mintlify.com",
    "miro":        "https://miro.com",
    "mistral.ai":  "https://mistral.ai",
    "mongodb":     "https://www.mongodb.com",
    "notion":      "https://www.notion.so",
    "nvidia":      "https://www.nvidia.com",
    "ollama":      "https://ollama.com",
    "opencode.ai": "https://opencode.ai",
    "pinterest":   "https://www.pinterest.com",
    "posthog":     "https://posthog.com",
    "raycast":     "https://www.raycast.com",
    "renault":     "https://www.renault.com",
    "replicate":   "https://replicate.com",
    "resend":      "https://resend.com",
    "revolut":     "https://www.revolut.com",
    "runwayml":    "https://runwayml.com",
    "sanity":      "https://www.sanity.io",
    "sentry":      "https://sentry.io",
    "spacex":      "https://www.spacex.com",
    "spotify":     "https://www.spotify.com",
    "stripe":      "https://stripe.com",
    "supabase":    "https://supabase.com",
    "superhuman":  "https://superhuman.com",
    "tesla":       "https://www.tesla.com",
    "together.ai": "https://www.together.ai",
    "uber":        "https://www.uber.com",
    "vercel":      "https://vercel.com",
    "voltagent":   "https://voltagent.dev",
    "warp":        "https://www.warp.dev",
    "webflow":     "https://webflow.com",
    "wise":        "https://wise.com",
    "x.ai":        "https://x.ai",
    "zapier":      "https://zapier.com",
}

# ── 字段默认值 ─────────────────────────────────────────────────────────────────
DEFAULTS = {
    "category":      "未分类",
    "filterGroup":   "dev",
    "theme":         "light",
    "bg":            "#ffffff",
    "text":          "#111111",
    "accent":        "#0070f3",
    "surface":       "#f4f4f4",
    "border":        "rgba(0,0,0,0.1)",
    "neutral":       "#666666",
    "accent2":       "#999999",
    "colors":        ["#ffffff","#111111","#0070f3","#f4f4f4","#666666","#999999"],
    "font":          "System UI",
    "fontProxy":     "system-ui",
    "headingWeight": "600",
    "headingSpacing":"0px",
    "btnRadius":     "8px",
    "boxRadius":     "8px",
    "shadow":        "none",
    "btnColor":      "#ffffff",
    "tags":          [],
}

# filterGroup → 过滤标签中文名
GROUP_LABELS = {
    "AI":       "AI / ML",
    "dev":      "开发工具",
    "fin":      "金融科技",
    "auto":     "汽车",
    "saas":     "SaaS",
    "consumer": "消费",
}


def load_brands() -> list:
    """读取所有 YAML 文件，规范化字段，返回 list[dict]。"""
    yaml_files = sorted(BRAND_DATA_DIR.glob("*.yaml"))
    if not yaml_files:
        raise FileNotFoundError(f"No YAML files found in {BRAND_DATA_DIR}")

    brands = []
    for yf in yaml_files:
        try:
            with open(yf, encoding="utf-8") as f:
                raw = yaml.safe_load(f)
            if not isinstance(raw, dict):
                print(f"  [SKIP] {yf.name}: not a dict")
                continue

            b = normalize(raw)

            # 读取 DESIGN.md 原文（用于复制功能）
            dm_path = DESIGN_ROOT / b["id"] / "DESIGN.md"
            b["_md"]  = dm_path.read_text(encoding="utf-8") if dm_path.exists() else ""
            b["_url"] = BRAND_URLS.get(b["id"],
                        f"https://www.google.com/search?q={b['name']}+design+system")

            brands.append(b)
        except Exception as e:
            print(f"  [WARN] {yf.name}: {e}")

    brands.sort(key=lambda b: b["name"].lower())
    print(f"Loaded {len(brands)} brands from {BRAND_DATA_DIR}")
    return brands


def normalize(raw: dict) -> dict:
    """规范化单个品牌数据：填充默认值、修正常见问题。"""
    b = {**DEFAULTS, **raw}

    # theme: drop 'dual' → use 'light' as primary
    if b["theme"] == "dual":
        b["theme"] = "light"

    # colors: ensure list of 6 strings
    colors = b.get("colors", [])
    if not isinstance(colors, list):
        colors = []
    colors = [str(c) for c in colors]
    while len(colors) < 6:
        colors.append("#cccccc")
    b["colors"] = colors[:6]

    # tags: ensure list of strings, max 3
    tags = b.get("tags", [])
    if not isinstance(tags, list):
        tags = []
    b["tags"] = [str(t) for t in tags][:3]

    # border: 'none' stays as 'none' (handled in JS)
    if b["border"] in (None, "null", ""):
        b["border"] = "none"

    # shadow: None → 'none'
    if not b["shadow"] or b["shadow"] in ("null", "None"):
        b["shadow"] = "none"

    # Ensure string types for CSS values
    for key in ("headingWeight", "headingSpacing", "btnRadius", "boxRadius"):
        b[key] = str(b[key])

    # JS-friendly field names (keep YAML names, map in JS template)
    return b


def brands_to_js(brands: list) -> str:
    """Serialize brands list to a JS array literal (via JSON)."""
    # Build JS-friendly objects
    js_brands = []
    for b in brands:
        obj = {
            "id":      b["id"],
            "name":    b["name"],
            "cat":     b["category"],
            "group":   b["filterGroup"],
            "theme":   b["theme"],
            "bg":      b["bg"],
            "text":    b["text"],
            "accent":  b["accent"],
            "surface": b["surface"],
            "border":  b["border"],
            "neutral": b["neutral"],
            "colors":  b["colors"],
            "font":    b["font"],
            "fw":      b["headingWeight"],
            "ls":      b["headingSpacing"],
            "btnR":    b["btnRadius"],
            "boxR":    b["boxRadius"],
            "btnC":    b["btnColor"],
            "shadow":  b["shadow"],
            "tags":    b["tags"],
            "url":     b.get("_url", ""),
            "md":      b.get("_md", ""),
        }
        js_brands.append(obj)

    return json.dumps(js_brands, ensure_ascii=False, indent=2)


def build_html(brands: list) -> str:
    """Generate the complete gallery HTML."""
    total   = len(brands)
    brands_js = brands_to_js(brands)

    # Count per group for filter labels
    group_counts = {}
    theme_counts = {}
    for b in brands:
        g = b["filterGroup"]
        t = b["theme"]
        group_counts[g] = group_counts.get(g, 0) + 1
        theme_counts[t] = theme_counts.get(t, 0) + 1

    def filter_btn(key, label, extra_class=""):
        return f'<button class="filter-btn{" " + extra_class if extra_class else ""}" data-filter="{key}">{label}</button>'

    filter_btns = "\n    ".join([
        filter_btn("light",    f"浅色 ({theme_counts.get('light',0)})"),
        filter_btn("dark",     f"深色 ({theme_counts.get('dark',0)})"),
        filter_btn("special",  f"特殊背景 ({theme_counts.get('special',0)})"),
        '<span class="filter-sep"></span>',
        filter_btn("AI",       f"AI / ML ({group_counts.get('AI',0)})"),
        filter_btn("dev",      f"开发工具 ({group_counts.get('dev',0)})"),
        filter_btn("fin",      f"金融科技 ({group_counts.get('fin',0)})"),
        filter_btn("auto",     f"汽车 ({group_counts.get('auto',0)})"),
        filter_btn("saas",     f"SaaS ({group_counts.get('saas',0)})"),
        filter_btn("consumer", f"消费 ({group_counts.get('consumer',0)})"),
    ])

    return f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>网页色卡库 · Web Design Card Gallery</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=DM+Sans:opsz,wght@9..40,300;9..40,400;9..40,500;9..40,600;9..40,700&family=IBM+Plex+Mono:wght@400;500&display=swap" rel="stylesheet">
  <style>
    *, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}

    body {{
      background: #0d0d0d;
      color: #e0e0e0;
      font-family: 'DM Sans', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
      min-height: 100vh;
      padding: 32px 20px 64px;
    }}

    /* ── PAGE HEADER ── */
    .page-header {{
      max-width: 1480px;
      margin: 0 auto 24px;
      display: flex;
      align-items: flex-start;
      justify-content: space-between;
      flex-wrap: wrap;
      gap: 12px;
    }}
    .page-title   {{ font-size: 21px; font-weight: 700; letter-spacing: -0.4px; color: #fff; }}
    .page-sub     {{ font-size: 12px; color: rgba(255,255,255,0.38); margin-top: 3px; font-family: 'IBM Plex Mono', monospace; }}
    .page-meta    {{ font-size: 11px; color: rgba(255,255,255,0.2); font-family: 'IBM Plex Mono', monospace; text-align: right; line-height: 1.7; }}

    /* ── GITHUB STAR BUTTON ── */
    .gh-star-btn {{
      display: inline-flex; align-items: center; gap: 7px;
      padding: 7px 14px; border-radius: 9px;
      border: 1px solid rgba(255,255,255,0.14);
      background: rgba(255,255,255,0.05);
      color: rgba(255,255,255,0.72); font-size: 12px; font-weight: 600;
      text-decoration: none; transition: all 0.15s; white-space: nowrap;
      font-family: 'DM Sans', sans-serif;
    }}
    .gh-star-btn:hover {{
      background: rgba(255,255,255,0.1);
      border-color: rgba(255,255,255,0.28);
      color: #fff;
    }}
    .gh-star-btn .gh-icon {{ flex-shrink: 0; opacity: 0.7; transition: opacity 0.15s; }}
    .gh-star-btn:hover .gh-icon {{ opacity: 1; }}
    .gh-star-sep {{ color: rgba(255,255,255,0.18); margin: 0 1px; }}
    .gh-star-count {{
      font-family: 'IBM Plex Mono', monospace; font-size: 11px;
      background: rgba(255,255,255,0.08); padding: 1px 6px; border-radius: 4px;
      min-width: 22px; text-align: center;
    }}

    /* ── FILTER BAR ── */
    .filter-bar {{
      max-width: 1480px;
      margin: 0 auto 20px;
      display: flex;
      gap: 6px;
      flex-wrap: wrap;
      align-items: center;
    }}
    .filter-label {{ font-size: 11px; color: rgba(255,255,255,0.28); margin-right: 4px; flex-shrink: 0; }}
    .filter-sep   {{ width: 1px; height: 18px; background: rgba(255,255,255,0.1); margin: 0 4px; }}
    .filter-btn {{
      padding: 4px 12px;
      border-radius: 9999px;
      border: 1px solid rgba(255,255,255,0.1);
      background: rgba(255,255,255,0.04);
      color: rgba(255,255,255,0.45);
      font-size: 11px;
      cursor: pointer;
      transition: all 0.15s;
      font-family: inherit;
      font-weight: 500;
      white-space: nowrap;
    }}
    .filter-btn:hover {{ background: rgba(255,255,255,0.08); color: rgba(255,255,255,0.8); border-color: rgba(255,255,255,0.2); }}
    .filter-btn.active {{ background: rgba(255,255,255,0.13); color: #fff; border-color: rgba(255,255,255,0.3); }}
    #allBtn {{ margin-right: 4px; }}
    .count-badge {{ font-size: 11px; color: rgba(255,255,255,0.25); font-family: 'IBM Plex Mono', monospace; margin-left: 6px; }}

    /* ── CARD GRID ── */
    .card-grid {{
      max-width: 1480px;
      margin: 0 auto;
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(224px, 1fr));
      gap: 13px;
    }}

    /* ── CARD ── */
    .card {{
      border-radius: 12px;
      overflow: hidden;
      transition: transform 0.2s cubic-bezier(0.34,1.4,0.64,1);
      cursor: default;
    }}
    .card:hover {{ transform: translateY(-4px); }}
    .card.hidden {{ display: none !important; }}

    .card-header {{
      padding: 11px 13px 9px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 6px;
    }}
    .brand-name {{ font-size: 13px; line-height: 1; flex: 1; min-width: 0; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; letter-spacing: -0.2px; }}
    .header-actions {{ display: flex; gap: 3px; flex-shrink: 0; opacity: 0; transition: opacity 0.15s; }}
    .card:hover .header-actions {{ opacity: 1; }}
    .action-btn {{
      display: flex; align-items: center; justify-content: center;
      width: 22px; height: 22px; border-radius: 5px;
      border: none; background: transparent; cursor: pointer;
      transition: background 0.12s;
      text-decoration: none; padding: 0;
    }}
    .action-btn:hover {{ background: rgba(128,128,128,0.18); }}
    .action-btn svg {{ display: block; pointer-events: none; }}
    .cat-tag {{ font-size: 8px; padding: 2px 6px; border-radius: 3px; font-weight: 700; text-transform: uppercase; letter-spacing: 0.5px; white-space: nowrap; line-height: 1.4; }}

    /* ── TOAST ── */
    #toast {{
      position: fixed; bottom: 28px; left: 50%; transform: translateX(-50%) translateY(12px);
      background: rgba(255,255,255,0.92); color: #111; font-size: 12px; font-weight: 600;
      padding: 7px 18px; border-radius: 9999px; pointer-events: none;
      opacity: 0; transition: opacity 0.18s, transform 0.18s; z-index: 9999;
      font-family: 'DM Sans', sans-serif; white-space: nowrap;
    }}
    #toast.show {{ opacity: 1; transform: translateX(-50%) translateY(0); }}

    .div-line {{ height: 1px; margin: 0 13px; }}

    .card-palette {{ padding: 8px 13px; display: flex; gap: 5px; align-items: center; }}
    .swatch {{
      width: 21px; height: 21px; border-radius: 50%; flex-shrink: 0;
      box-shadow: inset 0 0 0 1px rgba(0,0,0,0.12), inset 0 0 0 1px rgba(255,255,255,0.1);
    }}

    .card-preview {{ padding: 10px 13px 11px; }}

    /* Render heading at real-world size then zoom down — preserves ALL px proportions */
    .preview-heading-wrap {{ margin-bottom: 3px; overflow: hidden; }}
    .preview-heading {{
      font-size: 48px; line-height: 1; display: block;
      white-space: nowrap; overflow: hidden;
      zoom: 0.35;          /* 48px × 0.35 ≈ 17px visual — letter-spacing scales too */
    }}
    .preview-body    {{ font-size: 10px; line-height: 1.5; margin-bottom: 9px; }}
    .preview-btns    {{ display: flex; gap: 5px; margin-bottom: 9px; }}
    .preview-btn     {{ font-size: 10px; padding: 4px 9px; cursor: default; font-family: inherit; line-height: 1; font-weight: 500; }}
    .mini-card       {{ padding: 7px 9px; }}
    .mini-card-title {{ font-size: 9px; font-weight: 700; margin-bottom: 2px; }}
    .mini-card-body  {{ font-size: 8px; opacity: 0.75; }}

    .card-footer {{ padding: 7px 13px 11px; }}
    .font-label  {{ font-size: 9px; font-family: 'IBM Plex Mono', monospace; margin-bottom: 5px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }}
    .tags        {{ display: flex; gap: 4px; flex-wrap: wrap; }}
    .tag         {{ font-size: 8px; padding: 2px 6px; border-radius: 3px; font-weight: 700; text-transform: none; letter-spacing: 0.1px; line-height: 1.4; }}

    /* ── EMPTY STATE ── */
    .empty-state {{ max-width: 1480px; margin: 60px auto; text-align: center; color: rgba(255,255,255,0.18); font-size: 13px; display: none; }}

    /* ── FOOTER ── */
    .page-footer {{
      max-width: 1480px;
      margin: 40px auto 0;
      padding-top: 24px;
      border-top: 1px solid rgba(255,255,255,0.06);
      display: flex;
      align-items: center;
      justify-content: space-between;
      flex-wrap: wrap;
      gap: 12px;
    }}
    .legend {{ display: flex; gap: 20px; flex-wrap: wrap; }}
    .legend-item {{ display: flex; align-items: center; gap: 7px; font-size: 11px; color: rgba(255,255,255,0.28); }}
    .legend-dot  {{ width: 9px; height: 9px; border-radius: 50%; flex-shrink: 0; }}
  </style>
</head>
<body>

<!-- HEADER -->
<div class="page-header">
  <div>
    <div class="page-title">网页色卡库</div>
    <div class="page-sub">Web Design Card Gallery · {total} brands · LLM-extracted design tokens</div>
  </div>
  <a href="https://github.com/likeUMR/web-design-card-gallery"
     target="_blank" rel="noopener"
     class="gh-star-btn"
     title="如果这个工具对你有帮助，请给个 Star ⭐">
    <svg class="gh-icon" width="15" height="15" viewBox="0 0 16 16" fill="currentColor">
      <path d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27.68 0 1.36.09 2 .27 1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.013 8.013 0 0016 8c0-4.42-3.58-8-8-8z"/>
    </svg>
    <span>Star on GitHub</span>
    <span class="gh-star-sep">|</span>
    <span class="gh-star-count" id="ghStarCount">…</span>
  </a>
</div>

<!-- FILTER BAR -->
<div class="filter-bar">
  <span class="filter-label">筛选</span>
  <button class="filter-btn active" id="allBtn" data-filter="all">全部 ({total})</button>
  {filter_btns}
  <span class="count-badge" id="countBadge">{total}</span>
</div>

<!-- CARD GRID -->
<div class="card-grid" id="cardGrid"></div>
<div class="empty-state" id="emptyState">该分类暂无色卡</div>
<div id="toast">YAML 已复制</div>

<!-- FOOTER -->
<div class="page-footer">
  <div class="legend">
    <div class="legend-item"><div class="legend-dot" style="background:#e0e0e0;border:1px solid rgba(0,0,0,0.1)"></div>浅色主题</div>
    <div class="legend-item"><div class="legend-dot" style="background:#222"></div>深色主题</div>
    <div class="legend-item"><div class="legend-dot" style="background:linear-gradient(135deg,#f03e2f 50%,#9fe870 50%)"></div>特殊背景</div>
  </div>
  <div style="font-size:11px;color:rgba(255,255,255,0.18);text-align:right;line-height:1.8;">
    色卡颜色取自品牌设计文档 · 悬停查看动效<br>
    <a href="https://github.com/VoltAgent/awesome-design-md" target="_blank" rel="noopener"
       style="color:rgba(255,255,255,0.13);text-decoration:none;font-size:10px;font-family:'IBM Plex Mono',monospace;"
       onmouseover="this.style.color='rgba(255,255,255,0.35)'" onmouseout="this.style.color='rgba(255,255,255,0.13)'">
      Design tokens: VoltAgent/awesome-design-md · MIT License
    </a>
  </div>
</div>

<script>
// ── BRAND DATA (LLM extracted) ────────────────────────────────────────────────
const brands = {brands_js};

// ── RENDER CARD ───────────────────────────────────────────────────────────────
function renderCard(b) {{
  const isDark    = b.theme === 'dark';
  const isSpecial = b.theme === 'special';

  // Divider & chrome colors
  const divCol     = isDark ? 'rgba(255,255,255,0.06)' : 'rgba(0,0,0,0.06)';
  const actualBorder = (b.border && b.border !== 'none') ? b.border : divCol;
  const footBg     = isDark ? 'rgba(0,0,0,0.22)' : isSpecial ? 'rgba(0,0,0,0.1)' : 'rgba(0,0,0,0.04)';
  const tagBg      = isDark ? 'rgba(255,255,255,0.1)' : isSpecial ? 'rgba(255,255,255,0.18)' : 'rgba(0,0,0,0.07)';
  const cardBorder = isDark ? 'rgba(255,255,255,0.08)' : isSpecial ? 'rgba(255,255,255,0.18)' : 'rgba(0,0,0,0.07)';

  // Swatches
  const swatchHtml = b.colors.slice(0,6).map(c =>
    `<div class="swatch" style="background:${{c}}" title="${{c}}"></div>`
  ).join('');

  // Footer tags: category first, then abstract tags
  const catTagHtml = `<span class="cat-tag" style="background:${{tagBg}};color:${{b.neutral}}">${{b.cat}}</span>`;
  const tagsHtml = b.tags.map(t =>
    `<span class="tag" style="background:${{tagBg}};color:${{b.neutral}}">${{t}}</span>`
  ).join('');

  // Primary button: outline if accent is white/transparent
  const isLightAccent = b.accent === '#ffffff' || b.accent === 'white' || b.accent.startsWith('rgba(255,255,255');
  const primBorder = isLightAccent ? `1px solid ${{b.neutral}}` : 'none';

  // Icon colors (adapt to card bg)
  const iconColor = isDark || isSpecial ? 'rgba(255,255,255,0.45)' : 'rgba(0,0,0,0.35)';
  const sourceUrl = b.url;

  return `
  <div class="card" data-theme="${{b.theme}}" data-group="${{b.group}}"
       style="background:${{b.bg}}; border:1px solid ${{cardBorder}}; box-shadow:0 2px 10px rgba(0,0,0,0.2);">

    <div class="card-header">
      <span class="brand-name" style="color:${{b.text}};font-weight:${{b.fw}}">${{b.name}}</span>
      <div class="header-actions">
        <button class="action-btn copy-btn" data-id="${{b.id}}" title="复制 DESIGN.md">
          <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="${{iconColor}}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <rect x="9" y="9" width="13" height="13" rx="2"></rect>
            <path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"></path>
          </svg>
        </button>
        <a class="action-btn" href="${{sourceUrl}}" target="_blank" rel="noopener" title="查看源站">
          <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="${{iconColor}}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"></path>
            <polyline points="15 3 21 3 21 9"></polyline>
            <line x1="10" y1="14" x2="21" y2="3"></line>
          </svg>
        </a>
      </div>
    </div>

    <div class="div-line" style="background:${{actualBorder}}"></div>

    <div class="card-palette">${{swatchHtml}}</div>

    <div class="div-line" style="background:${{actualBorder}}"></div>

    <div class="card-preview">
      <div class="preview-heading-wrap">
        <div class="preview-heading" style="color:${{b.text}};font-weight:${{b.fw}};letter-spacing:${{b.ls}}">Display Text</div>
      </div>
      <div class="preview-body"    style="color:${{b.neutral}}">Body copy in brand style</div>
      <div class="preview-btns">
        <button class="preview-btn"
                style="background:${{b.accent}};color:${{b.btnC}};border-radius:${{b.btnR}};border:${{primBorder}};">Primary</button>
        <button class="preview-btn"
                style="background:${{b.surface}};color:${{b.text}};border-radius:${{b.btnR}};border:1px solid ${{actualBorder}};">Secondary</button>
      </div>
      <div class="mini-card"
           style="background:${{b.surface}};border:1px solid ${{actualBorder}};border-radius:${{b.boxR}};box-shadow:${{b.shadow}};">
        <div class="mini-card-title" style="color:${{b.text}}">Card Element</div>
        <div class="mini-card-body"  style="color:${{b.neutral}}">Surface · Border · Shadow</div>
      </div>
    </div>

    <div class="div-line" style="background:${{actualBorder}}"></div>

    <div class="card-footer" style="background:${{footBg}}">
      <div class="font-label" style="color:${{b.neutral}}" title="${{b.font}}">${{b.font}}</div>
      <div class="tags">${{catTagHtml}}${{tagsHtml}}</div>
    </div>

  </div>`;
}}

// ── BRAND LOOKUP MAP ─────────────────────────────────────────────────────────
const brandMap = {{}};
brands.forEach(b => {{ brandMap[b.id] = b; }});

// ── COPY DESIGN.MD ────────────────────────────────────────────────────────────
function copyDesignMd(id) {{
  const b = brandMap[id];
  if (!b) return;
  const text = b.md || '(DESIGN.md not available)';
  const toast = document.getElementById('toast');

  const show = (msg) => {{
    toast.textContent = msg;
    toast.classList.add('show');
    clearTimeout(toast._t);
    toast._t = setTimeout(() => toast.classList.remove('show'), 2200);
  }};

  if (navigator.clipboard && navigator.clipboard.writeText) {{
    navigator.clipboard.writeText(text).then(() => show('DESIGN.md \u5df2\u590d\u5236 \u2713')).catch(() => fallback(text, show));
  }} else {{
    fallback(text, show);
  }}
}}

function fallback(text, show) {{
  const ta = document.createElement('textarea');
  ta.value = text;
  ta.style.cssText = 'position:fixed;top:-9999px;left:-9999px;';
  document.body.appendChild(ta);
  ta.select();
  try {{ document.execCommand('copy'); show('DESIGN.md \u5df2\u590d\u5236 \u2713'); }}
  catch(e) {{ show('\u590d\u5236\u5931\u8d25\uff0c\u8bf7\u624b\u52a8\u590d\u5236'); }}
  document.body.removeChild(ta);
}}

// ── COPY BUTTON EVENT DELEGATION ─────────────────────────────────────────────
document.addEventListener('click', e => {{
  const btn = e.target.closest('.copy-btn');
  if (btn) {{ e.preventDefault(); copyDesignMd(btn.dataset.id); }}
}});

// ── INIT ──────────────────────────────────────────────────────────────────────
const grid  = document.getElementById('cardGrid');
const empty = document.getElementById('emptyState');
const badge = document.getElementById('countBadge');

brands.forEach(b => {{ grid.insertAdjacentHTML('beforeend', renderCard(b)); }});

// ── FILTER ────────────────────────────────────────────────────────────────────
document.querySelector('.filter-bar').addEventListener('click', e => {{
  const btn = e.target.closest('.filter-btn');
  if (!btn) return;
  document.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
  btn.classList.add('active');

  const f     = btn.dataset.filter;
  const cards = grid.querySelectorAll('.card');
  let visible = 0;

  cards.forEach(card => {{
    const show = f === 'all'
      || f === card.dataset.theme
      || f === card.dataset.group;
    card.classList.toggle('hidden', !show);
    if (show) visible++;
  }});

  badge.textContent = visible;
  empty.style.display = visible === 0 ? 'block' : 'none';
}});

// ── GITHUB STAR COUNT (live) ──────────────────────────────────────────────────
(function () {{
  const el = document.getElementById('ghStarCount');
  if (!el) return;
  fetch('https://api.github.com/repos/likeUMR/web-design-card-gallery', {{
    headers: {{ Accept: 'application/vnd.github.v3+json' }}
  }})
    .then(r => r.json())
    .then(d => {{
      if (typeof d.stargazers_count === 'number') {{
        el.textContent = d.stargazers_count >= 1000
          ? (d.stargazers_count / 1000).toFixed(1) + 'k'
          : d.stargazers_count;
      }}
    }})
    .catch(() => {{ el.textContent = '★'; }});
}})();
</script>

</body>
</html>"""


def main():
    brands = load_brands()
    if not brands:
        print("No brands loaded. Run extract_yaml.py first.")
        return

    html = build_html(brands)
    OUTPUT_HTML.write_text(html, encoding="utf-8")
    print(f"✅ Written → {OUTPUT_HTML}  ({len(html):,} chars, {len(brands)} brands)")


if __name__ == "__main__":
    main()
