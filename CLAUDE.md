# Claude Instructions — asr.k12.com

## Mandatory: Read Cross-Project Patterns First

Before writing any code or making any changes, read:

```
/Volumes/Overflow/Repositories/core.rescor.net/docs/PROJECT-PATTERNS.md
```

This file defines mandatory patterns for all RESCOR projects.

## Key Facts

- **Client**: Stride (k12.com)
- **Engagement**: Security Reference Architecture + Automated Security Review
- **Build toolchain**: Python 3.11+ scripts in `build/`
- **LaTeX**: BasicTeX 2026 for PDF generation (`eval "$(/usr/libexec/path_helper)"` before `pdflatex`)
- **D2 CLI**: `/opt/homebrew/bin/d2` v0.7.1 (ELK layout only)
- **Single source of truth**: `build/asr_questions.yaml` (7 domains, 48 questions + classification)
- **Scoring**: RSK/STORM 3-factor model (answer × weight × classification)
- **All paths**: Repo-relative via `Path(__file__).resolve().parent`
- **Diagrams**: 22 D2 sources in `diagrams/`, rendered PNGs in `diagrams/rendering_png_v2/`

## Build Commands

```bash
# PDF deliverables
eval "$(/usr/libexec/path_helper)"
python3 build/build_deliverables.py

# Word deliverables
python3 build/build_docx.py

# Excel ASR
python3 build/build_excel_asr.py

# Extract policy/workpaper text
python3 build/extract_all.py
```

## Directory Structure

| Directory | Purpose |
|-----------|---------|
| `artifacts/` | Final client-facing deliverables |
| `policies/` | Stride ISP + IISP policy PDFs |
| `evidence/` | SCTASK attachments, architecture diagrams |
| `workpapers/` | Working documents, memos, markdown |
| `workpapers/superseded/` | Historical versions |
| `diagrams/` | D2 sources + rendered PNGs |
| `build/` | Build scripts, YAML config, templates |
| `build/output/` | Generated output (gitignored) |
| `build/extracted/` | Extracted text JSON (gitignored) |
| `cypher/` | Stride-specific Neo4j overlay scripts for asr.rescor.net |
| `docs/` | Project documentation |

## ASR Web Application Overlay

Stride-specific Neo4j seed data lives in `cypher/`.
To apply it when setting up the asr.rescor.net web application:

```bash
npm run cypher:setup -w api -- --overlay /Volumes/Overflow/Repositories/asr.k12.com/cypher
```
