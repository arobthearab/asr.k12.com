# Governance Memo: SRA §13 — Regulatory Compliance Alignment

**Document Classification:** Internal / Controlled  
**SRA Section Reference:** §13  
**Version:** 1.0 — Draft  
**Date:** March 2, 2026  
**Control Owner:** Compliance  
**Approved By:** *[Pending — Executive Security Leadership]*  

---

## 1. Purpose and Scope

This governance memo establishes the security architecture governance position for **Regulatory Compliance Alignment** as defined in the Trust Security Reference Architecture (TSRA), Section §13 — Regulatory Compliance Alignment (SOX, FERPA).

**Scope:**
- SOX (Sarbanes-Oxley Act) — IT General Controls (ITGCs) for logical access, program change management, computer operations, and segregation of duties applicable to systems supporting financial reporting
- FERPA (Family Educational Rights and Privacy Act) — protection of student education records, access controls, and breach notification requirements
- Contractual commitments — security obligations derived from customer contracts and partnership agreements
- Control framework alignment: TOGAF (enterprise architecture), NIST CSF 2.0 (control mapping), NIST SP 800-207 (Zero Trust)
- Six implemented control domains: Identity & Access Management, Privileged Access Management, Application Security Controls, Device Posture Controls, Exposure & Vulnerability Management, Incident Detection & Response
- Evidence and assurance model: control evidence artifacts, risk-control-evidence traceability, audit and attestation readiness

**Exclusions:**
- Domain-specific control implementation details (covered in respective governance memos: §4–§9)
- Legal interpretation of regulatory requirements (deferred to Legal/Compliance counsel)
- Non-security regulatory obligations (e.g., financial reporting controls outside IT scope)

**Authoritative References:**
- Trust Security Reference Architecture (TSRA), §13
- SRA Control Register (`SRA_Control_Register.xlsx`), Control ID: CTRL-013
- D2 Architecture Diagram: `18-regulatory-compliance-alignment.d2`
- STRIDE ISP — Governance, Risk, and Compliance (GV.RM, GV.OV, RC.CO)

---

## 2. Governance Authority

| Role | Responsibility | RACI |
|---|---|---|
| Compliance | Owns regulatory compliance mapping, manages control narratives, coordinates audit readiness activities | Accountable |
| Security Architecture | Ensures architecture controls map to regulatory requirements; maintains traceability in the SRA | Responsible |
| GRC | Validates control effectiveness, manages risk acceptance register, produces compliance dashboards | Responsible |
| Domain Control Owners (IAM, Endpoint, AppSec, VulnMgmt, SecOps) | Produce evidence artifacts within their respective domains for regulatory validation | Consulted |
| Legal | Advises on regulatory interpretation and breach notification obligations | Consulted |
| Executive Security Leadership | Approves compliance posture, risk acceptance for unresolved findings, and audit response strategy | Approver |

*RACI assignments align to STRIDE GV.RR policy intent.*

---

## 3. Architecture Summary

The Regulatory Compliance Alignment architecture establishes the traceability chain from external regulatory drivers through control frameworks to implemented control domains and evidence assurance:

**Regulatory Drivers:**
- **SOX (Sarbanes-Oxley)**: IT General Controls requirements for systems supporting financial reporting — logical access, change management, computer operations, and SoD
- **FERPA (Family Educational Rights and Privacy Act)**: Protection of student education records — access controls, audit logging, disclosure restrictions, and breach notification
- **Contractual Commitments**: Security obligations in customer contracts and partnership agreements that impose controls beyond baseline regulatory requirements

**Control Frameworks:**
- **TOGAF**: Enterprise architecture methodology guiding the structural organization of the TSRA
- **NIST CSF 2.0**: Primary control mapping framework — all SRA controls are mapped to CSF subcategories with implementation status tracking
- **NIST SP 800-207 (Zero Trust)**: Zero Trust principles inform identity-centric access controls (§4), privileged access (§5), and device trust (§6)

**Implemented Control Domains:**
Each regulatory requirement maps through the control frameworks to one or more of six implemented control domains:

