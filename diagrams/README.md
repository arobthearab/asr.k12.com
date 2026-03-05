# Enterprise Trust Security Reference Architecture — D2 Diagram Set

Generated from `SecurityReferenceArchitecture.docx` (January 2026).

This set is intentionally based on document text/tables by section and does **not** use the cover page image.

## Files — SRA Section Mapping

| D2 File | SRA Section |
|---|---|
| `00-legend-conventions.d2` | Cross-cutting diagram reference |
| `01-trust-security-architecture-overview.d2` | §2 — Trust Security Architecture Overview |
| `02-trust-logical-architecture-components.d2` | §2 — Logical Architecture Detail |
| `03-persona-trust-boundaries.d2` | §3 — Personas and Trust Boundaries |
| `04-staff-authentication-flow.d2` | §4 — Identity and Access Architecture (Staff) |
| `05-staff-conditional-access-policy-matrix.d2` | §4 — Identity and Access Architecture (Conditional Access) |
| `06-student-authentication-flow.d2` | §4 — Identity and Access Architecture (Student) |
| `07-customer-authentication-flow.d2` | §4 — Identity and Access Architecture (Customer) |
| `08-identity-and-access-architecture.d2` | §4 — Identity and Access Architecture |
| `09-privileged-trust-architecture.d2` | §5 — Privileged Trust |
| `10-device-trust-architecture.d2` | §6 — Device Trust |
| `11-exposure-and-posture-architecture.d2` | §7 — Exposure and Posture |
| `12-application-and-api-trust-architecture.d2` | §8 — Application and API Trust |
| `13-operational-trust-architecture.d2` | §9 — Operational Trust |
| `14-nist-csf-outcome-mapping.d2` | §10 — NIST CSF 2.0 Outcome Mapping |
| `15-implementation-roadmap.d2` | §11 — Implementation Roadmap |
| `15-implementation-roadmap-v2.d2` | §11 — Implementation Roadmap (v2) |
| `16-executive-summary-and-platform-stack.d2` | §1 — Executive Summary |
| `17-kpi-framework.d2` | §12 — Key Performance Indicators |
| `18-regulatory-compliance-alignment.d2` | §13 — Regulatory Compliance Alignment |
| `19-acronyms-and-definitions-map.d2` | Appendix A — Acronyms and Definitions |
| `20-document-control-metadata.d2` | §14 — Document Control |

## Render

From `d2.rescor.net` root:

```bash
d2 --layout elk diagrams/security-reference-architecture/01-trust-security-architecture-overview.d2
```

Or render all:

```bash
for f in diagrams/security-reference-architecture/*.d2; do d2 --layout elk "$f"; done
```

Landscape-style rendering (8.5x11 wide) is intended: keep rightward flow and export into a landscape page in your document/PDF workflow.

## Notes

- AWS, Azure, and GCP provider icons are included in the overview and cloud posture diagrams.
- Labels incorporate explanatory text from section prose/tables where possible.
- Section coverage follows the document structure (Executive Summary through Document Control).
- A standalone legend is provided in `00-legend-conventions.d2` for shape, size, color, and edge conventions.

