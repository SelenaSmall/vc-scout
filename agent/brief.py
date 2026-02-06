import re
from datetime import date
from pathlib import Path

OUTPUT_PATH = Path(__file__).parent.parent / "output" / "weekly_brief.md"


def sanitise_markdown(text):
    """Escape characters that have special meaning in markdown."""
    return re.sub(r"([\\`*_\{\}\[\]()#+\-.!|])", r"\\\1", text)


def generate_brief(memory):
    today = date.today().isoformat()
    entities = memory["entities"]

    new_this_week = {
        name: data for name, data in entities.items()
        if data["first_seen"] == today
    }
    seen_again = {
        name: data for name, data in entities.items()
        if data["first_seen"] != today and data["last_seen"] == today
    }

    lines = [f"# VC Scout Weekly Brief — {today}", ""]

    lines.append("## New this week")
    lines.append("")
    if new_this_week:
        for name, data in new_this_week.items():
            safe_name = sanitise_markdown(name)
            lines.append(f"- **{safe_name}** ({data['type']})")
    else:
        lines.append("No new entities this week.")
    lines.append("")

    lines.append("## Previously seen")
    lines.append("")
    if seen_again:
        for name, data in seen_again.items():
            safe_name = sanitise_markdown(name)
            count = len(data["sightings"])
            lines.append(f"- **{safe_name}** ({data['type']}) — {count} sightings")
    else:
        lines.append("No returning entities this week.")
    lines.append("")

    return "\n".join(lines)


def write_brief(memory):
    content = generate_brief(memory)
    OUTPUT_PATH.parent.mkdir(exist_ok=True)
    with open(OUTPUT_PATH, "w") as f:
        f.write(content)
    return OUTPUT_PATH