| Control Domain | SRA Section | Primary Tooling | Key SOX Relevance | Key FERPA Relevance |
|---|---|---|---|---|
| Identity & Access Management | §4 | Entra ID, Okta CIAM, SailPoint | Logical access, user account management, SoD | Access to student records |
| Privileged Access Management | §5 | Delinea, Entra PIM | Privileged access restriction and monitoring | Admin access to student data |
| Device Posture Controls | §6 | CrowdStrike, Defender | Endpoint protection for financial systems | Device controls for FERPA-scope apps |
| Exposure & Vulnerability Mgmt | §7 | Tenable VM, CSPM | IT risk assessment, secure configuration | Vulnerability management for student systems |
| Application Security Controls | §8 | Sonatype, Burp Suite, Salt | Program change management, code security | Application testing for student data apps |
| Incident Detection & Response | §9 | ServiceNow SecOps | Monitoring, incident response, evidence | Incident handling for student data |

**Evidence and Assurance:**
- **Control Evidence Artifacts**: Each domain control owner produces evidence artifacts (policy exports, scan reports, audit logs, certification records) that validate control effectiveness
- **Risk-Control-Evidence Traceability**: The SRA Control Register (`SRA_Control_Register.xlsx`) provides bidirectional traceability from regulatory requirements → NIST CSF subcategories → SRA controls → evidence sources
- **Audit and Attestation Readiness**: Evidence is organized for assessor consumption with defined retention periods, artifact locations, and verification dates

> **Cross-References:**
> - All domain governance memos providing evidence: §4, §5, §6, §7, §8, §9
> - NIST CSF 2.0 outcome mapping: SRA §10
> - KPI framework for compliance metrics: SRA §12
> - Executive governance oversight: SRA §1

**Current-State Architecture Diagram:**

> See: `18-regulatory-compliance-alignment.d2` (rendered in `rendering_svg_v3/` and `rendering_png_v3/`)

---

## 4. NIST CSF 2.0 Alignment

| NIST CSF 2.0 ID | Function | Subcategory Description | Implementation Status |
|---|---|---|---|
| GV.RM-03 | Govern | Cybersecurity risk management activities and outcomes are included in enterprise risk management processes | Partially Implemented |
| GV.OV-03 | Govern | Risk management strategy and results are documented and developed through a coordinated approach | Partially Implemented |
| RC.CO-03 | Recover | Recovery activities and progress are communicated to designated internal and external stakeholders | Partially Implemented |

*Source: SRA Control Register, "NIST CSF Crosswalk" sheet, filtered to CTRL-013.*

**Gap Notes:**
- **GV.RM-03**: Cybersecurity risk management is integrated into the TSRA governance model, and control outcomes are tracked in the SRA Control Register. Gap: formal integration with enterprise risk management (ERM) processes beyond IT security is in progress
- **GV.OV-03**: Risk management strategy is documented through the TSRA and governance memos; results are tracked via the control register and KPI framework. Gap: automated compliance dashboarding that consolidates domain-level evidence into a single view is not yet operational
- **RC.CO-03**: Recovery communication protocols exist for major incidents. Gap: structured regulatory notification workflows (especially FERPA breach notification) need formalization and testing

---

## 5. Control Objectives and Requirements

| Control ID | Control Description | Primary Tooling | Evidence Source | Review Frequency |
|---|---|---|---|---|
| CTRL-013 | Regulatory compliance controls including SOX ITGC alignment, FERPA compliance, control narratives, evidence traceability, and audit readiness | Compliance framework; SRA Control Register | Compliance control narratives; audit workpapers | Quarterly |

**Key Requirements:**
1. All SRA controls must maintain documented traceability from regulatory requirements through NIST CSF 2.0 subcategories to implementation and evidence artifacts
2. SOX ITGC control narratives must be reviewed and updated annually, or upon material changes to underlying systems or controls
3. FERPA compliance documentation must include access control inventories, audit logging confirmation, and breach notification procedures for all systems processing student data
4. Evidence artifacts must be organized by control domain with defined artifact locations, retention periods, and last-verified dates in the SRA Control Register
5. Compliance gaps identified through audit or self-assessment must be tracked in the risk acceptance register with remediation plans and target dates
6. Annual compliance readiness assessments must be conducted prior to external audit cycles

---

## 6. Implementation Status and Roadmap

**Current Status:** Partially Implemented

