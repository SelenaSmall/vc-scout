# Future Improvements

Issues and ideas identified during development that aren't worth solving now but should be revisited as the project scales.

---

## Code quality

No outstanding items.

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