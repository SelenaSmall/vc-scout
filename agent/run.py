import json
from datetime import date
from pathlib import Path
from fetch import fetch_articles
from discover import extract_entities
from brief import write_brief

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


def store_entity(memory, entity, article):
    name = entity["name"]
    today = date.today().isoformat()
    sighting = {
        "date": today,
        "source": "startupdaily.net",
        "article": article["title"],
        "url": article["url"],
    }

    if name in memory["entities"]:
        memory["entities"][name]["last_seen"] = today
        memory["entities"][name]["sightings"].append(sighting)
    else:
        memory["entities"][name] = {
            "type": entity["type"],
            "first_seen": today,
            "last_seen": today,
            "sightings": [sighting],
        }


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
                    store_entity(memory, entity, article)
                    print(f"    -> {entity['name']} ({entity['type']})")
                else:
                    print(f"    [skipped] Invalid entity: {str(entity)[:80]}")
        else:
            print("    -> No VC entities found")

    save_memory(memory)
    print(f"Memory saved: {len(memory['entities'])} entities")

    brief_path = write_brief(memory)
    print(f"Weekly brief written to {brief_path}")
