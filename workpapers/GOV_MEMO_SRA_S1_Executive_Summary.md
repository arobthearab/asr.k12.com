# Governance Memo: SRA §1 — Executive Summary

**Document Classification:** Internal / Controlled  
**SRA Section Reference:** §1  
**Version:** 1.0 — Draft  
**Date:** March 2, 2026  
**Control Owner:** Security Architecture / GRC  
**Approved By:** *[Pending — Executive Security Leadership]*  

---

## 1. Purpose and Scope

This governance memo establishes the executive-level governance position for the **Trust Security Reference Architecture (TSRA)** as defined in Section §1 — Executive Summary. It serves as the strategic governance anchor for all domain-specific governance memos and provides the overarching context for the architecture program.

**Scope:**
- Strategic direction and mission of the TSRA: establish, evaluate, enforce, degrade, and restore trust across the Stride environment
- Target audiences: staff, students, customers in a cloud-native edtech platform
- Governance authority over all domain-specific SRA sections (§2–§14)
- Integrated platform stack alignment: Entra ID, Okta CIAM, SailPoint IdentityNow, Delinea, Entra PIM, CrowdStrike Falcon, Defender for Endpoint, Tenable VM/CSPM, Sonatype, Burp Suite, Salt Security (future), ServiceNow SecOps
- Framework alignment: TOGAF, NIST CSF 2.0, NIST SP 800-207 (Zero Trust)

**Exclusions:**
- Domain-specific control details (covered in respective governance memos: §4–§9)
- Operational runbooks and tactical procedures

**Authoritative References:**
- Trust Security Reference Architecture (TSRA), §1
- SRA Control Register (`SRA_Control_Register.xlsx`), Control ID: CTRL-001
- D2 Architecture Diagram: `16-executive-summary-and-platform-stack.d2`
- All domain-specific governance memos (§4, §5, §6, §7, §8, §9)

---

## 2. Governance Authority

| Role | Responsibility | RACI |
|---|---|---|
| Security Architecture / GRC | Owns the TSRA as a governance artifact, maintains architecture standards, coordinates cross-domain alignment | Accountable |
| Executive Security Leadership | Sponsors the architecture program, approves strategic direction and risk posture | Approver |
| IAM / Endpoint / AppSec / VulnMgmt / SecOps | Execute domain-specific controls aligned to the TSRA; produce evidence within their respective domains | Responsible |
| Program Management | Coordinates implementation roadmap execution across domains | Consulted |
| Legal / Compliance | Advises on regulatory obligations (SOX, FERPA) that shape architecture requirements | Informed |

*RACI assignments align to STRIDE GV.RR policy intent.*

---

## 3. Architecture Summary

The Trust Security Reference Architecture defines a comprehensive, trust-centric security posture for Stride (K12.com) across all personas, platforms, and cloud environments. The architecture is organized around a central trust model that evaluates, enforces, and adapts trust decisions across eight interconnected security domains.

**TSRA Mission:**
> Establish, evaluate, enforce, degrade, and restore trust for staff, students, and customers in a cloud-native edtech environment.

**Strategic Objectives:**
1. **Identity-centric, risk-adaptive controls** — Entra ID (workforce) and Okta CIAM (external) provide persona-specific authentication with conditional access based on real-time risk signals
2. **Unified governance** — SailPoint IdentityNow aggregates identities across both IdPs for lifecycle management, certification, and SoD enforcement
3. **Privileged trust** — Delinea and Entra PIM enforce just-in-time elevation, session recording, and role governance for administrative access
4. **Device trust** — CrowdStrike Falcon (primary) and Defender for Endpoint (secondary) feed composite device trust scores into access decisions
5. **Exposure and posture** — Tenable VM and CSPM provide continuous vulnerability identification and cloud configuration drift detection
6. **Secure SDLC and API trust** — Sonatype SCA, Burp Suite DAST, and Salt Security (future) protect the application delivery pipeline and runtime
7. **Operational trust** — ServiceNow SecOps centralizes incident management, vulnerability response, and evidence collection from all upstream signals
8. **Measurable compliance** — SOX and FERPA alignment with audit-ready evidence traceability

