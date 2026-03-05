# Governance Memo: SRA §4 — Identity and Access Architecture

**Document Classification:** Internal / Controlled  
**SRA Section Reference:** §4  
**Version:** 1.0 — Draft  
**Date:** March 2, 2026  
**Control Owner:** IAM  
**Approved By:** *[Pending — Executive Security Leadership]*  

---

## 1. Purpose and Scope

This governance memo establishes the security architecture governance position for **Identity and Access Architecture** as defined in the Trust Security Reference Architecture (TSRA), Section §4 — Identity and Access Architecture.

**Scope:**
- Workforce identity (Microsoft Entra ID) — conditional access, identity protection, SAML/OIDC app registrations for staff
- External identity (Okta CIAM) — adaptive authentication and token services for students and customers
- Unified identity governance (SailPoint IdentityNow) — identity cube, joiner/mover/leaver lifecycle, access certifications, and separation of duties (SoD) enforcement
- Staff authentication flows including risk-adaptive conditional access and MFA (FIDO2, Windows Hello for Business)
- Student authentication flows including enrollment provisioning (SailPoint → Okta CIAM), policy SSO, and withdrawal deprovisioning
- Customer authentication flows including self-service registration, credential verification, MFA setup, and risk-sensitive session policy
- Conditional access policy matrix across four risk tiers (Privileged, High, Medium, Low)

**Exclusions:**
- Privileged access management (covered under SRA §5 — Privileged Trust)
- Device trust signals as CA inputs (covered under SRA §6 — Device Trust)
- Service account lifecycle beyond identity governance scope (future roadmap item)

**Authoritative References:**
- Trust Security Reference Architecture (TSRA), §4
- SRA Control Register (`SRA_Control_Register.xlsx`), Control ID: CTRL-004
- D2 Architecture Diagrams:
  - `04-staff-authentication-flow.d2` — Staff authentication with Entra CA risk assessment
  - `05-staff-conditional-access-policy-matrix.d2` — Four-tier conditional access matrix
  - `06-student-authentication-flow.d2` — Student provisioning and SSO flow
  - `07-customer-authentication-flow.d2` — Customer registration and access control
  - `08-identity-and-access-architecture.d2` — Unified IAM architecture overview
- STRIDE ISP 4.1 — Identity Management, Authentication, and Access Control (PR.AA)

---

## 2. Governance Authority

| Role | Responsibility | RACI |
|---|---|---|
| IAM | Owns identity platform operations (Entra, Okta, SailPoint), manages access policies, produces control evidence | Accountable |
| Security Architecture | Defines identity architecture standards, reviews design decisions, maintains D2 diagrams | Responsible |
| Security Operations | Monitors authentication anomalies, escalates identity-related incidents | Consulted |
| GRC / Compliance | Validates SOX ITGC and FERPA alignment for identity controls; reviews audit evidence | Informed |
| Executive Security Leadership | Approves governance position and any risk acceptance for deferred controls | Approver |

*RACI assignments align to STRIDE GV.RR policy intent.*

---

## 3. Architecture Summary

The Identity and Access Architecture implements a dual-IdP model with unified governance, serving three distinct persona sets across the Stride environment:

**Workforce Identity — Microsoft Entra ID:**
- Primary identity provider for all staff personas (SRA §3)
- Conditional access policies enforce risk-adaptive authentication across four tiers:
  - **Privileged Access:** Device compliance + CrowdStrike required, strong MFA (FIDO/WHfB), 15-minute session timeout, re-auth every session
  - **High Risk:** Device compliance + CrowdStrike required, FIDO/WHfB, 1-hour session timeout, re-auth every session
  - **Medium Risk:** Device compliance + CrowdStrike required, numeric OTP, 4-hour session timeout, daily re-auth
  - **Low Risk:** Device compliance + CrowdStrike required, standard auth, 8-hour session timeout, weekly re-auth
- Entra Identity Protection provides risk-based conditional access evaluation; high-risk sign-ins trigger MFA step-up before token issuance
- SAML/OIDC app registrations federate workforce applications

