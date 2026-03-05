# Governance Memo: SRA §8 — Application and API Trust Architecture

**Document Classification:** Internal / Controlled  
**SRA Section Reference:** §8  
**Version:** 1.0 — Draft  
**Date:** March 2, 2026  
**Control Owner:** AppSec  
**Approved By:** *[Pending — Executive Security Leadership]*  

---

## 1. Purpose and Scope

This governance memo establishes the security architecture governance position for **Application and API Trust** as defined in the Trust Security Reference Architecture (TSRA), Section §8 — Application and API Trust (Sonatype, Burp Suite, Salt).

**Scope:**
- Sonatype Software Composition Analysis (SCA) — open-source dependency risk and license compliance assessment
- Policy gate enforcement — blocking non-compliant builds from progressing through the delivery pipeline
- Burp Suite DAST — dynamic application security testing for runtime vulnerability validation
- Salt Security (future state) — API discovery, behavioral analytics, and enforcement
- Secure software delivery lifecycle (SDLC) integration from code through deployment
- Supply-chain risk reduction, runtime assurance, and API visibility outcomes

**Exclusions:**
- Infrastructure vulnerability scanning (covered under SRA §7 — Exposure and Posture)
- Identity controls for application access (covered under SRA §4 — Identity and Access Architecture)
- Operational incident response for application-layer events (covered under SRA §9)

**Authoritative References:**
- Trust Security Reference Architecture (TSRA), §8
- SRA Control Register (`SRA_Control_Register.xlsx`), Control ID: CTRL-008
- D2 Architecture Diagram: `12-application-and-api-trust-architecture.d2`
- STRIDE ISP — Application Security and Secure Development (PR.DS, PR.PS)

---

## 2. Governance Authority

| Role | Responsibility | RACI |
|---|---|---|
| AppSec | Owns application security tooling (Sonatype, Burp Suite, Salt), manages secure SDLC policies, produces control evidence | Accountable |
| Security Architecture | Defines application and API trust architecture standards, reviews pipeline security design | Responsible |
| Development / Engineering | Integrates security gates into CI/CD pipelines, remediates findings within SLA | Consulted |
| Security Operations | Monitors runtime application security events, escalates critical findings | Consulted |
| GRC / Compliance | Validates secure development alignment to SOX and regulatory requirements | Informed |
| Executive Security Leadership | Approves governance position and risk acceptance for deferred capabilities (e.g., Salt Security) | Approver |

*RACI assignments align to STRIDE GV.RR policy intent.*

---

## 3. Architecture Summary

The Application and API Trust Architecture implements security controls across the delivery pipeline from code to runtime, with a future-state API security layer:

**Delivery Pipeline Security:**
- **Code + Dependencies**: Development teams commit code along with third-party open-source dependencies
- **Sonatype SCA**: Scans all open-source components for known vulnerabilities, license risk, and policy violations; integrated into the CI/CD pipeline as an automated gate
- **Policy Gate**: Non-compliant builds (critical CVEs, prohibited licenses) are blocked from progressing past the build stage; exceptions require documented risk acceptance
- **Burp Suite DAST**: Dynamic application security testing validates deployed applications against runtime vulnerabilities (OWASP Top 10, injection, authentication flaws); scan results generate remediation tickets
- **Deployment**: Applications passing all security gates are promoted to production

**Runtime and API Security (Future State):**
- **API Traffic Monitoring**: Post-deployment API traffic is monitored for anomalies and abuse patterns
- **Salt Security (future)**: Planned API discovery and behavioral analytics platform to provide API visibility, shadow API detection, and enforcement capabilities
- API trust outcomes include API visibility and enforcement, complementing SCA-driven supply-chain risk reduction and DAST-driven runtime assurance

**Trust Outcomes:**
- **Supply-chain risk reduction**: Sonatype SCA prevents vulnerable or non-compliant dependencies from reaching production
- **Runtime assurance**: Burp Suite DAST validates that deployed applications are free of exploitable runtime vulnerabilities
- **API visibility and enforcement**: Salt Security (future) will provide comprehensive API discovery and behavioral analytics

> **Cross-References:**
> - Trust model and policy engine: SRA §2
> - Identity controls for application authentication: SRA §4
> - Vulnerability context for infrastructure layer: SRA §7
> - Operational incident response for AppSec findings: SRA §9
> - Implementation roadmap for Salt Security deployment: SRA §11

**Current-State Architecture Diagram:**

> See: `12-application-and-api-trust-architecture.d2` (rendered in `rendering_svg_v3/` and `rendering_png_v3/`)

---

## 4. NIST CSF 2.0 Alignment

| NIST CSF 2.0 ID | Function | Subcategory Description | Implementation Status |
|---|---|---|---|
| PR.DS-01 | Protect | The confidentiality, integrity, and availability of data-at-rest are protected | Partially Implemented |
| PR.PS-05 | Protect | Installation and execution of unauthorized software are prevented | Partially Implemented |
| DE.CM-07 | Detect | The personnel activity and technology usage environment is monitored | Partially Implemented |

*Source: SRA Control Register, "NIST CSF Crosswalk" sheet, filtered to CTRL-008.*

**Gap Notes:**
- **PR.DS-01**: Sonatype SCA protects application integrity by preventing vulnerable dependencies from entering the build; DAST validates data handling in deployed applications. Gap: data-at-rest encryption validation for application datastores is not in scope of current AppSec tooling
- **PR.PS-05**: Pipeline policy gates prevent unauthorized or non-compliant software components from deploying. Gap: enforcement coverage extends to CI/CD-managed deployments but does not yet cover all legacy deployment paths
- **DE.CM-07**: Burp Suite DAST scans validate application behavior at runtime; future Salt Security will extend monitoring to API traffic. Gap: API discovery and behavioral analytics are future-state; current API monitoring is limited

