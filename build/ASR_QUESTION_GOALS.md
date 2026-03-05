# ASR Questionnaire — Goal-State Questions

> **Purpose:** Track proposed new questions that address gaps identified in the
> March 2026 control-target analysis (NIST CSF 2.0, FERPA, SOX §404 ITGC).
> These questions are **not yet in `asr_questions.yaml`** — they represent the
> target state for future questionnaire versions.
>
> **Current state:** 7 domains, 48 domain questions + 1 classification = 49 total (V4).

---

## 1. Risk Management Governance (GV.RM) — NEW DOMAIN

**Gap refs:** GAP-08 (GV.RM-02), SRA §11

| # | Proposed Question | Choices | Weight | Rationale |
|---|---|---|---|---|
| 1 | Has a formal risk appetite or tolerance statement been defined for this application? | Yes — documented and approved / Yes — informal or draft / No — not defined / N/A | High | GV.RM-02 is In Progress; no ASR question captures per-app risk appetite. |
| 2 | Is the application included in the enterprise risk register? | Yes — with risk owner and treatment plan / Yes — listed without treatment plan / No — not in register / Unknown | High | GV.RM-01 is Implemented at enterprise level but per-app inclusion is unverified. |
| 3 | Has a formal risk assessment been performed for this application within the past 12 months? | Yes — quantitative or semi-quantitative / Yes — qualitative only / No / Not applicable | High | Bridges GV.RM-03 to per-application level. |

---

## 2. Awareness and Training (PR.AT) — NEW DOMAIN

**Gap refs:** GAP-11 (PR.AT-01, PR.AT-02), GAP-13, SRA §13

| # | Proposed Question | Choices | Weight | Rationale |
|---|---|---|---|---|
| 1 | Is role-based security awareness training required for users of this application? | Yes — mandatory with completion tracking / Yes — recommended but not enforced / No — general awareness only / No training requirement | High | PR.AT-01 (awareness for all users) entirely unmapped. |
| 2 | Do administrators and privileged users receive specialized training for this application's security controls? | Yes — documented specialized training / Yes — informal knowledge transfer / No specialized training / N/A — no privileged roles | High | PR.AT-02 (role-specific training) entirely unmapped. |

---

## 3. Adverse Event Analysis (DE.AE) — NEW DOMAIN

**Gap refs:** GAP-06 (DE.AE-02–08), GAP-13, SRA §9

| # | Proposed Question | Choices | Weight | Rationale |
|---|---|---|---|---|
| 1 | Are security events from this application correlated with other data sources for anomaly detection? | Yes — SIEM correlation with automated rules / Yes — manual correlation / Partial — limited log integration / No correlation | High | DE.AE-02 (events analyzed for anomalies) absent from SRA. |
| 2 | Is there a defined threshold or baseline for what constitutes an adverse event for this application? | Yes — documented with automated alerting / Yes — documented but manually monitored / Informal understanding only / No baseline defined | High | DE.AE-03 (event context established) absent from SRA. |
| 3 | Are incident indicators from this application enriched with threat intelligence? | Yes — automated TI enrichment / Yes — manual enrichment during triage / No enrichment / N/A | Medium | DE.AE-06 (information on adverse events shared) absent from SRA. |

---

## 4. Supply Chain / Third-Party Risk (GV.SC) — NEW DOMAIN

**Gap refs:** GAP-07 (GV.SC-01), GAP-09 (GV.SC-02–10), SRA §11

| # | Proposed Question | Choices | Weight | Rationale |
|---|---|---|---|---|
| 1 | Has the vendor or third-party provider been assessed under a formal supply chain risk management program? | Yes — assessed with documented findings / Yes — questionnaire only / No formal assessment / N/A — internally developed | High | GV.SC-01 Planned; no ASR question addresses supplier risk posture. |
| 2 | Do contracts with the application vendor include security requirements and right-to-audit clauses? | Yes — with SLA and audit rights / Yes — general security terms only / No security clauses / Unknown | High | GV.SC-04/05 (contractual requirements) unmapped. |
| 3 | Is the vendor's supply chain integrity verified (e.g., SBOM, code signing, build provenance)? | Yes — SBOM and provenance verified / Yes — code signing only / No verification / N/A | Medium | GV.SC-07/08 (supply chain integrity) unmapped. |
| 4 | Is ongoing monitoring of vendor security posture performed? | Yes — continuous monitoring (e.g., SecurityScorecard, BitSight) / Yes — periodic reassessment / No ongoing monitoring / N/A | High | GV.SC-09/10 (post-acquisition monitoring) unmapped. |

---

## 5. SOX §404 ITGC Gaps — Additions to Existing Domains

### 5a. Change Management (Secure Dev domain)

**Gap refs:** GAP-03 (CM-1, PD-3, PD-4), SRA §8

