#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Daily arXiv digest for the awsome_depth_noise research topics.

Queries the arXiv API (export.arxiv.org) with the keyword topics defined in
scripts/config.json, deduplicates against daily_updates/.seen.json, and writes
one markdown digest per day into daily_updates/YYYY-MM-DD.md. Also maintains
the index at daily_updates/README.md.

Notes
-----
* arXiv API etiquette: at least 3 s between requests (config request_delay_seconds).
* Digests are UN-curated candidates. A human (or the assistant) should verify
  entries and promote the good ones into docs/papers.md with links checked.

Usage
-----
    python scripts/arxiv_daily_search.py                 # lookback days from config
    python scripts/arxiv_daily_search.py --days 7        # look back 7 days
    python scripts/arxiv_daily_search.py --dry-run       # print, write nothing
    python scripts/arxiv_daily_search.py --no-write      # run queries, print summary
"""

import argparse
import html
import json
import re
import sys
import time
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CONFIG_PATH = Path(__file__).resolve().parent / "config.json"
DIGEST_DIR = ROOT / "daily_updates"
SEEN_PATH = DIGEST_DIR / ".seen.json"
INDEX_PATH = DIGEST_DIR / "README.md"
ATOM = "{http://www.w3.org/2005/Atom}"
API = "https://export.arxiv.org/api/query"
USER_AGENT = "awsome_depth_noise-daily-search/1.0 (daily digest bot)"


def log(msg: str) -> None:
    print(f"[{datetime.now(timezone.utc):%Y-%m-%d %H:%M:%S}Z] {msg}", flush=True)


def load_config() -> dict:
    with open(CONFIG_PATH, encoding="utf-8") as f:
        return json.load(f)


def load_seen() -> set:
    if SEEN_PATH.exists():
        return set(json.loads(SEEN_PATH.read_text(encoding="utf-8")))
    return set()


def save_seen(seen: set) -> None:
    SEEN_PATH.write_text(
        json.dumps(sorted(seen), ensure_ascii=False, indent=1) + "\n", encoding="utf-8"
    )


def api_query(search_query: str, max_results: int, delay: float, max_retries: int = 2) -> list[dict]:
    params = {
        "search_query": search_query,
        "start": 0,
        "max_results": max_results,
        "sortBy": "submittedDate",
        "sortOrder": "descending",
    }
    url = f"{API}?{urllib.parse.urlencode(params)}"
    for attempt in range(max_retries + 1):
        time.sleep(delay)  # arXiv API etiquette: space out requests *before* sending
        try:
            req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
            with urllib.request.urlopen(req, timeout=60) as resp:
                raw = resp.read().decode("utf-8", errors="replace")
            return parse_feed(raw)
        except urllib.error.HTTPError as e:
            if e.code == 429 and attempt < max_retries:
                log(
                    f"    ! HTTP 429 rate-limited, retrying in 30 s "
                    f"(attempt {attempt + 1}/{max_retries})"
                )
                time.sleep(30)
                continue
            raise
    return []  # unreachable; kept for clarity


def parse_feed(raw: str) -> list[dict]:
    entries = []
    try:
        root = ET.fromstring(raw)
    except ET.ParseError as e:
        log(f"  ! XML parse error: {e}")
        return entries
    for entry in root.findall(f"{ATOM}entry"):
        eid = entry.findtext(f"{ATOM}id") or ""
        m = re.search(r"abs/([^v/]+)", eid)
        arxiv_id = m.group(1) if m else eid.rsplit("/", 1)[-1]
        title = clean(entry.findtext(f"{ATOM}title") or "")
        summary = clean(entry.findtext(f"{ATOM}summary") or "")
        published = (entry.findtext(f"{ATOM}published") or "")[:10]
        authors = [a.findtext(f"{ATOM}name") or "" for a in entry.findall(f"{ATOM}author")]
        cats = [c.get("term", "") for c in entry.findall(f"{ATOM}category")]
        if not title or not arxiv_id:
            continue
        entries.append(
            {
                "id": arxiv_id,
                "title": title,
                "summary": summary,
                "published": published,
                "authors": [a for a in authors if a],
                "categories": cats,
            }
        )
    return entries


def clean(text: str) -> str:
    text = html.unescape(text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def truncate(text: str, max_chars: int) -> str:
    if len(text) <= max_chars:
        return text
    cut = text[: max_chars - 1]
    return cut.rsplit(" ", 1)[0] + "…"


def authors_str(authors: list[str], limit: int = 5) -> str:
    if not authors:
        return "n/a"
    shown = ", ".join(authors[:limit])
    if len(authors) > limit:
        shown += f" et al. (共 {len(authors)} 人)"
    return shown


def entry_md(idx: int, e: dict, abstract_max: int) -> str:
    cats = ", ".join(e["categories"]) or "n/a"
    return (
        f"### {idx}. {e['title']}\n"
        f"- **arXiv**: [{e['id']}](https://arxiv.org/abs/{e['id']}) · "
        f"**类别**: {cats} · **提交**: {e['published']}\n"
        f"- **作者**: {authors_str(e['authors'])}\n"
        f"- **摘要**: {truncate(e['summary'], abstract_max)}\n"
    )


def build_index(digest_files: list[Path]) -> str:
    lines = [
        "# 每日 arXiv 检索摘要（Daily Digests）",
        "",
        "> 由 GitHub Actions 每日自动生成（`scripts/arxiv_daily_search.py`）。",
        "> **内容为未筛选候选**：请人工（或让助手）核对条目后，将高质量论文提升到",
        "> [docs/papers.md](../docs/papers.md)（补全 venue/链接），并在",
        "> [docs/research_notes.md](../docs/research_notes.md) §5 检索日志中追加记录。",
        "",
        "**上次更新**: " + datetime.now(timezone.utc).strftime("%Y-%m-%d"),
        "",
        "## 摘要列表（新 → 旧）",
        "",
    ]
    for p in sorted(digest_files, reverse=True):
        lines.append(f"- [{p.stem}]({p.name})")
    if not digest_files:
        lines.append("_（暂无摘要，首次自动运行后生成）_")
    lines.append("")
    return "\n".join(lines)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--days", type=int, default=None, help="lookback days (default: config)")
    ap.add_argument("--dry-run", action="store_true", help="print results, write nothing")
    ap.add_argument("--no-write", action="store_true", help="run queries, print summary only")
    args = ap.parse_args()

    cfg = load_config()
    lookback = args.days if args.days is not None else cfg.get("lookback_days", 2)
    max_results = cfg.get("max_results_per_query", 25)
    delay = cfg.get("request_delay_seconds", 3.0)
    abstract_max = cfg.get("abstract_max_chars", 600)
    topics = cfg.get("topics", [])

    if not topics:
        log("ERROR: no topics in config")
        return 1

    cutoff = datetime.now(timezone.utc).date() - timedelta(days=lookback)
    seen = load_seen()
    new_entries: list[dict] = []

    log(f"lookback={lookback}d cutoff={cutoff} topics={len(topics)} seen={len(seen)}")
    for topic in topics:
        name = topic.get("name", "?")
        for q in topic.get("queries", []):
            log(f"  query [{name}]: {q}")
            try:
                entries = api_query(q, max_results, delay)
            except Exception as e:  # noqa: BLE001
                log(f"    ! query failed: {e}")
                continue
            for e in entries:
                try:
                    pub_date = datetime.strptime(e["published"], "%Y-%m-%d").date()
                except ValueError:
                    continue
                if pub_date < cutoff:
                    continue
                if e["id"] in seen:
                    continue
                seen.add(e["id"])
                new_entries.append(e)
            log(f"    -> {len(entries)} returned")

    # de-dup by id (in case the same paper matched multiple queries)
    by_id: dict[str, dict] = {}
    for e in new_entries:
        by_id.setdefault(e["id"], e)
    new_entries = sorted(by_id.values(), key=lambda e: e["published"], reverse=True)

    log(f"new papers: {len(new_entries)}")
    if args.dry_run or args.no_write:
        for e in new_entries:
            print(entry_md(new_entries.index(e) + 1, e, abstract_max))
        if args.dry_run:
            return 0

    if not new_entries:
        log("no new papers; nothing to write")
        return 0

    DIGEST_DIR.mkdir(parents=True, exist_ok=True)
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    digest_path = DIGEST_DIR / f"{today}.md"

    header = [
        f"# arXiv 每日检索 Digest — {today}",
        "",
        "> 自动生成（`scripts/arxiv_daily_search.py`）· **未经人工筛选**。",
        "> 候选入库流程：核对链接/venue → 提升到 `docs/papers.md` → 更新检索日志。",
        "",
        f"## 新增候选（{len(new_entries)} 篇）",
        "",
    ]
    body = [entry_md(i + 1, e, abstract_max) for i, e in enumerate(new_entries)]
    queries = []
    for t in topics:
        queries.extend(t.get("queries", []))
    footer = [
        "## 本次检索查询",
        "",
        "```",
        *queries,
        "```",
        "",
    ]
    digest_path.write_text("\n".join(header + body + footer), encoding="utf-8")
    log(f"wrote {digest_path}")

    save_seen(seen)
    log(f"saved seen registry ({len(seen)} ids)")

    digest_files = sorted(DIGEST_DIR.glob("20*.md"))
    INDEX_PATH.write_text(build_index(digest_files), encoding="utf-8")
    log(f"updated {INDEX_PATH} ({len(digest_files)} digests)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
