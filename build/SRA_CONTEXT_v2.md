# SRA Working Context (Authoritative Session Anchor)
_Last updated: Mar 3, 2026 — 00:15 ET_

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
| Python venv | `/Volumes/Overflow/Repositories/d2.rescor.net/.venv/` Python 3.11.11 | Has pypdf, python-docx, jinja2, Pillow, lxml. **Use full path** — system python3 is 3.9.6 |
| pdflatex | `/Library/TeX/texbin/pdflatex` TeX Live 2026/BasicTeX | Packages: enumitem, colortbl, longtable, booktabs, tabularx, hyperref, fancyhdr, xcolor, graphicx, float, amsmath, amssymb, array. **Run** `eval "$(/usr/libexec/path_helper)"` before using |
| Build script | `/Volumes/Overflow/stride_build/build_deliverables.py` (~1600 lines) | Generates all 3 deliverables in one run (no CLI args) |

### Key Paths

| What | Path |
|---|---|
| Build dir | `/Volumes/Overflow/stride_build/` |
| PDF output | `/Volumes/Overflow/stride_build/output/` |
| LaTeX intermediate | `/Volumes/Overflow/stride_build/tex/` |
| D2 sources | `/Volumes/Overflow/Repositories/d2.rescor.net/diagrams/security-reference-architecture/` |
| PNG render dir | `.../security-reference-architecture/rendering_png_v2/` |
| Extracted policies | `/Volumes/Overflow/stride_build/extracted/` (30 PDFs + 18 DOCX + 11 MD = 731K chars) |
| OneDrive workspace | `/Users/atr/Library/CloudStorage/OneDrive-RESCORLLC/Stride (k12.com)/` |
| Deliverable copies | `.../Stride (k12.com)/Work Papers/` |

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

## Three Deliverables

| # | Deliverable | File | Status | Size |
|---|---|---|---|---|
| 1 | Stride Policy Cross Reference V6 | `Stride_Policy_Cross_Reference_V6.pdf` | Done | 129,268 B |
| 2 | Stride Security Reference Architecture V7 | `Stride_SRA_V7.pdf` | Needs rebuild after diagram fixes | 3,518,622 B |
| 3 | Stride ASR Questionnaire V3 | `Stride_ASR_Questionnaire_V3.pdf` | Done | 162,864 B |

### OneDrive copy status (Work Papers/)
- **Policy Cross Ref V6**: STALE copy in OneDrive has 92,401 B; build has 129,268 B. **Needs copy.**
- **SRA V7**: Will need re-copy after diagram routing fixes complete.
- **ASR V3**: Current (162,864 B matches).

---

## build_deliverables.py Key Components

### Deliverable 1 — Policy Cross Reference V6
- `NIST_CSF` dict (full GV/ID/PR/DE/RS/RC taxonomy)
- `FERPA_SECTIONS` dict (99.1-99.67), `SOX_404_ITGCS` dict (4 domains)
- `POLICY_INVENTORY` list (31 entries with csf/ferpa/sox mappings)
- `ISP_12_DEFINITIONS` — 25 key terms with definitions (enrichment table)
- `IISP_20_CLASSIFICATIONS` — 4 classification levels (enrichment table)
- `_pol_label()`, `_pol_hyperref()`, `_linkify_policy_refs()` — hotlinking helpers
- Bordered tables with `\arrayrulecolor{rulegray}`, `\rowcolor{headgray}` headers
- APPENDIX A/B/C with em-dash headers, hotlinked policy names back to Section 2

### Deliverable 2 — SRA V7
- Embeds 22 D2-rendered PNGs from `rendering_png_v2/`
- `_STRIP_RE` regex strips extraction artifacts ("Stride - ISP X.X" prefixes)
- `extract_section_content()` with bullet heuristic (short lines to `\begin{itemize}`)
- `escape_latex()` handles Unicode chars + LaTeX special chars

### Deliverable 3 — ASR Questionnaire V3
- RSK/STORM diminishing-impact scoring: `f(V,a) = ceil(sum(V_j / 4^j))`
- `rsk_aggregate()`, `rsk_normalize()`, `question_measurement()`, `choice_scores()`
- Per-question `m=` labels, domain RSK aggregates, worked example appendix
- RSK constants: RSK_DAMPING=4, RSK_VMAX=100, RSK_RAW_MAX=134, WEIGHT_MAX=4

---

## D2 Diagram Routing Fixes — IN PROGRESS

User inspected all 22 rendered diagrams and identified 6 with suboptimal connector routing:

### Status Table

