# Security Considerations

Tracked vulnerabilities and threat surfaces to revisit as the project evolves.

---

## Untrusted feed content

RSS feed content (titles, summaries) comes from external sources and is passed into Claude prompts via `discover.py`.

**Mitigated:**
- [x] Raw HTML in summaries — `fetch.py` now strips HTML to plain text before returning articles

**Open:**
- [ ] Prompt injection — malicious titles or summaries could attempt to manipulate Claude's entity extraction. Current blast radius is log output only (no data persisted yet). Revisit before Phase 5.
- [ ] Content injection — when entities are written to markdown (Phase 6), untrusted content could include unexpected formatting or links. Revisit before Phase 6.