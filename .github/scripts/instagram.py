#!/usr/bin/env python3
"""Post new blog posts to Instagram, from the feed Hugo prepares.

Hugo does the content work: layouts/tags/term.rss.xml turns every blog post tagged with
params.instagram.tag into a feed item with a finished caption and an Instagram-ready JPEG.
This script only validates that feed and talks to the Instagram API. Standard library
only, so the workflow needs no install step.

    instagram.py check FEED [--public DIR]   validate a built feed; used on pull requests
    instagram.py publish [--feed URL|FILE]   post every item that is not on Instagram yet

How "new" is decided: the account itself is the record of what was posted. Every caption
contains the post's permalink, so an item whose permalink already appears in one of the
account's recent captions is skipped. That makes publish idempotent — it can run after
every deploy, on a schedule and by hand without ever posting twice, and an item that
failed (or whose page was not live yet) is simply picked up by the next run. Nothing is
written back to the repository.

As a guard against mass-posting (e.g. someone tags old posts, or edits the link out of a
caption on Instagram), only items dated within --max-age-days are considered.

Environment for publish:
    IG_USER_ID        Instagram professional account ID
    IG_ACCESS_TOKEN   token with instagram_content_publish (never printed)
    IG_API_HOST       graph.facebook.com (Facebook Login / System User token, default)
                      or graph.instagram.com (Instagram Login token)
    IG_API_VERSION    Graph API version, default v26.0
"""

import argparse
import email.utils
import json
import os
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from pathlib import Path

DEFAULT_FEED = "https://starship-factory.ch/tags/instagram/index.xml"
MEDIA_NS = "{http://search.yahoo.com/mrss/}"

# Instagram's limits for single-image feed posts.
MAX_CAPTION = 2200
MAX_HASHTAGS = 30
MIN_WIDTH, MAX_WIDTH = 320, 1440
MIN_RATIO, MAX_RATIO = 4 / 5, 1.91

# How many of the account's latest posts are searched for an item's permalink.
MEDIA_LOOKBACK = 200
USER_AGENT = "starship-factory-instagram/1.0 (+https://github.com/starshipfactory/starshipfactory.github.io)"


@dataclass
class Item:
    title: str
    link: str
    published: datetime
    caption: str
    image: str | None
    width: int | None
    height: int | None


def parse_feed(xml_text):
    root = ET.fromstring(xml_text)
    items = []
    for node in root.iterfind("channel/item"):
        enclosure = node.find("enclosure")
        media = node.find(f"{MEDIA_NS}content")
        items.append(Item(
            title=(node.findtext("title") or "").strip(),
            link=(node.findtext("link") or "").strip(),
            published=email.utils.parsedate_to_datetime(node.findtext("pubDate")),
            caption=node.findtext("description") or "",
            image=enclosure.get("url") if enclosure is not None else None,
            width=int(media.get("width")) if media is not None else None,
            height=int(media.get("height")) if media is not None else None,
        ))
    return items


def problems(item):
    """Everything about an item that Instagram would reject."""
    found = []
    if not item.caption.strip():
        found.append("empty caption")
    if len(item.caption) > MAX_CAPTION:
        found.append(f"caption is {len(item.caption)} characters, Instagram allows {MAX_CAPTION}")
    hashtags = len(re.findall(r"(?<!\S)#\w", item.caption))
    if hashtags > MAX_HASHTAGS:
        found.append(f"caption has {hashtags} hashtags, Instagram allows {MAX_HASHTAGS}")
    if item.link not in item.caption:
        found.append("caption does not contain the permalink, so duplicates cannot be detected")
    if not item.image:
        found.append("no JPEG enclosure: give the post an `images` entry or a JPEG/PNG/WebP image")
    elif not (item.width and item.height):
        found.append("enclosure has no media:content width/height")
    else:
        if not MIN_WIDTH <= item.width <= MAX_WIDTH:
            found.append(f"image is {item.width}px wide, Instagram needs {MIN_WIDTH}-{MAX_WIDTH}")
        ratio = item.width / item.height
        if not MIN_RATIO - 0.005 <= ratio <= MAX_RATIO + 0.005:
            found.append(f"image aspect ratio {ratio:.2f} is outside 0.8-1.91")
    return found


