# VC Scout - Phased Release Plan (v1)

This document outlines the step-by-step plan for building and releasing VC Scout v1.
Each phase is designed to be independently releasable and verifiable, ensuring the agent is always runnable and observable.

---

## Phase 1 - “Hello, agent” (no Claude yet)

### Step 1.1: Add a single Python entrypoint
- [ ] Create `agent/run.py`
- [ ] Hardcode output:

```python
if __name__ == "__main__":
    print("VC Scout agent ran successfully")
```

### Step 1.2: Add GitHub Actions

- [ ] Add scheduled GitHub Actions workflow (weekly)
- [ ] No dependencies
- [ ] Workflow runs python agent/run.py

**Checkpoint**

- [ ] GitHub Action runs on schedule and logs output
- [ ] Runtime and scheduler are trusted

_No logic yet. This phase is about infrastructure confidence._

---

## Phase 2 - Fetch something boring

### Step 2.1: Add a fetcher

- [ ] Pull one RSS feed
- [ ] Return article titles only

_No parsing or intelligence_


### Step 2.2: Wire fetcher into run.py

- [ ] Call fetcher from run.py
- [ ] Print fetched titles to logs

**Checkpoint**

- [ ] Agent runs end-to-end
- [ ] Network access works
- [ ] Output is deterministic

_If this breaks, only this layer is fixed._

---

## Phase 3 - Persist state (major milestone)

### Step 3.1: Add memory store

- [ ] Create memory.json with empty structure:

```json
  {
    "entities": {}
  }
```

### Step 3.2: Load and save memory

- [ ] Load memory at agent start
- [ ] Write memory back at end (even if unchanged)

### Step 3.3: Commit memory updates automatically

- [ ] Agent commits memory.json if it changes

**Checkpoint**

- [ ] Memory survives between runs
- [ ] Repo history shows state evolving over time

_At this point, VC Scout is officially an agent._

---

## Phase 4 - First Claude integration (discovery only)

### Step 4.1: Add discovery module

- [ ] Input: article text
- [ ] Output: structured JSON
- [ ] No ranking or opinions
- [ ] Claude used only for entity extraction

### Step 4.2: Log extracted entities

- [ ] Print extracted entities to logs
- [ ] Do not store them yet

**Checkpoint**

- [ ] Claude is callable from the agent
- [ ] Output is structured and predictable
- [ ] Failures are visible, not silent

_If Claude breaks, the rest of the agent still runs._

---

## Phase 5 - Teach the agent to remember

### Step 5.1: Store discovered entities

- [ ] Add entities to memory.json
- [ ] Increment mention counts
- [ ] Track first_seen and last_seen

### Step 5.2: Track “new this run”

- [ ] Flag newly discovered entities per run

**Checkpoint**

- [ ] memory.json evolves meaningfully
- [ ] You can explain why every entity exists

_Discovery is now persistent._

--- 

## Phase 6 - Generate a human-readable output

### Step 6.1: Create weekly brief

- [ ] Generate weekly_brief.md
- [ ] Include sections:

    - New entities
    - Increased activity
    - No ranking yet

### Step 6.2: Commit output automatically

- [ ] Agent commits weekly_brief.md

**Checkpoint**

- [ ] Someone can read the brief and learn something
- [ ] Output is stable week-to-week

_This is the first public-facing artefact._

---

## Phase 7 - Add opinion (ranking)

### Step 7.1: Encode simple heuristics

- [ ] Mentions count
- [ ] Lead vs participant (where available)
- [ ] Presence across multiple sources

### Step 7.2: Explain the ranking

- [ ] Plain English reasons for ordering

**Checkpoint**

- [ ] You agree with the ordering
- [ ] You can defend the logic

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
