---
name: web-research
description: >
  Web research skill v1.0. Governs how the research agent discovers,
  retrieves, evaluates, and extracts information from the live web.
  Uses #tool:browser for discovery and #tool:web/fetch for full-content
  retrieval. Composes with the research-report skill — this skill handles
  SOURCING; research-report handles REPORTING.
---

# Skill: Web Research & Browsing — v1.0

> This skill governs HOW the agent discovers, retrieves, evaluates, and
> extracts information from the live web. It composes with the
> research-report skill — this skill handles SOURCING;
> research-report handles REPORTING.

---

## 1. Tool Architecture

The research agent uses TWO web tools with distinct roles:

```
TOPIC
  │
  ▼
#tool:browser  ("<query>")          ← DISCOVERY TOOL
  │  Use for: Searching the web to find relevant pages
  │  Returns: Page content, URLs, search result summaries
  │
  ▼
Evaluate URLs from search results
  │  Assess: Source tier, recency, relevance
  │
  ▼
#tool:web/fetch  <url>              ← RETRIEVAL TOOL
  │  Use for: Reading the full content of a specific URL
  │  Returns: Full page text
  │
  ▼
Extract facts, data, quotes → record with citation
```

**Rule: Always use #tool:browser to search BEFORE using #tool:web/fetch.**
Never fetch a URL constructed from training memory without first verifying
it appears in a search result — with the exception of known stable
government and institution domains listed in Section 4.1.

---

## 2. Tool Availability Check

At the start of every research task, check tool availability (done in
the agent Pre-Flight Check 1). The result determines which workflow to follow:

```
IF #tool:browser is available:
    → Use the Full Browsing Workflow (Section 3)

IF #tool:browser is NOT available but #tool:web/fetch is:
    → Use the Fetch-Only Fallback Workflow (Section 4)
    → Declare at the start of Section 1: "Note: Web search was
      unavailable for this report. Sources were retrieved from
      known URLs and may not reflect the most current information.
      Verify key statistics against live sources before acting."

IF NEITHER tool is available:
    → Use pre-trained knowledge only
    → Label ALL facts as [Analyst Perspective — unverified]
    → Declare prominently in Section 1 and Executive Summary
    → Reduce confidence language throughout
```

---

## 3. Full Browsing Workflow (#tool:browser + #tool:web/fetch)

### Step 3.1 — Formulate Search Queries

Before executing any search, formulate a complete search query set.
Do NOT search once with the topic title and stop. Design multiple
targeted queries that triangulate the topic from different angles.

**Query formulation rules:**
- Use 3–6 words per query — specific enough to return relevant results
- Include the current year in queries about current events or statistics
- Use site: operators for authoritative sources
- Vary by angle: statistics, policy, market, risk, recent news

**Query set template (adapt to topic):**
```
Query 1 — Official/Statistical:
  "[topic] statistics data [current year] site:gov OR site:un.org OR site:worldbank.org"

Query 2 — Research/Academic:
  "[topic] research report [current year] site:mckinsey.com OR site:oecd.org OR site:imf.org"

Query 3 — Current news/developments:
  "[topic] latest developments [current year] site:ft.com OR site:reuters.com OR site:bloomberg.com"

Query 4 — Industry/Market:
  "[topic] market size outlook [current year] site:gartner.com OR site:idc.com OR site:forrester.com"

Query 5 — Regulatory/Policy:
  "[topic] regulation policy [current year] site:gov OR site:europa.eu OR site:rbi.org.in"

Query 6 — Specific sub-question:
  "[specific aspect of topic] [current year]"
```

**Topic-type query adjustments:**

