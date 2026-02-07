# VC Scout - Phased Release Plan (v1)

This document outlines the step-by-step plan for building and releasing VC Scout v1.
Each phase is designed to be independently releasable and verifiable, ensuring the agent is always runnable and observable.

---

## Phase 1 - “Hello, agent” (no Claude yet)

### Step 1.1: Add a single Python entrypoint
- [x] Create `agent/run.py`
- [x] Hardcode output:

```python
if __name__ == "__main__":
    print("VC Scout agent ran successfully")
```

### Step 1.2: Add GitHub Actions

- [x] Add scheduled GitHub Actions workflow (weekly)
- [x] No dependencies
- [x] Workflow runs python agent/run.py

**Checkpoint**

- [x] GitHub Action runs on schedule and logs output
- [x] Runtime and scheduler are trusted

_No logic yet. This phase is about infrastructure confidence._

---

## Phase 2 - Fetch something boring

### Step 2.1: Add a fetcher

- [x] Pull one RSS feed
- [x] Return article titles only

_No parsing or intelligence_


### Step 2.2: Wire fetcher into run.py

- [x] Call fetcher from run.py
- [x] Print fetched titles to logs

**Checkpoint**

- [x] Agent runs end-to-end
- [x] Network access works
- [x] Output is deterministic

_If this breaks, only this layer is fixed._

---

## Phase 3 - First Claude integration (discovery only)

### Step 3.1: Add discovery module

- [x] Input: article text
- [x] Output: structured JSON
- [x] No ranking or opinions
- [x] Claude used only for entity extraction

### Step 3.2: Log extracted entities

- [x] Print extracted entities to logs
- [x] Do not store them yet

**Checkpoint**

- [x] Claude is callable from the agent
- [x] Output is structured and predictable
- [x] Failures are visible, not silent

_If Claude breaks, the rest of the agent still runs._

---

## Phase 4 - Persist state (major milestone)

### Step 4.1: Add memory store

- [x] Create memory.json with empty structure:

```json
  {
    "entities": {}
  }
```

### Step 4.2: Load and save memory

- [x] Load memory at agent start
- [x] Write memory back at end (even if unchanged)

### Step 4.3: Commit memory updates automatically

- [x] Agent commits memory.json if it changes

**Checkpoint**

- [x] Memory survives between runs
- [x] Repo history shows state evolving over time

_At this point, VC Scout is officially an agent._

---

## Phase 5 - Teach the agent to remember

### Step 5.1: Store discovered entities

- [x] Add entities to memory.json
- [x] Track sightings with date, source, article title, and URL
- [x] Track first_seen and last_seen

### Step 5.2: Track "new this run"

- [x] Derived from first_seen date — no separate flag needed

**Checkpoint**

- [x] memory.json evolves meaningfully
- [x] You can explain why every entity exists

_Discovery is now persistent._

--- 

## Phase 6 - Generate a human-readable output

### Step 6.1: Create weekly brief

- [x] Generate weekly_brief.md
- [x] Include sections:

    - New this week (entities where first_seen is this run)
    - Previously seen (entities seen again this run, with sighting count)
    - No ranking yet

### Step 6.2: Commit output automatically

- [x] Agent commits weekly_brief.md

**Checkpoint**

- [x] Someone can read the brief and learn something
- [x] Output is stable week-to-week

_This is the first public-facing artefact._

---

## Phase 7 - Add opinion (ranking)

### Step 7.1: Add test mode and reset memory

- [x] `VC_SCOUT_MODE` environment variable — defaults to `test`, CI sets `production`
- [x] Test mode writes to gitignored `test/` directory (mirrors `data/` and `output/` structure)
- [x] Production data moved to `data/memory.json` (separate from code in `agent/`)
- [x] Reset memory.json to empty state — existing data was test pollution

### Step 7.2: Skip already-processed articles

- [ ] Track processed article URLs in memory (`seen_urls`)
- [ ] Filter out already-seen articles in run.py after fetch, before discover
- [ ] Prevents duplicate sightings and saves Claude API calls

### Step 7.3: Add `role` to entity extraction

- [ ] Update Claude prompt to extract role: `lead`, `participant`, or `unknown`
- [ ] Validate role in run.py before storage
- [ ] Store role per-sighting (not per-entity — role can vary across deals)

### Step 7.4: Add a second RSS source

- [ ] Add SmartCompany StartupSmart feed (`smartcompany.com.au/startupsmart/feed/`)
- [ ] Article dicts carry a `source` field (remove hardcoded source in `store_entity`)
- [ ] `fetch_all_articles()` iterates all configured feeds

### Step 7.5: Encode ranking heuristics

- [ ] New `rank.py` module — pure function, no I/O
- [ ] Sighting count (+1 per sighting)
- [ ] Lead bonus (+2 per sighting where role is lead)
- [ ] Multi-source presence (+3 if seen across 2+ sources)

### Step 7.6: Integrate ranking into weekly brief

- [ ] Order entities by rank score in both sections
- [ ] Plain English explanations for ordering (e.g. "3 sightings; led 1 round; seen across 2 sources")

### Step 7.7: Update documentation

- [ ] Update getting-started.md with test mode instructions
- [ ] Add role validation to security considerations

**Checkpoint**

- [ ] You agree with the ordering
- [ ] You can defend the logic
- [ ] Local runs are safe (test mode by default)
- [ ] Both RSS sources return data
- [ ] No duplicate sightings from repeated runs

---

## Phase 8 - Tighten and observe

### Step 8.1: Let the agent run

- [ ] Allow agent to run for several weeks
- [ ] Do not add features during this period

### Step 8.2: Observe behaviour

- [ ] Note false positives
- [ ] Note missed signals
- [ ] Identify noisy or over-weighted actors

_Observations here inform v2 ideas, not immediate changes._
