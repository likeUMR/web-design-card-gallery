# coding=utf-8
"""
extract_yaml.py
───────────────
从每个 DESIGN.md 调用 LLM，提取结构化 YAML 设计 token 数据。
结果保存至 brand_data/<brand_id>.yaml，支持断点续传。

用法:
    python extract_yaml.py            # 提取全部
    python extract_yaml.py cursor     # 仅重新提取指定品牌
"""

import os
import sys
import time
import yaml
from pathlib import Path
from openai import OpenAI

# ── 配置：优先读取 config.py，回退到环境变量 ────────────────────────────────────
try:
    import config as _cfg
    BASE_URL = _cfg.LLM_BASE_URL
    MODEL    = _cfg.LLM_MODEL
    API_KEY  = _cfg.LLM_TOKEN
except ImportError:
    # config.py 不存在时回退到环境变量
    BASE_URL = os.getenv("LLM_BASE_URL", "")
    MODEL    = os.getenv("LLM_MODEL", "gemini-3-flash-preview")
    API_KEY  = os.getenv("LLM_TOKEN", "")

# Windows 控制台 UTF-8 输出
import sys as _sys
if hasattr(_sys.stdout, "reconfigure"):
    _sys.stdout.reconfigure(encoding="utf-8", errors="replace")

DESIGN_ROOT = Path(__file__).parent / "design-md-download"
OUTPUT_DIR  = Path(__file__).parent / "brand_data"
OUTPUT_DIR.mkdir(exist_ok=True)

client = OpenAI(api_key=API_KEY, base_url=BASE_URL)

# 品牌显示名称特殊映射
NAME_MAP = {
    "x.ai":        "xAI",
    "mistral.ai":  "Mistral AI",
    "linear.app":  "Linear",
    "opencode.ai": "OpenCode",
    "together.ai": "Together AI",
    "voltagent":   "VoltAgent",
    "runwayml":    "Runway ML",
    "spacex":      "SpaceX",
    "clickhouse":  "ClickHouse",
    "elevenlabs":  "ElevenLabs",
    "minimax":     "MiniMax",
    "mintlify":    "Mintlify",
    "hashicorp":   "HashiCorp",
    "posthog":     "PostHog",
    "supabase":    "Supabase",
    "webflow":     "Webflow",
    "nvidia":      "NVIDIA",
    "mongodb":     "MongoDB",
    "coinbase":    "Coinbase",
    "intercom":    "Intercom",
    "superhuman":  "Superhuman",
    "revolut":     "Revolut",
    "airbnb":      "Airbnb",
    "airtable":    "Airtable",
    "raycast":     "Raycast",
    "zapier":      "Zapier",
    "replicate":   "Replicate",
    "lamborghini": "Lamborghini",
    "ferrari":     "Ferrari",
    "renault":     "Renault",
    "lovable":     "Lovable",
    "composio":    "Composio",
    "sanity":      "Sanity",
    "sentry":      "Sentry",
    "resend":      "Resend",
    "framer":      "Framer",
    "figma":       "Figma",
    "notion":      "Notion",
    "spotify":     "Spotify",
    "pinterest":   "Pinterest",
    "warp":        "Warp",
    "ollama":      "Ollama",
    "expo":        "Expo",
    "miro":        "Miro",
    "wise":        "Wise",
    "kraken":      "Kraken",
    "uber":        "Uber",
    "stripe":      "Stripe",
    "vercel":      "Vercel",
    "cohere":      "Cohere",
    "tesla":       "Tesla",
    "apple":       "Apple",
    "ibm":         "IBM",
    "bmw":         "BMW",
    "cal":         "Cal.com",
    "claude":      "Claude",
    "clay":        "Clay",
}

# ── 提示词 ─────────────────────────────────────────────────────────────────────
SYSTEM_PROMPT = (
    "You are a precise design system analyzer. "
    "Extract design tokens from DESIGN.md files. "
    "Return ONLY valid YAML. No markdown fences. No inline comments. No explanation."
)

