import feedparser

FEED_URL = "https://www.startupdaily.net/feed/"


def fetch_titles():
    feed = feedparser.parse(FEED_URL)
    return [entry.title for entry in feed.entries]