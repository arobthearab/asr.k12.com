# Governance Memo: SRA §7 — Exposure and Posture Architecture

**Document Classification:** Internal / Controlled  
**SRA Section Reference:** §7  
**Version:** 1.0 — Draft  
**Date:** March 2, 2026  
**Control Owner:** Vulnerability Management  
**Approved By:** *[Pending — Executive Security Leadership]*  

---

## 1. Purpose and Scope

This governance memo establishes the security architecture governance position for **Exposure and Posture Management** as defined in the Trust Security Reference Architecture (TSRA), Section §7 — Exposure and Posture (Tenable VM and CSPM).

**Scope:**
- Tenable Vulnerability Management (VM) — vulnerability identification across infrastructure, endpoints, and applications
- Tenable Cloud Security Posture Management (CSPM) — posture assessment and configuration drift detection across AWS, Azure, and GCP
- ServiceNow integration for vulnerability workflow operationalization — ownership assignment, SLA tracking, and verification
- Asset owner accountability for remediation within defined SLAs
- Cloud estate coverage across all three major cloud providers (AWS, Azure, GCP)

**Exclusions:**
- Endpoint protection and EDR capabilities (covered under SRA §6 — Device Trust)
- Application-layer security testing — SCA/DAST (covered under SRA §8 — Application and API Trust)
- API-specific vulnerability management (covered under SRA §8)

**Authoritative References:**
- Trust Security Reference Architecture (TSRA), §7
- SRA Control Register (`SRA_Control_Register.xlsx`), Control ID: CTRL-007
- D2 Architecture Diagram: `11-exposure-and-posture-architecture.d2`
- STRIDE ISP — Vulnerability Management and Risk Assessment (ID.RA)

---

## 2. Governance Authority

| Role | Responsibility | RACI |
|---|---|---|
| Vulnerability Management | Owns Tenable VM and CSPM platforms, manages scan policies, produces vulnerability evidence | Accountable |
| Security Architecture | Defines exposure management architecture standards and cloud posture baselines | Responsible |
| Security Operations | Triages critical vulnerabilities, escalates SLA breaches, coordinates emergency patching | Consulted |
| Cloud Engineering | Remediates cloud posture findings and maintains infrastructure configuration compliance | Consulted |
| GRC / Compliance | Validates vulnerability management alignment to SOX and regulatory requirements | Informed |
| Executive Security Leadership | Approves governance position and risk acceptance for deferred remediation | Approver |

*RACI assignments align to STRIDE GV.RR policy intent.*

---

## 3. Architecture Summary

The Exposure and Posture Architecture implements a continuous assessment model across infrastructure and cloud estates with operationalized remediation through ServiceNow:

**Cloud Estate — Multi-Cloud Coverage:**
- Tenable CSPM scans and monitors configuration posture across AWS, Azure, and GCP
- Drift detection identifies configuration changes that deviate from established security baselines
- Cloud misconfigurations are classified by severity and mapped to asset ownership

**Assessment and Drift Detection:**
- **Tenable VM**: Continuous vulnerability scanning identifies known vulnerabilities (CVEs) across infrastructure, servers, and endpoints; findings are scored by CVSS and prioritized by asset criticality
- **Tenable CSPM**: Posture assessments against CIS benchmarks and cloud-native security baselines; drift detection alerts trigger remediation workflows when configurations deviate from approved state

**Operationalization — ServiceNow Integration:**
- Vulnerability findings from both Tenable VM and CSPM are ingested into ServiceNow SecOps for workflow automation
- ServiceNow assigns ownership based on CMDB asset records, applies SLA timers by severity, and tracks remediation through verification
- Asset owners and accountable teams receive notifications and are responsible for remediation within policy SLAs
- Verified remediation evidence is retained for audit and compliance reporting

> **Cross-References:**
> - Trust model and policy engine: SRA §2
> - Device trust scores informed by vulnerability context: SRA §6
> - Operational trust workflows for vulnerability response: SRA §9
> - KPI measurement for vulnerability SLAs: SRA §12

**Current-State Architecture Diagram:**

> See: `11-exposure-and-posture-architecture.d2` (rendered in `rendering_svg_v3/` and `rendering_png_v3/`)

---

## 4. NIST CSF 2.0 Alignment

| NIST CSF 2.0 ID | Function | Subcategory Description | Implementation Status |
|---|---|---|---|
| ID.RA-01 | Identify | Vulnerabilities in assets are identified, validated, and recorded | Partially Implemented |
| DE.CM-02 | Detect | The physical environment is monitored to detect potentially adverse events | Partially Implemented |
| PR.PS-04 | Protect | Adequate capacity to ensure availability is maintained | Partially Implemented |

*Source: SRA Control Register, "NIST CSF Crosswalk" sheet, filtered to CTRL-007.*

**Gap Notes:**
- **ID.RA-01**: Tenable VM provides comprehensive vulnerability identification across managed infrastructure and endpoints; CSPM extends coverage to cloud configuration. Gap: container and serverless workload scanning is not yet fully integrated into the Tenable pipeline
- **DE.CM-02**: Tenable CSPM continuously monitors cloud environments for configuration changes and posture drift. Gap: real-time drift alerting is operational but automated remediation (auto-fix) is not yet enabled for most finding types
- **PR.PS-04**: Scan capacity and scheduling are managed to avoid operational impact. Gap: scan coverage metrics for dynamic cloud workloads (auto-scaling groups, ephemeral instances) require improvement

---

## 5. Control Objectives and Requirements

