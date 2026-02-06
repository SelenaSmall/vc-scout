# VC Scout

VC Scout is a lightweight agent designed to **discover and track Australian venture capital activity** using only public startup signals.

Rather than starting with a predefined list of VC firms, VC Scout continuously observes startup news, extracts investor entities, and builds a picture over time of **which actors are gaining momentum and why**.

The goal is not completeness, but **signal over noise**.

---

## What is this agent for?

VC Scout exists to answer a simple question:

> *“Who should I be paying attention to in the Australian VC ecosystem right now?”*

It is built for people who **don’t already know the map** — founders, operators, or technologists who want a systematic way to learn the landscape through observable behaviour rather than reputation.

---

## What v1 will do

VC Scout v1 is intentionally narrow and opinionated.

- **Geography:** Australia only
- **Sources:** 2–3 public startup news sites
- **Discovery:** Extract VC firms and individual investors from funding-related news
- **Signals:**
    - Frequency of mentions
    - Role in rounds (lead vs participant, where available)
- **Cadence:** Weekly analysis
- **Memory:** Single human-readable JSON file committed to the repo
- **Infrastructure:** GitHub Actions only (scheduled, no long-running services)

The primary output of v1 is a **weekly markdown brief** highlighting:
- Newly discovered VC actors
- VC actors showing increased activity or momentum

---

## What v1 explicitly will not do

To avoid scope creep and overfitting, v1 will **not**:

- Attempt to be a comprehensive directory of VC firms
- Track deal sizes, valuations, or fund performance
- Scrape LinkedIn, X, or other social platforms
- Use paid datasets or proprietary APIs
- Perform predictions or investment recommendations
- Optimise for real-time updates

These may be explored in later versions, but are out of scope for v1.

---

## How this agent evolves safely

VC Scout is developed using a **build → release → observe → refine** loop.

Principles guiding evolution:

- Small, reversible changes
- Each iteration remains runnable and observable
- Intelligence is added only after infrastructure and memory are stable
- Behaviour is explainable by inspecting code and data

This ensures the agent remains understandable, trustworthy, and easy to extend.

---

## Status

🚧 VC Scout is in active development.  
v1 focuses on discovery, memory, and weekly signal surfacing.
