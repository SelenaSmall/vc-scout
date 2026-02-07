import json
import re
import anthropic
from schema import ENTITY_TYPES, ENTITY_ROLES

_types = ", ".join(f'"{t}"' for t in ENTITY_TYPES)
_roles = ", ".join(f'"{r}"' for r in ENTITY_ROLES)

SYSTEM_PROMPT = f"""You extract venture capital entities from Australian startup news.

Given an article title and summary, return a JSON array of entities found.
Each entity should have:
- "name": the entity name (VC firm or individual investor)
- "type": one of {_types}
- "role": the entity's role in the deal — "lead" if they led the round, "participant" if they participated, or "unknown" if unclear. Must be one of {_roles}

Only include entities that are clearly venture capital firms or investors.
If no VC entities are found, return an empty array.
Return only valid JSON, no other text."""


def extract_entities(article, client):
    try:
        response = client.messages.create(
            model="claude-sonnet-4-5-20250929",
            max_tokens=512,
            timeout=30,
            system=SYSTEM_PROMPT,
            messages=[
                {
                    "role": "user",
                    "content": f"Title: {article['title']}\n\nSummary: {article['summary']}",
                }
            ],
        )
    except (anthropic.APIError, anthropic.APIConnectionError) as e:
        print(f"    [error] API call failed: {e}")
        return None

    text = response.content[0].text.strip()
    # Claude sometimes produces multiple fenced code blocks when it self-corrects
    # mid-response (e.g. first block has entities, then "Wait, let me reconsider",
    # then a corrected block). Take the last block as the final answer.
    fenced_blocks = re.findall(r"```(?:json)?\s*\n(.*?)```", text, re.DOTALL)
    if fenced_blocks:
        text = fenced_blocks[-1].strip()
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        print(f"    [error] Could not parse response: {text[:100]}")
        return None