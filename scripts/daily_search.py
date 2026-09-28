#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Daily literature digest for the awsome_depth_noise research topics.

Multi-source design (v2, 2026-09-28)
------------------------------------
1. **arXiv RSS** (`https://rss.arxiv.org/rss/<category>`) — one request per
   category per day returns the *full* daily announcement; candidate filtering
   happens locally with keywords. This replaced the keyword-query-only design,
   which broke silently when the arXiv API started returning HTTP 429 for our
   IPs (a week of "0 new papers" that was really "0 successful queries").
2. **OpenAlex** (`https://api.openalex.org`) — keyword search restricted to the
   lookback window, using the polite pool via `mailto`. Backfills days the RSS
   feed no longer carries and covers unrelated categories.
3. **arXiv API keyword queries** — retained for reference but **disabled by
   default** (config `sources.arxiv_api.enabled`).

Health / fail-loud behaviour
----------------------------
Every source reports success or failure. If **all enabled sources fail** the
script exits with code 2 (GitHub Actions run turns red instead of silently
reporting "0 new papers"). Partial failures are recorded in
`daily_updates/.health.json` and flagged at the top of the digest.

Usage
-----
    python scripts/daily_search.py                 # use config defaults
    python scripts/daily_search.py --days 7        # override lookback window
    python scripts/daily_search.py --dry-run       # print candidates, write nothing
    python scripts/daily_search.py --source rss    # only arXiv RSS
