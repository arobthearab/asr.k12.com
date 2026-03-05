# Governance Memo: SRA §9 — Operational Trust Architecture

**Document Classification:** Internal / Controlled  
**SRA Section Reference:** §9  
**Version:** 1.0 — Draft  
**Date:** March 2, 2026  
**Control Owner:** Security Operations + ITSM  
**Approved By:** *[Pending — Executive Security Leadership]*  

---

## 1. Purpose and Scope

This governance memo establishes the security architecture governance position for **Operational Trust** as defined in the Trust Security Reference Architecture (TSRA), Section §9 — Operational Trust (ServiceNow SecOps, CMDB, Tagging).

**Scope:**
- ServiceNow Security Operations (SecOps) — incident management, vulnerability response, and evidence collection
- Workflow automation — ownership assignment, SLA enforcement, and verification tracking
- CMDB maturity (future enhancement) — asset-to-control linkage and criticality classification
- Cloud tagging governance (future enhancement) — criticality and ownership context for cloud resources
- Integration with all upstream security signal sources: CrowdStrike, Tenable, Sonatype, and Burp Suite
- Operational outcomes: clear ownership, risk-based prioritization, and audit-ready evidence

**Exclusions:**
- Individual security domain controls (covered under respective SRA sections §4–§8)
- SOC/SIEM platform architecture (operational tooling outside SRA scope)
- IT service management beyond security operations workflows

**Authoritative References:**
- Trust Security Reference Architecture (TSRA), §9
- SRA Control Register (`SRA_Control_Register.xlsx`), Control ID: CTRL-009
- D2 Architecture Diagram: `13-operational-trust-architecture.d2`
- STRIDE ISP — Incident Detection, Response, and Recovery (DE.CM, RS.MA, RC.RP)

---

## 2. Governance Authority

| Role | Responsibility | RACI |
|---|---|---|
| Security Operations + ITSM | Owns ServiceNow SecOps platform, manages operational workflows, produces operational evidence | Accountable |
| Security Architecture | Defines operational trust architecture standards and integration patterns | Responsible |
| IAM / Endpoint / AppSec / VulnMgmt | Provide upstream security signals; consume operational workflows for remediation | Consulted |
| Cloud Engineering | Maintains CMDB accuracy and cloud tagging compliance | Consulted |
| GRC / Compliance | Validates operational control effectiveness for SOX/FERPA evidence | Informed |
| Executive Security Leadership | Approves governance position and risk acceptance for operational maturity deferrals | Approver |

*RACI assignments align to STRIDE GV.RR policy intent.*

---

## 3. Architecture Summary

The Operational Trust Architecture serves as the central operations plane that ingests security signals from all domain-specific controls and operationalizes them through consistent workflow automation:

**Security Signal Inputs:**
- **CrowdStrike**: Endpoint detection alerts, device health events, and threat intelligence indicators
- **Tenable**: Vulnerability scan findings, CSPM posture drift alerts, and exposure metrics
- **Sonatype**: SCA findings, policy gate violations, and dependency risk notifications
- **Burp Suite**: DAST findings, runtime vulnerability detections, and scan completion events

All four signal sources are integrated into ServiceNow SecOps through automated ingestion pipelines.

**Central Operations Plane — ServiceNow SecOps:**
- **Incident Management**: Security incidents from upstream sources are created, classified, and assigned to response teams with severity-based SLAs
- **Vulnerability Response**: Vulnerability findings are ingested, deduplicated, and assigned to asset owners for remediation with SLA tracking
- **Evidence Collection**: All operational actions (assignment, escalation, remediation, verification) are logged as audit-ready evidence trails
- **Workflow Automation**: Automated ownership assignment based on CMDB records (where available), SLA timer management, escalation for SLA breaches, and verification workflows post-remediation

**Maturity Enhancements (Future State):**
- **CMDB Maturity**: Improving the CMDB to provide reliable asset-to-control linkage, enabling automated ownership assignment and criticality-based prioritization for all security findings
- **Cloud Tagging Governance**: Establishing mandatory cloud resource tagging for criticality classification and ownership context, feeding into ServiceNow for more accurate SLA assignment and reporting

