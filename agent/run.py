import json
import os
from datetime import date
from pathlib import Path
from fetch import fetch_all_articles
from discover import extract_entities
from brief import write_brief

from schema import ENTITY_TYPES, ENTITY_ROLES


def _resolve_paths():
    mode = os.environ.get("VC_SCOUT_MODE", "test")
    root = Path(__file__).parent.parent
    if mode == "production":
        data_dir = root / "data"
        output_path = root / "output" / "weekly_brief.md"
    else:
        data_dir = root / "test" / "data"
        output_path = root / "test" / "output" / "weekly_brief.md"
    return mode, data_dir, output_path


def load_entities(path):
    if not path.exists():
        return {}
    with open(path) as f:
        return json.load(f)


def save_entities(entities, path):
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w") as f:
        json.dump(entities, f, indent=2)
        f.write("\n")


def load_seen_urls(path):
    if not path.exists():
        return {}
    with open(path) as f:
        return json.load(f)


def save_seen_urls(seen_urls, path):
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w") as f:
        json.dump(seen_urls, f, indent=2)
        f.write("\n")


def is_valid_entity(entity):
    return (
        isinstance(entity, dict)
        and isinstance(entity.get("name"), str)
        and entity.get("type") in ENTITY_TYPES
        and entity.get("role") in ENTITY_ROLES
    )


def store_entity(entities, entity, article):
    name = entity["name"]
    today = date.today().isoformat()
    sighting = {
        "date": today,
        "source": article["source"],
        "article": article["title"],
        "url": article["url"],
        "role": entity["role"],
    }

    if name in entities:
        entities[name]["last_seen"] = today
        entities[name]["sightings"].append(sighting)
    else:
        entities[name] = {
            "type": entity["type"],
            "first_seen": today,
            "last_seen": today,
            "sightings": [sighting],
        }


if __name__ == "__main__":
    mode, data_dir, output_path = _resolve_paths()
    print(f"Running in {mode} mode")

    entities = load_entities(data_dir / "entities.json")
    seen_urls = load_seen_urls(data_dir / "seen_urls.json")
    print(f"Loaded {len(entities)} entities, {len(seen_urls)} seen URLs")

    all_articles = fetch_all_articles()
    articles = [a for a in all_articles if a["url"] not in seen_urls]
    print(f"Fetched {len(all_articles)} articles, {len(articles)} new")

    for article in articles:
        print(f"\n  - {article['title']}")
        extracted = extract_entities(article)
        if extracted is None:
            print("    -> Extraction failed, will retry next run")
            continue
        if extracted:
            for entity in extracted:
                if is_valid_entity(entity):
                    store_entity(entities, entity, article)
                    print(f"    -> {entity['name']} ({entity['type']}, {entity['role']})")
                else:
                    print(f"    [skipped] Invalid entity: {str(entity)[:80]}")
        else:
            print("    -> No VC entities found")
        seen_urls[article["url"]] = date.today().isoformat()

    save_entities(entities, data_dir / "entities.json")
    save_seen_urls(seen_urls, data_dir / "seen_urls.json")
    print(f"Saved {len(entities)} entities, {len(seen_urls)} seen URLs")

    brief_path = write_brief(entities, output_path)
    print(f"Weekly brief written to {brief_path}")