EXTRACT_PROMPT = """\
Analyze the DESIGN.md below. Return ONLY valid YAML with EXACTLY these fields:

id: {brand_id}
name: {brand_name}
category: <chinese category name, e.g. 开发工具/AI平台/电动汽车/金融科技/音乐流媒体>
filterGroup: <exactly one: AI | dev | fin | auto | saas | consumer>

theme: <light | dark | special>

bg: "<primary page background hex or rgba>"
text: "<primary text color>"
accent: "<primary CTA brand accent color>"
surface: "<secondary surface: card or button background>"
border: "<border/divider color, or 'none' if not used>"
neutral: "<secondary/muted text color>"
accent2: "<second notable accent color>"

colors:
  - "<bg>"
  - "<text>"
  - "<accent>"
  - "<surface>"
  - "<neutral>"
  - "<accent2>"

font: "<brand font name(s)>"
fontProxy: "<web-safe CSS font-family, e.g.: system-ui | 'Inter, sans-serif' | 'IBM Plex Sans, sans-serif' | 'Georgia, serif' | monospace>"
headingWeight: "<display heading font-weight: 300|400|500|600|700>"
headingSpacing: "<heading letter-spacing CSS value, e.g. -1.4px>"

btnRadius: "<button/badge border-radius, e.g. 9999px|8px|4px|0px>"
boxRadius: "<card/container/input border-radius>"
shadow: "<main card box-shadow CSS value, or none>"
btnColor: "<text color ON primary button; #000000 if accent is yellow/bright-green>"

tags:
  - "<abstract tag 1>"
  - "<abstract tag 2>"

RULES:
- theme: 'light' if page is mainly white/light (even if dark sections exist). 'dark' if mainly black/dark. 'special' only if brand color IS the page background (e.g. Sanity=red, Wise=green)
- filterGroup: AI=AI/ML companies; dev=dev tools/databases/platforms; fin=fintech/crypto/banking; auto=automotive/aerospace; saas=productivity/collab/CMS/email; consumer=consumer apps/media/social/travel
- tags must be ABSTRACT (philosophy, tone, methodology) - NOT color names, NOT radius values. 2 tags only.
- Tag vocab: 暖系工艺 冷工程美学 奢华克制 极简禅意 戏剧张力 开放社区感 三字体编排 可变字重 等宽字展示 衬线主导 超大字号冲击 无阴影平面 微边框阴影 大模糊氛围影 品牌色阴影 多层叠影 摄影主导 印刷排版感 终端原生 画廊美学 产品即设计
- fontProxy examples: for custom sans → "system-ui"; for Inter/Geist → "'Inter', sans-serif"; for IBM Plex → "'IBM Plex Sans', sans-serif"; for serif → "Georgia, serif"
- Output ONLY the YAML. No markdown. No commentary.

DESIGN.md:
{content}
"""


def clean_yaml(text: str) -> str:
    """Strip markdown fences from LLM response."""
    text = text.strip()
    lines = text.splitlines()
    if lines and lines[0].strip().startswith("```"):
        lines = lines[1:]
    if lines and lines[-1].strip() == "```":
        lines = lines[:-1]
    return "\n".join(lines).strip()


def extract_one(brand_id: str, md_path: Path) -> tuple:
    """Call LLM and extract YAML for one brand. Returns (dict, raw_yaml_str)."""
    content = md_path.read_text(encoding="utf-8")
    display_name = NAME_MAP.get(brand_id, brand_id.replace("-", " ").replace(".", " ").title())

    prompt = EXTRACT_PROMPT.format(
        brand_id=brand_id,
        brand_name=display_name,
        content=content,
    )

    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user",   "content": prompt},
        ],
        temperature=0.05,
    )

    raw = clean_yaml(response.choices[0].message.content)
    parsed = yaml.safe_load(raw)

    # Basic sanity check
    required = ["id", "name", "bg", "text", "accent", "theme", "filterGroup"]
    missing = [k for k in required if k not in parsed]
    if missing:
        raise ValueError(f"Missing required fields: {missing}")

    return parsed, raw


def extract_all(force_ids: list = None):
    """Extract YAML for all brands. Skip already-done unless forced."""
    brand_dirs = sorted(
        d for d in DESIGN_ROOT.iterdir()
        if d.is_dir() and (d / "DESIGN.md").exists()
    )
    total = len(brand_dirs)
    print(f"Found {total} brands in {DESIGN_ROOT}\n")

    results = []
    errors  = []

    for i, brand_dir in enumerate(brand_dirs, 1):
        brand_id  = brand_dir.name
        yaml_path = OUTPUT_DIR / f"{brand_id}.yaml"
        forced    = force_ids and brand_id in force_ids

        # Resume: skip if done
        if yaml_path.exists() and not forced:
            print(f"[{i:02d}/{total}] SKIP  {brand_id}")
            try:
                with open(yaml_path, encoding="utf-8") as f:
                    results.append(yaml.safe_load(f))
            except Exception as e:
                print(f"         ↳ could not parse cached YAML: {e}")
            continue

        print(f"[{i:02d}/{total}] FETCH {brand_id} ...", end="", flush=True)

        try:
            parsed, raw = extract_one(brand_id, brand_dir / "DESIGN.md")
            yaml_path.write_text(raw, encoding="utf-8")
            results.append(parsed)
            print(f"  ✓  theme:{parsed.get('theme','?')}  accent:{parsed.get('accent','?')}")
        except Exception as e:
            errors.append(brand_id)
            print(f"  ✗  {e}")
            err_path = OUTPUT_DIR / f"{brand_id}.error.txt"
            err_path.write_text(str(e), encoding="utf-8")

        time.sleep(0.35)  # polite rate limiting

    print(f"\n{'='*50}")
    print(f"✅ Extracted: {len(results)}/{total}")
    if errors:
        print(f"❌ Errors ({len(errors)}): {', '.join(errors)}")
    return results


if __name__ == "__main__":
    # Optional: pass brand IDs to force re-extract
    force = sys.argv[1:] if len(sys.argv) > 1 else None
    if force:
        print(f"Force re-extracting: {force}\n")
    extract_all(force_ids=force)