"""

import argparse
import html
import json
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta, timezone
from email.utils import parsedate_to_datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CONFIG_PATH = Path(__file__).resolve().parent / "config.json"
DIGEST_DIR = ROOT / "daily_updates"
SEEN_PATH = DIGEST_DIR / ".seen.json"
HEALTH_PATH = DIGEST_DIR / ".health.json"
INDEX_PATH = DIGEST_DIR / "README.md"

ARXIV_API = "https://export.arxiv.org/api/query"
RSS_URL = "https://rss.arxiv.org/rss/{category}"
OPENALEX_API = "https://api.openalex.org/works"
USER_AGENT = "awsome_depth_noise-daily-digest/2.0 (+https://github.com/mingqian0850/awsome_depth_noise)"
ATOM = "{http://www.w3.org/2005/Atom}"
ARXIV_NS = "{http://arxiv.org/schemas/atom}"
DC_NS = "{http://purl.org/dc/elements/1.1/}"


def log(msg: str) -> None:
    print(f"[{datetime.now(timezone.utc):%Y-%m-%d %H:%M:%S}Z] {msg}", flush=True)


def http_get(url: str, timeout: int = 60) -> str:
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return resp.read().decode("utf-8", errors="replace")


def clean(text: str) -> str:
    return re.sub(r"\s+", " ", html.unescape(text or "")).strip()


def truncate(text: str, max_chars: int) -> str:
    if len(text) <= max_chars:
        return text
    return text[: max_chars - 1].rsplit(" ", 1)[0] + "…"


def authors_str(authors: list, limit: int = 5) -> str:
    if not authors:
        return "n/a"
    shown = ", ".join(authors[:limit])
    return shown + (f" et al. (共 {len(authors)} 人)" if len(authors) > limit else "")


def parse_date(value: str) -> str:
    """Normalise various date strings to YYYY-MM-DD ('' when unparseable)."""
    if not value:
        return ""
    value = value.strip()
    if re.match(r"^\d{4}-\d{2}-\d{2}", value):
        return value[:10]
    try:  # RFC 822 (RSS pubDate)
        return parsedate_to_datetime(value).strftime("%Y-%m-%d")
    except Exception:  # noqa: BLE001
        return ""


# --------------------------------------------------------------------------- #
# Source 1: arXiv RSS (full daily announcement, filtered locally)
# --------------------------------------------------------------------------- #
def fetch_rss(categories: list, include_types: list, delay: float = 1.0) -> list:
    entries = []
    for i, category in enumerate(categories):
        if i:
            time.sleep(delay)  # be polite even on the RSS endpoint
        url = RSS_URL.format(category=category)
        raw = http_get(url)
        entries.extend(parse_rss(raw, category, include_types))
    return entries


def parse_rss(raw: str, category: str, include_types: list) -> list:
    out = []
    try:
        root = ET.fromstring(raw)
    except ET.ParseError as e:
        log(f"  ! RSS parse error ({category}): {e}")
        return out
    for item in root.iter("item"):
        announce = (item.findtext(f"{ARXIV_NS}announce_type") or "new").strip()
        if include_types and announce not in include_types:
            continue
        title = clean(item.findtext("title"))
        link = (item.findtext("link") or "").strip()
        description = item.findtext("description") or ""
        # description looks like: "arXiv:2609.12345v1 Announce Type: new \nAbstract: ..."
        m = re.search(r"arXiv:(\d{4}\.\d{4,5})", description) or re.search(
            r"abs/(\d{4}\.\d{4,5})", link
        )
        arxiv_id = m.group(1) if m else ""
        abstract = re.sub(r"^.*?Abstract:\s*", "", clean(description), flags=re.S)
        creators = clean(item.findtext(f"{DC_NS}creator"))
        authors = [a.strip() for a in creators.split(",") if a.strip()]
        if not arxiv_id or not title:
            continue
        out.append(
            {
                "id": arxiv_id,
                "title": title,
                "summary": abstract,
                "published": parse_date(item.findtext("pubDate")),
                "authors": authors,
                "categories": [category],
                "source": "arxiv-rss",
                "url": f"https://arxiv.org/abs/{arxiv_id}",
            }
        )
    return out


# --------------------------------------------------------------------------- #
# Source 2: OpenAlex (keyword search within the lookback window)
# --------------------------------------------------------------------------- #
def fetch_openalex(
    queries: list, mailto: str, lookback_days: int, max_results: int, delay: float = 1.0
) -> list:
    entries = []
    since = (datetime.now(timezone.utc).date() - timedelta(days=lookback_days)).isoformat()
    for i, query in enumerate(queries):
        if i:
            time.sleep(delay)
        params = {
            "filter": f"from_publication_date:{since},title_and_abstract.search:{query}",
            "per-page": max_results,
            "sort": "publication_date:desc",
            "mailto": mailto,
        }
        raw = http_get(f"{OPENALEX_API}?{urllib.parse.urlencode(params)}")
        entries.extend(parse_openalex(raw, query))
    return entries


def parse_openalex(raw: str, query: str) -> list:
    out = []
    try:
        data = json.loads(raw)
    except json.JSONDecodeError as e:
        log(f"  ! OpenAlex JSON error ({query}): {e}")
        return out
    for w in data.get("results", []):
        title = clean(w.get("title") or w.get("display_name") or "")
        if not title:
            continue
        arxiv_id = ""
        ids = w.get("ids") or {}
        for key, value in ids.items():
            if "arxiv" in str(key).lower() and value:
                m = re.search(r"(\d{4}\.\d{4,5})", str(value))
                if m:
                    arxiv_id = m.group(1)
                    break
        if not arxiv_id:
            for loc in w.get("locations") or []:
                m = re.search(r"arxiv\.org/abs/(\d{4}\.\d{4,5})", str(loc.get("landing_page_url") or ""))
                if m:
                    arxiv_id = m.group(1)
                    break
        url = f"https://arxiv.org/abs/{arxiv_id}" if arxiv_id else (w.get("doi") or "")
        out.append(
            {
                "id": arxiv_id or f"openalex:{w.get('id', '').rsplit('/', 1)[-1]}",
                "title": title,
                "summary": clean(deinvert_abstract(w.get("abstract_inverted_index"))),
                "published": parse_date(w.get("publication_date") or ""),
                "authors": [
                    clean(a.get("author", {}).get("display_name", ""))
                    for a in (w.get("authorships") or [])
                    if a.get("author")
                ],
                "categories": [f"openalex:{query}"],
                "source": "openalex",
                "url": url,
            }
        )
    return out


def deinvert_abstract(inverted: dict) -> str:
    """Rebuild plain text from OpenAlex's abstract_inverted_index."""
    if not inverted:
        return ""
    positions = []
    for word, idxs in inverted.items():
        for i in idxs:
            positions.append((i, word))
    positions.sort()
    return " ".join(word for _, word in positions)