**External Identity — Okta CIAM:**
- Customer-facing identity for student and customer personas
- Adaptive authentication policies with token-based authorization
- Student lifecycle: enrollment → SailPoint provisioning to Okta CIAM → policy SSO with adaptive checks → token authentication → deprovisioning on withdrawal
- Customer lifecycle: self-service portal → credential verification → MFA setup → risk-sensitive session policy → token-based authorization

**Unified Governance — SailPoint IdentityNow:**
- Aggregates identities from both Entra ID and Okta CIAM into a unified identity cube
- Joiner/mover/leaver automation ensures consistent provisioning and deprovisioning across both IdPs
- Access certification campaigns enforce periodic review of entitlements
- Separation of duties (SoD) policies prevent toxic role combinations
- ServiceNow integration provides attestation workflows and evidence trails

> **Cross-References:**
> - Trust model and policy engine: SRA §2
> - Persona-specific boundaries (staff, student, customer): SRA §3
> - Privileged access (elevated staff): SRA §5
> - Device compliance signals as CA inputs: SRA §6
> - Operational correlation and incident handling: SRA §9

**Current-State Architecture Diagrams:**

> See: `08-identity-and-access-architecture.d2` (overview), `04-staff-authentication-flow.d2`, `05-staff-conditional-access-policy-matrix.d2`, `06-student-authentication-flow.d2`, `07-customer-authentication-flow.d2` (rendered in `rendering_svg_v3/` and `rendering_png_v3/`)

---

## 4. NIST CSF 2.0 Alignment

| NIST CSF 2.0 ID | Function | Subcategory Description | Implementation Status |
|---|---|---|---|
| PR.AA-01 | Protect | Identities and credentials for authorized users, services, and hardware are managed by the organization | Partially Implemented |
| PR.AA-02 | Protect | Identities are proofed and bound to credentials based on the context of interactions | Partially Implemented |
| PR.PS-01 | Protect | Configuration management practices are established and applied | Partially Implemented |

*Source: SRA Control Register, "NIST CSF Crosswalk" sheet, filtered to CTRL-004.*

**Gap Notes:**
- **PR.AA-01**: Entra ID and Okta CIAM fully manage workforce and external identities respectively; SailPoint provides unified lifecycle governance. Gap: automated credential lifecycle for non-federated service accounts is not yet fully onboarded
- **PR.AA-02**: Staff identities are proofed through HR-driven provisioning; student identities are proofed through enrollment verification; customer identities use self-service with credential verification. Gap: identity proofing strength varies by persona — no unified assurance-level framework yet
- **PR.PS-01**: Conditional access policies are version-controlled and tiered by risk. Gap: Okta CIAM policy configuration is not yet managed as code (future infrastructure-as-code initiative)

---

## 5. Control Objectives and Requirements

| Control ID | Control Description | Primary Tooling | Evidence Source | Review Frequency |
|---|---|---|---|---|
| CTRL-004 | Identity and access controls across workforce and external populations including conditional access, lifecycle management, and governance | Entra ID; Okta CIAM; SailPoint IdentityNow | Entra policy exports; IAM standards; SailPoint certification reports | Monthly |

**Key Requirements:**
1. All workforce authentication must traverse Entra ID conditional access policies with risk-tier-appropriate controls enforced (device compliance, MFA strength, session limits)
2. Student provisioning must flow through SailPoint → Okta CIAM with automated deprovisioning on withdrawal events within 24 hours
3. Customer registration must enforce credential verification and MFA enrollment before access is granted
4. Access certification campaigns must complete quarterly for workforce entitlements and semi-annually for external entitlements
5. Separation of duties (SoD) policy violations must be flagged and remediated or risk-accepted before access is granted
6. All conditional access policy changes must follow change management processes with documented approvals

---

## 6. Implementation Status and Roadmap

**Current Status:** Partially Implemented

**Maturity Assessment:**
- **In place:** Entra ID conditional access with four risk tiers enforced; Okta CIAM operational for student and customer authentication; SailPoint IdentityNow lifecycle automation for joiner/mover/leaver; FIDO2 and WHfB available for staff; MFA enforcement across all tiers
- **In flight:** SailPoint access certification campaign automation; SoD policy refinement for complex role combinations; Okta CIAM adaptive policy tuning based on risk analytics
- **Deferred:** Okta CIAM policy-as-code management; unified identity assurance-level framework; non-federated service account onboarding to SailPoint; decentralized identity exploration (long-term)