**Framework Alignment:**
- **TOGAF**: Enterprise architecture methodology guiding the TSRA structure and governance model
- **NIST CSF 2.0**: Control mapping framework providing subcategory-level traceability for all domain controls (see SRA §10)
- **NIST SP 800-207**: Zero Trust Architecture principles informing identity-centric access, micro-segmentation intent, and continuous trust evaluation

**Integrated Platform Stack:**

| Domain | Platform | SRA Section |
|---|---|---|
| Workforce Identity | Microsoft Entra ID | §4 |
| External Identity | Okta CIAM | §4 |
| Identity Governance | SailPoint IdentityNow | §4 |
| Privileged Access | Delinea + Entra PIM | §5 |
| Device Trust | CrowdStrike Falcon + Defender for Endpoint | §6 |
| Exposure Management | Tenable VM + CSPM | §7 |
| Application Security | Sonatype + Burp Suite | §8 |
| API Security | Salt Security (future) | §8 |
| Security Operations | ServiceNow SecOps | §9 |

> **Cross-References:**
> - Trust model and decision plane: SRA §2
> - Persona trust boundaries: SRA §3
> - All domain sections: SRA §4–§9
> - NIST CSF outcome mapping: SRA §10
> - Implementation roadmap: SRA §11
> - KPI framework: SRA §12
> - Regulatory compliance: SRA §13

**Current-State Architecture Diagram:**

> See: `16-executive-summary-and-platform-stack.d2` (rendered in `rendering_svg_v3/` and `rendering_png_v3/`)

---

## 4. NIST CSF 2.0 Alignment

| NIST CSF 2.0 ID | Function | Subcategory Description | Implementation Status |
|---|---|---|---|
| GV.OC-01 | Govern | The organizational context — mission, stakeholder expectations, and dependencies — is understood and informs cybersecurity risk management | Partially Implemented |
| GV.RM-01 | Govern | Risk management objectives are established and expressed as statements articulating the organization's risk appetite | Partially Implemented |
| GV.OV-01 | Govern | Cybersecurity risk management strategy outcomes are reviewed to inform and adjust strategy and direction | Partially Implemented |

*Source: SRA Control Register, "NIST CSF Crosswalk" sheet, filtered to CTRL-001.*

**Gap Notes:**
- **GV.OC-01**: Organizational context (Stride edtech mission, three persona populations, cloud-native environment) is documented in the TSRA. Gap: formal cybersecurity risk appetite statement is drafted but awaiting executive sign-off
- **GV.RM-01**: Risk management objectives are expressed through the TSRA strategic objectives and control register. Gap: quantitative risk thresholds are not yet defined — current approach is qualitative
- **GV.OV-01**: Architecture governance reviews are scheduled quarterly. Gap: automated governance outcome reporting (KPI-to-strategy linkage) is in development (SRA §12)

---

## 5. Control Objectives and Requirements

| Control ID | Control Description | Primary Tooling | Evidence Source | Review Frequency |
|---|---|---|---|---|
| CTRL-001 | Executive governance of the Trust Security Reference Architecture including strategic direction, risk posture, and cross-domain alignment | Architecture governance framework | Architecture governance brief; executive review notes | Quarterly |

**Key Requirements:**
1. The TSRA must be reviewed and reaffirmed at the executive level quarterly, with documented approval of any architectural changes
2. All domain-specific governance memos must maintain traceability to the TSRA strategic objectives and NIST CSF 2.0 subcategories
3. Risk acceptance decisions for deferred controls must be documented, time-bounded, and approved by Executive Security Leadership
4. Cross-domain architectural dependencies must be reviewed when any single domain memo is materially updated
5. The SRA Control Register must be maintained as the authoritative source of truth for all control, evidence, and compliance data

---

## 6. Implementation Status and Roadmap

**Current Status:** Partially Implemented

