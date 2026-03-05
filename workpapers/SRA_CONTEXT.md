# SRA Working Context (Authoritative Session Anchor)
_Last updated: Mar 4, 2026 — session checkpoint_

## Purpose
This file preserves working context for the Stride (k12.com) security deliverables project so work can be resumed across reboots, new chat sessions, or by other contributors.

---

## How to Resume This Work in a New Session

Say (or paste):
> "Read `Work Papers/SRA_CONTEXT.md` and resume where we left off."

---

## Toolchain

| Tool | Location / Version | Notes |
|---|---|---|
| D2 CLI | `/opt/homebrew/bin/d2` v0.7.1 | ELK layout only (tala commercial/unavailable); **ports not supported** |
| Python venv | `/Volumes/Overflow/Repositories/d2.rescor.net/.venv/` Python 3.11.11 | Has pypdf, python-docx, jinja2, Pillow, lxml, openpyxl, pyyaml. **Use full path** — system python3 is 3.9.6 |
| pdflatex | `/Library/TeX/texbin/pdflatex` TeX Live 2026/BasicTeX | Packages: enumitem, colortbl, longtable, booktabs, tabularx, hyperref, fancyhdr, xcolor, graphicx, float, amsmath, amssymb, array. **Run** `eval "$(/usr/libexec/path_helper)"` before using |
| Build scripts | See table below | |

### Build Scripts

| Script | Purpose | Output |
|---|---|---|
| `build_deliverables.py` (~1790 lines) | 3 LaTeX→PDF deliverables | `output/*.pdf` |
| `build_excel_asr.py` | Excel ASR V4 with live 3-factor formulas | `output/Stride_ASR_Questionnaire_V4.xlsx` |
| `build_docx.py` (~2200 lines) | 11 Word documents (Policy X-Ref V7, SRA V8, ASR V4, 8 Gov Memos) | `output/*.docx` |

### Key Paths

| What | Path |
|---|---|
| Build dir | `/Volumes/Overflow/stride_build/` |
| PDF output | `/Volumes/Overflow/stride_build/output/` |
| LaTeX intermediate | `/Volumes/Overflow/stride_build/tex/` |
| YAML config | `/Volumes/Overflow/stride_build/asr_questions.yaml` |
| D2 sources | `/Volumes/Overflow/Repositories/d2.rescor.net/diagrams/security-reference-architecture/` |
| PNG render dir | `.../security-reference-architecture/rendering_png_v2/` |
| Extracted policies | `/Volumes/Overflow/stride_build/extracted/` (30 PDFs + 18 DOCX + 11 MD = 731K chars) |
| OneDrive workspace | `/Users/atr/Library/CloudStorage/OneDrive-RESCORLLC/Stride (k12.com)/` |
| Artifacts deploy | `.../Stride (k12.com)/Artifacts/` |
| Goal-state questions | `/Volumes/Overflow/stride_build/ASR_QUESTION_GOALS.md` |

### Build command (from any directory)
```bash
eval "$(/usr/libexec/path_helper)" && \
/Volumes/Overflow/Repositories/d2.rescor.net/.venv/bin/python3 \
  /Volumes/Overflow/stride_build/build_deliverables.py 2>&1
```

### D2 render command pattern
```bash
/opt/homebrew/bin/d2 --layout=elk -t 0 --pad 20 <name>.d2 rendering_png_v2/<name>.png
```

---

## Deliverables

### PDF Deliverables (from build_deliverables.py)

| # | Deliverable | File | Status | Size |
|---|---|---|---|---|
| 1 | Stride Policy Cross Reference V6 | `Stride_Policy_Cross_Reference_V6.pdf` | Done | 129,268 B |
| 2 | Stride Security Reference Architecture V7 | `Stride_SRA_V7.pdf` | Done | 3,494,400 B |
| 3 | Stride ASR Questionnaire V3 | `Stride_ASR_Questionnaire_V3.pdf` | Done | 74,540 B |

### Word Deliverables (from build_docx.py)

| # | Deliverable | File | Status |
|---|---|---|---|
| 1 | Policy Cross Reference V7 | `Stride_Policy_Cross_Reference_V7.docx` | Done |
| 2 | SRA V8 | `Stride_SRA_V8.docx` | Done |
| 3 | ASR Questionnaire V4 | `Stride_ASR_Questionnaire_V4.docx` | Done |
| 4–11 | 8 Governance Memos | `Stride_Gov_Memo_*.docx` | Done |

### Excel Deliverable (from build_excel_asr.py)

| # | Deliverable | File | Status |
|---|---|---|---|
| 1 | ASR Questionnaire V4 (live formulas) | `Stride_ASR_Questionnaire_V4.xlsx` | Done |

### Artifacts (deployed to OneDrive)
All Word/Excel deliverables + SRA V7 PDF deployed to `Artifacts/`. PDFs from LaTeX build are NOT deployed to Artifacts (they stay in `output/` only), except SRA V7.