| Figure | D2 file | Issue | D2 Rewritten? | PNG Re-rendered? |
|---|---|---|---|---|
| 4 | `04-staff-authentication-flow.d2` | Lines transect diagram objects (backward edge s4 to ra) | YES — intermediate "Context Change" node, dashed connectors, numbered steps, classes, elk-crossingMinimization LAYER_SWEEP | YES (129 KB) |
| 10 | `10-device-trust-architecture.d2` | Gratuitous line crossing (fan-in 3 signals to risk_score, fan-out to 4 outcomes) | NO | NO |
| 16 | `15-implementation-roadmap.d2` | One phase box not like the others (inconsistent sizing/styling) | NO | NO |
| 18 | `18-regulatory-compliance-alignment.d2` | Lines transect diagram objects (mixed child-to-container + child-to-child cross-grid connections) | YES — container-to-container only ("Mandate"/"Inform"/"Produce"), explicit per-child sizing | YES (293 KB) |
| Acronyms | `19-acronyms-and-definitions-map.d2` | Gratuitous line crossing (7 cross-group child-to-child connections) | NO | NO |
| Doc Control | `20-document-control-metadata.d2` | Same — 9 cross-group child-to-child connections + backward edge | NO | NO |

### Analysis and Fix Strategy for Remaining 4

**Figure 10 (`10-device-trust-architecture.d2`)**:
Current structure: 3 groups (signals, decisioning, outcomes), direction: right.
- 3 signals (crowdstrike, defender, tenable) all connect to `decisioning.risk_score` (fan-in)
- `decisioning.risk_score` connects to `decisioning.conditional_access` (internal)
- `decisioning.conditional_access` fans out to 4 outcomes (allow, step_up, limit, deny)
- **Fix**: Use container-to-container connections instead of child-to-child. Or introduce an intermediate aggregation node between signals and decisioning.

**Figure 16 (`15-implementation-roadmap.d2`)**:
Current structure: 5 phase containers, each with label + one child node (p1d, p2d, etc.), direction: right.
- All parents have `width: 220`, children use default `width: 200, height: 100`
- **Fix**: Likely one phase label wraps differently. Equalize all labels to same line count and/or set explicit dimensions on all children.

**Acronyms (`19-acronyms-and-definitions-map.d2`)**:
Current structure: 5 groups (identity_terms, privileged_terms, posture_terms, operations_terms, framework_terms), direction: right.
- 7 cross-group connections zigzagging: iam-to-pam, iga-to-cmdb, ca-to-edr, jit-to-sla, cspm-to-csf, secops-to-zt, csf-to-togaf
- **Fix**: Switch to container-to-container connections with semantic labels, or reorganize into direction: down with groups as rows.

**Doc Control (`20-document-control-metadata.d2`)**:
Current structure: 4 groups (metadata, versioning, governance, distribution), direction: right.
- 9 connections including backward edge (governance.cadence to versioning.current)
- **Fix**: Container-to-container connections, or reorder groups so flow is naturally left-to-right.

---

## Completed Work (cumulative)

### Infrastructure
- D2 CLI v0.7.1 installed, ELK layout engine configured
- Python venv with all packages at `/Volumes/Overflow/Repositories/d2.rescor.net/.venv/`
- BasicTeX 2026 + packages installed via tlmgr
- 25 superseded files deduplicated to `Work Papers/Superseded/`
- All 30 PDFs + 18 DOCX + 11 MD extracted (731K chars)

### Diagrams
- 22 D2 diagrams created with SRA section title blocks
- All 22 rendered to PNG in `rendering_png_v2/`
- Style guide formalized (`STYLE_GUIDE.md`)
- Figure 4 D2 rewritten for clean routing + re-rendered
- Figure 18 D2 rewritten for clean routing + re-rendered

### Deliverable Builds
- Policy Cross Reference V6 — bordered tables, balanced appendix columns, hotlinked policies, ISP 1.2 definitions, IISP 2.0 classifications, auto-linked policy refs in text
- SRA V7 — 22 embedded PNGs, cleaned extraction artifacts, bullet-formatted action items
- ASR Questionnaire V3 — RSK/STORM diminishing-impact scoring with worked example

### Copies to OneDrive
- ASR V3 copied (current)
- Policy Cross Ref V6 — stale copy in OneDrive (92 KB vs 129 KB built)
- SRA V7 — will need re-copy after diagram fixes

---

## Remaining Work (resume here)

1. **Fix 4 remaining D2 diagrams** (Figure 10, Figure 16, Acronyms, Doc Control) — rewrite D2 sources for cleaner routing per analysis above
2. **Re-render all 4** to PNG using the d2 render command
3. **Rebuild all 3 deliverables** (build script always builds all three)
4. **Copy to OneDrive Work Papers/**:
   - Updated Policy Cross Ref V6 (129 KB, already built but stale copy in OneDrive)
   - Updated SRA V7 (after diagram fixes)

### Future / Parked
- Excel version of ASR with live RSK calculations (user said "ruminate, don't build yet")
- LeanIX diagram conversion (blocked — no exports available)
- Governance memo generation from template
