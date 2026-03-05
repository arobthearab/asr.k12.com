# Governance Memo: SRA §6 — Device Trust Architecture

**Document Classification:** Internal / Controlled  
**SRA Section Reference:** §6  
**Version:** 1.0 — Draft  
**Date:** March 2, 2026  
**Control Owner:** Endpoint Security  
**Approved By:** *[Pending — Executive Security Leadership]*  

---

## 1. Purpose and Scope

This governance memo establishes the security architecture governance position for **Device Trust** as defined in the Trust Security Reference Architecture (TSRA), Section §6 — Device Trust (CrowdStrike and Defender).

**Scope:**
- CrowdStrike Falcon — primary endpoint trust signal and EDR platform
- Microsoft Defender for Endpoint — monitor-mode telemetry and secondary signal
- Tenable exposure context — vulnerability-informed device risk input
- Composite device trust score computation and its integration with access decisions
- Conditional access policy enforcement of device compliance across all four risk tiers
- Trust outcomes: allow, step-up MFA, limit session, deny

**Exclusions:**
- Identity-layer conditional access policy definitions (covered under SRA §4 — Identity and Access Architecture)
- Privileged access device requirements (covered under SRA §5 — Privileged Trust)
- Vulnerability management program operations (covered under SRA §7 — Exposure and Posture)

**Authoritative References:**
- Trust Security Reference Architecture (TSRA), §6
- SRA Control Register (`SRA_Control_Register.xlsx`), Control ID: CTRL-006
- D2 Architecture Diagram: `10-device-trust-architecture.d2`
- STRIDE ISP — Endpoint Protection and Platform Security (PR.PS)

---

## 2. Governance Authority

| Role | Responsibility | RACI |
|---|---|---|
| Endpoint Security | Owns endpoint trust platforms (CrowdStrike, Defender), manages EDR policies, produces device compliance evidence | Accountable |
| Security Architecture | Defines device trust architecture standards, maintains integration with the trust decision plane | Responsible |
| IAM | Consumes device trust signals in conditional access policy decisions | Consulted |
| GRC / Compliance | Validates endpoint control alignment to SOX and FERPA requirements | Informed |
| Executive Security Leadership | Approves governance position and risk acceptance for device trust exceptions | Approver |

*RACI assignments align to STRIDE GV.RR policy intent.*

---

## 3. Architecture Summary

The Device Trust Architecture implements a multi-signal approach to establishing and maintaining endpoint trust across the Stride environment:

**CrowdStrike Falcon — Primary Trust Signal:**
- Deployed as the primary endpoint detection and response (EDR) platform across all managed devices
- Provides real-time threat detection, behavioral analytics, and device health attestation
- CrowdStrike sensor presence is a mandatory conditional access condition across all four risk tiers (Privileged, High, Medium, Low)
- Feeds device trust telemetry into the composite risk score

**Microsoft Defender for Endpoint — Secondary Signal:**
- Operates in monitor-mode to provide complementary telemetry and threat intelligence
- Provides additional device compliance signals for Microsoft ecosystem integration
- Does not serve as primary enforcement; supplements CrowdStrike with defense-in-depth visibility

**Tenable Exposure Context:**
- Vulnerability scan results from Tenable VM contribute vulnerability-informed risk data to the device trust score
- Devices with critical unpatched vulnerabilities receive elevated risk scores, potentially triggering step-up or deny outcomes

**Access Decision Integration:**
- Endpoint signals (CrowdStrike, Defender, Tenable) are aggregated into a composite device trust score
- The composite score feeds into Entra conditional access policies as a device compliance condition
- Four trust outcomes are possible based on the composite score and policy tier:
  - **Allow** — device meets all compliance requirements
  - **Step-up MFA** — device has minor compliance concerns
  - **Limit Session** — device has elevated risk; session restrictions applied
  - **Deny** — device is non-compliant or has critical risk indicators

> **Cross-References:**
> - Trust model and policy engine: SRA §2
> - Persona-specific device requirements: SRA §3
> - Conditional access policy tiers consuming device signals: SRA §4
> - Privileged access device enforcement (15-min session, every-session reauth): SRA §5
> - Vulnerability context feeding device scores: SRA §7
> - Operational incident escalation for device compromise: SRA §9

**Current-State Architecture Diagram:**

> See: `10-device-trust-architecture.d2` (rendered in `rendering_svg_v3/` and `rendering_png_v3/`)

---

## 4. NIST CSF 2.0 Alignment

| NIST CSF 2.0 ID | Function | Subcategory Description | Implementation Status |
|---|---|---|---|
| PR.PS-03 | Protect | Hardware is maintained, replaced, and removed commensurate with risk | Partially Implemented |
| DE.CM-01 | Detect | Networks and network services are monitored to find potentially adverse events | Partially Implemented |

*Source: SRA Control Register, "NIST CSF Crosswalk" sheet, filtered to CTRL-006.*

**Gap Notes:**
- **PR.PS-03**: CrowdStrike sensor deployment covers all managed endpoints; Defender provides supplementary coverage. Gap: unmanaged/BYOD device trust enforcement is limited — future conditional access enhancements will address device registration gating for personal devices
- **DE.CM-01**: CrowdStrike provides real-time endpoint monitoring with behavioral analytics; alert telemetry feeds SOC workflows. Gap: automated correlation between device trust score changes and conditional access policy re-evaluation is partially manual