---

## ASR Questionnaire Architecture

### Single Source of Truth
`asr_questions.yaml` — 7 domains, 48 domain questions + 1 classification question = 49 total.

### 3-Factor Scoring Model
```
measurement = INT(answer_score/100 × weight/100 × classification_factor)
```
- **Answer score**: ordinal from choices (20/40/55/70/85 for 5-choice, etc.)
- **Weight tiers**: Critical=100, High=67, Medium=33, Info=13
- **Classification factors**: Low=40, Medium=60, High=80, Critical=100, None=100
- Classification is a "transcendental" question — multiplies all other scores

### Domains (7)
1. Governance and Program Management (12 questions)
2. Identity and Access Management (6 questions, incl. API auth)
3. Data Protection and Privacy (6 questions)
4. Secure Development and Change Management (7 questions)
5. Vulnerability and Threat Management (7 questions)
6. Incident Response and Business Continuity (5 questions)
7. Third-Party and Supply Chain Risk (5 questions)

---

## SRA V7 Gap Annotations (added Mar 4, 2026)

Five sections now have `\colorbox{gapred!10}` gap callouts in both `sra_v7.tex` and `build_deliverables.py`:

| SRA § | Gap Summary |
|---|---|
| §4 Identity & Access | FERPA §99.30/§99.35 consent controls; PR.AA-04, PR.AA-06 unmapped |
| §8 Application & API | API auth standard absent; SOX CM-1, PD-3, PD-4 verification gates missing |
| §9 Operational Trust | DE.CM-06 In Progress; CO-1/CO-4 evidence gaps; DE.AE entirely absent |
| §11 Roadmap | GV.SC-01 Planned; GV.RM-02 In Progress; GV.SC-02–10 unmapped |
| §13 Regulatory | 5 FERPA sections (§99.4/7/12/33/37) without controls; PR.AT unmapped |

### Appendix E — Consolidated Gap Register (new)
Added to both `sra_v7.tex` and `build_deliverables.py`. Contains 13 tracked gaps (GAP-01 through GAP-13) with CSF/regulatory reference, SRA section, description, and priority (High/Medium).

---

## ASR Question Goals (goal-state backlog)

File: `/Volumes/Overflow/stride_build/ASR_QUESTION_GOALS.md`

23 proposed new questions across 8 areas that would bring the questionnaire from 48 → 71 domain questions:

| Area | New Qs | New Domain? |
|---|---|---|
| Risk Management (GV.RM) | 3 | Yes |
| Awareness & Training (PR.AT) | 2 | Yes |
| Adverse Event Analysis (DE.AE) | 3 | Yes |
| Supply Chain (GV.SC) | 4 | Yes |
| SOX Change Mgmt additions | 3 | No (Secure Dev) |
| SOX Computer Ops additions | 2 | No (IR/BC) |
| FERPA additions | 4 | No (Data Protection) |
| IAM enhancements | 2 | No (IAM) |

---

## build_deliverables.py Key Components

### Deliverable 1 — Policy Cross Reference V6
- `NIST_CSF` dict (full GV/ID/PR/DE/RS/RC taxonomy)
- `FERPA_SECTIONS` dict (99.1-99.67), `SOX_404_ITGCS` dict (4 domains)
- `POLICY_INVENTORY` list (31 entries with csf/ferpa/sox mappings)
- `ISP_12_DEFINITIONS` — 25 key terms with definitions (enrichment table)
- `IISP_20_CLASSIFICATIONS` — 4 classification levels (enrichment table)
- `_pol_label()`, `_pol_hyperref()`, `_linkify_policy_refs()` — hotlinking helpers

### Deliverable 2 — SRA V7
- `SRA_SECTIONS` list (13 sections with csf/ferpa/sox/gap keys)
- `CSF_SRA_MAP` (29 mapped subcategories: 25 Implemented, 3 In Progress, 1 Planned)
- `_build_appendix_c()` — NIST CSF 2.0 mapping table
- `_build_appendix_d()` — Evidence traceability matrix (21 artifacts)
- `_build_appendix_e()` — Consolidated Gap Register (13 gaps)
- Embeds 22 D2-rendered PNGs from `rendering_png_v2/`
- Gap rendering: `gap` key → `\colorbox{gapred!10}{\parbox{...}{\small\textbf{Gap ---} ...}}`

### Deliverable 3 — ASR Questionnaire V3
- Internal RSK/STORM scoring — proprietary details stripped from PDF output
- `rsk_aggregate()`, `rsk_normalize()`, `question_measurement()`, `choice_scores()`
- RSK constants: RSK_DAMPING=4, RSK_VMAX=100, RSK_RAW_MAX=134, WEIGHT_MAX=4

---

## Completed Work (cumulative, Mar 4, 2026)