def marker(link):
    """The part of a permalink that identifies the post inside a caption. The trailing
    slash stays, so /2026/09/19/foo/ does not also match /2026/09/19/foo-2/."""
    return link.split("://", 1)[-1]


# ---------------------------------------------------------------------------- check


def cmd_check(args):
    feed = Path(args.feed)
    if not feed.exists():
        print(f"{feed} does not exist: no post is tagged for Instagram. Nothing to check.")
        return 0
    items = parse_feed(feed.read_text(encoding="utf-8"))
    failed = False
    for item in items:
        found = problems(item)
        if item.image and args.public:
            local = Path(args.public) / urllib.parse.urlparse(item.image).path.lstrip("/")
            if not local.exists():
                found.append(f"enclosure {item.image} was not built (expected {local})")
        status = "FAIL" if found else "ok"
        print(f"[{status}] {item.title} — {item.link}")
        for problem in found:
            print(f"::error title=Instagram feed::{item.title}: {problem}")
        failed |= bool(found)
    print(f"{len(items)} item(s) checked.")
    return 1 if failed else 0


# -------------------------------------------------------------------------- publish


class GraphError(Exception):
    pass


class Graph:
    def __init__(self, host, version, user_id, token):
        self.base = f"https://{host}/{version}"
        self.user_id = user_id
        self.token = token

    def call(self, method, path_or_url, params=None):
        params = dict(params or {}, access_token=self.token)
        url = path_or_url if path_or_url.startswith("https://") else f"{self.base}/{path_or_url}"
        data = None
        if method == "GET":
            url = f"{url}{'&' if '?' in url else '?'}{urllib.parse.urlencode(params)}"
        else:
            data = urllib.parse.urlencode(params).encode()
        request = urllib.request.Request(url, data=data, method=method, headers={"User-Agent": USER_AGENT})
        try:
            with urllib.request.urlopen(request, timeout=60) as response:
                return json.load(response)
        except urllib.error.HTTPError as error:
            # Report Meta's error message, never the URL: it can carry the token.
            try:
                detail = json.load(error).get("error", {})
                message = f"{detail.get('type')}: {detail.get('message')} (code {detail.get('code')})"
            except ValueError:
                message = error.reason
            what = "next page" if path_or_url.startswith("https://") else path_or_url
            raise GraphError(f"{method} {what} failed: HTTP {error.code} {message}") from None

    def recent_captions(self):
        captions = []
        page = self.call("GET", f"{self.user_id}/media", {"fields": "caption", "limit": 50})
        while True:
            captions += [media.get("caption") or "" for media in page.get("data", [])]
            next_url = page.get("paging", {}).get("next")
            if not next_url or len(captions) >= MEDIA_LOOKBACK:
                return captions
            # The next URL already carries the token; strip it so call() adds it once.
            parts = urllib.parse.urlsplit(next_url)
            query = [(k, v) for k, v in urllib.parse.parse_qsl(parts.query) if k != "access_token"]
            page = self.call("GET", urllib.parse.urlunsplit(parts._replace(query=urllib.parse.urlencode(query))))

    def post_image(self, image_url, caption):
        container = self.call("POST", f"{self.user_id}/media", {"image_url": image_url, "caption": caption})["id"]
        # Instagram fetches and processes the image asynchronously; publishing before
        # the container is FINISHED fails.
        for _ in range(20):
            status = self.call("GET", container, {"fields": "status_code"}).get("status_code")
            if status == "FINISHED":
                break
            if status in ("ERROR", "EXPIRED"):
                raise GraphError(f"media container {container} ended in status {status}")
            time.sleep(3)
        else:
            raise GraphError(f"media container {container} not ready after 60s")
        media_id = self.call("POST", f"{self.user_id}/media_publish", {"creation_id": container})["id"]
        return self.call("GET", media_id, {"fields": "permalink"}).get("permalink", media_id)


