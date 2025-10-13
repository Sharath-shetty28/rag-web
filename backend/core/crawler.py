#!/usr/bin/env python3
# crawler.py — polite site crawler that extracts main text and saves URL->text mapping

import argparse
import json
import logging
import time
from collections import deque
from urllib.parse import urljoin, urlparse, urldefrag

import requests
from readability import Document
from bs4 import BeautifulSoup
import tldextract
from urllib.robotparser import RobotFileParser

logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(message)s')


def get_registered_domain(url: str) -> str:
    e = tldextract.extract(url)
    return e.registered_domain


def build_robots_parser(start_url: str) -> RobotFileParser:
    parsed = urlparse(start_url)
    robots_url = f"{parsed.scheme}://{parsed.netloc}/robots.txt"
    rp = RobotFileParser()
    rp.set_url(robots_url)
    try:
        rp.read()
    except Exception:
        logging.warning("Couldn't read robots.txt at %s (continuing without strict rules)", robots_url)
    return rp


def can_fetch_robots(rp: RobotFileParser, url: str) -> bool:
    try:
        return rp.can_fetch('*', url)
    except Exception:
        return True


def extract_main_text(html: str, url: str = "") -> str:
    """
    Try readability -> fallback to BeautifulSoup text.
    Returns a cleaned text string.
    """
    try:
        doc = Document(html)
        summary = doc.summary()
        soup = BeautifulSoup(summary, "html.parser")
        text = soup.get_text(separator=" ", strip=True)
        if text and len(text) > 10:
            return text
    except Exception as e:
        logging.debug("readability failed for %s: %s", url, e)

    # fallback
    try:
        soup = BeautifulSoup(html, "html.parser")
        text = soup.get_text(separator=" ", strip=True)
        return text
    except Exception:
        return ""


def normalize_url(base: str, href: str) -> str | None:
    if not href:
        return None
    href = href.strip()
    if href.startswith("mailto:") or href.startswith("tel:") or href.startswith("javascript:") or href.startswith("#"):
        return None
    joined = urljoin(base, href)
    joined, _ = urldefrag(joined)  # remove fragment
    parsed = urlparse(joined)
    if parsed.scheme not in ("http", "https"):
        return None
    return joined


def crawl_site(start_url: str, max_pages: int = 40, delay: float = 0.5, out_file: str = "data/pages.json"):
    registered_domain = get_registered_domain(start_url)
    logging.info("Crawl start: %s (registrable domain: %s) max_pages=%d", start_url, registered_domain, max_pages)

    rp = build_robots_parser(start_url)
    q = deque([start_url])
    visited = set()
    pages = {}
    skipped = 0
    headers = {"User-Agent": "RAG-Crawler/1.0 (+https://example.org)"}

    while q and len(pages) < max_pages:
        url = q.popleft()
        if url in visited:
            continue

        if not can_fetch_robots(rp, url):
            logging.info("Blocked by robots.txt: %s", url)
            skipped += 1
            visited.add(url)
            continue

        logging.info("Fetching: %s", url)
        try:
            resp = requests.get(url, headers=headers, timeout=12)
        except requests.RequestException as e:
            logging.warning("Request failed for %s: %s", url, e)
            skipped += 1
            visited.add(url)
            continue

        visited.add(url)
        if resp.status_code != 200:
            logging.info("Non-200 status %s: %d", url, resp.status_code)
            skipped += 1
            continue

        content_type = resp.headers.get("Content-Type", "")
        if "text/html" not in content_type:
            logging.info("Skipping non-HTML content: %s (%s)", url, content_type)
            skipped += 1
            continue

        html = resp.text
        text = extract_main_text(html, url)
        if not text or len(text) < 30:
            logging.info("No useful text found at %s", url)
            skipped += 1
            continue

        pages[url] = text
        logging.info("Saved text from %s (chars=%d)", url, len(text))

        # find links and enqueue same-domain URLs
        soup = BeautifulSoup(html, "html.parser")
        for a in soup.find_all("a", href=True):
            nurl = normalize_url(url, a["href"])
            if not nurl:
                continue
            if get_registered_domain(nurl) != registered_domain:
                continue
            if nurl not in visited and nurl not in q:
                q.append(nurl)

        time.sleep(delay)

    # persist results
    import os
    os.makedirs(os.path.dirname(out_file), exist_ok=True)
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump({"start_url": start_url, "page_count": len(pages), "pages": pages}, f, ensure_ascii=False, indent=2)

    logging.info("Crawl finished. pages=%d skipped=%d saved=%s", len(pages), skipped, out_file)
    return {"page_count": len(pages), "skipped_count": skipped, "urls": list(pages.keys())}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog="crawler.py")
    parser.add_argument("start_url", help="Starting URL (e.g. https://example.com)")
    parser.add_argument("--max-pages", type=int, default=40)
    parser.add_argument("--delay", type=float, default=0.5, help="crawl delay in seconds")
    parser.add_argument("--out", default="data/pages.json", help="output JSON file")
    args = parser.parse_args()

    crawl_site(args.start_url, max_pages=args.max_pages, delay=args.delay, out_file=args.out)
