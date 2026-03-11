# asr.k12.com — Stride (k12.com) Security Assessment

Security Reference Architecture (SRA), Automated Security Review (ASR), and
governance deliverables for the Stride (k12.com) engagement.

## Repository Layout

```
artifacts/          Final client-facing deliverables (docx, xlsx, pdf)
policies/           Stride ISP + IISP policy PDFs (source material)
evidence/           SCTASK attachments and architecture diagrams
workpapers/         Working documents, memos, markdown sources
  superseded/       Historical versions (preserved for audit trail)
diagrams/           D2 diagram sources + rendered PNGs (SRA architecture)
build/              Build scripts and configuration
  asr_questions.yaml  ASR questionnaire (single source of truth)
  build_deliverables.py  LaTeX → PDF pipeline (Policy X-Ref, SRA, ASR)
  build_docx.py     Word document builder (11 deliverables)
  build_excel_asr.py  Excel ASR with live scoring formulas
  extract_all.py    Policy/workpaper text extraction
cypher/             Stride-specific Neo4j overlay scripts for asr.rescor.net
docs/               Project documentation
```

## Build

Requires Python 3.11+ with `pypdf`, `python-docx`, `openpyxl`, `pyyaml`,
`jinja2`, `Pillow`, `lxml`. Also needs `pdflatex` (BasicTeX) for PDF builds.

```bash
# PDF deliverables (Policy Cross Ref V6, SRA V7, ASR V3)
eval "$(/usr/libexec/path_helper)"
python3 build/build_deliverables.py

# Word deliverables (Policy Cross Ref V7, SRA V8, ASR V4, 8 Gov Memos)
python3 build/build_docx.py

# Excel ASR V4 with live formulas
python3 build/build_excel_asr.py
```

## Deliverables

| # | Document | Format | Builder |
|---|----------|--------|---------|
| 1 | Stride Policy Cross Reference V6 | PDF | build_deliverables.py |
| 2 | Stride Security Reference Architecture V7 | PDF | build_deliverables.py |
| 3 | Stride ASR Questionnaire V3 | PDF | build_deliverables.py |
| 4 | Stride Policy Cross Reference V7 | DOCX | build_docx.py |
| 5 | Stride SRA V8 | DOCX | build_docx.py |
| 6 | Stride ASR Questionnaire V4 | DOCX | build_docx.py |
| 7 | Stride ASR Questionnaire V4 | XLSX | build_excel_asr.py |
| 8–15 | Governance Memos (8 sections) | DOCX | build_docx.py |

## Scoring Model

ASR uses a 3-factor scoring model:
- **Answer score**: Ordinal from choices (risk-level scaled)
- **Weight tiers**: Critical=75, High=50, Medium=25, Info=10
- **Classification factor**: Transcendental multiplier based on data classification

Domain aggregation uses the RSK/STORM aggregate function.