**Maturity Assessment:**
- **In place:** TSRA v1.0 complete with 14 sections, 22 D2 architecture diagrams, NIST CSF 2.0 subcategory mapping, control register (5 sheets), governance memo framework, and KPI framework
- **In flight:** Executive approval of TSRA governance position; formal risk appetite statement; automated KPI reporting; domain memo completion for all sections
- **Deferred:** Quantitative risk modeling; architecture-as-code governance automation; formal third-party architecture review

**Roadmap Alignment:**
> See: SRA §11, Implementation Roadmap — all phases  
> Diagram: `15-implementation-roadmap-v2.d2`

| Milestone | Target Date | Status |
|---|---|---|
| TSRA v1.0 executive approval | Q2 2026 | In Flight |
| Formal risk appetite statement | Q2 2026 | In Flight |
| All domain governance memos complete | Q2 2026 | In Flight |
| Automated KPI-to-strategy reporting | Q3 2026 | Planned |
| Quantitative risk modeling | Q4 2026 | Deferred |
| Architecture-as-code governance automation | Q1 2027 | Deferred |

---

## 7. Key Performance Indicators

| KPI | Metric Type | Target / Threshold | Cadence | Owner |
|---|---|---|---|---|
| TSRA governance review completion | Coverage % | 100% quarterly reviews completed on schedule | Quarterly | Security Architecture |
| Domain memo currency | Coverage % | 100% of domain memos reviewed within trailing 6 months | Quarterly | Security Architecture |
| Control register completeness | Coverage % | 100% of SRA sections have corresponding CTRL entries | Quarterly | GRC |
| Risk acceptance register currency | Coverage % | 0 expired risk acceptances without renewal | Quarterly | GRC |
| Cross-domain dependency review completion | Coverage % | 100% of dependency reviews completed per trigger events | Per Event | Security Architecture |
| NIST CSF mapping completeness | Coverage % | 100% of SRA sections mapped to CSF subcategories | Quarterly | GRC |

*Source: SRA §12, KPI Framework. See diagram: `17-kpi-framework.d2`.*

---

## 8. Regulatory Alignment

| Regulation | Applicable Requirements | SRA Mapping | Evidence |
|---|---|---|---|
| SOX (IT General Controls) | IT governance: an overarching security architecture must exist with documented controls, risk assessments, and executive oversight | §1, CTRL-001 | TSRA document; control register; governance memo set; executive review records |
| SOX (IT General Controls) | Risk assessment: IT risks must be identified, assessed, and managed through a formal framework | §1, CTRL-001 | NIST CSF 2.0 mapping; risk acceptance register; governance review minutes |
| FERPA | Institutional safeguards: administrative, technical, and physical safeguards must protect the security of education records | §1, CTRL-001 | TSRA as overarching safeguard framework; domain control evidence per §4–§9 memos |

*Source: SRA §13, Regulatory Compliance Alignment. See diagram: `18-regulatory-compliance-alignment.d2`.*

---

## Appendix D — Control Register Snapshot

*This appendix is a derived snapshot from `SRA_Control_Register.xlsx`, filtered to SRA §1. **Do not edit this table directly** — update the Excel register and regenerate.*

| Control ID | SRA Section | NIST CSF 2.0 IDs | Evidence Source | Control Owner | Review Frequency | Implementation Status |
|---|---|---|---|---|---|---|
| CTRL-001 | §1 | GV.OC-01, GV.RM-01, GV.OV-01 | Architecture governance brief; executive review notes | Security Architecture / GRC | Quarterly | Partially Implemented |

---

## Document Control

| Field | Value |
|---|---|
| Version | 1.0 — Draft |
| Created | March 2, 2026 |
| Last Updated | March 2, 2026 |
| Next Review | June 2, 2026 (Quarterly) |
| Approval Chain | Security Architecture / GRC → Executive Security Leadership |

---

*This memo is governed by the TSRA Document Control model (SRA §14). See diagram: `20-document-control-metadata.d2`.*
