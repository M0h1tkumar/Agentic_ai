---
name: research-report
description: >
  Research report skill v2.0. Governs the structure, section content,
  word floors, citation format, APA 7th references, and quality gates
  (Q1–Q13) for all reports produced by the research agent.
  Composes with the web-research skill — this skill handles REPORTING;
  web-research handles SOURCING.
---

# Skill: Research Report Structure — v2.0

> This skill governs the STRUCTURE and QUALITY of the finished report.
> It defines 11 mandatory sections, word floors per section, inline
> citation rules, reference format, and the Q1–Q13 quality gate
> checklist. It composes with the web-research skill.

---

## 1. Report Structure — 11 Mandatory Sections

Every report produced by the research agent must contain all 11 sections
below, in this order, with no section omitted.

| # | Section Title | Word Floor | Key Content |
|---|---|---|---|
| 1 | Research Scope & Methodology | 300 words | Research question, scope, method, limitations, web research notes |
| 2 | Executive Summary | 400 words | Standalone summary: question, 3–5 key findings, 2–3 top recommendations |
| 3 | Context & Background | 500 words | Why this topic matters now; historical context; key definitions |
| 4 | Research Findings | 800 words | ≥ 4 themed findings subsections, each ≥ 200 words of continuous prose |
| 5 | Data & Evidence Summary | 200 words + table | Key statistics table; all figures sourced and dated |
| 6 | Analysis | 500 words | Named analytical framework applied; strengths, weaknesses, tensions |
| 7 | Implications | 450 words | Three time horizons: near-term (0–12 months), medium-term (1–3 years), long-term (3+ years) |
| 8 | Recommendations | 350 words + table | ≥ 5 SMART recommendations in structured table; priority ratings |
| 9 | Knowledge Gaps & Limitations | 200 words | What remains unknown; confidence caveats; what would change the conclusions |
| 10 | Conclusion | 200 words | Synthesis of the primary research question answer; forward-looking close |
| 11 | References | No word floor | All sources in APA 7th edition; tier and ACCESSED date on every entry |

**Total prose floor: 3,900 words minimum** (references excluded).
Combined with references, total document must reach **≥ 4,000 words**.

---

## 2. Section-by-Section Content Rules

### Section 1 — Research Scope & Methodology

Required sub-sections:

**1.1 Primary Research Question**
State the single precise question this report answers.
Format: one sentence, no sub-bullets.

**1.2 Scope**
- Geographic scope (global / regional / country)
- Time horizon (current state / trend / projection)
- Intended audience

**1.3 Methodology**
How the research was conducted. Reference the web-research skill explicitly:
"Research was conducted using the Web Research Skill v1.0: web search
discovery followed by full-content retrieval and source verification."

**1.4 Limitations**
Known constraints: source availability, data recency, scope exclusions.

**1.5 Web Research Notes** ← added by the research agent
Populated by the agent at research time:
- Browser tool status (AVAILABLE / UNAVAILABLE)
- Fetch tool status (AVAILABLE / UNAVAILABLE)
- Queries executed (N)
- URLs evaluated (N)
- URLs fetched — full content retrieved (N)
- Source tier breakdown: Tier 1: N | Tier 2: N | Tier 3: N
- Date range of sources: [oldest] → [newest]
- Sources sought but unavailable: [list or "none"]

---

### Section 2 — Executive Summary

**Must stand alone.** A reader who reads only this section must be able to:
- Understand the research question
- Know the 3–5 most important findings (with data points)
- Know the 2–3 highest-priority recommendations
- Understand any critical caveats

Rules:
- Write in plain English — no jargon without definition
- Include at least 3 specific statistics or data points from the research
- Name the top recommendation explicitly
- Do NOT use forward-references to later sections ("see Section 4...")
- Minimum 400 words of continuous prose (not a bullet list)

---

### Section 3 — Context & Background

Rules:
- Open with why this topic is significant now — what has changed recently?
- Define the key terms or concepts a board-level reader needs
- Provide historical trajectory: where did the topic come from?
- Set the baseline that makes the findings in Section 4 meaningful
- Every factual claim must have an inline citation in (Author/Org, Year) format
- Minimum 500 words

---

### Section 4 — Research Findings

Rules:
- Minimum 4 themed finding subsections (e.g., 4.1, 4.2, 4.3, 4.4)
- Each subsection: minimum 200 words of continuous analytical prose
- Each subsection must be anchored to at least one cited data point
- Subsection headings must reflect the finding content, not be generic
  (GOOD: "4.1 — AI Adoption in Indian Banking Reaches 38% of Processes"
   BAD:  "4.1 — Finding 1")
