from html.parser import HTMLParser
import feedparser

FEEDS = [
    {"url": "https://www.startupdaily.net/feed/", "source": "startupdaily.net"},
    {"url": "https://www.smartcompany.com.au/startupsmart/feed/", "source": "smartcompany.com.au"},
]


class _HTMLTextExtractor(HTMLParser):
    """Collects text content from HTML, stripping all tags."""

    def __init__(self):
        super().__init__()
        self._parts = []

    # Called by the parser for each chunk of text between tags
    def handle_data(self, data):
        self._parts.append(data)

    def get_text(self):
        return "".join(self._parts).strip()


def _strip_html(html):
    extractor = _HTMLTextExtractor()
    extractor.feed(html)
    return extractor.get_text()


def fetch_articles(feed_url, source):
    feed = feedparser.parse(feed_url)
    if feed.bozo and not feed.entries:
        print(f"  [{source}] Failed to fetch feed: {feed.bozo_exception}")
        return []
    return [
        {
            "title": entry.title,
            "summary": _strip_html(entry.get("summary", "")),
            "url": entry.get("link", ""),
            "source": source,
        }
        for entry in feed.entries
    ]


def fetch_all_articles():
    all_articles = []
    for feed in FEEDS:
        articles = fetch_articles(feed["url"], feed["source"])
        print(f"  [{feed['source']}] {len(articles)} articles")
        all_articles.extend(articles)
    return all_articles