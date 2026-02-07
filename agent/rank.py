WEIGHT_SIGHTING = 1
WEIGHT_LEAD_ROLE = 2
WEIGHT_MULTI_SOURCE = 3


def rank_entities(entities):
    """Rank entities by activity signals.

    Returns list of (name, score, explanations) sorted descending by score.
    """
    scored = []
    for name, data in entities.items():
        sightings = data["sightings"]
        score = 0
        explanations = []

        count = len(sightings)
        score += count * WEIGHT_SIGHTING
        explanations.append(f"{count} sighting{'s' if count != 1 else ''}")

        lead_count = sum(1 for s in sightings if s.get("role") == "lead")
        if lead_count:
            score += lead_count * WEIGHT_LEAD_ROLE
            explanations.append(f"led {lead_count} round{'s' if lead_count != 1 else ''}")

        sources = {s["source"] for s in sightings}
        if len(sources) > 1:
            score += WEIGHT_MULTI_SOURCE
            explanations.append(f"seen across {len(sources)} sources")

        scored.append((name, score, explanations))

    scored.sort(key=lambda x: x[1], reverse=True)
    return scored