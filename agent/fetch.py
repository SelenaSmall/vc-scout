from html.parser import HTMLParser
import feedparser

FEED_URL = "https://www.startupdaily.net/feed/"


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


def fetch_articles():
    feed = feedparser.parse(FEED_URL)
    if feed.bozo and not feed.entries:
        print(f"[error] Failed to fetch feed: {feed.bozo_exception}")
        return []
    return [
        {"title": entry.title, "summary": _strip_html(entry.get("summary", ""))}
        for entry in feed.entries
    ]