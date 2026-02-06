import feedparser

FEED_URL = "https://www.startupdaily.net/feed/"


def fetch_articles():
    feed = feedparser.parse(FEED_URL)
    return [
        {"title": entry.title, "summary": entry.get("summary", "")}
        for entry in feed.entries
    ]