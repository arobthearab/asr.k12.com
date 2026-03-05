# Governance Memo: SRA §5 — Privileged Trust Architecture

**Document Classification:** Internal / Controlled  
**SRA Section Reference:** §5  
**Version:** 1.0 — Draft  
**Date:** March 2, 2026  
**Control Owner:** IAM + Security Operations  
**Approved By:** *[Pending — Executive Security Leadership]*  

---

## 1. Purpose and Scope

This governance memo establishes the security architecture governance position for **Privileged Trust** as defined in the Trust Security Reference Architecture (TSRA), Section §5 — Privileged Trust (Delinea and Entra PIM).

**Scope:**
- All privileged access management (PAM) capabilities including just-in-time (JIT) elevation, session recording, and role governance
- Delinea Secret Server / Privilege Manager for vault-based credential management
- Microsoft Entra Privileged Identity Management (PIM) for Azure AD role activation
- Applicable to all staff personas with elevated or administrative access (ref: SRA §3)

**Exclusions:**
- Standard user access controls (covered under SRA §4 — Identity and Access Architecture)
- Service account management beyond privileged scope (future roadmap item)

**Authoritative References:**
- Trust Security Reference Architecture (TSRA), §5
- SRA Control Register (`SRA_Control_Register.xlsx`), Control ID: CTRL-005
- D2 Architecture Diagram: `09-privileged-trust-architecture.d2`
- STRIDE ISP 4.1 — Identity Management, Authentication, and Access Control (PR.AA)

---

## 2. Governance Authority

| Role | Responsibility | RACI |
|---|---|---|
| IAM + Security Operations | Owns privileged access controls, manages PIM/PAM platforms, produces evidence | Accountable |
| Security Architecture | Defines privileged trust architecture standards and reviews design decisions | Responsible |
| Security Operations | Monitors privileged session activity, escalates anomalies | Consulted |
| GRC / Compliance | Validates SOX ITGC alignment for privileged access; reviews audit evidence | Informed |
| Executive Security Leadership | Approves governance position and any risk acceptance for deferred controls | Approver |

*RACI assignments align to STRIDE GV.RR policy intent.*

---

## 3. Architecture Summary

The Privileged Trust Architecture implements a layered approach to controlling elevated access across the Stride environment:

**Delinea (Secret Server / Privilege Manager):**
- Vault-based credential storage and rotation for infrastructure and application administrator accounts
- Session recording and privileged session management for auditability
- Just-in-time checkout with time-limited credential access and automatic revocation

**Microsoft Entra PIM:**
- Role-based activation for Azure AD administrative roles (Global Admin, Exchange Admin, Security Admin, etc.)
- Activation requires MFA step-up and approval workflow for high-risk roles
- Time-bounded role assignments with automatic deactivation
- Audit logging of all PIM activations and approvals

**Trust Decision Integration:**
- Privileged access requests feed into the Trust Decision Plane (SRA §2) as high-assurance signals
- Conditional Access policies at the **Privileged Access** tier require: device compliance, CrowdStrike active, strong MFA (FIDO/WHfB), 15-minute session timeout, and re-authentication every session (ref: SRA §4, `05-staff-conditional-access-policy-matrix.d2`)
- Privileged session telemetry is forwarded to the operational trust layer for incident correlation (ref: SRA §9)

> **Cross-References:**
> - Trust model and policy engine: SRA §2
> - Persona-specific boundaries (staff privileged): SRA §3
> - Conditional Access privileged tier: SRA §4 (`05-staff-conditional-access-policy-matrix.d2`)
> - Device compliance signals: SRA §6
> - Operational correlation: SRA §9

**Current-State Architecture Diagram:**

> See: `09-privileged-trust-architecture.d2` (rendered in `rendering_svg_v3/` and `rendering_png_v3/`)

---

## 4. NIST CSF 2.0 Alignment

| NIST CSF 2.0 ID | Function | Subcategory Description | Implementation Status |
|---|---|---|---|
| PR.AA-05 | Protect | Access permissions and authorizations are defined using least privilege and separation of duties | Partially Implemented |
| PR.PS-02 | Protect | Software is maintained, replaced, and removed in a timely manner | Partially Implemented |
| DE.CM-03 | Detect | Personnel activity and technology usage are monitored | Partially Implemented |

*Source: SRA Control Register, "NIST CSF Crosswalk" sheet, filtered to CTRL-005.*

**Gap Notes:**
- **PR.AA-05**: Least-privilege role definitions are in place for Entra PIM; Delinea role scoping is operational but requires periodic access certification automation
- **PR.PS-02**: Delinea credential rotation is automated; Entra PIM role lifecycle management is partially manual for custom roles
- **DE.CM-03**: Session recording is active in Delinea; Entra PIM audit logs feed SIEM, but advanced analytics (UEBA) for privileged behavior is a future-state enhancement

---