def fetch(url):
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(request, timeout=60) as response:
        return response.read().decode("utf-8")


def is_live(url):
    request = urllib.request.Request(url, method="HEAD", headers={"User-Agent": USER_AGENT})
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            return response.status == 200
    except urllib.error.URLError:
        return False


def cmd_publish(args):
    if re.match(r"https?://", args.feed):
        # GitHub Pages sits behind a CDN that caches for up to ten minutes; right after
        # a deploy the cached feed may predate the new post. A unique query string
        # bypasses the cache.
        try:
            xml_text = fetch(f"{args.feed}?t={int(time.time())}")
        except urllib.error.HTTPError as error:
            if error.code != 404:
                raise
            # Hugo only renders the term page while at least one post carries the tag.
            print(f"{args.feed} does not exist: no post is tagged for Instagram. Nothing to do.")
            return 0
    else:
        xml_text = Path(args.feed).read_text(encoding="utf-8")
    items = parse_feed(xml_text)

    cutoff = datetime.now(timezone.utc) - timedelta(days=args.max_age_days)
    candidates = sorted((i for i in items if i.published >= cutoff), key=lambda i: i.published)
    print(f"{len(items)} item(s) in the feed, {len(candidates)} dated within the last {args.max_age_days} days.")
    if not candidates:
        return 0

    user_id, token = os.environ.get("IG_USER_ID"), os.environ.get("IG_ACCESS_TOKEN")
    graph = None
    if user_id and token:
        graph = Graph(os.environ.get("IG_API_HOST") or "graph.facebook.com",
                      os.environ.get("IG_API_VERSION") or "v26.0", user_id, token)
    elif not args.dry_run:
        print("::error::IG_USER_ID and IG_ACCESS_TOKEN must be set to publish.")
        return 1

    if graph:
        # If this fails, stop: without it there is no way to tell what is new.
        captions = graph.recent_captions()
        print(f"Checked the account's {len(captions)} most recent post(s) for existing links.")
    else:
        captions = []
        print("::warning::No Instagram credentials: dry run without the duplicate check.")

    failed = False
    for item in candidates:
        label = f"{item.title} — {item.link}"
        if any(marker(item.link) in caption for caption in captions):
            print(f"[skip] already on Instagram: {label}")
            continue
        found = problems(item)
        if found:
            for problem in found:
                print(f"::error title=Instagram::{item.title}: {problem}")
            failed = True
            continue
        if not (is_live(item.link) and is_live(item.image)):
            # Not deployed (or not through the CDN) yet. The next run picks it up.
            print(f"::warning title=Instagram::not live yet, will retry on the next run: {label}")
            continue
        if args.dry_run:
            print(f"[dry run] would post: {label}\n  image: {item.image}\n  caption:\n"
                  + "\n".join(f"    {line}" for line in item.caption.splitlines()))
            continue
        try:
            permalink = graph.post_image(item.image, item.caption)
            print(f"[posted] {label}\n  {permalink}")
        except GraphError as error:
            print(f"::error title=Instagram::{item.title}: {error}")
            failed = True
    return 1 if failed else 0


def main():
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    sub = parser.add_subparsers(dest="command", required=True)

    check = sub.add_parser("check", help="validate a built feed")
    check.add_argument("feed", help="path to the built feed, e.g. public/tags/instagram/index.xml")
    check.add_argument("--public", help="build output directory; verifies the JPEGs were written")
    check.set_defaults(run=cmd_check)

    publish = sub.add_parser("publish", help="post items that are not on Instagram yet")
    publish.add_argument("--feed", default=DEFAULT_FEED, help="feed URL or local file (default: the live German feed)")
    publish.add_argument("--max-age-days", type=int, default=30, help="ignore items older than this (default: 30)")
    publish.add_argument("--dry-run", action="store_true", help="print what would be posted, post nothing")
    publish.set_defaults(run=cmd_publish)

    args = parser.parse_args()
    sys.exit(args.run(args))


if __name__ == "__main__":
    main()
