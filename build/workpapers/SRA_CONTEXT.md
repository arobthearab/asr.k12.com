# SRA Working Context (Authoritative Session Anchor)
_Last updated: Mar 2, 2026_

## Purpose
This file preserves working context for the Security Reference Architecture (SRA) so work can be resumed across reboots, new chat sessions, or by other contributors.

---

## Core Design Decisions (Do Not Re‑decide Unless Required)

### 1. Governance Model
- **Excel is the source of truth** for controls, mappings, ownership, tooling, and evidence.
- **Word documents are narrative + snapshots**, not authoritative data stores.
- Governance memos include:
  - Inline cross‑references to SRA sections
  - Appendix D as a *derived snapshot* from the Excel register
- Update order is always:
  1. Excel register
  2. Refresh Word links / snapshots
  3. Regenerate diagrams if structure changed

Key file:
- `SRA_Control_Register.xlsx`

---

### 2. Diagram Strategy (Visio replacement)
- All architecture diagrams are being converted to **D2 (diagrams‑as‑code)**.
- Goal: versionable, auditable, regenerable diagrams aligned to SRA sections.
- Pixel‑perfect fidelity is *not* required; semantic fidelity is.

D2 files created so far:
- `sra_raci_swimlane.d2` — RACI overlay by role × SRA section
- `sra_source_of_truth_pipeline.d2` — Excel → Word → Evidence → Audit loop
- `sra_trust_zones_skeleton.d2` — SRA §5.2 trust zones (logical)
- `stride_platform_reference_architecture.d2` — Platform architecture (from PDF)
- `stride_security_reference_architecture.d2` — Security architecture (from PDF)

Rendering:
- Use D2 CLI or VS Code D2 extension to export SVG for Word/Confluence.

---

### 3. Source Diagrams Converted
The only “real” diagrams available were embedded structurally (not as images) in:
- `StrideReferenceEnterpriseArchitecture 1.pdf`

Converted faithfully to D2:
- Platform & Reference Architecture
- Security Reference Architecture

Not accessible yet (require exports/screenshots):
- LeanIX diagrams (Application, Platform, Data, Integration)
- Network diagrams (e.g., “RESTON OFFICE”)
- AI/MLOps diagrams (placeholders only)

---

### 4. SRA Alignment
D2 diagrams and governance artifacts align to:
- SRA §§6–13 (Governance, IAM, AppSec, Data, Infra, Monitoring, Resilience, Assurance)
- NIST CSF 2.0 mappings already captured in the Excel register
- RACI model consistent with STRIDE GV.RR policy intent

---

## How to Resume This Work in a New Session

Say (or paste):
> “Use the context from `SRA_CONTEXT.md`. Resume SRA work.”

Then continue from:
- Updating `SRA_Control_Register.xlsx`
- Converting additional diagrams to D2 as they become available
- Embedding rendered SVGs into SRA / governance documents

---

## Open Items / Next Logical Steps
- Convert LeanIX‑exported diagrams to D2 when available (blocked — no exports in workspace as of Mar 2, 2026)
- Convert C3 Service drawio diagrams to D2 if structural data becomes available (4 PNGs in SCTASK0153206 folder)
- Generate remaining 7 governance memos (§4 IAM, §6 Device, §7 Exposure, §8 App/API, §9 Operational, §12 KPI, §13 Compliance) using `GOVERNANCE_MEMO_TEMPLATE.md`
- Convert governance memos from Markdown to DOCX for formal distribution

## Completed Items (Mar 2, 2026)
- ✅ Tied all 22 D2 diagrams to SRA document sections via **SRA §N** subtitle in title blocks
- ✅ Updated README.md with authoritative file → SRA-section mapping table
- ✅ Formalized D2 style guide (`STYLE_GUIDE.md`) covering naming, title blocks, config, palette, sizing, icons, rendering, and lifecycle
- ✅ Re-rendered all 22 diagrams to SVG + PNG v3 (`rendering_svg_v3/`, `rendering_png_v3/`)
- ✅ Created `SRA_Control_Register.xlsx` with 5 sheets: Control Register, NIST CSF Crosswalk, Evidence Traceability, Diagram Inventory, Metadata
- ✅ Created governance memo template (`GOVERNANCE_MEMO_TEMPLATE.md`) and exemplar memo (`GOV_MEMO_SRA_S5_Privileged_Trust.md`)