## 5. Control Objectives and Requirements

| Control ID | Control Description | Primary Tooling | Evidence Source | Review Frequency |
|---|---|---|---|---|
| CTRL-005 | Privileged access controls including just-in-time elevation, session monitoring, and PIM role governance | Delinea; Entra PIM | PIM role assignments; privileged session audit logs | Monthly |

**Key Requirements:**
1. All administrative access must be provisioned through JIT activation (Entra PIM) or time-limited checkout (Delinea) — standing privileges are prohibited for Tier 0/1 roles
2. Privileged sessions for infrastructure accounts must be recorded and retrievable for 12 months minimum
3. PIM role activations for high-risk Azure AD roles require approval from a second authorized administrator
4. Credential rotation for vaulted accounts must occur at policy-defined intervals (90 days maximum, 30 days for Tier 0)
5. Monthly access certification reviews must validate that privileged role assignments remain appropriate

---

## 6. Implementation Status and Roadmap

**Current Status:** Partially Implemented

**Maturity Assessment:**
- **In place:** Delinea vault operational for infrastructure credentials; Entra PIM active for Azure AD roles; conditional access at privileged tier enforced; session recording enabled
- **In flight:** Entra PIM access review automation; Delinea role scoping refinement; integration of privileged session telemetry with ServiceNow SecOps
- **Deferred:** UEBA-based privileged behavior analytics; automated service account discovery and onboarding

**Roadmap Alignment:**
> See: SRA §11, Implementation Roadmap Phase 2 — Identity + Privileged  
> Diagram: `15-implementation-roadmap-v2.d2`, Phase 2

| Milestone | Target Date | Status |
|---|---|---|
| Entra PIM access review automation | Q2 2026 | In Flight |
| Delinea role scope refinement (Tier 0/1/2 segmentation) | Q2 2026 | In Flight |
| Privileged session telemetry → ServiceNow SecOps integration | Q3 2026 | Planned |
| UEBA for privileged behavior analytics | Q4 2026 | Deferred |
| Automated service account discovery | Q1 2027 | Deferred |

---

## 7. Key Performance Indicators

| KPI | Metric Type | Target / Threshold | Cadence | Owner |
|---|---|---|---|---|
| Privileged JIT adoption rate | Coverage % | ≥ 95% of Tier 0/1 activations via PIM/Delinea | Monthly | IAM |
| Standing privilege count | Risk Outcome | 0 standing Tier 0 privileges; ≤ 5 Tier 1 exceptions | Monthly | IAM |
| Credential rotation compliance | Coverage % | 100% within policy SLA | Monthly | Security Operations |
| Mean time to revoke terminated privileged access | Time-Based | ≤ 4 hours | Monthly | IAM |
| Privileged access certification completion | Coverage % | 100% monthly cycle completion | Monthly | IAM |
| Privileged session recording gaps | Control Quality | 0 unrecorded privileged sessions | Weekly | Security Operations |

*Source: SRA §12, KPI Framework. See diagram: `17-kpi-framework.d2`.*

---

## 8. Regulatory Alignment

| Regulation | Applicable Requirements | SRA Mapping | Evidence |
|---|---|---|---|
| SOX (IT General Controls) | Logical access to programs and data: privileged access must be restricted, monitored, and periodically reviewed | §5, CTRL-005 | PIM activation logs; Delinea session recordings; monthly access certification reports |
| SOX (IT General Controls) | Segregation of duties: privileged role assignments must enforce SoD constraints | §5, CTRL-005 | Role conflict analysis; PIM approval workflows |
| FERPA | Access to student records by privileged administrators must be logged and auditable | §5, CTRL-005 | Privileged session audit logs; access-to-FERPA-data reports |

*Source: SRA §13, Regulatory Compliance Alignment. See diagram: `18-regulatory-compliance-alignment.d2`.*

---

## Appendix D — Control Register Snapshot

*This appendix is a derived snapshot from `SRA_Control_Register.xlsx`, filtered to SRA §5. **Do not edit this table directly** — update the Excel register and regenerate.*

| Control ID | SRA Section | NIST CSF 2.0 IDs | Evidence Source | Control Owner | Review Frequency | Implementation Status |
|---|---|---|---|---|---|---|
| CTRL-005 | §5 | PR.AA-05, PR.PS-02, DE.CM-03 | PIM role assignments; privileged session audit logs | IAM + Security Operations | Monthly | Partially Implemented |

---

## Document Control

| Field | Value |
|---|---|
| Version | 1.0 — Draft |
| Created | March 2, 2026 |
| Last Updated | March 2, 2026 |
| Next Review | June 2, 2026 (Quarterly) |
| Approval Chain | IAM + Security Operations → Security Architecture → Executive Security Leadership |

---

*This memo is governed by the TSRA Document Control model (SRA §14). See diagram: `20-document-control-metadata.d2`.*
