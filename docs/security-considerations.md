# Security Considerations

Tracked vulnerabilities and threat surfaces to revisit as the project evolves.

---

## Untrusted feed content

RSS feed content (titles, descriptions, etc.) comes from external sources and should be treated as untrusted input. Currently we only extract titles as plain strings, limiting blast radius. However, as later phases pass feed content into Claude prompts (Phase 4) or write it into markdown output (Phase 6), this becomes a concern:

- **Prompt injection**: Malicious titles could attempt to manipulate Claude's behaviour during entity extraction.
- **Content injection**: Titles written directly into markdown could include unexpected formatting or links.

**When to address**: Before Phase 4 (first Claude integration).