# --------------------------------------------------------------------------- #
# Source 3: arXiv API keyword queries (disabled by default — 429-prone)
# --------------------------------------------------------------------------- #
def fetch_arxiv_api(queries: list, max_results: int, delay: float, max_retries: int = 2) -> list:
    entries = []
    for query in queries:
        params = {
            "search_query": query,
            "start": 0,
            "max_results": max_results,
            "sortBy": "submittedDate",
            "sortOrder": "descending",
        }
        url = f"{ARXIV_API}?{urllib.parse.urlencode(params)}"
        for attempt in range(max_retries + 1):
            time.sleep(delay)  # arXiv API etiquette: space requests *before* sending
            try:
                raw = http_get(url)
                entries.extend(parse_atom(raw))
                break
            except urllib.error.HTTPError as e:
                if e.code == 429 and attempt < max_retries:
                    log(f"    ! HTTP 429, retry in 30 s ({attempt + 1}/{max_retries})")
                    time.sleep(30)
                    continue
                raise
    return entries


def parse_atom(raw: str) -> list:
    out = []
    try:
        root = ET.fromstring(raw)
    except ET.ParseError as e:
        log(f"  ! Atom parse error: {e}")
        return out
    for entry in root.findall(f"{ATOM}entry"):
        eid = entry.findtext(f"{ATOM}id") or ""
        m = re.search(r"abs/([^v/]+)", eid)
        out.append(
            {
                "id": m.group(1) if m else eid,
                "title": clean(entry.findtext(f"{ATOM}title")),
                "summary": clean(entry.findtext(f"{ATOM}summary")),
                "published": (entry.findtext(f"{ATOM}published") or "")[:10],
                "authors": [clean(a.findtext(f"{ATOM}name")) for a in entry.findall(f"{ATOM}author")],
                "categories": [c.get("term", "") for c in entry.findall(f"{ATOM}category")],
                "source": "arxiv-api",
                "url": f"https://arxiv.org/abs/{m.group(1)}" if m else eid,
            }
        )
    return out


# --------------------------------------------------------------------------- #
# Local keyword filtering (used for the full-feed RSS source and OpenAlex)
# --------------------------------------------------------------------------- #
def keyword_match(entry: dict, filt: dict) -> bool:
    """Two-tier relevance filter.

    Tier A: a *core* topic (depth camera / structured light / ToF / sim2real ...)
            plus any modifier (noise / simulation / calibration ...), anywhere.
    Tier B: a *broad* topic (point cloud, LiDAR, depth estimation ...) plus a
            *strong* modifier (noise, denoising, multipath, fidelity ...) that
            must appear in the **title** — this keeps the precision usable when
            scanning the full arXiv RSS feed.

    Recall is protected by the targeted OpenAlex / arXiv-API keyword queries,
    which do not go through this filter.
    """
    text = f"{entry['title']} {entry['summary']}".lower()
    title = entry["title"].lower()
    core = any(t.lower() in text for t in filt.get("core_topics", []))
    broad = any(t.lower() in text for t in filt.get("broad_topics", []))
    modifier = any(m.lower() in text for m in filt.get("modifiers", []))
    strong_in_title = any(m.lower() in title for m in filt.get("strong_modifiers", []))
    return (core and modifier) or (broad and strong_in_title)


# --------------------------------------------------------------------------- #
# Reporting helpers
# --------------------------------------------------------------------------- #
def entry_md(idx: int, e: dict, abstract_max: int) -> str:
    src = e.get("source", "?")
    cats = ", ".join([c for c in e["categories"] if c]) or "n/a"
    link = e.get("url") or f"https://arxiv.org/abs/{e['id']}"
    return (
        f"### {idx}. {e['title']}\n"
        f"- **来源**: {src} · **标识**: [{e['id']}]({link}) · **类别**: {cats} · "
        f"**日期**: {e['published'] or 'n/a'}\n"
        f"- **作者**: {authors_str(e['authors'])}\n"
        f"- **摘要**: {truncate(e['summary'], abstract_max) or '（无摘要）'}\n"
    )