| Control ID | Control Description | Primary Tooling | Evidence Source | Review Frequency |
|---|---|---|---|---|
| CTRL-007 | Exposure and posture management including vulnerability scanning, cloud posture assessment, and drift detection | Tenable VM; Tenable CSPM | Vulnerability scans; CSPM posture trend reports | Weekly |

**Key Requirements:**
1. All in-scope infrastructure, endpoints, and cloud environments must be scanned by Tenable VM on a recurring schedule (weekly minimum for infrastructure, daily for internet-facing assets)
2. Cloud environments (AWS, Azure, GCP) must be continuously monitored by Tenable CSPM against CIS benchmarks
3. Critical vulnerabilities (CVSS ≥ 9.0) must be remediated or mitigated within 7 days; high vulnerabilities (CVSS 7.0–8.9) within 30 days
4. Cloud posture drift findings rated Critical or High must trigger automated ServiceNow incident creation within 4 hours
5. All findings must be assigned to accountable asset owners via ServiceNow with SLA tracking enabled
6. Remediation must be verified through rescan before closure — self-attestation alone is insufficient

---

## 6. Implementation Status and Roadmap

**Current Status:** Partially Implemented

**Maturity Assessment:**
- **In place:** Tenable VM scanning operational across managed infrastructure; Tenable CSPM active for AWS, Azure, and GCP; ServiceNow integration for vulnerability workflow; SLA-based remediation tracking; weekly compliance reporting
- **In flight:** Container workload scanning integration; CSPM drift auto-alerting refinement; ServiceNow CMDB linkage improvement for dynamic cloud assets
- **Deferred:** Automated remediation (auto-fix) for low-risk cloud posture findings; serverless workload scanning; predictive exposure analytics

**Roadmap Alignment:**
> See: SRA §11, Implementation Roadmap Phase 3 — Device + Posture  
> Diagram: `15-implementation-roadmap-v2.d2`, Phase 3

| Milestone | Target Date | Status |
|---|---|---|
| Container workload scanning integration | Q2 2026 | In Flight |
| CSPM drift alerting refinement | Q2 2026 | In Flight |
| ServiceNow CMDB linkage for dynamic cloud assets | Q3 2026 | Planned |
| Automated remediation for low-risk CSPM findings | Q4 2026 | Deferred |
| Serverless workload scanning | Q1 2027 | Deferred |
| Predictive exposure analytics | Q2 2027 | Deferred |

---

## 7. Key Performance Indicators

| KPI | Metric Type | Target / Threshold | Cadence | Owner |
|---|---|---|---|---|
| Scan coverage (infrastructure) | Coverage % | ≥ 98% of managed assets scanned on schedule | Weekly | Vulnerability Management |
| Scan coverage (cloud workloads) | Coverage % | ≥ 95% of cloud accounts monitored by CSPM | Weekly | Vulnerability Management |
| Critical vulnerability remediation SLA | Time-Based | 100% remediated within 7 days | Weekly | Vulnerability Management |
| High vulnerability remediation SLA | Time-Based | ≥ 95% remediated within 30 days | Monthly | Vulnerability Management |
| Cloud posture compliance rate | Coverage % | ≥ 90% CIS benchmark compliance across all clouds | Weekly | Cloud Engineering |
| Mean time to assign vulnerability ownership | Time-Based | ≤ 4 hours for Critical/High findings | Weekly | Security Operations |
| Overdue vulnerability count | Risk Outcome | 0 Critical; ≤ 10 High past SLA | Weekly | Vulnerability Management |

*Source: SRA §12, KPI Framework. See diagram: `17-kpi-framework.d2`.*

---

## 8. Regulatory Alignment

| Regulation | Applicable Requirements | SRA Mapping | Evidence |
|---|---|---|---|
| SOX (IT General Controls) | IT risk assessment: vulnerabilities in systems supporting financial reporting must be identified, assessed, and remediated | §7, CTRL-007 | Tenable VM scan reports; vulnerability SLA compliance dashboards; remediation verification records |
| SOX (IT General Controls) | Computer operations: cloud environments hosting financial applications must maintain configuration baselines with drift detection | §7, CTRL-007 | Tenable CSPM posture trend reports; drift detection alerts; CIS benchmark compliance scores |
| FERPA | Systems processing student data must be assessed for vulnerabilities and maintained in a secure configuration | §7, CTRL-007 | Vulnerability scan results for FERPA-scope systems; CSPM findings for student data cloud accounts |

*Source: SRA §13, Regulatory Compliance Alignment. See diagram: `18-regulatory-compliance-alignment.d2`.*

---

## Appendix D — Control Register Snapshot

*This appendix is a derived snapshot from `SRA_Control_Register.xlsx`, filtered to SRA §7. **Do not edit this table directly** — update the Excel register and regenerate.*

| Control ID | SRA Section | NIST CSF 2.0 IDs | Evidence Source | Control Owner | Review Frequency | Implementation Status |
|---|---|---|---|---|---|---|
| CTRL-007 | §7 | ID.RA-01, DE.CM-02, PR.PS-04 | Vulnerability scans; CSPM posture trend reports | Vulnerability Management | Weekly | Partially Implemented |

---

## Document Control

| Field | Value |
|---|---|
| Version | 1.0 — Draft |
| Created | March 2, 2026 |
| Last Updated | March 2, 2026 |
| Next Review | June 2, 2026 (Quarterly) |
| Approval Chain | Vulnerability Management → Security Architecture → Executive Security Leadership |

---

*This memo is governed by the TSRA Document Control model (SRA §14). See diagram: `20-document-control-metadata.d2`.*