**Roadmap Alignment:**
> See: SRA §11, Implementation Roadmap Phase 2 — Identity + Privileged  
> Diagram: `15-implementation-roadmap-v2.d2`, Phase 2

| Milestone | Target Date | Status |
|---|---|---|
| SailPoint access certification automation (workforce) | Q2 2026 | In Flight |
| SoD policy expansion for cross-IdP role combinations | Q2 2026 | In Flight |
| Okta CIAM adaptive policy tuning | Q3 2026 | Planned |
| Okta CIAM policy-as-code migration | Q4 2026 | Deferred |
| Unified identity assurance-level framework | Q1 2027 | Deferred |
| Non-federated service account SailPoint onboarding | Q1 2027 | Deferred |

---

## 7. Key Performance Indicators

| KPI | Metric Type | Target / Threshold | Cadence | Owner |
|---|---|---|---|---|
| MFA enforcement rate (workforce) | Coverage % | 100% of staff sign-ins | Monthly | IAM |
| MFA enrollment rate (students + customers) | Coverage % | ≥ 95% of active external accounts | Monthly | IAM |
| Conditional access policy coverage | Coverage % | 100% of workforce apps under CA | Monthly | IAM |
| Access certification completion rate | Coverage % | 100% of campaigns completed by deadline | Quarterly | IAM |
| Joiner provisioning SLA | Time-Based | ≤ 4 hours from HR event to account activation | Monthly | IAM |
| Leaver deprovisioning SLA | Time-Based | ≤ 24 hours from termination event to full deprovisioning | Monthly | IAM |
| SoD violation rate | Risk Outcome | 0 unresolved violations beyond grace period | Monthly | IAM |

*Source: SRA §12, KPI Framework. See diagram: `17-kpi-framework.d2`.*

---

## 8. Regulatory Alignment

| Regulation | Applicable Requirements | SRA Mapping | Evidence |
|---|---|---|---|
| SOX (IT General Controls) | Logical access to programs and data: identity controls must authenticate and authorize all users before access is granted | §4, CTRL-004 | Entra CA policy exports; Okta CIAM policy configurations; SailPoint certification reports |
| SOX (IT General Controls) | User account management: joiner/mover/leaver processes must ensure timely provisioning and deprovisioning | §4, CTRL-004 | SailPoint lifecycle audit trails; deprovisioning SLA reports |
| SOX (IT General Controls) | Segregation of duties: access entitlements must not create toxic role combinations | §4, CTRL-004 | SoD policy configuration; violation and remediation reports |
| FERPA | Access to student education records must be restricted to authorized personnel with valid need | §4, CTRL-004 | Okta CIAM access logs; SailPoint role-to-application mappings; student app authorization records |

*Source: SRA §13, Regulatory Compliance Alignment. See diagram: `18-regulatory-compliance-alignment.d2`.*

---

## Appendix D — Control Register Snapshot

*This appendix is a derived snapshot from `SRA_Control_Register.xlsx`, filtered to SRA §4. **Do not edit this table directly** — update the Excel register and regenerate.*

| Control ID | SRA Section | NIST CSF 2.0 IDs | Evidence Source | Control Owner | Review Frequency | Implementation Status |
|---|---|---|---|---|---|---|
| CTRL-004 | §4 | PR.AA-01, PR.AA-02, PR.PS-01 | Entra policy exports; IAM standards; SailPoint certification reports | IAM | Monthly | Partially Implemented |

---

## Document Control

| Field | Value |
|---|---|
| Version | 1.0 — Draft |
| Created | March 2, 2026 |
| Last Updated | March 2, 2026 |
| Next Review | June 2, 2026 (Quarterly) |
| Approval Chain | IAM → Security Architecture → Executive Security Leadership |

---

*This memo is governed by the TSRA Document Control model (SRA §14). See diagram: `20-document-control-metadata.d2`.*