- For EVERY statistic or data point:
  - State the data date, not just the report publication date
  - Name the source organisation inline
  - If cross-verified: append [verified: Org2, Year]
  - If single source only: append [single source — verify]
- Do NOT use bullet lists as a substitute for analytical prose

---

### Section 5 — Data & Evidence Summary

A structured table of all key statistics used in the report.

Required table format:

| Metric | Value | Source Organisation | Data Date | Tier | Verified |
|---|---|---|---|---|---|
| [metric name] | [value with unit] | [org] | [date data refers to] | [1/2/3] | Y / N (single source) |

Rules:
- Every row must be populated — no blanks
- "Data Date" is the date the data refers to, not the report date
- "Verified" = Y only if confirmed in 2+ independent sources
- Minimum 8 rows (one per key statistic in the report)
- Below the table: a paragraph noting any significant data gaps or conflicts
  between sources, and what those mean for the report's conclusions

---

### Section 6 — Analysis

Rules:
- **Name the specific analytical framework used** in the opening sentence.
  Acceptable frameworks: SWOT, PESTLE, Porter's Five Forces, VRIO,
  McKinsey 7-S, Technology Adoption Lifecycle, Diffusion of Innovation,
  Risk-Return Matrix, or equivalent with citation.
- Apply the framework rigorously — do not use it as a label and then
  write generic prose. Each element of the framework must be explicitly
  populated with evidence from the research.
- Identify tensions, contradictions, or trade-offs surfaced by the data
- Connect analytical conclusions explicitly to the research question
- Minimum 500 words
- Every analytical claim grounded in the findings must have an inline citation

---

### Section 7 — Implications

Must cover all three time horizons — each horizon gets its own sub-section:

**7.1 Near-Term Implications (0–12 months)**
What happens if current trends continue? What actions must be taken now?
Minimum 150 words.

**7.2 Medium-Term Implications (1–3 years)**
What structural changes are underway? What decisions made now will constrain
or enable outcomes in 1–3 years? Minimum 150 words.

**7.3 Long-Term Implications (3+ years)**
What does the trajectory suggest about the landscape in 3–5+ years?
What assumptions does this depend on? Minimum 150 words.

Rules:
- Each horizon must be explicitly labelled (not merged)
- Each horizon must reference specific findings from Section 4
- Avoid generic language ("this will be important") — be specific about
  who is affected and how

---

### Section 8 — Recommendations

Required table format:

| # | Recommendation | Owner | Timeline | Success Metric | Priority |
|---|---|---|---|---|---|
| R1 | [Specific action — verb-led, named actor, measurable outcome] | [Who] | [When] | [How measured] | High / Medium / Low |

Rules:
- Minimum 5 recommendations
- Every recommendation must be SMART:
  - **Specific**: names a concrete action and who takes it
  - **Measurable**: states how success is measured
  - **Achievable**: grounded in the evidence from the report
  - **Relevant**: directly addresses a finding or implication
  - **Time-bound**: states a deadline or milestone
- After the table: a paragraph of 150+ words explaining the rationale for
  the priority ordering and any dependencies between recommendations