---

## 5. Control Objectives and Requirements

| Control ID | Control Description | Primary Tooling | Evidence Source | Review Frequency |
|---|---|---|---|---|
| CTRL-006 | Device trust controls including EDR enrollment, compliance signal enforcement, and health attestation | CrowdStrike Falcon; Defender for Endpoint | EDR posture dashboards; compliance policy reports | Weekly |

**Key Requirements:**
1. All managed endpoints must have CrowdStrike Falcon sensor active and reporting — sensor absence must trigger conditional access denial
2. Defender for Endpoint must be deployed in monitor-mode on all managed Windows and macOS endpoints
3. Composite device trust scores must be computed from CrowdStrike health, Defender compliance, and Tenable vulnerability context
4. Device compliance is a mandatory conditional access condition across all four risk tiers
5. Devices with critical unpatched vulnerabilities (Tenable CVSS ≥ 9.0) must be denied or session-limited within 24 hours of detection
6. Endpoint compliance posture must be reported weekly with escalation paths for non-compliant devices

---

## 6. Implementation Status and Roadmap

**Current Status:** Partially Implemented

**Maturity Assessment:**
- **In place:** CrowdStrike Falcon deployed across managed fleet; Defender for Endpoint in monitor-mode; conditional access enforces CrowdStrike presence at all tiers; EDR posture dashboards operational; weekly compliance reporting active
- **In flight:** Composite device trust score integration (CrowdStrike + Tenable); automated conditional access re-evaluation on score change; Defender telemetry enrichment into SOC alerts
- **Deferred:** BYOD/unmanaged device trust model; mobile device trust signal integration; hardware attestation (TPM-based) for highest-assurance tiers

**Roadmap Alignment:**
> See: SRA §11, Implementation Roadmap Phase 2 — Identity + Privileged, Phase 3 — Device + Posture  
> Diagram: `15-implementation-roadmap-v2.d2`, Phase 3

| Milestone | Target Date | Status |
|---|---|---|
| Composite device trust score (CrowdStrike + Tenable) | Q2 2026 | In Flight |
| Automated CA re-evaluation on trust score change | Q3 2026 | Planned |
| Defender telemetry SOC enrichment | Q3 2026 | In Flight |
| BYOD device trust model (registration gating) | Q4 2026 | Deferred |
| Mobile device trust signal integration | Q1 2027 | Deferred |
| Hardware attestation (TPM) for Tier 0/1 | Q1 2027 | Deferred |

---

## 7. Key Performance Indicators

| KPI | Metric Type | Target / Threshold | Cadence | Owner |
|---|---|---|---|---|
| CrowdStrike sensor coverage | Coverage % | ≥ 99% of managed endpoints | Weekly | Endpoint Security |
| Defender for Endpoint coverage | Coverage % | ≥ 98% of managed Windows/macOS | Weekly | Endpoint Security |
| Device compliance rate (CA-enforced) | Coverage % | ≥ 97% of access attempts from compliant devices | Weekly | Endpoint Security |
| Mean time to isolate compromised device | Time-Based | ≤ 1 hour from detection to isolation | Weekly | Security Operations |
| Critical vulnerability device remediation SLA | Time-Based | ≤ 24 hours for CVSS ≥ 9.0 devices | Weekly | Endpoint Security |
| Non-compliant device escalation rate | Risk Outcome | 100% of non-compliant devices escalated within SLA | Weekly | Endpoint Security |

*Source: SRA §12, KPI Framework. See diagram: `17-kpi-framework.d2`.*

---

## 8. Regulatory Alignment

| Regulation | Applicable Requirements | SRA Mapping | Evidence |
|---|---|---|---|
| SOX (IT General Controls) | Program change management and logical access: endpoints accessing financial systems must meet compliance standards | §6, CTRL-006 | CrowdStrike compliance dashboards; CA policy enforcement logs; device compliance attestation reports |
| SOX (IT General Controls) | Computer operations: endpoint protection must be continuously monitored with documented response procedures | §6, CTRL-006 | EDR alert logs; incident response runbooks; device isolation records |
| FERPA | Devices accessing student education records must have active endpoint protection and meet compliance requirements | §6, CTRL-006 | CrowdStrike sensor status for FERPA-scope applications; conditional access policy audit trails |

*Source: SRA §13, Regulatory Compliance Alignment. See diagram: `18-regulatory-compliance-alignment.d2`.*

---

## Appendix D — Control Register Snapshot

*This appendix is a derived snapshot from `SRA_Control_Register.xlsx`, filtered to SRA §6. **Do not edit this table directly** — update the Excel register and regenerate.*

| Control ID | SRA Section | NIST CSF 2.0 IDs | Evidence Source | Control Owner | Review Frequency | Implementation Status |
|---|---|---|---|---|---|---|
| CTRL-006 | §6 | PR.PS-03, DE.CM-01 | EDR posture dashboards; compliance policy reports | Endpoint Security | Weekly | Partially Implemented |

---

## Document Control

| Field | Value |
|---|---|
| Version | 1.0 — Draft |
| Created | March 2, 2026 |
| Last Updated | March 2, 2026 |
| Next Review | June 2, 2026 (Quarterly) |
| Approval Chain | Endpoint Security → Security Architecture → Executive Security Leadership |

---

*This memo is governed by the TSRA Document Control model (SRA §14). See diagram: `20-document-control-metadata.d2`.*