| Topic Type | Priority Site Operators |
|---|---|
| Technology / AI | site:ieee.org, site:acm.org, site:nist.gov, site:gartner.com |
| Finance / Banking | site:imf.org, site:bis.org, site:rbi.org.in, site:sebi.gov.in |
| Healthcare | site:who.int, site:cdc.gov, site:nih.gov, site:pubmed.ncbi.nlm.nih.gov |
| Policy / Law | site:gov, site:parliament.uk, site:europa.eu, site:prsindia.org |
| Climate / Energy | site:iea.org, site:ipcc.ch, site:unfccc.int |
| Business / Markets | site:ft.com, site:reuters.com, site:economist.com |
| India-specific | site:gov.in, site:rbi.org.in, site:sebi.gov.in, site:mospi.gov.in |

---

### Step 3.2 — Execute Searches and Evaluate Results

For each query:

1. Execute the search using #tool:browser with the query string
2. Scan the returned content for relevant URLs and summaries
3. For each result, assess:
   - **Source tier** (Tier 1 / Tier 2 / Tier 3 / Unacceptable — see Section 3.2a)
   - **Publication date** — is it current enough?
   - **Relevance** — does it address one of the research sub-questions?
4. Shortlist URLs to fetch: prioritise Tier 1, recent, directly relevant
5. Skip URLs that are: paywalled with no accessible summary, personal
   blogs or opinion pieces, PR content presented as research,
   older than 3 years (unless historical context is the purpose)

**Source Tier Definitions:**

| Tier | Examples | Usage |
|---|---|---|
| Tier 1 | Government bodies, central banks, UN agencies, peer-reviewed journals, major IGOs | Primary — always prefer |
| Tier 2 | Major consultancies (McKinsey, PwC, Deloitte), reputable think tanks, established financial press (FT, Reuters, Bloomberg) | Strong — use freely |
| Tier 3 | Trade publications, industry associations, credible news outlets | Acceptable — cross-verify each claim |
| Unacceptable | Blogs, press releases without corroboration, Wikipedia as sole source, undated pages | Do not cite directly |

**Record for each search result evaluated:**
```
URL:             [url]
Source:          [organisation]
Tier:            [1 / 2 / 3 / Unacceptable]
Publication date:[date or "undated"]
Relevance:       [which sub-question this addresses]
Decision:        [FETCH / SKIP — reason for skip]
```

---

### Step 3.3 — Retrieve Full Content

For each shortlisted URL: use #tool:web/fetch with the exact URL.

On retrieval, immediately:

1. **Confirm source identity** — verify the page is from the expected
   organisation (check domain and byline)
2. **Confirm publication date** — look for the date on the page itself,
   not just what the search showed. Search results can show a crawl date,
   not the publication date.
3. **Extract relevant information:**
   - Key statistics with their exact wording and date reference
   - Definitions or frameworks the source uses
   - Direct quotes (short — for citation accuracy)
   - References the source itself cites (may lead to better primary sources)
4. **Record the extraction immediately:**
   ```
   Source:    [Organisation, Author, Year]
   URL:       [exact URL fetched]
   ACCESSED:  [today's date]
   Tier:      [1/2/3]
   Extracted: [bullet list of specific facts/stats/quotes with
                location note if document is long]
   Answers:   [which sub-question(s) this source addresses]
   ```

---

### Step 3.4 — Handle Retrieval Failures Gracefully

| Failure Type | Response |
|---|---|
| 404 — Page not found | Note "Sought but unavailable: [description]". Do NOT fabricate. Search for an alternative source on the same topic. |
| Paywall — content blocked | Use only the abstract/summary visible in the browser result. Note "Full text unavailable — abstract only". Cite what was accessible. |
| PDF — long document | Target the relevant chapter or section. Do not attempt to read the entire document. |
| Content irrelevant on retrieval | Mark as SKIP. Return to search results for an alternative. |
| Outdated content (>3 years) | Use for historical context only. Flag clearly: "Source is [N] years old — verify current status." |
| Site error/timeout | Retry once after a brief pause. If still failing, seek an alternative source. |

---

### Step 3.5 — Verify Source Currency

For any statistic or finding that is time-sensitive:

1. **Check the publication date** — not the URL date or the date shown in search results
2. **Check if the data itself is dated** — a 2024 report may cite 2022 data.
   Use the data vintage date in the citation, not the report date.