---

## 5. Control Objectives and Requirements

| Control ID | Control Description | Primary Tooling | Evidence Source | Review Frequency |
|---|---|---|---|---|
| CTRL-008 | Application and API trust controls including SCA, DAST, pipeline policy enforcement, and API security | Sonatype; Burp Suite; Salt Security (future) | SCA/SAST reports; API test findings; remediation tickets | Per Release |

**Key Requirements:**
1. All production deployments must pass Sonatype SCA scan with no unmitigated critical vulnerabilities and no prohibited licenses
2. Policy gates must be enforced in CI/CD pipelines — manual bypass requires documented risk acceptance with AppSec approval
3. Burp Suite DAST scans must be executed against all internet-facing applications on a scheduled cadence (monthly minimum) and on major releases
4. Critical DAST findings (OWASP Top 10 exploitation-ready) must be remediated before the next production release or within 14 days, whichever is sooner
5. All AppSec findings must be tracked as remediation tickets with assigned ownership, severity classification, and SLA targets
6. Salt Security (when deployed) must achieve API inventory coverage for all production API endpoints within 90 days of deployment

---

## 6. Implementation Status and Roadmap

**Current Status:** Partially Implemented

**Maturity Assessment:**
- **In place:** Sonatype SCA integrated into primary CI/CD pipelines; policy gates enforcing critical CVE and license blocks; Burp Suite DAST operational for internet-facing applications; finding-to-ticket workflow via ServiceNow
- **In flight:** SCA coverage expansion to remaining CI/CD pipelines; DAST scan scheduling automation; Burp Suite authenticated scanning for internal applications
- **Deferred:** Salt Security API discovery and analytics deployment; SAST integration (future consideration); API behavioral enforcement; legacy deployment path coverage

**Roadmap Alignment:**
> See: SRA §11, Implementation Roadmap Phase 4 — Application + Ops  
> Diagram: `15-implementation-roadmap-v2.d2`, Phase 4

| Milestone | Target Date | Status |
|---|---|---|
| SCA coverage expansion (remaining pipelines) | Q2 2026 | In Flight |
| DAST scan scheduling automation | Q2 2026 | In Flight |
| Burp Suite authenticated scanning (internal apps) | Q3 2026 | Planned |
| Salt Security procurement and pilot | Q3 2026 | Planned |
| Salt Security production deployment | Q4 2026 | Deferred |
| API behavioral enforcement policies | Q1 2027 | Deferred |
| Legacy deployment path security gate coverage | Q1 2027 | Deferred |

---

## 7. Key Performance Indicators

| KPI | Metric Type | Target / Threshold | Cadence | Owner |
|---|---|---|---|---|
| SCA pipeline coverage | Coverage % | 100% of production CI/CD pipelines | Monthly | AppSec |
| Policy gate enforcement rate | Coverage % | 100% of builds scanned; 0 bypasses without risk acceptance | Monthly | AppSec |
| Critical SCA finding remediation SLA | Time-Based | 100% remediated before next release or within 14 days | Per Release | Development |
| DAST scan coverage (internet-facing apps) | Coverage % | 100% of internet-facing apps scanned monthly | Monthly | AppSec |
| Critical DAST finding remediation SLA | Time-Based | 100% remediated within 14 days | Monthly | Development |
| Open AppSec finding backlog | Risk Outcome | 0 Critical; ≤ 5 High past SLA | Monthly | AppSec |
| API endpoint inventory coverage (post-Salt) | Coverage % | ≥ 95% of production APIs discovered | Monthly | AppSec |

*Source: SRA §12, KPI Framework. See diagram: `17-kpi-framework.d2`.*

---

## 8. Regulatory Alignment

| Regulation | Applicable Requirements | SRA Mapping | Evidence |
|---|---|---|---|
| SOX (IT General Controls) | Program change management: code changes must be reviewed and tested for security before production deployment | §8, CTRL-008 | SCA scan results; DAST test reports; policy gate enforcement logs; risk acceptance records |
| SOX (IT General Controls) | Logical access to programs: third-party software components must be assessed for known vulnerabilities | §8, CTRL-008 | Sonatype SCA dependency inventory; CVE assessment reports; license compliance records |
| FERPA | Applications processing student data must undergo security testing to protect the confidentiality of education records | §8, CTRL-008 | DAST scan reports for FERPA-scope applications; remediation evidence; SCA reports for student-facing app dependencies |

*Source: SRA §13, Regulatory Compliance Alignment. See diagram: `18-regulatory-compliance-alignment.d2`.*

---

## Appendix D — Control Register Snapshot

*This appendix is a derived snapshot from `SRA_Control_Register.xlsx`, filtered to SRA §8. **Do not edit this table directly** — update the Excel register and regenerate.*

| Control ID | SRA Section | NIST CSF 2.0 IDs | Evidence Source | Control Owner | Review Frequency | Implementation Status |
|---|---|---|---|---|---|---|
| CTRL-008 | §8 | PR.DS-01, PR.PS-05, DE.CM-07 | SCA/SAST reports; API test findings; remediation tickets | AppSec | Per Release | Partially Implemented |

---

## Document Control

| Field | Value |
|---|---|
| Version | 1.0 — Draft |
| Created | March 2, 2026 |
| Last Updated | March 2, 2026 |
| Next Review | June 2, 2026 (Quarterly) |
| Approval Chain | AppSec → Security Architecture → Executive Security Leadership |

---

*This memo is governed by the TSRA Document Control model (SRA §14). See diagram: `20-document-control-metadata.d2`.*