**Operational Outcomes:**
- **Clear Ownership**: Every security finding has an assigned accountable owner with documented resolution expectations
- **Risk-Based Prioritization**: Findings are triaged using composite risk scores (severity × asset criticality) rather than raw CVSS alone
- **Audit-Ready Evidence**: Complete operational lifecycle from detection through remediation is documented and retrievable for audit

> **Cross-References:**
> - Trust model and policy engine: SRA §2
> - Identity controls feeding IAM-related incidents: SRA §4
> - Privileged session telemetry as high-priority signal: SRA §5
> - Device trust alerts from CrowdStrike/Defender: SRA §6
> - Vulnerability findings from Tenable: SRA §7
> - AppSec findings from Sonatype/Burp: SRA §8
> - KPI measurement for operational SLAs: SRA §12

**Current-State Architecture Diagram:**

> See: `13-operational-trust-architecture.d2` (rendered in `rendering_svg_v3/` and `rendering_png_v3/`)

---

## 4. NIST CSF 2.0 Alignment

| NIST CSF 2.0 ID | Function | Subcategory Description | Implementation Status |
|---|---|---|---|
| DE.CM-06 | Detect | External service provider activities and services are monitored to find potentially adverse events | Partially Implemented |
| RS.MA-01 | Respond | The incident response plan is executed in coordination with relevant third parties once an incident is declared | Partially Implemented |
| RC.RP-01 | Recover | The recovery portion of the incident response plan is executed once initiated from the incident response process | Partially Implemented |

*Source: SRA Control Register, "NIST CSF Crosswalk" sheet, filtered to CTRL-009.*

**Gap Notes:**
- **DE.CM-06**: ServiceNow ingests security signals from external service providers (CrowdStrike, Tenable, Sonatype); monitoring is operational. Gap: coverage of third-party SaaS security events beyond current tool integrations requires expansion
- **RS.MA-01**: ServiceNow SecOps provides coordinated incident response workflows with automated escalation. Gap: playbook-driven response automation is partially manual — future enhancement via ServiceNow SOAR capabilities
- **RC.RP-01**: Recovery workflows exist for major incident types; ServiceNow tracks recovery milestones. Gap: automated recovery verification and SLA measurement for recovery activities need formalization

---

## 5. Control Objectives and Requirements

| Control ID | Control Description | Primary Tooling | Evidence Source | Review Frequency |
|---|---|---|---|---|
| CTRL-009 | Operational trust controls including security workflow automation, SLA enforcement, CMDB linkage, and evidence management | ServiceNow SecOps | SecOps incident records; CMDB linkage and tagging evidence | Weekly |

**Key Requirements:**
1. All security signals from CrowdStrike, Tenable, Sonatype, and Burp Suite must be automatically ingested into ServiceNow SecOps — manual finding entry is prohibited for integrated sources
2. Every security incident and vulnerability finding must have an assigned owner within 4 hours of creation (Critical/High) or 24 hours (Medium/Low)
3. SLA timers must be enforced by severity: Critical ≤ 4 hours to acknowledge / ≤ 24 hours to resolve; High ≤ 8 hours / ≤ 7 days; Medium ≤ 24 hours / ≤ 30 days
4. SLA breaches must trigger automated escalation to the next management tier
5. Remediation closure requires verification evidence — self-attestation alone is insufficient for Critical and High findings
6. All operational evidence (assignment, action, resolution, verification) must be retained for 12 months minimum for audit

---

## 6. Implementation Status and Roadmap

**Current Status:** Partially Implemented

**Maturity Assessment:**
- **In place:** ServiceNow SecOps operational for incident management and vulnerability response; automated ingestion from CrowdStrike and Tenable; SLA-based workflow enforcement; evidence trail retention; weekly operational reporting
- **In flight:** Sonatype and Burp Suite ingestion pipeline completion; CMDB asset-to-control linkage improvement; SLA automation refinements for escalation
- **Deferred:** Cloud tagging governance enforcement; CMDB full maturity for dynamic cloud workloads; ServiceNow SOAR playbook automation; predictive operational analytics