### Infrastructure
- D2 CLI v0.7.1 installed, ELK layout engine configured
- Python venv with all packages at `/Volumes/Overflow/Repositories/d2.rescor.net/.venv/`
- BasicTeX 2026 + packages installed via tlmgr
- 25 superseded files deduplicated to `Work Papers/Superseded/`
- All 30 PDFs + 18 DOCX + 11 MD extracted (731K chars)

### Diagrams
- 22 D2 diagrams created with SRA section title blocks
- All 22 rendered to PNG in `rendering_png_v2/`
- 6 diagrams rewritten for clean routing

### ASR Questionnaire Evolution
- V3: Initial 42 questions across 7 domains
- V3→V4: Added RACI (Q6, Q7), business necessity (Q8), scoping (Q9), productivity (Q10), legal (Q11), EA governance (Q12), out-of-band patching (Q24), human review (Q25), detective controls (Q30), corrective controls (Q31), usage KPIs (Q32), phased deployment (Q39), AI risk (Q40), API auth (IAM domain) = 48 domain questions
- Classification question added as transcendental multiplier
- 3-factor scoring model: answer × weight × classification
- YAML single source of truth (`asr_questions.yaml`)
- Excel V4 with live formulas, Scoring Model sheet, Instructions sheet

### SRA Evolution
- V6: Initial 22-diagram architecture with NIST CSF alignment
- V7: Appendices A–D, per-section FERPA/SOX boxes, gap annotations (§4/8/9/11/13), Appendix E gap register (13 gaps)

### Gap Analysis (Mar 4, 2026)
- Comprehensive control-target analysis: NIST CSF 2.0 (100 subcategories), FERPA 34 CFR Part 99 (18 sections), SOX §404 ITGC (19 controls)
- 29 of 100 CSF subcategories mapped in SRA; 71 unmapped (many not applicable)
- 3 In Progress: GV.RM-02, PR.PS-05, DE.CM-06
- 1 Planned: GV.SC-01
- 5 FERPA sections without architectural controls: §99.4, §99.7, §99.12, §99.33, §99.37
- 3 SOX controls with gaps: CM-1, PD-3, PD-4
- ASR missing: GV.RM, PR.AT, DE.AE domains entirely
- Goal-state: 23 new questions documented in ASR_QUESTION_GOALS.md

### Artifacts Cleanup
- Removed stale PDFs and superseded DOCX files from Artifacts/
- Only current versions deployed

### ASR Web Application (asr.rescor.net) — Mar 4, 2026
- Full-stack scaffold built: React 19 + MUI 7 + Vite 6 (frontend :5174) / Express 4 + @rescor/core-* (API :3100) / Neo4j 5 (graph DB)
- Repo: `/Volumes/Overflow/Repositories/asr.rescor.net/` — previous scaffold moved to `legacy2/`
- Dedicated Neo4j container `asr-neo4j` on ports 17474/17687 (docker-compose.yml, creds: neo4j/asrdev123)
- Cypher DDL seeded: 9 uniqueness constraints, 5 indexes, ScoringConfig, 4 WeightTiers, ClassificationQuestion + 5 factor choices, 7 Domains, 48 Questions (with per-question choiceScores), 20 Policies, 12 CSF Subcategories, all relationship edges
- Scoring engine (RSK/STORM) fully configurable — four admin-tunable dials, zero hardcoded constants:
  1. ScoringConfig node (dampingFactor=4, rawMax=134, ratingThresholds, ratingLabels)
  2. ClassificationChoice.factor (40–100)
  3. WeightTier.value (Critical=100, High=67, Medium=33, Info=13)
  4. Question.choiceScores (per-question override arrays)
- API routes verified: GET /api/config, POST /api/reviews, PUT /api/reviews/:id/answers, GET /api/health
- Frontend: DashboardPage (review table + New Review dialog), ReviewPage (placeholder for ClassificationBanner, DomainSection, QuestionCard, ScoreDashboard components)
- Client-side scoring mirror + localStorage draft adapter + typed API client
- Existence constraints commented out (Community Edition limitation)
- Both servers running and proxied — ready for UI component buildout

---

## Remaining Work / Parked Items

- **HIGH PRIORITY — Data Governance coverage**: Add SRA sections AND ASR questions for data governance controls (data masking, DLP, classification enforcement, retention policies, etc.). Both deliverables currently lack explicit coverage of this area.
- **ASR web app — next steps**: Build ReviewPage components (ClassificationBanner, DomainSection, QuestionCard, ScoreDashboard, ReviewActions)
- **Goal-state ASR questions**: 23 proposed questions in `ASR_QUESTION_GOALS.md` — not yet added to YAML or built
- LeanIX diagram conversion (blocked — no exports available)
- Governance memo generation from template (8 memos already built in Word)
- Close gaps in ASR Gap Register (policy + SRA reciprocal updates needed)
