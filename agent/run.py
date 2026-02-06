from fetch import fetch_articles
from discover import extract_entities

if __name__ == "__main__":
    articles = fetch_articles()
    print(f"Fetched {len(articles)} articles:")

    for article in articles:
        print(f"\n  - {article['title']}")
        entities = extract_entities(article)
        if entities:
            for entity in entities:
                print(f"    -> {entity['name']} ({entity['type']})")
        else:
            print("    -> No VC entities found")