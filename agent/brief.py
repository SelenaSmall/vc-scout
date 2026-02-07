import re
from datetime import date
from rank import rank_entities


def sanitise_markdown(text):
    """Escape characters that have special meaning in markdown."""
    return re.sub(r"([\\`*_\{\}\[\]()#+\-.!|])", r"\\\1", text)


def generate_brief(entities):
    today = date.today().isoformat()

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
        for name, score, explanations in rank_entities(new_this_week):
            safe_name = sanitise_markdown(name)
            entity_type = new_this_week[name]["type"]
            lines.append(f"- **{safe_name}** ({entity_type}) — {'; '.join(explanations)}")
    else:
        lines.append("No new entities this week.")
    lines.append("")

    lines.append("## Previously seen")
    lines.append("")
    if seen_again:
        for name, score, explanations in rank_entities(seen_again):
            safe_name = sanitise_markdown(name)
            entity_type = seen_again[name]["type"]
            lines.append(f"- **{safe_name}** ({entity_type}) — {'; '.join(explanations)}")
    else:
        lines.append("No returning entities this week.")
    lines.append("")

    return "\n".join(lines)


def write_brief(entities, output_path):
    content = generate_brief(entities)
    output_path.parent.mkdir(exist_ok=True)
    with open(output_path, "w") as f:
        f.write(content)
    return output_path