def build_index(digest_files: list) -> str:
    lines = [
        "# 每日 arXiv 检索摘要（Daily Digests）",
        "",
        "> 由 GitHub Actions 每日自动生成（`scripts/daily_search.py`）。",
        "> **内容为未筛选候选**：请人工（或让助手）核对条目后，将高质量论文提升到",
        "> [docs/papers.md](../docs/papers.md)（补全 venue/链接），并在",
        "> [docs/research_notes.md](../docs/research_notes.md) §5 检索日志中追加记录。",
        "",
        f"**上次更新**: {datetime.now(timezone.utc):%Y-%m-%d}",
        "",
        "## 摘要列表（新 → 旧）",
        "",
    ]
    lines += [f"- [{p.stem}]({p.name})" for p in sorted(digest_files, reverse=True)]
    if not digest_files:
        lines.append("_（暂无摘要，首次自动运行后生成）_")
    lines.append("")
    return "\n".join(lines)


def record_health(status: dict) -> None:
    history = []
    if HEALTH_PATH.exists():
        try:
            history = json.loads(HEALTH_PATH.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            history = []
    history.append(status)
    HEALTH_PATH.write_text(
        json.dumps(history[-30:], ensure_ascii=False, indent=1) + "\n", encoding="utf-8"
    )


# --------------------------------------------------------------------------- #
def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--days", type=int, default=None, help="lookback days (default: config)")
    ap.add_argument("--dry-run", action="store_true", help="print candidates, write nothing")
    ap.add_argument("--no-write", action="store_true", help="run sources, print summary only")
    ap.add_argument("--source", default="", help="comma list: rss,openalex,arxiv-api")
    args = ap.parse_args()

    cfg = json.loads(CONFIG_PATH.read_text(encoding="utf-8"))
    lookback = args.days if args.days is not None else cfg.get("lookback_days", 3)
    abstract_max = cfg.get("abstract_max_chars", 600)
    filt = cfg.get("filter", {})
    sources_cfg = cfg.get("sources", {})
    aliases = {"rss": "arxiv-rss", "arxivrss": "arxiv-rss", "api": "arxiv-api", "oa": "openalex"}
    want = {aliases.get(s.strip().lower(), s.strip().lower()) for s in args.source.split(",") if s.strip()}

    cutoff = (datetime.now(timezone.utc).date() - timedelta(days=lookback)).isoformat()
    seen = set(json.loads(SEEN_PATH.read_text(encoding="utf-8"))) if SEEN_PATH.exists() else set()

    collected: list = []
    health: dict = {"at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
                    "lookback_days": lookback, "sources": {}}

    def run_source(name: str, enabled: bool, fn) -> None:
        if not enabled or (want and name not in want):
            health["sources"][name] = {"enabled": False}
            return
        try:
            got = fn()
            health["sources"][name] = {"enabled": True, "ok": True, "fetched": len(got)}
            collected.extend(got)
            log(f"  [{name}] fetched {len(got)} entries")
        except Exception as e:  # noqa: BLE001
            health["sources"][name] = {"enabled": True, "ok": False, "error": f"{type(e).__name__}: {e}"}
            log(f"  [{name}] FAILED: {type(e).__name__}: {e}")

    log(f"lookback={lookback}d cutoff={cutoff} seen={len(seen)}")

    rss_cfg = sources_cfg.get("arxiv_rss", {})
    run_source(
        "arxiv-rss",
        rss_cfg.get("enabled", True),
        lambda: fetch_rss(rss_cfg.get("categories", ["cs.CV"]),
                          rss_cfg.get("include_announce_types", ["new"])),
    )
    oa_cfg = sources_cfg.get("openalex", {})
    run_source(
        "openalex",
        oa_cfg.get("enabled", True),
        lambda: fetch_openalex(
            oa_cfg.get("queries", []), oa_cfg.get("mailto", ""), lookback,
            oa_cfg.get("max_results_per_query", 25),
        ),
    )
    api_cfg = sources_cfg.get("arxiv_api", {})
    run_source(
        "arxiv-api",
        api_cfg.get("enabled", False),
        lambda: fetch_arxiv_api(
            api_cfg.get("queries", []), api_cfg.get("max_results_per_query", 25),
            api_cfg.get("request_delay_seconds", 4),
        ),
    )

    enabled = [k for k, v in health["sources"].items() if v.get("enabled")]
    ok = [k for k in enabled if health["sources"][k].get("ok")]
    health["enabled_sources"] = enabled
    health["ok_sources"] = ok

    if not enabled:
        health["result"] = "no-sources-enabled"
        record_health(health)
        log("::error::No data source is enabled (check scripts/config.json)")
        return 2

    if not ok:  # fail loud instead of silently reporting zero
        health["result"] = "all-sources-failed"
        record_health(health)
        log("::error::ALL enabled sources failed — nothing was searched (this is NOT 'no new papers')")
        return 2

    # filter + dedupe (arXiv API queries are already targeted; RSS/OpenAlex are not)
    kept = [e for e in collected if e["source"] == "arxiv-api" or keyword_match(e, filt)]

    fresh: dict = {}
    seen_titles: set = set()
    for e in kept:
        if e["published"] and e["published"] < cutoff:
            continue
        title_key = re.sub(r"[^a-z0-9]+", " ", e["title"].lower()).strip()
        if e["id"] in seen or e["id"] in fresh or title_key in seen_titles:
            continue
        seen_titles.add(title_key)
        fresh[e["id"]] = e
    new_entries = sorted(fresh.values(), key=lambda e: e["published"], reverse=True)

    log(f"collected={len(collected)} after-filter={len(new_entries)} "
        f"(sources ok: {', '.join(ok) or 'none'})")
    health["result"] = "ok" if ok else "partial"
    health["candidates"] = len(new_entries)

    if args.dry_run or args.no_write:
        for i, e in enumerate(new_entries):
            print(entry_md(i + 1, e, abstract_max))
        if args.dry_run:
            return 0

    if not new_entries:
        record_health(health)
        log("no new candidates; nothing to write")
        return 0

    DIGEST_DIR.mkdir(parents=True, exist_ok=True)
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    degraded = len(ok) < len(enabled)
    header = [
        f"# 每日文献 Digest — {today}",
        "",
        "> 自动生成（`scripts/daily_search.py`）· **未经人工筛选**。",
        "> 数据源：arXiv RSS（全量日志 + 本地关键词过滤）、OpenAlex（关键词 + 日期窗口）。",
    ]
    if degraded:
        header.append(f"> ⚠️ **数据源降级**：{', '.join(enabled)} 中仅 {', '.join(ok)} 成功。")
    header += [
        "> 候选入库流程：核对链接/venue → 提升到 `docs/papers.md` → 更新检索日志。",
        "",
        f"## 新增候选（{len(new_entries)} 篇）",
        "",
    ]
    body = [entry_md(i + 1, e, abstract_max) for i, e in enumerate(new_entries)]
    footer = [
        "## 本次运行摘要",
        "",
        "```",
        f"lookback_days: {lookback}",
        *[f"{k}: {json.dumps(v, ensure_ascii=False)}" for k, v in health["sources"].items()],
        "```",
        "",
    ]
    digest_path = DIGEST_DIR / f"{today}.md"
    digest_path.write_text("\n".join(header + body + footer), encoding="utf-8")
    log(f"wrote {digest_path}")

    seen.update(e["id"] for e in new_entries)
    SEEN_PATH.write_text(json.dumps(sorted(seen), ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    record_health(health)

    digest_files = sorted(DIGEST_DIR.glob("20*.md"))
    INDEX_PATH.write_text(build_index(digest_files), encoding="utf-8")
    log(f"updated {INDEX_PATH} ({len(digest_files)} digests)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