**Maturity Assessment:**
- **In place:** NIST CSF 2.0 subcategory mapping complete for all 14 SRA sections; SRA Control Register with evidence traceability; SOX ITGC control narratives for identity and access domains; FERPA access control documentation for primary student-facing applications; audit-ready governance memo framework
- **In flight:** Evidence automation for domain control artifacts; compliance dashboard consolidation; FERPA breach notification workflow formalization; SOX ITGC narrative expansion to Tenable and ServiceNow domains
- **Deferred:** Automated evidence collection and freshness monitoring; GRC platform integration (e.g., ServiceNow GRC module); contractual commitment compliance tracking automation

**Roadmap Alignment:**
> See: SRA §11, Implementation Roadmap — cross-cutting governance strand  
> Diagram: `15-implementation-roadmap-v2.d2`

| Milestone | Target Date | Status |
|---|---|---|
| SOX ITGC narrative expansion (all domains) | Q2 2026 | In Flight |
| FERPA breach notification workflow formalization | Q2 2026 | In Flight |
| Evidence automation for domain artifacts | Q3 2026 | Planned |
| Compliance dashboard consolidation | Q3 2026 | Planned |
| GRC platform integration | Q4 2026 | Deferred |
| Automated evidence freshness monitoring | Q1 2027 | Deferred |
| Contractual commitment tracking automation | Q1 2027 | Deferred |

---

## 7. Key Performance Indicators

| KPI | Metric Type | Target / Threshold | Cadence | Owner |
|---|---|---|---|---|
| SOX ITGC control narrative currency | Coverage % | 100% of narratives reviewed within trailing 12 months | Quarterly | Compliance |
| FERPA compliance documentation completeness | Coverage % | 100% of FERPA-scope systems with documented access controls and audit logging | Quarterly | Compliance |
| Evidence artifact freshness | Coverage % | ≥ 95% of evidence artifacts verified within defined cadence | Quarterly | GRC |
| Compliance gap remediation rate | Coverage % | 100% of identified gaps with active remediation plans | Quarterly | GRC |
| Audit finding closure rate | Time-Based | ≥ 90% of findings remediated within agreed timelines | Quarterly | Compliance |
| Risk acceptance register currency | Coverage % | 0 expired acceptances without renewal | Quarterly | GRC |

*Source: SRA §12, KPI Framework. See diagram: `17-kpi-framework.d2`.*

---

## 8. Regulatory Alignment

| Regulation | Applicable Requirements | SRA Mapping | Evidence |
|---|---|---|---|
| SOX (IT General Controls) | Overall IT control environment: an IT control framework must exist with documented controls, risk assessments, monitoring, and management oversight | §13, CTRL-013 | TSRA architecture document; SRA Control Register; governance memo set; NIST CSF 2.0 mapping; executive review records |
| SOX (IT General Controls) | Internal audit coordination: IT controls must be assessed for design and operating effectiveness | §13, CTRL-013 | Control self-assessment results; evidence traceability matrix; audit workpapers |
| FERPA | Institutional safeguards: reasonable methods must be used to ensure the security and confidentiality of education records | §13, CTRL-013 | FERPA control inventory; access control documentation; audit logging confirmation; breach notification procedures |
| FERPA | Breach notification: institutions must notify affected parties in a timely manner following a breach of student records | §13, CTRL-013 | Breach notification procedures; incident response integration (SRA §9); notification testing records |

*Source: SRA §13, Regulatory Compliance Alignment. See diagram: `18-regulatory-compliance-alignment.d2`.*

---

## Appendix D — Control Register Snapshot

*This appendix is a derived snapshot from `SRA_Control_Register.xlsx`, filtered to SRA §13. **Do not edit this table directly** — update the Excel register and regenerate.*

| Control ID | SRA Section | NIST CSF 2.0 IDs | Evidence Source | Control Owner | Review Frequency | Implementation Status |
|---|---|---|---|---|---|---|
| CTRL-013 | §13 | GV.RM-03, GV.OV-03, RC.CO-03 | Compliance control narratives; audit workpapers | Compliance | Quarterly | Partially Implemented |

---

## Document Control

| Field | Value |
|---|---|
| Version | 1.0 — Draft |
| Created | March 2, 2026 |
| Last Updated | March 2, 2026 |
| Next Review | June 2, 2026 (Quarterly) |
| Approval Chain | Compliance → Security Architecture → Executive Security Leadership |

---

*This memo is governed by the TSRA Document Control model (SRA §14). See diagram: `20-document-control-metadata.d2`.*