| # | Proposed Question | Choices | Weight | Rationale |
|---|---|---|---|---|
| 1 | Is there a documented change management policy specific to this application? | Yes — application-specific CMP / Yes — covered by enterprise CMP / No documented policy / N/A — SaaS | High | SOX CM-1 referenced but no artefact prescribed. |
| 2 | Are security testing results formally reviewed and signed off before production deployment? | Yes — mandatory sign-off gate / Yes — documented but not enforced / No formal sign-off / N/A — vendor managed | High | SOX PD-3 (security testing sign-off) lacks verification gate. |
| 3 | For system conversions or data migrations, is testing and validation formally documented? | Yes — documented test plan with acceptance criteria / Yes — ad-hoc testing / No formal validation / N/A — no conversions | Medium | SOX PD-4 (conversion testing) lacks validation evidence. |

### 5b. Computer Operations (IR/BC domain)

**Gap refs:** GAP-05 (CO-1, CO-4), SRA §9

| # | Proposed Question | Choices | Weight | Rationale |
|---|---|---|---|---|
| 1 | Are batch jobs or scheduled processes for this application managed through an enterprise job scheduler? | Yes — enterprise scheduler with monitoring / Yes — application-native scheduling / Manual or ad-hoc execution / N/A — no batch processing | Medium | SOX CO-1 (job scheduling) lacks ServiceNow automation evidence. |
| 2 | Are data integrity checks performed on batch processing outputs? | Yes — automated reconciliation and alerting / Yes — manual reconciliation / No integrity checks / N/A | Medium | SOX CO-4 (batch processing integrity) evidence gap. |

---

## 6. FERPA Gaps — Additions to Data Protection Domain

**Gap refs:** GAP-10 (§99.4, §99.7, §99.12, §99.33, §99.37), SRA §13

| # | Proposed Question | Choices | Weight | Rationale |
|---|---|---|---|---|
| 1 | Does the application support notification of student/parent rights as required by FERPA §99.7? | Yes — integrated annual notice mechanism / Yes — manual process / Not applicable / Not implemented | High | §99.7 annual FERPA notice requirements have no architectural control. |
| 2 | Are re-disclosure restrictions enforced when sharing data from this application with third parties (FERPA §99.33)? | Yes — technical controls preventing unauthorized re-disclosure / Yes — contractual controls only / No controls / Not applicable | High | §99.33 re-disclosure conditions lack architectural enforcement. |
| 3 | Does the application support directory information opt-out procedures (FERPA §99.37)? | Yes — automated opt-out with data suppression / Yes — manual opt-out process / Not applicable / Not implemented | Medium | §99.37 directory information opt-out not addressed. |
| 4 | Are limitations on re-disclosure to third parties technically enforced (FERPA §99.12)? | Yes — DLP or access controls restricting re-disclosure / Yes — policy-based only / No technical enforcement / Not applicable | Medium | §99.12 re-disclosure limitations unaddressed. |

---

## 7. IAM Enhancements — Additions to IAM Domain

**Gap refs:** GAP-01 (PR.AA-04, PR.AA-06), SRA §4

| # | Proposed Question | Choices | Weight | Rationale |
|---|---|---|---|---|
| 1 | Are identity assertions (e.g., SAML claims, OIDC tokens) validated and managed per a documented standard? | Yes — assertion validation with claim mapping / Yes — default IdP configuration / No documented standard / N/A | High | PR.AA-04 (identity assertions managed) unmapped. |
| 2 | Is there a formal process for managing and certifying access rights granted to this application? | Yes — automated access certification with SailPoint / Yes — manual periodic review / No certification process / N/A | High | PR.AA-06 (access rights managed) unmapped. |

---

## Summary

| Area | New Questions | New Domains? |
|---|---|---|
| Risk Management (GV.RM) | 3 | Yes |
| Awareness & Training (PR.AT) | 2 | Yes |
| Adverse Event Analysis (DE.AE) | 3 | Yes |
| Supply Chain (GV.SC) | 4 | Yes |
| SOX Change Mgmt additions | 3 | No (Secure Dev) |
| SOX Computer Ops additions | 2 | No (IR/BC) |
| FERPA additions | 4 | No (Data Protection) |
| IAM enhancements | 2 | No (IAM) |
| **Total** | **23** | **4 new** |

Implementing all 23 questions would bring the ASR from 48 → 71 domain questions
(+ 1 classification = 72 total). Excel summary row and RSK composite ranges
would need to be updated accordingly.

---

*Generated: March 4, 2026 — from gap analysis comparing SRA V7 coverage against
NIST CSF 2.0 (100 subcategories), FERPA 34 CFR Part 99 (18 sections), and
SOX §404 ITGC (19 controls).*
