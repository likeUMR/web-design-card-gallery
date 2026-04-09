# coding=utf-8
"""
run_pipeline.py
───────────────
一键执行完整流程：
  1. extract_yaml.py  → 从 DESIGN.md 提取品牌 YAML（LLM，支持断点续传）
  2. generate_gallery.py → 从 YAML 生成 card-gallery.html

用法:
    python run_pipeline.py          # 全量（跳过已提取）
    python run_pipeline.py --force  # 强制重新提取所有品牌
"""

import sys
import time
import importlib
from pathlib import Path

def section(title: str):
    print(f"\n{'='*52}")
    print(f"  {title}")
    print(f"{'='*52}\n")

def run():
    force = "--force" in sys.argv

    # ── Step 1: Extract YAML ──────────────────────────────────────────────────
    section("Step 1 / 2 — Extract YAML from DESIGN.md (via LLM)")

    import extract_yaml
    if force:
        # Pass all brand IDs to force re-extraction
        brand_dirs = sorted(
            d.name for d in (Path(__file__).parent / "design-md-download").iterdir()
            if d.is_dir() and (d / "DESIGN.md").exists()
        )
        print(f"Force mode: re-extracting {len(brand_dirs)} brands\n")
        extract_yaml.extract_all(force_ids=brand_dirs)
    else:
        extract_yaml.extract_all()

    # ── Step 2: Generate HTML ─────────────────────────────────────────────────
    section("Step 2 / 2 — Generate card-gallery.html")

    import generate_gallery
    generate_gallery.main()

    section("Done ✅")
    output = Path(__file__).parent / "card-gallery.html"
    print(f"  Open: {output}\n")

if __name__ == "__main__":
    t0 = time.time()
    run()
    elapsed = time.time() - t0
    print(f"Total time: {elapsed:.1f}s")
