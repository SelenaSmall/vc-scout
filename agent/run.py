from fetch import fetch_articles

if __name__ == "__main__":
    articles = fetch_articles()
    print(f"Fetched {len(articles)} articles:")
    for article in articles:
        print(f"  - {article['title']}")