**Roadmap Alignment:**
> See: SRA §11, Implementation Roadmap Phase 4 — Application + Ops  
> Diagram: `15-implementation-roadmap-v2.d2`, Phase 4

| Milestone | Target Date | Status |
|---|---|---|
| Sonatype → ServiceNow ingestion pipeline | Q2 2026 | In Flight |
| Burp Suite → ServiceNow ingestion pipeline | Q2 2026 | In Flight |
| CMDB asset-to-control linkage improvement | Q3 2026 | Planned |
| SLA escalation automation refinements | Q3 2026 | Planned |
| Cloud tagging governance enforcement | Q4 2026 | Deferred |
| ServiceNow SOAR playbook automation | Q1 2027 | Deferred |
| CMDB full maturity for dynamic cloud workloads | Q1 2027 | Deferred |

---

## 7. Key Performance Indicators

| KPI | Metric Type | Target / Threshold | Cadence | Owner |
|---|---|---|---|---|
| Signal ingestion coverage | Coverage % | 100% of integrated tools actively ingesting | Weekly | Security Operations |
| Mean time to assign ownership | Time-Based | ≤ 4 hours (Critical/High); ≤ 24 hours (Medium/Low) | Weekly | Security Operations |
| SLA compliance rate (incidents) | Coverage % | ≥ 95% of incidents resolved within SLA | Weekly | Security Operations |
| SLA compliance rate (vulnerabilities) | Coverage % | ≥ 90% of vulnerability findings remediated within SLA | Monthly | Security Operations |
| SLA breach escalation rate | Coverage % | 100% of breaches escalated within policy | Weekly | Security Operations |
| Evidence completeness rate | Coverage % | ≥ 98% of closed items with complete evidence trail | Monthly | ITSM |
| CMDB linkage accuracy | Coverage % | ≥ 85% of findings linked to CMDB CI (target: ≥ 95% post-maturity) | Monthly | Cloud Engineering |

*Source: SRA §12, KPI Framework. See diagram: `17-kpi-framework.d2`.*

---

## 8. Regulatory Alignment

| Regulation | Applicable Requirements | SRA Mapping | Evidence |
|---|---|---|---|
| SOX (IT General Controls) | Monitoring of information processing: security incidents affecting financial systems must be detected, responded to, and documented | §9, CTRL-009 | ServiceNow incident records; SLA compliance reports; resolution and verification evidence |
| SOX (IT General Controls) | IT risk assessment: vulnerability remediation for financial systems must be tracked with ownership and SLA compliance | §9, CTRL-009 | Vulnerability response records; remediation SLA dashboards; escalation logs |
| FERPA | Security incidents involving student data must be investigated, documented, and reported per institutional policy | §9, CTRL-009 | FERPA-tagged incident records; investigation and resolution evidence; notification records |

*Source: SRA §13, Regulatory Compliance Alignment. See diagram: `18-regulatory-compliance-alignment.d2`.*

---

## Appendix D — Control Register Snapshot

*This appendix is a derived snapshot from `SRA_Control_Register.xlsx`, filtered to SRA §9. **Do not edit this table directly** — update the Excel register and regenerate.*

| Control ID | SRA Section | NIST CSF 2.0 IDs | Evidence Source | Control Owner | Review Frequency | Implementation Status |
|---|---|---|---|---|---|---|
| CTRL-009 | §9 | DE.CM-06, RS.MA-01, RC.RP-01 | SecOps incident records; CMDB linkage and tagging evidence | Security Operations + ITSM | Weekly | Partially Implemented |

---

## Document Control

| Field | Value |
|---|---|
| Version | 1.0 — Draft |
| Created | March 2, 2026 |
| Last Updated | March 2, 2026 |
| Next Review | June 2, 2026 (Quarterly) |
| Approval Chain | Security Operations + ITSM → Security Architecture → Executive Security Leadership |

---

*This memo is governed by the TSRA Document Control model (SRA §14). See diagram: `20-document-control-metadata.d2`.*
