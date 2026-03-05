# NIST CSF 2.0 Subcategory Mapping — Top-Level Document Headers

This matrix maps TSRA top-level headers to representative NIST CSF 2.0 subcategory IDs and implementation status.

| Document Section (Top-Level Header) | Representative NIST CSF 2.0 Subcategory IDs | Implementation Status | Notes |
|---|---|---|---|
| 1. Executive Summary | GV.OC-01, GV.RM-01, GV.OV-01 | Partially Implemented | Strategic direction and governance context are defined; maturity rollout continues. |
| 2. Trust Security Architecture Overview | GV.PO-01, PR.AA-01, PR.PS-01 | Partially Implemented | Trust model and enforcement intent are defined with implementation in progress. |
| 3. Personas and Trust Boundaries | PR.AA-01, PR.AA-03, ID.AM-01 | Partially Implemented | Persona-specific controls are mapped; operational consistency is still maturing. |
| 4. Identity and Access Architecture | PR.AA-01, PR.AA-02, PR.PS-01 | Partially Implemented | Core identity controls are present with staged enhancements. |
| 5. Privileged Trust (Delinea and Entra PIM) | PR.AA-05, PR.PS-02, DE.CM-03 | Partially Implemented | Current controls exist; future-state PIM maturity is planned/in flight. |
| 6. Device Trust (CrowdStrike and Defender) | PR.PS-03, DE.CM-01 | Partially Implemented | Device telemetry and control signals are active with integration growth planned. |
| 7. Exposure and Posture (Tenable VM and CSPM) | ID.RA-01, DE.CM-02, PR.PS-04 | Partially Implemented | Vulnerability and posture capabilities are active with workflow optimization ongoing. |
| 8. Application and API Trust (Sonatype, Burp Suite, Salt) | PR.DS-01, PR.PS-05, DE.CM-07 | Partially Implemented | SDLC/runtime controls are in place; API-specific maturity is partially future-state. |
| 9. Operational Trust (ServiceNow SecOps, CMDB, Tagging) | DE.CM-06, RS.MA-01, RC.RP-01 | Partially Implemented | Operations and response are active; CMDB/tagging maturity continues. |
| 10. NIST CSF 2.0 Outcome Mapping | GV.OV-01, ID.RA-01, PR.AA-01, DE.CM-01, RS.MA-01, RC.RP-01 | Fully Implemented | Mapping section is complete as documentation baseline. |
| 11. Implementation Roadmap | GV.SC-01, GV.RM-02 | Partially Implemented | Governance and sequencing are documented; execution is phased. |
| 12. Key Performance Indicators (KPIs) | GV.OV-02, DE.CM-08, RS.MA-04 | Partially Implemented | Measurement model is defined and being operationalized. |
| 13. Regulatory Compliance Alignment (SOX, FERPA) | GV.RM-03, GV.OV-03, RC.CO-03 | Partially Implemented | Compliance alignment exists; evidence automation/maturity continues. |
| Document Control | GV.OV-01, GV.PO-02 | Fully Implemented | Document governance metadata and control artifacts are in place. |

## Evidence Traceability Matrix

This matrix extends the section-to-subcategory mapping with representative evidence sources, system-of-record context, control owners, and review frequencies.

| Document Section (Top-Level Header) | Representative NIST CSF 2.0 Subcategory IDs | Evidence Source / System of Record | Control Owner | Review Frequency | Implementation Status |
|---|---|---|---|---|---|
| 1. Executive Summary | GV.OC-01, GV.RM-01, GV.OV-01 | Architecture governance brief; executive review notes | Security Architecture / GRC | Quarterly | Partially Implemented |
| 2. Trust Security Architecture Overview | GV.PO-01, PR.AA-01, PR.PS-01 | TSRA baseline diagrams and design decisions | Security Architecture | Quarterly | Partially Implemented |
| 3. Personas and Trust Boundaries | PR.AA-01, PR.AA-03, ID.AM-01 | Persona boundary matrix; identity inventory extracts | IAM + Architecture | Quarterly | Partially Implemented |
| 4. Identity and Access Architecture | PR.AA-01, PR.AA-02, PR.PS-01 | Entra policy exports; IAM standards | IAM | Monthly | Partially Implemented |
| 5. Privileged Trust (Delinea and Entra PIM) | PR.AA-05, PR.PS-02, DE.CM-03 | PIM role assignments; privileged session audit logs | IAM + Security Operations | Monthly | Partially Implemented |
| 6. Device Trust (CrowdStrike and Defender) | PR.PS-03, DE.CM-01 | EDR posture dashboards; compliance policy reports | Endpoint Security | Weekly | Partially Implemented |
| 7. Exposure and Posture (Tenable VM and CSPM) | ID.RA-01, DE.CM-02, PR.PS-04 | Vulnerability scans; CSPM posture trend reports | Vulnerability Management | Weekly | Partially Implemented |
| 8. Application and API Trust (Sonatype, Burp Suite, Salt) | PR.DS-01, PR.PS-05, DE.CM-07 | SCA/SAST reports; API test findings; remediation tickets | AppSec | Per Release | Partially Implemented |
| 9. Operational Trust (ServiceNow SecOps, CMDB, Tagging) | DE.CM-06, RS.MA-01, RC.RP-01 | SecOps incident records; CMDB linkage and tagging evidence | Security Operations + ITSM | Weekly | Partially Implemented |
| 10. NIST CSF 2.0 Outcome Mapping | GV.OV-01, ID.RA-01, PR.AA-01, DE.CM-01, RS.MA-01, RC.RP-01 | Control mapping register and crosswalk workbook | GRC | Quarterly | Fully Implemented |
| 11. Implementation Roadmap | GV.SC-01, GV.RM-02 | Roadmap milestones; dependency tracker; risk acceptance records | Program Management | Monthly | Partially Implemented |
| 12. Key Performance Indicators (KPIs) | GV.OV-02, DE.CM-08, RS.MA-04 | KPI scorecards; trend and threshold breach records | Security Operations + GRC | Monthly | Partially Implemented |
| 13. Regulatory Compliance Alignment (SOX, FERPA) | GV.RM-03, GV.OV-03, RC.CO-03 | Compliance control narratives; audit workpapers | Compliance | Quarterly | Partially Implemented |
| Document Control | GV.OV-01, GV.PO-02 | Version history; approval chain; document repository metadata | Document Control | On Change | Fully Implemented |

## Status Legend

- **Fully Implemented**: Mapped subcategories are implemented and documented in the current architecture state.
- **Partially Implemented**: Mapped subcategories are implemented for some systems/personas or require maturity enhancements.
- **Not Implemented**: Mapped subcategories are identified but not yet implemented in the current state.

Note: Subcategory IDs are representative for architecture-to-control traceability and may be refined during formal control assessment.
Operational note: Evidence references are representative artifacts and should be aligned to the formal control library during assessment cycles.

## Goal State Backlog

- Deferred enhancement: Produce an audit-ready DOCX variant extending the evidence matrix with `Evidence ID`, `Artifact Location`, and `Last Verified Date` columns for assessor-ready traceability.