3. **Seek a more current version** — if a source is the right authority but
   the data is old, search again:
   `site:[domain] "[metric name]" [current year]`
4. **Flag dated evidence in the report** — where current data is unavailable,
   state: "As of [date], the most recent available data shows [X]. More current
   data was not available at time of writing."

---

### Step 3.6 — Cross-Verification Protocol

For every key finding (a statistic or claim that materially affects conclusions):

1. **Single-source key claims are not acceptable.** If a key finding appears in
   only one source, search specifically for corroborating or contradicting
   evidence from a second source.
2. **Wikipedia facts must be cross-verified** — for every fact sourced from
   Wikipedia, find the primary source Wikipedia cites and fetch that instead.
   Never cite Wikipedia directly.
3. **Press release facts require verification** — a company's press release
   claiming their product achieved X must be corroborated by independent
   analysis or regulatory data.

---

## 4. Fetch-Only Fallback Workflow (no #tool:browser)

When browser search is unavailable, use this reduced workflow:

### Step 4.1 — Construct Known Authoritative URLs

Based on the topic, identify URLs known from training for authoritative sources:

```
World Bank data:     data.worldbank.org
IMF reports:         imf.org/en/Publications
WHO publications:    who.int/publications
India government:    data.gov.in, mospi.gov.in
RBI publications:    rbi.org.in/scripts/PublicationsView.aspx
SEBI reports:        sebi.gov.in/reports.html
OECD:                oecd.org/en/publications.html
EU Open Data:        data.europa.eu
US government data:  data.gov
```

### Step 4.2 — Fetch and Verify

Use #tool:web/fetch on each URL. If the page returns a directory or index,
navigate to the most recent relevant report. Extract and record as per Step 3.3.

### Step 4.3 — Declare the Limitation

Mandatory declaration in Section 1.5 of the report:
> "This report was produced without active web search capability.
> Source URLs were constructed from training knowledge and retrieved
> via #tool:web/fetch. Source currency has been verified to the extent
> possible, but readers should independently verify any time-sensitive
> statistics before acting on this report."

---

## 5. Minimum Browsing Requirements

| Requirement | Standard |
|---|---|
| Minimum search queries executed | 5 distinct queries with different angles |
| Minimum URLs evaluated (search results) | 15 across all searches |
| Minimum URLs fetched (full content) | 8 |
| Minimum Tier 1 sources fetched | 4 |
| Maximum Tier 3 sources in final report | 2 (each cross-verified) |
| Maximum source age for current-event topics | 18 months |
| Maximum source age for structural/background context | 5 years |
| Cross-verification of key findings | Every major statistical claim verified in 2+ sources |

---

## 6. Citation Extraction Standard

When extracting a fact from a retrieved page, record it in this format
immediately — do not rely on memory to reconstruct citations later:

```
FACT:      [exact statistic or claim — use the source's own wording]
CONTEXT:   [what the surrounding paragraph says — for accuracy]
SOURCE:    [Organisation / Author]
DATE:      [publication date of this specific content]
URL:       [exact URL fetched]
ACCESSED:  [today's date]
TIER:      [1/2/3]
QUOTE:     [yes/no — if yes, the exact wording must appear in quotation marks in the report]
```

---

## 7. What NOT to Do

- **NEVER** construct a URL from memory and fetch it without first confirming
  it appears in a browser search result — unless it is a known stable
  government or institution domain listed in Section 4.1
- **NEVER** present a browser search summary as the full source — always use
  #tool:web/fetch to retrieve the full content before citing specific claims
- **NEVER** use a date shown in search results as the publication date —
  always confirm on the fetched page itself
- **NEVER** fabricate a URL if a source is unavailable
- **NEVER** cite Wikipedia as the sole source for any factual claim
- **NEVER** use a source older than 18 months for current-state claims without
  an explicit "As of [date]" caveat
- **NEVER** skip cross-verification for key findings
- **NEVER** count a source as "retrieved" if the fetch failed or returned
  irrelevant content
