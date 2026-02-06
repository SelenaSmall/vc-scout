# Security Considerations

Tracked vulnerabilities and threat surfaces to revisit as the project evolves.

---

## Untrusted feed content

RSS feed content (titles, summaries) comes from external sources and is passed into Claude prompts via `discover.py`.

**Mitigated:**
- [x] Raw HTML in summaries — `fetch.py` strips HTML to plain text before returning articles
- [x] Output schema validation — `run.py` validates entity shape and type before use; malformed Claude responses are skipped and logged

**Open:**
- [ ] Content injection — when entities are written to markdown (Phase 6), untrusted content could include unexpected formatting or links. Revisit before Phase 6.