#!/usr/bin/env python3
"""
从 getdesign.md 批量下载各品牌的 DESIGN.md。

用法:
  python download_all_design_md.py              # 抓取首页解析 slug，下载到 ./design-md-download/
  python download_all_design_md.py -o out_dir
  python download_all_design_md.py --slugs-json counts.json  # 使用 JSON 中的 counts 键作为 slug 列表

说明:
  - 直链格式: https://getdesign.md/design-md/<slug>/DESIGN.md
  - 站点对无 User-Agent 的请求可能返回 403，脚本已模拟常见浏览器。
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

BASE = "https://getdesign.md"
DESIGN_URL = BASE + "/design-md/{slug}/DESIGN.md"
INDEX_URL = BASE + "/"

DEFAULT_UA = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/146.0.0.0 Safari/537.36"
)


def fetch_bytes(url: str, *, timeout: float = 60) -> bytes:
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": DEFAULT_UA,
            "Accept": "*/*",
            "Accept-Language": "en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7",
        },
    )
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return resp.read()


def slugs_from_homepage() -> list[str]:
    html = fetch_bytes(INDEX_URL).decode("utf-8", errors="replace")
    slugs: set[str] = set()
    # 站点常见为相对链接：href="/minimax/design-md"
    for m in re.findall(r'href=["\']/([^/"\']+)/design-md["\']', html, re.IGNORECASE):
        slugs.add(m)
    # 兼容绝对地址
    for m in re.findall(
        r"https://getdesign\.md/([^/\"'\s>]+)/design-md",
        html,
        flags=re.IGNORECASE,
    ):
        slugs.add(m.strip("/"))
    if not slugs:
        raise RuntimeError("首页未解析到任何 /design-md 链接，网站结构可能已变更。")
    return slugs


def slugs_from_counts_json(path: Path) -> list[str]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict) or "counts" not in data:
        raise ValueError("JSON 需包含顶层键 counts（对象），键名为 slug。")
    counts = data["counts"]
    if not isinstance(counts, dict):
        raise ValueError("counts 必须是对象。")
    return sorted(counts.keys())


def safe_dir_name(slug: str) -> str:
    """避免路径中的 '.' 等在 Windows 上引起困惑；保留可读性。"""
    return slug.replace("/", "_")


def download_one(slug: str, dest_dir: Path) -> tuple[str, str | None]:
    """
    返回 (slug, None) 成功；(slug, error_message) 失败。
    """
    url = DESIGN_URL.format(slug=slug)
    sub = dest_dir / safe_dir_name(slug)
    sub.mkdir(parents=True, exist_ok=True)
    out = sub / "DESIGN.md"
    try:
        body = fetch_bytes(url)
    except urllib.error.HTTPError as e:
        return slug, f"HTTP {e.code} {e.reason}"
    except urllib.error.URLError as e:
        return slug, f"网络错误: {e.reason}"
    except TimeoutError:
        return slug, "请求超时"
    out.write_bytes(body)
    return slug, None


def main() -> int:
    parser = argparse.ArgumentParser(description="批量下载 getdesign.md 的 DESIGN.md")
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        default=Path("design-md-download"),
        help="输出目录（默认: design-md-download）",
    )
    parser.add_argument(
        "--slugs-json",
        type=Path,
        default=None,
        help="含 counts 的 JSON 文件路径；不提供则从首页解析 slug",
    )
    parser.add_argument(
        "--delay",
        type=float,
        default=0.35,
        help="每次请求间隔秒数，降低对源站压力（默认 0.35）",
    )
    args = parser.parse_args()

    if args.slugs_json:
        slugs = slugs_from_counts_json(args.slugs_json)
    else:
        slugs = slugs_from_homepage()

    dest: Path = args.output
    dest.mkdir(parents=True, exist_ok=True)

    errors: list[tuple[str, str]] = []
    for i, slug in enumerate(slugs):
        slug, err = download_one(slug, dest)
        if err:
            errors.append((slug, err))
            print(f"[FAIL] {slug}: {err}", file=sys.stderr)
        else:
            print(f"[ok]   {slug}")
        if i + 1 < len(slugs) and args.delay > 0:
            time.sleep(args.delay)

    if errors:
        print(f"\n完成: 成功 {len(slugs) - len(errors)}/{len(slugs)}，失败 {len(errors)}", file=sys.stderr)
        return 1
    print(f"\n完成: 共 {len(slugs)} 个 DESIGN.md → {dest.resolve()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
