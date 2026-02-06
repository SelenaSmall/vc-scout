from fetch import fetch_titles

if __name__ == "__main__":
    titles = fetch_titles()
    print(f"Fetched {len(titles)} titles:")
    for title in titles:
        print(f"  - {title}")