- Do NOT write generic recommendations ("invest in technology", "build
  capability") without specifics

---

### Section 9 — Knowledge Gaps & Limitations

Rules:
- Explicitly state what the research could NOT establish, and why
- State the impact of each gap on confidence in the conclusions
  (e.g., "The absence of [X] means the finding in Section 4.2 should be
  treated as directional rather than definitive")
- List sources that were sought but unavailable
- List sub-questions from Section 1 that could not be answered satisfactorily
- State what additional research or data would resolve the key gaps
- Minimum 200 words

---

### Section 10 — Conclusion

Rules:
- Return to the primary research question from Section 1.1
- State the answer directly in the first sentence
- Synthesise the most significant findings in 2–3 sentences
- Close with a forward-looking statement about what this means for
  decision-makers
- Do NOT introduce new findings or data not already in the report
- Minimum 200 words

---

### Section 11 — References

**Format: APA 7th Edition** throughout.

Required fields for every reference entry:
- Author(s) or Organisation
- Year of publication (in parentheses)
- Title of document/article (italicised for reports/books; roman for articles)
- Source/Publication name
- URL (exact URL fetched — not a search result URL, not a redirect)
- ACCESSED: [date the URL was retrieved]
- [Tier 1 / Tier 2 / Tier 3] — appended in square brackets

**APA 7th format examples:**

Organisation report:
> World Bank. (2024). *World Development Report 2024: The Middle Income Trap*.
> World Bank Group. https://www.worldbank.org/en/publication/wdr2024
> ACCESSED: 22 July 2026. [Tier 1]

Journal article:
> Agarwal, R., & Prasad, J. (2023). Artificial intelligence adoption in
> Indian financial services: Barriers and enablers. *Journal of Financial
> Technology*, 12(3), 45–67. https://doi.org/10.xxxx/xxxxx
> ACCESSED: 22 July 2026. [Tier 2]

News article:
> Sharma, P. (2025, March 14). RBI sets new AI governance framework for banks.
> *The Economic Times*. https://economictimes.indiatimes.com/[article-path]
> ACCESSED: 22 July 2026. [Tier 2]

Rules:
- References must be listed in alphabetical order by author/organisation surname
- No reference may appear in the reference list that is not cited in the body
- No in-body citation may lack a corresponding reference list entry
- Minimum 10 references for any report
- Minimum 6 references must be Tier 1 or Tier 2

---

## 3. Inline Citation Format

In the report body, cite all factual claims using this format:

**(Author/Organisation, Year)**

Examples:
- "AI adoption in Indian banking reached 38% of processes in 2024 (Reserve Bank of India, 2024)."
- "The global AI market is projected to reach USD 1.8 trillion by 2030 (McKinsey Global Institute, 2024; Gartner, 2024)."
- "Regulatory uncertainty remains the primary barrier to adoption (PwC India, 2024) [single source — verify]."

Rules:
- Every factual claim in Sections 3 through 7 must have an inline citation
- Multiple sources for one claim: list all "(Org1, Year; Org2, Year)"
- Pre-trained knowledge with no external source: append [Analyst Perspective]
- Analyst interpretation (even based on cited data): no citation needed if
  clearly framed as analysis ("This suggests...", "The data indicates...")

---

## 4. Writing Standards

**Tone:** Authoritative, precise, and objective. The register is appropriate
for a board presentation or investor briefing — not academic, not journalistic.

**Voice:** Third person. Avoid "I" or "we". Use "the evidence suggests",
"the data indicates", "this analysis finds".

**Structure within sections:**
- Each section opens with a topic sentence stating the section's main point
- Prose is continuous — avoid bullet lists in the main body of Sections 3–7
- Use bold sparingly to highlight only the most critical terms or statistics
- Subheadings within Section 4 and Section 7 are mandatory (numbered: 4.1, 4.2 etc.)
- Tables are permitted in Sections 5 and 8 but must be accompanied by
  interpretive prose — a table never stands alone without commentary

**Numbers and statistics:**
- Always include the unit (%, USD, persons, percentage points)
- For percentages: state the base ("38% of surveyed banks" not "38%")
- For forecasts: include the source's confidence level or scenario label
  if available ("base case forecast", "high scenario")
- Round to no more precision than the source uses

**Hedging protocol:**
- Retrieved and cross-verified facts: use direct language ("adoption has reached...")
- Single-source claims: hedge ("according to X, adoption has reached...")
- Pre-trained knowledge with no current verification: hedge strongly
  ("as of training data, the market was estimated at...")
- Forecasts: always attribute ("[Org] projects that by [year]...")

---

## 5. Quality Gate Checklist — Q1 to Q13

The agent runs this checklist in STEP 5 before conversion. All gates
must pass before the report is saved.

| Gate | Check | Pass Condition |
|---|---|---|
| Q1 | Research question stated in Section 1.1 | One precise sentence present |
| Q2 | Source minimums met | ≥ 10 sources; ≥ 6 Tier 1 or Tier 2 |
| Q3 | Inline citations in Sections 3–7 | Every factual claim has (Org, Year) citation |
| Q4 | Executive Summary stands alone | Contains question, ≥ 3 data points, top recommendation |
| Q5 | Section 4 depth | ≥ 4 subsections; each ≥ 200 words of continuous prose |
| Q6 | Analytical framework named and applied | Framework named in first sentence of Section 6; all elements populated |
| Q7 | All three time horizons present | Sections 7.1, 7.2, 7.3 each present and ≥ 150 words |
| Q8 | SMART recommendations table | ≥ 5 rows; Owner, Timeline, Success Metric, Priority populated |
| Q9 | Knowledge gaps explicit | Each gap has stated impact on confidence level |
| Q10 | Pre-trained content labelled | All [Analyst Perspective] labels in place |
| Q11 | References APA 7th with tier and ACCESSED | Every reference has URL, ACCESSED date, and [Tier N] |
| Q12 | Total word count | `wc -w research-draft.md` returns ≥ 4,000 |
| Q13 | No section below word floor | Each section meets the floor in the table in Section 1 above |
