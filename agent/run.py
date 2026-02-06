import json
from pathlib import Path
from fetch import fetch_articles
from discover import extract_entities

MEMORY_PATH = Path(__file__).parent / "memory.json"


def load_memory():
    with open(MEMORY_PATH) as f:
        return json.load(f)


def save_memory(memory):
    with open(MEMORY_PATH, "w") as f:
        json.dump(memory, f, indent=2)
        f.write("\n")


if __name__ == "__main__":
    memory = load_memory()
    print(f"Memory loaded: {len(memory['entities'])} entities")

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

    save_memory(memory)
    print("Memory saved")