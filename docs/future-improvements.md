# Future Improvements

Issues and ideas identified during development that aren't worth solving now but should be revisited as the project scales.

---

## Code quality

### Unclosed file handles in load functions
`run.py` uses `json.load(open(path))` without `with`. Works in CPython but isn't guaranteed. Switch to `with open(...) as f:` for correctness.

### Duplicate constants between prompt and validation
Entity types and roles are defined in prose in `discover.py` and as sets in `run.py`. A single source of truth (e.g. constants imported by both) would prevent drift.

### Anthropic client instantiated per article
`discover.py` creates a new `Anthropic()` client for every article. Instantiate once per run and pass it in to reduce overhead as article volume grows.

## Data integrity

### No within-run dedup across feeds
`seen_urls` prevents cross-run duplicates but not within a single run. If two feeds return the same canonical URL, it gets processed twice. Low risk today (feeds use different URLs for the same story) but worth addressing if more sources are added.

### Entity name as primary key
Entities are keyed by name string. Different sources may use different names for the same entity ("Blackbird Ventures" vs "Blackbird VC"). Entity resolution/dedup is a future concern as the dataset grows.

### No schema versioning
If the entity or sighting schema changes, old data won't have new fields. Currently handled gracefully with `.get()`, but explicit schema versioning would help if migrations become more frequent.

## Scalability

### JSON files as database
Works fine for a weekly batch job with small data. If entity count reaches thousands or seen_urls reaches tens of thousands, JSON load/save becomes slow and files become unwieldy in git diffs. Consider SQLite or similar if this becomes a problem.

### Ranking weight tuning
Scoring weights in `rank.py` are inline numbers (1/sighting, +2/lead, +3/multi-source). Extract to named constants at the top of the file to make tuning easier during Phase 8 observation.