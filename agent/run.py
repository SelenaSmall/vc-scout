import json
from pathlib import Path
from fetch import fetch_articles
from discover import extract_entities

MEMORY_PATH = Path(__file__).parent / "memory.json"
VALID_ENTITY_TYPES = {"vc_firm", "investor"}


def load_memory():
    with open(MEMORY_PATH) as f:
        return json.load(f)


def save_memory(memory):
    with open(MEMORY_PATH, "w") as f:
        json.dump(memory, f, indent=2)
        f.write("\n")


def is_valid_entity(entity):
    return (
        isinstance(entity, dict)
        and isinstance(entity.get("name"), str)
        and entity.get("type") in VALID_ENTITY_TYPES
    )


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
                if is_valid_entity(entity):
                    print(f"    -> {entity['name']} ({entity['type']})")
                else:
                    print(f"    [skipped] Invalid entity: {str(entity)[:80]}")
        else:
            print("    -> No VC entities found")

    save_memory(memory)
    print("Memory saved")