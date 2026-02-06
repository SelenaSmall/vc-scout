import json
import anthropic

SYSTEM_PROMPT = """You extract venture capital entities from Australian startup news.

Given an article title and summary, return a JSON array of entities found.
Each entity should have:
- "name": the entity name (VC firm or individual investor)
- "type": either "vc_firm" or "investor"

Only include entities that are clearly venture capital firms or investors.
If no VC entities are found, return an empty array.
Return only valid JSON, no other text."""


def extract_entities(article):
    client = anthropic.Anthropic()
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
    except anthropic.APIError as e:
        print(f"    [error] API call failed: {e}")
        return None

    text = response.content[0].text.strip()
    # Strip markdown code fences if present
    if text.startswith("```"):
        text = text.split("\n", 1)[1].rsplit("```", 1)[0].strip()
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        print(f"    [error] Could not parse response: {text[:100]}")
        return None