#!/usr/bin/env python3
"""
Stride Deliverables Master Build Script
========================================
Generates three PDF deliverables:
  1. Stride Policy Cross Reference V6
  2. Stride Security Reference Architecture V7
  3. Stride ASR Questionnaire V3

Requires: pypdf, python-docx, jinja2 in venv; pandoc + pdflatex on PATH
"""
import json, os, sys, pathlib, subprocess, textwrap, re, math
from datetime import date

# --- Paths ---
BASE = pathlib.Path(__file__).resolve().parent          # <repo>/build/
REPO = BASE.parent                                        # <repo>/
EXTRACTED = BASE / "extracted"
PNG_DIR = REPO / "diagrams" / "rendering_png_v2"
OUTPUT = BASE / "output"
OUTPUT.mkdir(exist_ok=True)
TEX_DIR = BASE / "tex"
TEX_DIR.mkdir(exist_ok=True)

# Ensure LaTeX is on PATH
os.environ["PATH"] = "/Library/TeX/texbin:" + os.environ.get("PATH", "")

# --- Load extracted data ---
with open(EXTRACTED / "policies.json") as f:
    policies_data = json.load(f)
with open(EXTRACTED / "workpapers.json") as f:
    workpapers_data = json.load(f)

# ============================================================
# REGULATORY REFERENCE DATA
# ============================================================

# NIST CSF 2.0 - Complete Function → Category → Subcategory taxonomy
NIST_CSF = {
    "GV": {
        "name": "GOVERN",
        "categories": {
            "GV.OC": {
                "name": "Organizational Context",
                "subcategories": {
                    "GV.OC-01": "The organizational mission is understood and informs cybersecurity risk management",
                    "GV.OC-02": "Internal and external stakeholders are understood, and their needs and expectations regarding cybersecurity risk management are understood and considered",
                    "GV.OC-03": "Legal, regulatory, and contractual requirements regarding cybersecurity — including privacy and civil liberties obligations — are understood and managed",
                    "GV.OC-04": "Critical objectives, capabilities, and services that external stakeholders depend on or expect are understood and communicated",
                    "GV.OC-05": "Outcomes, capabilities, and services that the organization depends on are understood and communicated",
                }
            },
            "GV.RM": {
                "name": "Risk Management Strategy",
                "subcategories": {
                    "GV.RM-01": "Risk management objectives are established and expressed as statements that organizational leadership broadly agrees with",
                    "GV.RM-02": "Risk appetite and risk tolerance statements are established, communicated, and maintained",
                    "GV.RM-03": "Cybersecurity risk management activities and outcomes are included in enterprise risk management processes",
                    "GV.RM-04": "Strategic direction that describes appropriate risk response options is established and communicated",
                    "GV.RM-05": "Lines of communication across the organization are established for cybersecurity risks, including risks from suppliers and other third parties",
                    "GV.RM-06": "A standardized method for calculating, documenting, categorizing, and prioritizing cybersecurity risks is established and communicated",
                    "GV.RM-07": "Strategic opportunities (i.e., positive risks) are characterized and are included in organizational cybersecurity risk discussions",
                }
            },
            "GV.RR": {
                "name": "Roles, Responsibilities, and Authorities",
                "subcategories": {
                    "GV.RR-01": "Organizational leadership is responsible and accountable for cybersecurity risk and fosters a culture that is risk-aware, ethical, and continually improving",
                    "GV.RR-02": "Roles, responsibilities, and authorities related to cybersecurity risk management are established, communicated, understood, and enforced",
                    "GV.RR-03": "Adequate resources are allocated commensurate with the cybersecurity risk strategy, roles, responsibilities, and policies",
                    "GV.RR-04": "Cybersecurity is included in human resources practices",
                }
            },
            "GV.PO": {
                "name": "Policy",
                "subcategories": {
                    "GV.PO-01": "Policy for managing cybersecurity risks is established based on organizational context, cybersecurity strategy, and priorities and is communicated and enforced",
                    "GV.PO-02": "Policy for managing cybersecurity risks is reviewed, updated, communicated, and enforced to reflect changes in requirements, threats, technology, and organizational mission",
                }
            },
            "GV.OV": {
                "name": "Oversight",
                "subcategories": {
                    "GV.OV-01": "Cybersecurity risk management strategy outcomes are reviewed to inform and adjust strategy and direction",
                    "GV.OV-02": "The cybersecurity risk management strategy is reviewed and adjusted to ensure coverage of organizational requirements and risks",
                    "GV.OV-03": "Organizational cybersecurity risk management performance is evaluated and reviewed for adjustments needed",
                }
            },
            "GV.SC": {
                "name": "Cybersecurity Supply Chain Risk Management",
                "subcategories": {
                    "GV.SC-01": "A cybersecurity supply chain risk management program, strategy, objectives, policies, and processes are established and agreed to by organizational stakeholders",
                    "GV.SC-02": "Cybersecurity roles and responsibilities for suppliers, customers, and partners are established, communicated, and coordinated internally and externally",
                    "GV.SC-03": "Cybersecurity supply chain risk management is integrated into cybersecurity and enterprise risk management, risk assessment, and improvement processes",
                    "GV.SC-04": "Suppliers are known and prioritized by criticality",
                    "GV.SC-05": "Requirements to address cybersecurity risks in supply chains are established, prioritized, and integrated into contracts and other types of agreements with suppliers and other relevant third parties",
                    "GV.SC-06": "Planning and due diligence are performed to reduce risks before entering into formal supplier or other third-party relationships",
                    "GV.SC-07": "The risks posed by a supplier, their products and services, and other third parties are understood, recorded, prioritized, assessed, responded to, and monitored over the course of the relationship",
                    "GV.SC-08": "Relevant suppliers and other third parties are included in incident planning, response, and recovery activities",
                    "GV.SC-09": "Supply chain security practices are integrated into cybersecurity and enterprise risk management programs, and their performance is monitored throughout the technology product and service life cycle",
                    "GV.SC-10": "Cybersecurity supply chain risk management plans include provisions for activities that occur after the conclusion of a partnership or service agreement",
                }
            },
        }
    },
    "ID": {
        "name": "IDENTIFY",
        "categories": {
            "ID.AM": {
                "name": "Asset Management",
                "subcategories": {
                    "ID.AM-01": "Inventories of hardware managed by the organization are maintained",
                    "ID.AM-02": "Inventories of software, services, and systems managed by the organization are maintained",
                    "ID.AM-03": "Representations of the organization's authorized network communication and internal and external network data flows are maintained",
                    "ID.AM-04": "Inventories of services provided by suppliers are maintained",
                    "ID.AM-05": "Assets are prioritized based on classification, criticality, resources, and impact on the mission",
                    "ID.AM-07": "Inventories of data and corresponding metadata for designated data types are maintained",
                    "ID.AM-08": "Systems, hardware, software, services, and data are managed throughout their life cycles",
                }
            },
            "ID.RA": {
                "name": "Risk Assessment",
                "subcategories": {
                    "ID.RA-01": "Vulnerabilities in assets are identified, validated, and recorded",
                    "ID.RA-02": "Cyber threat intelligence is received from information sharing forums and sources",
                    "ID.RA-03": "Internal and external threats to the organization are identified and recorded",
                    "ID.RA-04": "Potential impacts and likelihoods of threats exploiting vulnerabilities are identified and recorded",
                    "ID.RA-05": "Threats, vulnerabilities, likelihoods, and impacts are used to understand inherent risk and inform risk response prioritization",
                    "ID.RA-06": "Risk responses are chosen, prioritized, planned, tracked, and communicated",
                    "ID.RA-07": "Changes and exceptions are managed, assessed for risk impact, recorded, and tracked",
                    "ID.RA-08": "Processes for receiving, analyzing, and responding to vulnerability disclosures are established",
                    "ID.RA-09": "The authenticity and integrity of hardware and software are assessed prior to acquisition and use",
                    "ID.RA-10": "Critical suppliers are assessed prior to acquisition",
                }
            },
            "ID.IM": {
                "name": "Improvement",
                "subcategories": {
                    "ID.IM-01": "Improvements are identified from evaluations",
                    "ID.IM-02": "Improvements are identified from security tests and exercises, including those done in coordination with suppliers and relevant third parties",
                    "ID.IM-03": "Improvements are identified from execution of operational processes, procedures, and activities",
                    "ID.IM-04": "Incident response plans and other cybersecurity plans that affect operations are established, communicated, maintained, and improved",
                }
            },
        }
    },
    "PR": {
        "name": "PROTECT",
        "categories": {
            "PR.AA": {
                "name": "Identity Management, Authentication, and Access Control",
                "subcategories": {
                    "PR.AA-01": "Identities and credentials for authorized users, services, and hardware are managed by the organization",
                    "PR.AA-02": "Identities are proofed and bound to credentials based on the context of interactions",
                    "PR.AA-03": "Users, services, and hardware are authenticated",
                    "PR.AA-04": "Identity assertions are protected, conveyed, and verified",
                    "PR.AA-05": "Access permissions, entitlements, and authorizations are defined in a policy, managed, enforced, and reviewed, and incorporate the principles of least privilege and separation of duties",
                    "PR.AA-06": "Physical access to assets is managed, monitored, and enforced commensurate with risk",
                }
            },
            "PR.AT": {
                "name": "Awareness and Training",
                "subcategories": {
                    "PR.AT-01": "Personnel are provided with awareness and training so that they possess the knowledge and skills to perform general tasks with cybersecurity risks in mind",
                    "PR.AT-02": "Individuals in specialized roles are provided with awareness and training so that they possess the knowledge and skills to perform relevant tasks with cybersecurity risks in mind",
                }
            },
            "PR.DS": {
                "name": "Data Security",
                "subcategories": {
                    "PR.DS-01": "The confidentiality, integrity, and availability of data-at-rest are protected",
                    "PR.DS-02": "The confidentiality, integrity, and availability of data-in-transit are protected",
                    "PR.DS-10": "The confidentiality, integrity, and availability of data-in-use are protected",
                    "PR.DS-11": "Backups of data are created, protected, maintained, and tested",
                }
            },
            "PR.PS": {
                "name": "Platform Security",
                "subcategories": {
                    "PR.PS-01": "The configuration of technology assets is managed consistently with applicable security policies",
                    "PR.PS-02": "Software is maintained, replaced, and removed commensurate with risk",
                    "PR.PS-03": "Hardware is maintained, replaced, and removed commensurate with risk",
                    "PR.PS-04": "Log records are generated and made available for continuous monitoring",
                    "PR.PS-05": "Installation and execution of unauthorized software is prevented",
                    "PR.PS-06": "Secure software development practices are integrated, and their performance is monitored throughout the software development life cycle",
                }
            },
            "PR.IR": {
                "name": "Technology Infrastructure Resilience",
                "subcategories": {
                    "PR.IR-01": "Networks and environments are protected from unauthorized logical access and usage",
                    "PR.IR-02": "The organization's technology assets are protected from environmental threats",
                    "PR.IR-03": "Mechanisms are implemented to achieve resilience requirements in normal and adverse situations",
                    "PR.IR-04": "Adequate resource capacity to ensure availability is maintained",
                }
            },
        }
    },
    "DE": {
        "name": "DETECT",
        "categories": {
            "DE.CM": {
                "name": "Continuous Monitoring",
                "subcategories": {
                    "DE.CM-01": "Networks and network services are monitored to find potentially adverse events",
                    "DE.CM-02": "The physical environment is monitored to find potentially adverse events",
                    "DE.CM-03": "Personnel activity and technology usage are monitored to find potentially adverse events",
                    "DE.CM-06": "External service provider activities and services are monitored to find potentially adverse events",
                    "DE.CM-09": "Computing hardware and software, runtime environments, and their data are monitored to find potentially adverse events",
                }
            },
            "DE.AE": {
                "name": "Adverse Event Analysis",
                "subcategories": {
                    "DE.AE-02": "Potentially adverse events are analyzed to better understand associated activities",
                    "DE.AE-03": "Information is correlated from multiple sources",
                    "DE.AE-04": "The estimated impact and scope of adverse events are understood",
                    "DE.AE-06": "Information on adverse events is provided to authorized staff and tools",
                    "DE.AE-07": "Cyber threat intelligence and other contextual information are integrated into the analysis",
                    "DE.AE-08": "Incidents are declared when adverse events meet the defined incident criteria",
                }
            },
        }
    },
    "RS": {
        "name": "RESPOND",
        "categories": {
            "RS.MA": {
                "name": "Incident Management",
                "subcategories": {
                    "RS.MA-01": "The incident response plan is executed in coordination with relevant third parties once an incident is declared",
                    "RS.MA-02": "Incident reports are triaged and validated",
                    "RS.MA-03": "Incidents are categorized and prioritized",
                    "RS.MA-04": "Incidents are escalated or elevated as needed",
                    "RS.MA-05": "The criteria for initiating incident recovery are applied",
                }
            },
            "RS.AN": {
                "name": "Incident Analysis",
                "subcategories": {
                    "RS.AN-03": "Analysis is performed to establish what has taken place during an incident and the root cause of the incident",
                    "RS.AN-06": "Actions performed during an investigation are recorded, and the records' integrity and provenance are preserved",
                    "RS.AN-07": "Incident data and metadata are collected, and their integrity and provenance are preserved",
                    "RS.AN-08": "An incident's magnitude is estimated and validated",
                }
            },
            "RS.CO": {
                "name": "Incident Response Reporting and Communication",
                "subcategories": {
                    "RS.CO-02": "Internal and external stakeholders are notified of incidents",
                    "RS.CO-03": "Information is shared with designated internal and external stakeholders",
                }
            },
        }
    },
    "RC": {
        "name": "RECOVER",
        "categories": {
            "RC.RP": {
                "name": "Incident Recovery Plan Execution",
                "subcategories": {
                    "RC.RP-01": "The recovery portion of the incident response plan is executed once initiated from the incident response process",
                    "RC.RP-02": "Recovery actions are selected, scoped, prioritized, and performed",
                    "RC.RP-03": "The integrity of backups and other restoration assets is verified before using them for restoration",
                    "RC.RP-04": "Critical mission functions and cybersecurity risk management are considered to establish post-incident norms",
                    "RC.RP-05": "The integrity of restored assets is verified, systems and services are restored, and normal operating status is confirmed",
                    "RC.RP-06": "The end of incident recovery is declared based on criteria, and incident-related documentation is completed",
                }
            },
            "RC.CO": {
                "name": "Incident Recovery Communication",
                "subcategories": {
                    "RC.CO-03": "Recovery activities and progress in restoring operational capabilities are communicated to designated internal and external stakeholders",
                    "RC.CO-04": "Public updates on incident recovery are shared using approved methods and messaging",
                }
            },
        }
    },
}

# FERPA - 34 CFR Part 99 key sections
FERPA_SECTIONS = {
    "§99.1": "Purpose — To set forth requirements for the protection of privacy of parents and students under FERPA",
    "§99.2": "Applicability — Applies to all educational agencies receiving DOE funding",
    "§99.3": "Definitions — Education records, directory information, personally identifiable information (PII), legitimate educational interest",
    "§99.4": "Student rights — Transfer of rights at age 18 or postsecondary enrollment",
    "§99.5": "Right of access — Right to inspect and review education records; 45-day compliance window",
    "§99.7": "Annual notification — Schools must annually notify parents/students of their FERPA rights",
    "§99.10": "Right to inspect — Parents/eligible students may inspect and review education records",
    "§99.12": "Right to amend — Right to request amendment of records believed to be inaccurate",
    "§99.20": "Amendment hearing — Hearing procedures when amendment is refused",
    "§99.30": "Prior consent — Written consent required before disclosing PII from education records",
    "§99.31": "Consent exceptions — Exceptions including school officials with legitimate educational interest, directory info, health/safety emergencies, judicial orders",
    "§99.32": "Record of disclosures — Institutions must maintain records of each request for and disclosure of PII",
    "§99.33": "Redisclosure limitations — Recipients may not redisclose PII without consent",
    "§99.34": "Transfer conditions — Conditions for disclosure to other schools",
    "§99.35": "Research exceptions — Disclosure for studies for, or on behalf of, educational agencies",
    "§99.36": "Health/safety emergency — Disclosure permitted in health or safety emergencies",
    "§99.37": "Directory information — Designation, opt-out rights, and de-identification requirements",
    "§99.60-67": "Enforcement — Investigation and enforcement procedures by the Family Policy Compliance Office",
}

# SOX Section 404 - IT General Controls (ITGC)
SOX_404_ITGCS = {
    "Access Controls": {
        "description": "Restrict system access to authorized individuals; enforce least privilege and separation of duties",
        "controls": [
            "AC-1: Logical access provisioning/deprovisioning aligned with HR lifecycle events",
            "AC-2: Periodic user access reviews (quarterly for privileged, semi-annual for standard)",
            "AC-3: Privileged access management — just-in-time elevation, session recording, break-glass procedures",
            "AC-4: Authentication controls — MFA for all administrative and financially-significant system access",
            "AC-5: Service account governance — inventory, ownership, credential rotation",
        ]
    },
    "Change Management": {
        "description": "Ensure changes to IT systems are authorized, tested, and approved before production deployment",
        "controls": [
            "CM-1: Change request documentation including business justification and impact assessment",
            "CM-2: Segregation of development, test, and production environments",
            "CM-3: Code review / peer review before production deployment",
            "CM-4: Change approval by designated change authority (CAB or equivalent)",
            "CM-5: Emergency change procedures with post-implementation review",
            "CM-6: Release management and deployment automation controls",
        ]
    },
    "Computer Operations": {
        "description": "Ensure reliable processing of financial data through job scheduling, backup, and monitoring",
        "controls": [
            "CO-1: Job scheduling controls — automated scheduling with failure alerting",
            "CO-2: Backup and recovery — automated backups with tested restoration procedures",
            "CO-3: Incident management — defined escalation and resolution procedures",
            "CO-4: Batch processing integrity — reconciliation and completeness checks",
        ]
    },
    "Program Development": {
        "description": "Ensure systems are developed, tested, and implemented with appropriate controls",
        "controls": [
            "PD-1: System development lifecycle (SDLC) methodology with security requirements",
            "PD-2: Security testing — SAST, DAST, SCA integrated into CI/CD pipeline",
            "PD-3: User acceptance testing (UAT) for financially-significant system changes",
            "PD-4: Data migration controls with reconciliation and validation",
        ]
    },
}

# ============================================================
# POLICY METADATA — ISP/IISP inventory with NIST CSF mapping
# ============================================================

POLICY_INVENTORY = [
    # ISPs (Information Security Policies) — aligned to NIST CSF 2.0
    {"id": "ISP 1.0", "title": "Information Security Program Policy", "csf_function": "GV", "csf_categories": ["GV.OC", "GV.RM", "GV.PO"], "ferpa": ["§99.1", "§99.2"], "sox_itgc": [], "type": "ISP"},
    {"id": "ISP 1.1", "title": "IT Security Policy Index", "csf_function": "GV", "csf_categories": ["GV.PO"], "ferpa": [], "sox_itgc": [], "type": "ISP"},
    {"id": "ISP 1.2", "title": "IT Security Policy Definitions", "csf_function": "GV", "csf_categories": ["GV.PO", "GV.OC"], "ferpa": ["§99.3"], "sox_itgc": [], "type": "ISP"},
    {"id": "ISP 2.1", "title": "Organizational Context (GV.OC)", "csf_function": "GV", "csf_categories": ["GV.OC"], "ferpa": ["§99.2"], "sox_itgc": [], "type": "ISP"},
    {"id": "ISP 2.2", "title": "Risk Management Strategy (GV.RM)", "csf_function": "GV", "csf_categories": ["GV.RM"], "ferpa": [], "sox_itgc": [], "type": "ISP"},
    {"id": "ISP 2.3", "title": "Roles, Responsibilities, and Authorities (GV.RR)", "csf_function": "GV", "csf_categories": ["GV.RR"], "ferpa": [], "sox_itgc": ["Access Controls"], "type": "ISP"},
    {"id": "ISP 2.4", "title": "Policies, Processes, and Procedures (GV.PO)", "csf_function": "GV", "csf_categories": ["GV.PO"], "ferpa": ["§99.7"], "sox_itgc": ["Change Management"], "type": "ISP"},
    {"id": "ISP 2.5", "title": "Oversight (GV.OV)", "csf_function": "GV", "csf_categories": ["GV.OV"], "ferpa": ["§99.60-67"], "sox_itgc": [], "type": "ISP"},
    {"id": "ISP 2.6", "title": "Cybersecurity Supply Chain Risk Management (GV.SC)", "csf_function": "GV", "csf_categories": ["GV.SC"], "ferpa": ["§99.33", "§99.35"], "sox_itgc": ["Access Controls"], "type": "ISP"},
    {"id": "ISP 3.1", "title": "Asset Management (ID.AM)", "csf_function": "ID", "csf_categories": ["ID.AM"], "ferpa": ["§99.3"], "sox_itgc": ["Computer Operations"], "type": "ISP"},
    {"id": "ISP 3.2", "title": "Risk Assessment (ID.RA)", "csf_function": "ID", "csf_categories": ["ID.RA"], "ferpa": ["§99.36"], "sox_itgc": [], "type": "ISP"},
    {"id": "ISP 3.3", "title": "Response Improvement (ID.IM)", "csf_function": "ID", "csf_categories": ["ID.IM"], "ferpa": [], "sox_itgc": [], "type": "ISP"},
    {"id": "ISP 4.1", "title": "Identity Management, Authentication, and Access Control (PR.AA)", "csf_function": "PR", "csf_categories": ["PR.AA"], "ferpa": ["§99.31", "§99.32"], "sox_itgc": ["Access Controls"], "type": "ISP"},
    {"id": "ISP 4.2", "title": "Awareness and Training Standards (PR.AT)", "csf_function": "PR", "csf_categories": ["PR.AT"], "ferpa": ["§99.7"], "sox_itgc": [], "type": "ISP"},
    {"id": "ISP 4.3", "title": "Data Security (PR.DS)", "csf_function": "PR", "csf_categories": ["PR.DS"], "ferpa": ["§99.30", "§99.31", "§99.33"], "sox_itgc": ["Access Controls", "Computer Operations"], "type": "ISP"},
    {"id": "ISP 4.4", "title": "Platform Security (PR.PS)", "csf_function": "PR", "csf_categories": ["PR.PS"], "ferpa": [], "sox_itgc": ["Change Management", "Program Development"], "type": "ISP"},
    {"id": "ISP 4.5", "title": "Technology Infrastructure Resilience (PR.IR)", "csf_function": "PR", "csf_categories": ["PR.IR"], "ferpa": [], "sox_itgc": ["Computer Operations"], "type": "ISP"},
    {"id": "ISP 5.1", "title": "Continuous Monitoring (DE.CM)", "csf_function": "DE", "csf_categories": ["DE.CM"], "ferpa": ["§99.32"], "sox_itgc": ["Computer Operations"], "type": "ISP"},
    {"id": "ISP 5.2", "title": "Adverse Event Analysis (DE.AE)", "csf_function": "DE", "csf_categories": ["DE.AE"], "ferpa": [], "sox_itgc": [], "type": "ISP"},
    {"id": "ISP 6.1", "title": "Incident Management (RS.MA)", "csf_function": "RS", "csf_categories": ["RS.MA", "RS.CO"], "ferpa": ["§99.36", "§99.33"], "sox_itgc": ["Computer Operations"], "type": "ISP"},
    {"id": "ISP 6.2", "title": "Incident Analysis (RS.AN)", "csf_function": "RS", "csf_categories": ["RS.AN"], "ferpa": [], "sox_itgc": [], "type": "ISP"},
    # IISPs (Integrated Information Security Policies)
    {"id": "IISP 1.0", "title": "Business Continuity Policy", "csf_function": "RC", "csf_categories": ["RC.RP", "PR.IR"], "ferpa": [], "sox_itgc": ["Computer Operations"], "type": "IISP"},
    {"id": "IISP 2.0", "title": "Data Classification", "csf_function": "PR", "csf_categories": ["PR.DS", "ID.AM"], "ferpa": ["§99.3", "§99.37"], "sox_itgc": ["Access Controls"], "type": "IISP"},
    {"id": "IISP 3.0", "title": "International Travel Policy", "csf_function": "PR", "csf_categories": ["PR.DS", "PR.AA"], "ferpa": ["§99.33"], "sox_itgc": [], "type": "IISP"},
    {"id": "IISP 4.0", "title": "Acceptable Use Policy", "csf_function": "GV", "csf_categories": ["GV.PO", "PR.AT"], "ferpa": ["§99.7"], "sox_itgc": [], "type": "IISP"},
    {"id": "IISP 5.0", "title": "Artificial Intelligence Acceptable Use Policy (AI-AUP)", "csf_function": "GV", "csf_categories": ["GV.PO", "GV.RM", "PR.DS"], "ferpa": ["§99.30", "§99.31"], "sox_itgc": ["Program Development"], "type": "IISP"},
    {"id": "IISP 6.0", "title": "\\textit{[RESERVED — Policy Not Yet Published]}", "csf_function": "—", "csf_categories": [], "ferpa": [], "sox_itgc": [], "type": "IISP", "gap": True},
    {"id": "IISP 7.0", "title": "Vulnerability Management Policy", "csf_function": "ID", "csf_categories": ["ID.RA", "DE.CM"], "ferpa": [], "sox_itgc": ["Change Management"], "type": "IISP"},
    {"id": "IISP 8.0", "title": "Non-Employee Acceptable Use", "csf_function": "GV", "csf_categories": ["GV.PO", "PR.AA"], "ferpa": ["§99.31"], "sox_itgc": ["Access Controls"], "type": "IISP"},
    {"id": "IISP 9.0", "title": "Secure Software Development Policy", "csf_function": "PR", "csf_categories": ["PR.PS"], "ferpa": [], "sox_itgc": ["Program Development", "Change Management"], "type": "IISP"},
    {"id": "IISP 10.0", "title": "Forensics Handling of Sensitive Matters", "csf_function": "RS", "csf_categories": ["RS.AN", "RS.MA"], "ferpa": ["§99.31", "§99.36"], "sox_itgc": [], "type": "IISP"},
]

# Map file stems to policy IDs for text lookup
def find_policy_text(policy_id):
    """Find extracted text for a policy by its ID."""
    search_key = f"STRIDE {policy_id}"
    for stem, data in policies_data.items():
        if search_key in stem:
            return data.get("text", "")
    return ""

def get_policy_summary(text, max_sentences=4):
    """Extract a brief summary from policy text (first substantive sentences after boilerplate)."""
    if not text:
        return "\\textit{Text not available.}"
    # Skip typical boilerplate (title pages, headers)
    lines = text.split("\n")
    substantive = []
    for line in lines:
        line = line.strip()
        if len(line) > 60 and not line.startswith("STRIDE") and not line.startswith("Page ") and "Confidential" not in line and not line.startswith("Version"):
            substantive.append(line)
        if len(substantive) >= 8:
            break
    summary_text = " ".join(substantive)
    # Take first N sentences
    sentences = re.split(r'(?<=[.!?])\s+', summary_text)
    summary = " ".join(sentences[:max_sentences])
    if len(summary) > 500:
        summary = summary[:497] + "..."
    return escape_latex(summary)

def escape_latex(text):
    """Escape special LaTeX characters."""
    if not text:
        return ""
    # Don't escape already-escaped sequences or LaTeX commands
    chars = {
        '&': r'\&',
        '%': r'\%',
        '$': r'\$',
        '#': r'\#',
        '_': r'\_',
        '{': r'\{',
        '}': r'\}',
        '~': r'\textasciitilde{}',
        '^': r'\textasciicircum{}',
        '≤': r'$\leq$',
        '–': r'--',
        '—': r'---',
        '"': "``",
        '"': "''",
        ''': "'",
        ''': "`",
    }
    # Protect existing LaTeX commands
    text = text.replace('\\textit', '\x00TEXTIT')
    text = text.replace('\\textbf', '\x00TEXTBF')
    text = text.replace('\\\\', '\x00DBLBACK')
    for char, replacement in chars.items():
        text = text.replace(char, replacement)
    text = text.replace('\x00TEXTIT', '\\textit')
    text = text.replace('\x00TEXTBF', '\\textbf')
    text = text.replace('\x00DBLBACK', '\\\\')
    return text


# ============================================================
# DELIVERABLE 1: Policy Cross Reference V6
# ============================================================

# Build a lookup: policy label key → policy id/title for hotlinking
def _pol_label(pid):
    """Return LaTeX label key for a policy ID like 'ISP 1.0' → 'pol:ISP10'."""
    return "pol:" + pid.replace(' ', '').replace('.', '')

def _pol_hyperref(pid, display=None):
    r"""Return \hyperref[label]{display} for a policy ID."""
    label = _pol_label(pid)
    if display is None:
        # Find title from inventory
        for p in POLICY_INVENTORY:
            if p["id"] == pid:
                display = p["title"]
                break
        else:
            display = pid
    return f"\\hyperref[{label}]{{{escape_latex(display)}}}"

def _linkify_policy_refs(text):
    """Replace 'Stride - ISP X.X – Title' or 'ISP X.X' references with hyperlinks."""
    import re as _re
    # Build lookup
    lookup = {}
    for p in POLICY_INVENTORY:
        lookup[p["id"]] = p
    # Pattern: optional "Stride - " prefix, then ISP/IISP X.X, optional " – Title"
    def _repl(m):
        pid = m.group("pid")
        if pid not in lookup:
            return m.group(0)
        title = lookup[pid]["title"]
        label = _pol_label(pid)
        # Use just the title as display text when the full "Stride - ISP X.X – Title" form appears
        if m.group("prefix"):
            return f"\\hyperref[{label}]{{{escape_latex(title)}}}"
        # For bare "ISP X.X" references, show "ISP X.X"
        return f"\\hyperref[{label}]{{{escape_latex(pid)}}}"
    pattern = _re.compile(
        r'(?P<prefix>Stride\s*[-–]\s*)?(?P<pid>(?:I[IS]SP)\s+\d+\.\d+)(?:\s*[-–—]\s*[^.;,\n]{3,60})?'
    )
    return pattern.sub(_repl, text)

# Enrichment data for specific policies
ISP_12_DEFINITIONS = [
    ("AAR", "After Action Review --- postmortem review of timeline, results, and required actions on failed or partially successful changes"),
    ("Access", "The ability to use, modify, or manipulate an information resource or gain entry to a physical area"),
    ("Agentic AI", "AI that takes initiative, understands goals, makes decisions, and carries out tasks with minimal supervision"),
    ("Artificial Intelligence", "A machine-based system that infers from input how to generate outputs such as predictions, content, recommendations, or decisions"),
    ("Break Glass Account", "Emergency account providing immediate access to critical systems when standard methods are unavailable"),
    ("Business Continuity", "Activity to ensure critical business functions remain available; encompasses Disaster Recovery"),
    ("Business Critical Applications", "Financially Significant Applications (FSAs) identified based on SOX materiality scoping"),
    ("Change", "Any alteration to state or configuration of production software or hardware under Enterprise \\& Learning Technologies management"),
    ("Cloud Computing", "Model for ubiquitous, on-demand network access to shared configurable computing resources"),
    ("Control", "Technical, administrative, or physical safeguard used to manage risk through preventing, detecting, or lessening threats"),
    ("Control Objective", "Target or desired condition; statement describing what is to be achieved as a result of implementing a control"),
    ("Customers", "Consumers of products without the ability to modify data identified as in the purview of privacy, financial impact, or IP"),
    ("Encryption", "Conversion of data into a form that cannot be easily understood by unauthorized people or systems"),
    ("Guideline", "Recommended practices based on industry-recognized secure practices; allows discretion unlike Standards"),
    ("Non-Human Accounts", "Accounts used for scripts, bots, APIs, or other automated processes"),
    ("Policy", "High-level statements of management intent designed to influence decisions and guide desired outcomes"),
    ("Principle of Least Privilege", "Limit access privileges for any user to those essential for assigned duties and nothing more"),
    ("Principle of Separation of Duties", "Ensure duties that can lead to fraud, abuse, or harm are separated or controlled"),
    ("Privileged User", "Someone with administrative or higher-level access beyond a typical user, performing critical system tasks"),
    ("Procedure", "Documented set of steps to perform a specific task in conformance with an applicable standard"),
    ("Risk", "Potential exposure to harm or loss, often calculated as Threat $\\times$ Vulnerability $\\times$ Consequence"),
    ("Service Accounts", "Accounts used by multiple people; pose security risks since tracking individual activity is difficult"),
    ("SOX", "Sarbanes-Oxley Act --- US federal law setting enhanced standards for public company boards, management, and accounting"),
    ("Standard", "Mandatory requirements regarding processes, actions, and configurations designed to satisfy Control Objectives"),
    ("System Accounts", "Accounts used by operating systems or applications to perform background tasks"),
]

IISP_20_CLASSIFICATIONS = [
    ("Public", "Freely disclosed; intended for public use; minimum security controls",
     "Course catalogs, press releases, published marketing materials, regulatory filings"),
    ("Internal", "Limited to Stride employees; low sensitivity; internal controls apply",
     "Intranet, training materials, org charts, internal emails, Stride-wide policies"),
    ("Confidential", "Access based on business need-to-know; medium sensitivity; confidentiality agreements",
     "Non-directory student info, personnel records, non-public financial data, vendor contract data, source code"),
    ("Restricted / Highly Protected", "High sensitivity; strict controls; disclosure risks serious harm",
     "Passwords, private keys, government IDs (SSN, passport), financial account info, HIPAA/ADA/IDEA data, biometric data, trade secrets"),
]

def build_policy_cross_reference():
    """Generate LaTeX for Stride Policy Cross Reference V6."""
    print("Building Deliverable 1: Stride Policy Cross Reference V6...")
    
    # Header
    tex = r"""
\documentclass[11pt,landscape]{article}
\usepackage[landscape,margin=1in]{geometry}
\usepackage{longtable,booktabs,array,tabularx,xcolor,hyperref,fancyhdr,graphicx,colortbl,enumitem}
\usepackage[T1]{fontenc}
\usepackage{helvet}
\renewcommand{\familydefault}{\sfdefault}

\definecolor{stridegreen}{HTML}{2E7D32}
\definecolor{strideblue}{HTML}{1565C0}
\definecolor{stridegray}{HTML}{F5F5F5}
\definecolor{gapred}{HTML}{C62828}
\definecolor{rulegray}{HTML}{BDBDBD}
\definecolor{headgray}{HTML}{E0E0E0}

% Light gray borders on all table rules
\arrayrulecolor{rulegray}
\setlength{\arrayrulewidth}{0.4pt}

\hypersetup{colorlinks=true,linkcolor=strideblue,urlcolor=strideblue}

\pagestyle{fancy}
\fancyhf{}
\fancyhead[L]{\textcolor{gray}{\small Stride (K12) --- Policy Cross Reference V6}}
\fancyhead[R]{\textcolor{gray}{\small CONFIDENTIAL}}
\fancyfoot[C]{\thepage}
\fancyfoot[R]{\small March 2, 2026}
\renewcommand{\headrulewidth}{0.4pt}

\setlength{\parindent}{0pt}
\setlength{\parskip}{4pt}

\begin{document}

% --- Title Page ---
\begin{titlepage}
\vspace*{2cm}
\begin{center}
{\Huge\bfseries\textcolor{stridegreen}{Stride Policy Cross Reference}}\\[0.5cm]
{\LARGE Version 6.0}\\[1cm]
{\large Stride — K12 Inc.}\\[0.3cm]
{\large Information Security \& Governance}\\[2cm]
{\normalsize\textcolor{gray}{Regulatory Cross-Reference Frameworks:}}\\[0.3cm]
{\normalsize NIST Cybersecurity Framework 2.0}\\
{\normalsize FERPA (34 CFR Part 99)}\\
{\normalsize SOX Section 404 — IT General Controls}\\[2cm]
{\small Document Date: March 2, 2026}\\
{\small Classification: Confidential}\\[1cm]
\textcolor{gapred}{\textbf{Note:} IISP 6.0 is reserved and not yet published. Gap annotations are included throughout.}
\end{center}
\end{titlepage}

\tableofcontents
\newpage

% --- Section 1: Policy Inventory Overview ---
\section{Policy Inventory Overview}

The Stride information security program comprises \textbf{21 Information Security Policies (ISPs)} aligned to NIST CSF 2.0 functions and \textbf{10 Integrated Information Security Policies (IISPs)} addressing cross-cutting operational domains. Together, these 31 policy documents (30 published + 1 reserved) establish the governance foundation for cybersecurity risk management.

\vspace{0.3cm}
\textbf{NIST CSF 2.0 Function Coverage:}
\begin{itemize}
    \item \textbf{GOVERN (GV):} ISP 1.0--1.2, ISP 2.1--2.6, IISP 4.0, 5.0, 8.0
    \item \textbf{IDENTIFY (ID):} ISP 3.1--3.3, IISP 7.0
    \item \textbf{PROTECT (PR):} ISP 4.1--4.5, IISP 2.0, 3.0, 9.0
    \item \textbf{DETECT (DE):} ISP 5.1--5.2
    \item \textbf{RESPOND (RS):} ISP 6.1--6.2, IISP 10.0
    \item \textbf{RECOVER (RC):} IISP 1.0
\end{itemize}

\textcolor{gapred}{\textbf{Gap:} IISP 6.0 is reserved and not yet published. No policy currently occupies this slot in the numbering scheme.}

\newpage
"""

    # --- Section 2: Per-Policy Cross-Reference Tables ---
    tex += r"""
\section{Per-Policy Cross-Reference Detail}

Each policy below includes a summary, NIST CSF 2.0 subcategory alignment, FERPA applicability, and SOX §404 ITGC relevance.

"""

    for pol in POLICY_INVENTORY:
        pid = pol["id"]
        title = pol["title"]
        is_gap = pol.get("gap", False)
        
        # Get policy summary text
        policy_text = find_policy_text(pid)
        summary = get_policy_summary(policy_text) if not is_gap else "\\textcolor{gapred}{This policy number is reserved but has not yet been published. This represents a gap in the current policy framework.}"
        
        # Build CSF subcategory list
        csf_subs = []
        for cat_id in pol["csf_categories"]:
            for func_data in NIST_CSF.values():
                if cat_id in func_data["categories"]:
                    cat_data = func_data["categories"][cat_id]
                    for sub_id, sub_desc in cat_data["subcategories"].items():
                        csf_subs.append(f"{sub_id}")
        csf_text = ", ".join(csf_subs) if csf_subs else "---"
        if len(csf_text) > 120:
            # Truncate with count
            shown = csf_subs[:6]
            csf_text = ", ".join(shown) + f" \\textit{{(+{len(csf_subs)-6} more)}}"
        
        # FERPA references
        ferpa_text = ", ".join(pol["ferpa"]) if pol["ferpa"] else "---"
        
        # SOX ITGC references
        sox_text = ", ".join(pol["sox_itgc"]) if pol["sox_itgc"] else "---"
        
        color_cmd = "gapred" if is_gap else "strideblue"
        
        tex += f"""
\\subsection{{\\textcolor{{{color_cmd}}}{{STRIDE {escape_latex(pid)}}} --- {title}}}
\\label{{{_pol_label(pid)}}}

"""
        if is_gap:
            tex += f"\\colorbox{{gapred!10}}{{\\parbox{{0.95\\textwidth}}{{{summary}}}}}\n\n"
        else:
            # Linkify any policy references in the summary text
            tex += f"\\textbf{{Summary:}} {_linkify_policy_refs(summary)}\n\n"
        
        # Enrichment: ISP 1.2 definitions
        if pid == "ISP 1.2":
            tex += "\\textbf{Key Definitions (selected):}\n\n"
            tex += "\\begin{longtable}{|p{3.5cm}|p{6in}|}\n\\hline\n"
            tex += "\\rowcolor{headgray} \\textbf{Term} & \\textbf{Definition} \\\\\n\\hline\n"
            for term, defn in ISP_12_DEFINITIONS:
                tex += f"{escape_latex(term)} & {defn} \\\\\n\\hline\n"
            tex += "\\end{longtable}\n\n"
        
        # Enrichment: IISP 2.0 data classification levels
        if pid == "IISP 2.0":
            tex += "\\textbf{Data Classification Levels:}\n\n"
            tex += "\\begin{longtable}{|p{2.5cm}|p{4in}|p{3in}|}\n\\hline\n"
            tex += "\\rowcolor{headgray} \\textbf{Level} & \\textbf{Description \\& Controls} & \\textbf{Examples} \\\\\n\\hline\n"
            for level, desc, examples in IISP_20_CLASSIFICATIONS:
                tex += f"{escape_latex(level)} & {escape_latex(desc)} & {escape_latex(examples)} \\\\\n\\hline\n"
            tex += "\\end{longtable}\n\n"
        
        tex += f"""\\begin{{tabularx}}{{\\textwidth}}{{|p{{4cm}}|X|}}
\\hline
\\rowcolor{{headgray}} \\textbf{{Framework}} & \\textbf{{Alignment}} \\\\
\\hline
NIST CSF 2.0 Function & {escape_latex(pol['csf_function'])} --- {escape_latex(NIST_CSF.get(pol['csf_function'], {}).get('name', '---'))} \\\\
\\hline
NIST CSF 2.0 Subcategories & {csf_text} \\\\
\\hline
FERPA (34 CFR Part 99) & {escape_latex(ferpa_text)} \\\\
\\hline
SOX §404 ITGC Domains & {escape_latex(sox_text)} \\\\
\\hline
\\end{{tabularx}}

"""

    # --- Appendix A: NIST CSF 2.0 Reverse Map ---
    tex += r"""
\newpage
\appendix
\section{APPENDIX A --- NIST CSF 2.0 Reverse Mapping}
\label{app:nist}

This appendix maps each NIST CSF 2.0 subcategory back to the Stride policies that address it.

"""
    for func_id, func_data in NIST_CSF.items():
        tex += f"\\subsection{{{func_id} --- {func_data['name']}}}\n\n"
        for cat_id, cat_data in func_data["categories"].items():
            tex += f"\\subsubsection{{{cat_id}: {cat_data['name']}}}\n\n"
            tex += "\\begin{tabularx}{\\textwidth}{|p{3.5cm}|X|}\n\\hline\n"
            tex += "\\rowcolor{headgray} \\textbf{Subcategory} & \\textbf{Stride Policies} \\\\\n\\hline\n"
            for sub_id in cat_data["subcategories"]:
                # Find policies that cover this subcategory's category
                matching = []
                for pol in POLICY_INVENTORY:
                    if cat_id in pol["csf_categories"]:
                        matching.append(_pol_hyperref(pol["id"], pol["id"]))
                match_text = ", ".join(matching) if matching else "\\textit{No direct mapping}"
                tex += f"{sub_id} & {match_text} \\\\\n\\hline\n"
            tex += "\\end{tabularx}\n\n"

    # --- Appendix B: FERPA Reverse Map ---
    tex += r"""
\section{APPENDIX B --- FERPA (34 CFR Part 99) Reverse Mapping}
\label{app:ferpa}

"""
    tex += "\\begin{longtable}{|p{2cm}|p{4.5in}|p{3in}|}\n\\hline\n"
    tex += "\\rowcolor{headgray} \\textbf{Section} & \\textbf{Description} & \\textbf{Stride Policies} \\\\\n\\hline\n"
    tex += "\\endhead\n"
    for section_id, section_desc in FERPA_SECTIONS.items():
        matching = []
        for pol in POLICY_INVENTORY:
            if section_id in pol["ferpa"]:
                matching.append(_pol_hyperref(pol["id"], pol["id"]))
        match_text = ", ".join(matching) if matching else "\\textit{No direct mapping}"
        tex += f"{escape_latex(section_id)} & {escape_latex(section_desc)} & {match_text} \\\\\n\\hline\n"
    tex += "\\end{longtable}\n\n"

    # --- Appendix C: SOX §404 Reverse Map ---
    tex += r"""
\section{APPENDIX C --- SOX \S 404 ITGC Reverse Mapping}
\label{app:sox}

"""
    for domain, domain_data in SOX_404_ITGCS.items():
        tex += f"\\subsection{{{escape_latex(domain)}}}\n\n"
        tex += f"{escape_latex(domain_data['description'])}\n\n"
        # Find policies with hotlinks
        matching = []
        for pol in POLICY_INVENTORY:
            if domain in pol["sox_itgc"]:
                matching.append(_pol_hyperref(pol["id"], pol["id"]))
        pol_text = ", ".join(matching) if matching else "\\textit{No direct mapping}"
        tex += f"\\textbf{{Stride Policies:}} {pol_text}\n\n"
        tex += "\\textbf{Representative Controls:}\n\\begin{itemize}[leftmargin=*]\n"
        for ctrl in domain_data["controls"]:
            tex += f"  \\item {escape_latex(ctrl)}\n"
        tex += "\\end{itemize}\n\n"

    tex += r"""
\end{document}
"""
    
    tex_path = TEX_DIR / "policy_cross_reference_v6.tex"
    tex_path.write_text(tex)
    print(f"  LaTeX written: {tex_path}")
    return tex_path


# ============================================================
# DELIVERABLE 2: SRA V7 with embedded diagrams
# ============================================================

def _build_appendix_c():
    """Generate Appendix C: NIST CSF 2.0 Mapping and Implementation Status."""
    # Build a table mapping each CSF subcategory to the SRA section that addresses it
    CSF_SRA_MAP = [
        ("GV.OC-01", "Organizational context for cybersecurity risk management", "§1 Executive Summary", "Implemented"),
        ("GV.RM-01", "Risk management objectives established and communicated", "§1 Executive Summary", "Implemented"),
        ("GV.RM-02", "Risk appetite and tolerance statements defined", "§11 Implementation Roadmap", "In Progress"),
        ("GV.RM-03", "Risk management activities integrated across enterprise", "§13 Regulatory Compliance", "Implemented"),
        ("GV.OV-01", "Cybersecurity strategy outcomes assessed", "§1, §10 NIST CSF Mapping", "Implemented"),
        ("GV.OV-02", "Cybersecurity performance evaluated against KPIs", "§12 KPIs", "Implemented"),
        ("GV.OV-03", "Regulatory requirements integrated into governance", "§13 Regulatory Compliance", "Implemented"),
        ("GV.PO-01", "Cybersecurity policy established and communicated", "§2 Architecture Overview", "Implemented"),
        ("GV.SC-01", "Supply chain risk management program established", "§11 Implementation Roadmap", "Planned"),
        ("ID.AM-01", "Asset inventories maintained", "§3 Personas and Trust Boundaries", "Implemented"),
        ("ID.RA-01", "Vulnerabilities identified, validated, and recorded", "§7 Exposure and Posture, §10", "Implemented"),
        ("PR.AA-01", "Identities and credentials managed", "§4 Identity and Access", "Implemented"),
        ("PR.AA-02", "Identity proofing and binding to credentials", "§4 Identity and Access", "Implemented"),
        ("PR.AA-03", "Users, services, and hardware authenticated", "§3, §4 Identity and Access", "Implemented"),
        ("PR.AA-05", "Least privilege and separation of duties enforced", "§5 Privileged Trust", "Implemented"),
        ("PR.DS-01", "Data-at-rest and data-in-transit protected", "§8 Application and API Trust", "Implemented"),
        ("PR.PS-01", "Configuration baselines maintained", "§2, §4 Architecture Overview", "Implemented"),
        ("PR.PS-02", "Software maintained and replaced per policy", "§5 Privileged Trust", "Implemented"),
        ("PR.PS-03", "Hardware maintained and replaced per policy", "§6 Device Trust", "Implemented"),
        ("PR.PS-04", "Log integrity and availability ensured", "§7 Exposure and Posture", "Implemented"),
        ("PR.PS-05", "Installation and execution of unauthorized software prevented", "§8 Application and API", "In Progress"),
        ("DE.CM-01", "Networks monitored for anomalies and attacks", "§6 Device Trust", "Implemented"),
        ("DE.CM-02", "Physical environment monitored for anomalies", "§7 Exposure and Posture", "Implemented"),
        ("DE.CM-03", "Personnel activity monitored for anomalies", "§5 Privileged Trust", "Implemented"),
        ("DE.CM-06", "External service provider activities monitored", "§9 Operational Trust", "In Progress"),
        ("DE.CM-09", "Computing hardware and software monitored", "§8, §12 KPIs", "Implemented"),
        ("RS.MA-01", "Incident response plan executed", "§9 Operational Trust", "Implemented"),
        ("RS.MA-04", "Incident response performance evaluated", "§12 KPIs", "Implemented"),
        ("RC.RP-01", "Recovery plan executed during/after incident", "§9 Operational Trust", "Implemented"),
    ]

    rows = ""
    for sub, desc, sra_sec, status in CSF_SRA_MAP:
        color = ""
        if status == "Planned":
            color = "\\textcolor{gapred}{Planned}"
        elif status == "In Progress":
            color = "\\textcolor{orange}{In Progress}"
        else:
            color = "\\textcolor{stridegreen}{Implemented}"
        rows += f"{sub} & {desc} & {sra_sec} & {color} \\\\\n"

    return r"""\section{APPENDIX C --- NIST CSF 2.0 Mapping and Implementation Status}
\label{app:csf_mapping}

This appendix maps NIST Cybersecurity Framework 2.0 subcategories referenced in this SRA
to the corresponding architecture sections and their current implementation status.

\vspace{0.3cm}

\begin{longtable}{lp{3in}p{2in}l}
\toprule
\textbf{CSF Subcategory} & \textbf{Outcome Description} & \textbf{SRA Section} & \textbf{Status} \\
\midrule
\endhead
""" + rows + r"""\bottomrule
\end{longtable}

{\small\textit{Status definitions: \textcolor{stridegreen}{Implemented} = controls active and evidenced;
\textcolor{orange}{In Progress} = controls partially deployed or in current roadmap phase;
\textcolor{gapred}{Planned} = controls identified but not yet initiated.}}"""


def _build_appendix_d():
    """Generate Appendix D: NIST CSF 2.0 Evidence Traceability Matrix."""
    EVIDENCE_MAP = [
        ("GV.OC-01", "SRA document, governance charter", "Security Architecture"),
        ("GV.RM-01", "Risk register, risk appetite statement", "GRC / Risk Management"),
        ("GV.OV-01", "CSF outcome mapping (§10), annual review records", "Security Architecture"),
        ("GV.OV-02", "KPI dashboard (§12), quarterly metrics reports", "Security Operations"),
        ("GV.PO-01", "ISP 1.0–12.0 policy library, IISP 2.0", "Information Security"),
        ("ID.AM-01", "ServiceNow CMDB asset inventory, Entra directory", "IT Operations"),
        ("ID.RA-01", "Tenable scan reports, risk assessment records", "Vulnerability Management"),
        ("PR.AA-01", "Entra ID configurations, Okta CIC tenant configs", "Identity Engineering"),
        ("PR.AA-02", "FIDO2 key enrollment records, MFA registration logs", "Identity Engineering"),
        ("PR.AA-03", "Conditional Access policy exports, sign-in logs", "Identity Engineering"),
        ("PR.AA-05", "Delinea session recordings, PIM activation logs", "Privileged Access Mgmt"),
        ("PR.DS-01", "TLS configurations, encryption-at-rest settings", "Application Security"),
        ("PR.PS-01", "CIS benchmark scan results, baseline configs", "Infrastructure Security"),
        ("PR.PS-03", "CrowdStrike sensor deployment reports, Defender status", "Endpoint Security"),
        ("PR.PS-05", "Sonatype policy results, application allowlists", "Application Security"),
        ("DE.CM-01", "CrowdStrike detection logs, network alert reports", "Security Operations"),
        ("DE.CM-03", "PIM audit logs, privileged session recordings", "Security Operations"),
        ("DE.CM-09", "Burp Suite scan reports, Salt Security API findings", "Application Security"),
        ("RS.MA-01", "ServiceNow incident records, runbook executions", "Incident Response"),
        ("RS.MA-04", "MTTR reports, incident post-mortem records", "Incident Response"),
        ("RC.RP-01", "Recovery test results, backup verification logs", "Business Continuity"),
    ]

    rows = ""
    for sub, evidence, owner in EVIDENCE_MAP:
        rows += f"{sub} & {evidence} & {owner} \\\\\n"

    return r"""\section{APPENDIX D --- Evidence Traceability Matrix}
\label{app:evidence}

This appendix identifies the primary evidence artifacts for each NIST CSF 2.0 subcategory,
supporting audit readiness and attestation preparation.

\vspace{0.3cm}

\begin{longtable}{lp{3.5in}p{2in}}
\toprule
\textbf{CSF Subcategory} & \textbf{Evidence Artifacts} & \textbf{Evidence Owner} \\
\midrule
\endhead
""" + rows + r"""\bottomrule
\end{longtable}

{\small\textit{Evidence sources should be aligned to the formal control library and refreshed
during each assessment cycle. Artifacts are referenced in the control mapping tables
throughout this SRA.}}"""


def _build_appendix_e():
    """Generate Appendix E: Consolidated Gap Register."""
    GAP_REGISTER = [
        ("GAP-01", "PR.AA-04, PR.AA-06", "§4", "FERPA §99.30/§99.35 consent and disclosure controls lack explicit architectural enforcement; PR.AA-04 and PR.AA-06 unmapped.", "High"),
        ("GAP-02", "PR.AA (API)", "§8", "No formal API authentication standard (OAuth 2.0/OIDC vs. static keys); mutual-TLS and token lifecycle undefined.", "High"),
        ("GAP-03", "CM-1, PD-3, PD-4", "§8", "SOX CM-1 change management policy artefact not prescribed; PD-3/PD-4 security testing sign-off and conversion validation gates missing.", "Medium"),
        ("GAP-04", "DE.CM-06", "§9", "External service provider monitoring In Progress — ServiceNow integration with third-party telemetry not yet operational.", "High"),
        ("GAP-05", "CO-1, CO-4", "§9", "SOX CO-1 (job scheduling) and CO-4 (batch processing integrity) lack specific ServiceNow automation evidence.", "Medium"),
        ("GAP-06", "DE.AE-02–08", "§9", "Entire DE.AE (Adverse Event Analysis) function absent from SRA mapping; event correlation, enrichment, and escalation unaddressed.", "High"),
        ("GAP-07", "GV.SC-01", "§11", "Supply chain risk management program Planned but not initiated.", "High"),
        ("GAP-08", "GV.RM-02", "§11", "Risk appetite and tolerance statements In Progress.", "Medium"),
        ("GAP-09", "GV.SC-02–10", "§11", "Supplier due-diligence, contractual security, supply chain integrity, and post-acquisition monitoring subcategories unmapped.", "High"),
        ("GAP-10", "§99.4, §99.7, §99.12, §99.33, §99.37", "§13", "Five FERPA sections lack specific architectural controls or evidence sources in the SRA.", "High"),
        ("GAP-11", "PR.AT-01, PR.AT-02", "§13", "Awareness and Training subcategories not addressed in operational control architecture.", "Medium"),
        ("GAP-12", "PR.PS-05", "§8", "Unauthorized software prevention In Progress — Sonatype policy enforcement not fully deployed.", "Medium"),
        ("GAP-13", "GV.RM, PR.AT, DE.AE", "ASR", "ASR questionnaire lacks questions covering risk management governance, awareness training, and adverse event analysis domains.", "High"),
    ]

    rows = ""
    for gap_id, ref, sra_sec, desc, priority in GAP_REGISTER:
        pri_fmt = priority
        if priority == "High":
            pri_fmt = f"\\textcolor{{gapred}}{{{priority}}}"
        elif priority == "Medium":
            pri_fmt = f"\\textcolor{{orange}}{{{priority}}}"
        rows += f"{gap_id} & {ref} & {sra_sec} & {desc} & {pri_fmt} \\\\\n"

    return r"""\section{APPENDIX E --- Consolidated Gap Register}
\label{app:gaps}

This appendix consolidates all identified gaps across NIST CSF 2.0 subcategory coverage,
FERPA regulatory requirements, and SOX §404 ITGC controls. Each gap references the SRA
section where the deficiency is annotated and includes a priority for remediation planning.

\vspace{0.3cm}

\begin{longtable}{lp{1.2in}lp{3.5in}l}
\toprule
\textbf{Gap ID} & \textbf{CSF / Regulatory Ref} & \textbf{SRA §} & \textbf{Description} & \textbf{Priority} \\
\midrule
\endhead
""" + rows + r"""\bottomrule
\end{longtable}

{\small\textit{Gaps are derived from the comprehensive control-target analysis performed in
March 2026 comparing NIST CSF 2.0 (100 subcategories), FERPA 34 CFR Part 99 (18 sections),
and SOX §404 ITGC (19 controls) against the SRA and ASR questionnaire coverage.
Priority reflects the assessed impact on audit readiness and regulatory compliance.}}"""


def build_sra_v7():
    """Generate LaTeX for Stride Security Reference Architecture V7."""
    print("Building Deliverable 2: Stride Security Reference Architecture V7...")
    
    # Get SRA text from the latest version
    sra_enhanced = workpapers_data.get("SRA Enhanced", {})
    sra_v6 = workpapers_data.get("SRA v6", {})
    
    # Use SRA Enhanced as primary, fall back to v6
    sra_source = sra_enhanced if sra_enhanced.get("chars", 0) > sra_v6.get("chars", 0) else sra_v6
    sra_paras = sra_source.get("structured", [])
    sra_tables = sra_source.get("table_data", [])
    
    # Also get the consolidated anchored version
    sra_anchored = workpapers_data.get("Stride_SRA_Consolidated_Anchored_D2", {})
    sra_anchored_paras = sra_anchored.get("structured", [])
    
    # Diagram mapping — SRA section to PNG file
    DIAGRAM_MAP = {
        "1": "16-executive-summary-and-platform-stack.png",
        "2a": "01-trust-security-architecture-overview.png",
        "2b": "02-trust-logical-architecture-components.png",
        "3": "03-persona-trust-boundaries.png",
        "4a": "04-staff-authentication-flow.png",
        "4b": "05-staff-conditional-access-policy-matrix.png",
        "4c": "06-student-authentication-flow.png",
        "4d": "07-customer-authentication-flow.png",
        "4e": "08-identity-and-access-architecture.png",
        "5": "09-privileged-trust-architecture.png",
        "6": "10-device-trust-architecture.png",
        "7": "11-exposure-and-posture-architecture.png",
        "8": "12-application-and-api-trust-architecture.png",
        "9": "13-operational-trust-architecture.png",
        "10": "14-nist-csf-outcome-mapping.png",
        "11": "15-implementation-roadmap.png",
        "12": "17-kpi-framework.png",
        "13": "18-regulatory-compliance-alignment.png",
    }

    # SRA section structure with NIST CSF mapping
    SRA_SECTIONS = [
        {"num": "1", "title": "Executive Summary", "csf": ["GV.OC-01", "GV.RM-01", "GV.OV-01"], "diagrams": ["1"]},
        {"num": "2", "title": "Trust Security Architecture Overview", "csf": ["GV.PO-01", "PR.AA-01", "PR.PS-01"], "diagrams": ["2a", "2b"]},
        {"num": "3", "title": "Personas and Trust Boundaries", "csf": ["PR.AA-01", "PR.AA-03", "ID.AM-01"], "diagrams": ["3"]},
        {"num": "4", "title": "Identity and Access Architecture", "csf": ["PR.AA-01", "PR.AA-02", "PR.PS-01"], "diagrams": ["4a", "4b", "4c", "4d", "4e"],
         "ferpa": "FERPA §99.31 (consent exceptions for legitimate educational interest) and §99.32 (disclosure records) require identity controls that enforce role-based access aligned with educational purpose.",
         "sox": "SOX §404 AC-1 through AC-5: logical access provisioning, periodic reviews, PAM, MFA, and service account controls directly implement IAM architecture requirements.",
         "gap": "FERPA Consent and Disclosure Controls: §99.30 (consent for disclosures) and §99.35 (access by state/local officials) lack explicit architectural controls for consent management and disclosure tracking beyond role-based access. NIST CSF PR.AA-04 (identity assertions managed) and PR.AA-06 (access rights managed) are not addressed in the current SRA subcategory mapping. A formal consent-management workflow and disclosure-audit mechanism should be established within the SailPoint/Entra governance layer."},
        {"num": "5", "title": "Privileged Trust (Delinea and Entra PIM)", "csf": ["PR.AA-05", "PR.PS-02", "DE.CM-03"], "diagrams": ["5"],
         "sox": "SOX §404 AC-3: privileged access management with JIT elevation and session recording."},
        {"num": "6", "title": "Device Trust (CrowdStrike and Defender)", "csf": ["PR.PS-03", "DE.CM-01"], "diagrams": ["6"]},
        {"num": "7", "title": "Exposure and Posture (Tenable VM and CSPM)", "csf": ["ID.RA-01", "DE.CM-02", "PR.PS-04"], "diagrams": ["7"]},
        {"num": "8", "title": "Application and API Trust (Sonatype, Burp Suite, Salt)", "csf": ["PR.DS-01", "PR.PS-05", "DE.CM-09"], "diagrams": ["8"],
         "sox": "SOX §404 PD-1 through PD-2 and CM-2 through CM-6: SDLC methodology, security testing in CI/CD, environment segregation, and change approval.",
         "gap": "API Authentication Controls: The current architecture addresses application-layer testing (SAST/DAST/SCA) and future API behavioral analytics (Salt) but does not prescribe specific API authentication standards (e.g., OAuth 2.0/OIDC scoped tokens vs. static API keys). A formal API authentication standard should be developed under ISP 4.1 (PR.AA) to define acceptable mechanisms, token lifecycle management, and mutual-TLS requirements for service-to-service communication. The ASR Questionnaire (V4) now includes an API authentication assessment question to capture the current state per application. Additionally, SOX CM-1 (change management policy documentation) is referenced but the architecture does not prescribe a formal change management policy artefact. PD-3 (security testing sign-off) and PD-4 (system conversion testing) lack documented verification gates for security test acceptance and data-migration validation."},
        {"num": "9", "title": "Operational Trust (ServiceNow SecOps, CMDB, Tagging)", "csf": ["DE.CM-06", "RS.MA-01", "RC.RP-01"], "diagrams": ["9"],
         "sox": "SOX §404 CO-1 through CO-4: job scheduling, backup/recovery, incident management, and batch processing integrity.",
         "gap": "Operational Monitoring and Event Analysis: DE.CM-06 (external service provider activities monitored) is In Progress—ServiceNow integration with third-party telemetry feeds is not yet operational. SOX CO-1 (job scheduling) and CO-4 (batch processing integrity) lack specific ServiceNow automation evidence. The NIST CSF DE.AE (Adverse Event Analysis) function—covering DE.AE-02 through DE.AE-08—is entirely absent from the SRA subcategory mapping; correlation, enrichment, and escalation of security events require formal architectural treatment."},
        {"num": "10", "title": "NIST CSF 2.0 Outcome Mapping", "csf": ["GV.OV-01", "ID.RA-01", "PR.AA-01", "DE.CM-01", "RS.MA-01", "RC.RP-01"], "diagrams": ["10"]},
        {"num": "11", "title": "Implementation Roadmap", "csf": ["GV.SC-01", "GV.RM-02"], "diagrams": ["11"],
         "gap": "Supply Chain and Risk Appetite: GV.SC-01 (supply chain risk management program) is Planned and not yet initiated. GV.RM-02 (risk appetite and tolerance statements) is In Progress. Additional CSF subcategories GV.SC-02 through GV.SC-10—covering supplier due-diligence, contractual security requirements, supply chain integrity verification, and post-acquisition monitoring—are not mapped in the SRA. A formal third-party risk management program aligned to ISP 3.2 and NIST SP 800-161r1 should be established."},
        {"num": "12", "title": "Key Performance Indicators (KPIs)", "csf": ["GV.OV-02", "DE.CM-09", "RS.MA-04"], "diagrams": ["12"]},
        {"num": "13", "title": "Regulatory Compliance Alignment (SOX, FERPA)", "csf": ["GV.RM-03", "GV.OV-03"], "diagrams": ["13"],
         "ferpa": "This section provides the comprehensive FERPA alignment matrix covering all applicable sections of 34 CFR Part 99.",
         "sox": "This section provides the comprehensive SOX §404 ITGC alignment matrix.",
         "gap": "FERPA Coverage Gaps and Awareness Training: FERPA 34 CFR §§99.4 (student rights notification), 99.7 (annual FERPA notice requirements), 99.12 (limitations on re-disclosure), 99.33 (conditions on re-disclosure to third parties), and 99.37 (directory information opt-out procedures) lack specific architectural controls or evidence sources in the SRA. NIST CSF PR.AT (Awareness and Training) subcategories PR.AT-01 and PR.AT-02 are not addressed in the operational control architecture; a formal security awareness and role-based training program should be mapped."},
    ]

    # Patterns to strip from extracted DOCX content
    _STRIP_RE = re.compile(
        r'^\[DIAGRAM PLACEHOLDER\]'              # drafting placeholders
        r'|^Control\s*/\s*Policy\s*/\s*Compliance'  # leaked sub-heading
        r'|^Tightened Augmentation'               # continuation of the above
        r'|^Appendix\s+[A-Z]'                     # appendix titles that leaked into section 13
        r'|^See\s+SRA\s+Enhanced'                  # appendix cross-ref note
        r'|^Evidence\s+sources\s+are\s+referenced',  # appendix evidence note
        re.IGNORECASE,
    )

    # Extract section content from SRA paragraphs
    def extract_section_content(section_num, paras):
        """Extract paragraph text for a given section number.

        Strips drafting artifacts and converts runs of short action-
        statement paragraphs into LaTeX itemize lists.
        """
        in_section = False
        raw_lines = []
        section_pattern = re.compile(rf'^{re.escape(section_num)}[\.\s]')
        next_section = str(int(section_num) + 1) if section_num.isdigit() else None

        for p in paras:
            style = p.get("style", "")
            text = p.get("text", "").strip()
            if not text:
                continue

            if "Heading" in style and section_pattern.match(text):
                in_section = True
                continue
            elif "Heading" in style and next_section and text.startswith(f"{next_section}."):
                break
            elif "Heading" in style and in_section and any(text.startswith(f"{i}.") for i in range(1, 15)):
                break

            if in_section and text and not _STRIP_RE.search(text):
                raw_lines.append(text)

        # Cap to prevent oversized sections
        raw_lines = raw_lines[:20]
        if not raw_lines:
            return ""

        # Heuristic: a line ≤ 200 chars that starts with an action verb /
        # capital letter and has no trailing period is likely a bullet.
        # A "paragraph" is > 200 chars or ends with a period and > 80 chars.
        BULLET_THRESH = 200
        out_parts = []
        bullet_buf = []

        def flush_bullets():
            if not bullet_buf:
                return
            out_parts.append("\\begin{itemize}")
            for b in bullet_buf:
                out_parts.append(f"  \\item {escape_latex(b)}")
            out_parts.append("\\end{itemize}")
            bullet_buf.clear()

        for line in raw_lines:
            is_short = len(line) <= BULLET_THRESH
            if is_short:
                bullet_buf.append(line)
            else:
                flush_bullets()
                out_parts.append(escape_latex(line))

        flush_bullets()
        return "\n\n".join(out_parts)

    tex = r"""
\documentclass[11pt,landscape]{article}
\usepackage[landscape,margin=1in]{geometry}
\usepackage{longtable,booktabs,array,tabularx,xcolor,hyperref,fancyhdr,graphicx,float}
\usepackage[T1]{fontenc}
\usepackage{helvet}
\renewcommand{\familydefault}{\sfdefault}

\definecolor{stridegreen}{HTML}{2E7D32}
\definecolor{strideblue}{HTML}{1565C0}
\definecolor{stridegray}{HTML}{757575}
\definecolor{csfbox}{HTML}{E3F2FD}
\definecolor{ferpabox}{HTML}{FFF3E0}
\definecolor{soxbox}{HTML}{F3E5F5}
\definecolor{gapred}{HTML}{C62828}

\hypersetup{colorlinks=true,linkcolor=strideblue,urlcolor=strideblue}

\pagestyle{fancy}
\fancyhf{}
\fancyhead[L]{\small\textcolor{stridegray}{Stride Security Reference Architecture V7}}
\fancyhead[R]{\small\textcolor{stridegray}{CONFIDENTIAL}}
\fancyfoot[C]{\thepage}
\fancyfoot[R]{\small March 2, 2026}
\renewcommand{\headrulewidth}{0.4pt}

\setlength{\parindent}{0pt}
\setlength{\parskip}{6pt}

\newcommand{\csfbox}[1]{\colorbox{csfbox}{\parbox{0.95\textwidth}{\small\textbf{NIST CSF 2.0 Alignment:} #1}}}
\newcommand{\ferpabox}[1]{\colorbox{ferpabox}{\parbox{0.95\textwidth}{\small\textbf{FERPA Relevance:} #1}}}
\newcommand{\soxbox}[1]{\colorbox{soxbox}{\parbox{0.95\textwidth}{\small\textbf{SOX §404 Relevance:} #1}}}

\begin{document}

% --- Title Page ---
\begin{titlepage}
\vspace*{1.5cm}
\begin{center}
{\Huge\bfseries\textcolor{stridegreen}{Stride Security Reference Architecture}}\\[0.5cm]
{\LARGE Version 7.0}\\[0.8cm]
{\large Enterprise Trust Security Reference Architecture}\\[0.3cm]
{\large Stride — K12 Inc.}\\[2cm]
{\normalsize Incorporating:}\\[0.2cm]
{\normalsize 22 D2 Architecture Diagrams (Landscape-Optimized)}\\
{\normalsize Per-Section NIST CSF 2.0 Cross-References}\\
{\normalsize FERPA and SOX §404 Regulatory Alignment}\\[2cm]
{\small Document Date: March 2, 2026}\\
{\small Classification: Confidential}\\[0.5cm]
{\small\textcolor{stridegray}{Supersedes: SRA V6 (February 27, 2026)}}\\
\end{center}
\end{titlepage}

\tableofcontents
\newpage

"""

    # Legend page
    tex += r"""
\section*{Diagram Legend and Conventions}
\addcontentsline{toc}{section}{Diagram Legend and Conventions}

\begin{center}
\includegraphics[width=0.85\textwidth]{""" + str(PNG_DIR / "00-legend-conventions.png") + r"""}
\end{center}

\newpage
"""

    # Generate each section
    for sec in SRA_SECTIONS:
        section_content = extract_section_content(sec["num"], sra_paras) or extract_section_content(sec["num"], sra_anchored_paras)
        
        tex += f"\\section{{{sec['title']}}}\n"
        tex += f"\\label{{sra:s{sec['num']}}}\n\n"
        
        # CSF alignment box
        csf_list = ", ".join(sec["csf"])
        tex += f"\\csfbox{{{csf_list}}}\n\n"
        tex += "\\vspace{0.3cm}\n\n"
        
        # FERPA box if applicable
        if "ferpa" in sec:
            tex += f"\\ferpabox{{{escape_latex(sec['ferpa'])}}}\n\n"
            tex += "\\vspace{0.2cm}\n\n"
        
        # SOX box if applicable
        if "sox" in sec:
            tex += f"\\soxbox{{{escape_latex(sec['sox'])}}}\n\n"
            tex += "\\vspace{0.2cm}\n\n"

        # Gap callout if applicable
        if "gap" in sec:
            tex += "\\vspace{0.2cm}\n\n"
            tex += f"\\colorbox{{gapred!10}}{{\\parbox{{0.95\\textwidth}}{{\\small\\textbf{{Gap ---}} {escape_latex(sec['gap'])}}}}}\n\n"
            tex += "\\vspace{0.2cm}\n\n"
        
        # Section prose (already LaTeX-escaped inside extract_section_content)
        if section_content:
            tex += section_content + "\n\n"
        else:
            # Fallback: generate section narrative from SRA context
            tex += f"\\textit{{Section content derived from SRA V6 and governance memos. See source documents for full narrative.}}\n\n"
        
        # Embed diagrams
        for diag_key in sec.get("diagrams", []):
            png_file = DIAGRAM_MAP.get(diag_key, "")
            png_path = PNG_DIR / png_file
            if png_path.exists():
                tex += f"""
\\begin{{figure}}[H]
\\centering
\\includegraphics[width=0.92\\textwidth,height=0.72\\textheight,keepaspectratio]{{{str(png_path)}}}
\\caption{{{escape_latex(png_file.replace('.png','').replace('-',' ').title())}}}
\\end{{figure}}

"""
            else:
                tex += f"\\textit{{[Diagram not found: {escape_latex(png_file)}]}}\n\n"
        
        tex += "\\newpage\n\n"

    # Appendix A: Acronyms and Definitions
    tex += r"""
\appendix
\section{APPENDIX A --- Acronyms and Definitions}
\label{app:acronyms}

\begin{center}
\includegraphics[width=0.92\textwidth,height=0.72\textheight,keepaspectratio]{""" + str(PNG_DIR / "19-acronyms-and-definitions-map.png") + r"""}
\end{center}

\vspace{0.5cm}

\begin{longtable}{lp{7in}}
\toprule
\textbf{Term} & \textbf{Definition} \\
\midrule
\endhead
CA & Conditional Access --- policy-based access control in Microsoft Entra that evaluates signals (user, device, location, risk) to enforce authentication requirements. \\
CIAM & Customer Identity and Access Management --- IAM specifically for external/customer-facing authentication (e.g., Okta CIC for students and families). \\
CMDB & Configuration Management Database --- central repository of IT asset records and relationships (ServiceNow CMDB). \\
CSF & Cybersecurity Framework --- NIST framework (v2.0) organizing cybersecurity outcomes across Govern, Identify, Protect, Detect, Respond, and Recover functions. \\
CSPM & Cloud Security Posture Management --- continuous monitoring of cloud configurations against security baselines (Tenable Cloud Security). \\
EDR & Endpoint Detection and Response --- real-time endpoint monitoring and threat response (CrowdStrike Falcon). \\
FERPA & Family Educational Rights and Privacy Act --- 34 CFR Part 99, protecting student education records. \\
FIDO2 & Fast Identity Online 2 --- passwordless authentication standard using hardware security keys or platform authenticators. \\
IAM & Identity and Access Management --- policies and technologies ensuring the right individuals access the right resources at the right time. \\
IGA & Identity Governance and Administration --- lifecycle management, access certification, and compliance reporting for identities. \\
ITGC & IT General Controls --- SOX \S 404 controls over access, change management, computer operations, and program development. \\
JEA & Just-Enough Administration --- restricting privileged sessions to the minimum set of commands required for the task. \\
JIT & Just-in-Time Access --- time-bound privilege elevation that expires automatically (Entra PIM, Delinea). \\
MDM & Mobile Device Management --- device enrollment, policy enforcement, and remote wipe capabilities. \\
MFA & Multi-Factor Authentication --- requiring two or more verification factors for access. \\
MTTR & Mean Time to Remediate/Respond --- average time between detection of a vulnerability or incident and its resolution. \\
NIST & National Institute of Standards and Technology --- U.S. federal agency publishing cybersecurity standards and guidelines. \\
PAM & Privileged Access Management --- controls for discovering, managing, and auditing privileged accounts and sessions (Delinea). \\
PIM & Privileged Identity Management --- role-based JIT elevation with approval workflows (Microsoft Entra PIM). \\
RBAC & Role-Based Access Control --- access permissions assigned by organizational role rat her than individual identity. \\
SecOps & Security Operations --- the team and processes for monitoring, detecting, and responding to security events. \\
SLA & Service Level Agreement --- formal commitment on service availability, response time, or remediation timelines. \\
SOX & Sarbanes-Oxley Act --- U.S. legislation requiring internal controls over financial reporting (\S 404). \\
SRA & Security Reference Architecture --- this document; the enterprise trust and security architecture blueprint. \\
TOGAF & The Open Group Architecture Framework --- enterprise architecture methodology used for platform and security architecture alignment. \\
VM & Vulnerability Management --- continuous process of identifying, classifying, prioritizing, and remediating vulnerabilities (Tenable). \\
WHfB & Windows Hello for Business --- passwordless, certificate-based authentication using biometrics or PIN bound to a device. \\
ZT & Zero Trust --- security model requiring continuous verification of every user, device, and transaction regardless of network location (NIST SP 800-207). \\
\bottomrule
\end{longtable}

\newpage

\section{APPENDIX B --- Document Control}
\label{app:doccontrol}

\begin{center}
\includegraphics[width=0.92\textwidth,height=0.72\textheight,keepaspectratio]{""" + str(PNG_DIR / "20-document-control-metadata.png") + r"""}
\end{center}

\vspace{0.5cm}

\begin{tabularx}{\textwidth}{lX}
\toprule
\textbf{Attribute} & \textbf{Value} \\
\midrule
Document Title & Stride Security Reference Architecture \\
Version & 7.0 \\
Date & March 3, 2026 \\
Classification & Confidential \\
Author & Security Architecture / GRC \\
Supersedes & SRA V6 (February 27, 2026) \\
\bottomrule
\end{tabularx}

\vspace{0.5cm}

\begin{tabularx}{\textwidth}{llX}
\toprule
\textbf{Version} & \textbf{Date} & \textbf{Change Description} \\
\midrule
V6.0 & February 27, 2026 & Initial trust security architecture; 22 D2 diagrams; NIST CSF 2.0 alignment. \\
V7.0 & March 3, 2026 & Enhanced appendices (A--E); per-section FERPA/SOX alignment; gap annotations; consolidated gap register; diagram routing improvements; acronym and definitions table; NIST CSF and evidence traceability appendices. \\
\bottomrule
\end{tabularx}

\newpage

""" + _build_appendix_c() + r"""

\newpage

""" + _build_appendix_d() + r"""

\newpage

""" + _build_appendix_e() + r"""

\end{document}
"""

    tex_path = TEX_DIR / "sra_v7.tex"
    tex_path.write_text(tex)
    print(f"  LaTeX written: {tex_path}")
    return tex_path


# ============================================================
# RSK / STORM Diminishing Impact Function
# ============================================================
# Reference: Paper-RSK-NDA-V9.1 (Composite Measurement, Appendix B)
# f(V, a) = ceil( sum( V_j / a^j ) )  for j = 0 .. |V|-1
# where V is sorted descending.  a = 4 (damping base).
# Theoretical max (all V_j = 100, infinite items):
#   100 * a/(a-1) = 100 * 4/3 ≈ 133.33  →  ceil = 134

RSK_DAMPING = 4          # a
RSK_VMAX = 100           # maximum single measurement
RSK_RAW_MAX = 134        # ceil(RSK_VMAX * RSK_DAMPING / (RSK_DAMPING - 1))
WEIGHT_MAP = {"Critical": 4, "High": 3, "Medium": 2, "Info": 1}
WEIGHT_MAX = 4            # max weight tier value (Critical)


def rsk_aggregate(measurements, a=RSK_DAMPING):
    """RSK/STORM diminishing impact composite measurement.

    measurements: iterable of numeric values (each 0-100).
    Returns: int — the ceiling of the weighted geometric sum (0-134 range).
    """
    valid = sorted(
        (v for v in measurements if isinstance(v, (int, float)) and v > 0),
        reverse=True,
    )
    if not valid:
        return 0
    return math.ceil(sum(v / (a ** j) for j, v in enumerate(valid)))


def rsk_normalize(raw, maximum=RSK_RAW_MAX):
    """Normalize raw RSK aggregate (0-134) to 0-100 scale."""
    if maximum <= 0:
        return 0.0
    return min(100.0, raw / maximum * 100)


def question_measurement(raw_score, weight_tier):
    """Compute weight-adjusted measurement for one question.

    raw_score : int — ordinal-choice score on 1-100 scale.
    weight_tier : str — 'Critical' | 'High' | 'Medium' | 'Info'.
    Returns : float — measurement in (0, 100] range.
    """
    w = WEIGHT_MAP.get(weight_tier, 1)
    return raw_score * (w / WEIGHT_MAX)


def choice_scores(n_choices):
    """Return list of raw scores for N ordinal choices (1=best, N=worst).

    Maps evenly across 1-100: ceil(100*i/N) for i in 1..N.
    Examples: 4 → [25,50,75,100]; 5 → [20,40,60,80,100]; 6 → [17,34,50,67,84,100]
    """
    return [math.ceil(100 * i / n_choices) for i in range(1, n_choices + 1)]


# ============================================================
# DELIVERABLE 3: ASR Questionnaire V3
# ============================================================

def build_asr_questionnaire():
    """Generate LaTeX for Stride ASR Questionnaire V3."""
    print("Building Deliverable 3: Stride ASR Questionnaire V3...")
    
    # Load ASR Checklist V2 structure
    asr_data = workpapers_data.get("ASR Checklist V2", {})
    asr_paras = asr_data.get("structured", [])
    asr_tables = asr_data.get("table_data", [])
    
    # Define ASR question domains organized by ISP/IISP policy number
    ASR_DOMAINS = [
        {
            "domain": "Governance and Program Management",
            "policy_refs": ["ISP 1.0", "ISP 2.1", "ISP 2.4", "ISP 2.5"],
            "csf_refs": ["GV.OC", "GV.PO", "GV.OV"],
            "questions": [
                {"q": "Does the application have a designated security owner or steward?", "choices": ["Yes — named owner in CMDB", "Yes — informal ownership", "No — ownership not established", "N/A"], "weight": "High"},
                {"q": "Has a risk classification been assigned to this application?", "choices": ["Yes — High/Critical", "Yes — Medium", "Yes — Low", "No classification assigned"], "weight": "High"},
                {"q": "Is the application included in the organization's security policy scope?", "choices": ["Yes — explicitly referenced", "Yes — covered by umbrella policy", "No — not in scope", "Unknown"], "weight": "Medium"},
                {"q": "When was the last security review or assessment performed?", "choices": ["Within 6 months", "6–12 months ago", "More than 12 months ago", "Never assessed"], "weight": "High"},
                {"q": "Does the application have documented data flow diagrams?", "choices": ["Yes — current and reviewed", "Yes — but outdated", "No — not documented", "N/A"], "weight": "Medium"},
                {"q": "Has a RACI matrix been established for this application's security controls?", "choices": ["Yes — documented and current", "Yes — but outdated or incomplete", "No — roles informally understood", "No — accountability not defined"], "weight": "High"},
                {"q": "Are escalation paths and notification responsibilities documented for security incidents involving this application?", "choices": ["Yes — RACI-aligned runbook with named contacts", "Yes — general escalation via IRP", "Partial — ad-hoc escalation only", "No — not documented"], "weight": "High"},
                {"q": "What is the business necessity classification for this application?", "choices": ["KTLO — operationally required (MUST)", "Business need — supports key objectives (SHOULD)", "Nice to have — productivity enhancement (MAY)", "Not classified"], "weight": "Medium"},
                {"q": "Which teams and departments are authorized to use this application?", "choices": ["Enterprise-wide — all departments", "Multiple departments — formally scoped", "Single team or department", "Not formally scoped"], "weight": "Medium"},
                {"q": "Are productivity improvement estimates or benchmarks documented for this application?", "choices": ["Yes — quantified with baseline metrics and KPIs", "Yes — qualitative estimates documented", "Informal understanding only", "No estimates or benchmarks"], "weight": "Medium"},
                {"q": "Has legal counsel reviewed this application's terms of service, data handling, and intellectual property implications?", "choices": ["Yes — reviewed and approved", "Yes — reviewed with conditions or caveats", "Review requested but not completed", "Not reviewed"], "weight": "High"},
                {"q": "Has the application been reviewed and approved through the enterprise architecture governance process?", "choices": ["Yes — approved with defined boundaries and controls", "Yes — approved for limited or pilot use", "Under review", "No — not submitted for architecture review"], "weight": "High"},
            ]
        },
        {
            "domain": "Identity and Access Management",
            "policy_refs": ["ISP 4.1", "ISP 2.3", "IISP 8.0"],
            "csf_refs": ["PR.AA"],
            "questions": [
                {"q": "What authentication mechanism does the application use?", "choices": ["SSO with MFA (Entra ID)", "SSO without MFA", "Local authentication with MFA", "Local authentication without MFA"], "weight": "Critical"},
                {"q": "Are user roles and permissions based on the principle of least privilege?", "choices": ["Yes — RBAC/ABAC enforced", "Partially — some roles over-privileged", "No — broad access grants", "Unknown"], "weight": "High"},
                {"q": "How are service accounts and API keys managed?", "choices": ["Vault/managed identities with rotation", "Stored securely with manual rotation", "Hard-coded or shared credentials", "No service accounts used"], "weight": "Critical"},
                {"q": "Is there automated provisioning/deprovisioning tied to HR events?", "choices": ["Yes — fully automated via SCIM/JIT", "Partially automated", "Manual process only", "No process in place"], "weight": "High"},
                {"q": "Are access reviews performed periodically?", "choices": ["Quarterly or more frequently", "Semi-annually", "Annually", "No periodic reviews"], "weight": "High"},
            ]
        },
        {
            "domain": "Data Protection and Privacy",
            "policy_refs": ["ISP 4.3", "IISP 2.0", "IISP 3.0"],
            "csf_refs": ["PR.DS"],
            "ferpa_note": "Applications processing student education records must comply with FERPA §99.30 (consent), §99.31 (exceptions), and §99.37 (directory information). Responses in this section directly support FERPA compliance evidence.",
            "questions": [
                {"q": "Does the application process, store, or transmit student education records (FERPA-protected data)?", "choices": ["Yes — primary function", "Yes — incidental processing", "No — no education records", "Unknown / Not assessed"], "weight": "Critical"},
                {"q": "Is data encrypted at rest?", "choices": ["Yes — AES-256 or equivalent", "Yes — platform-managed encryption", "Partial encryption", "No encryption at rest"], "weight": "High"},
                {"q": "Is data encrypted in transit?", "choices": ["Yes — TLS 1.2+ enforced", "Yes — TLS with older versions allowed", "Partial — some endpoints unencrypted", "No encryption in transit"], "weight": "Critical"},
                {"q": "What is the data classification level of information processed?", "choices": ["Public", "Internal / Confidential", "Restricted / Highly Sensitive", "Not classified"], "weight": "High"},
                {"q": "Are data retention and disposal procedures implemented?", "choices": ["Yes — automated lifecycle management", "Yes — manual procedures documented", "Partial — some data managed", "No retention/disposal procedures"], "weight": "Medium"},
                {"q": "Does the application maintain disclosure records as required by FERPA §99.32?", "choices": ["Yes — automated logging", "Yes — manual records", "Not applicable (no education records)", "No — not implemented"], "weight": "High"},
            ]
        },
        {
            "domain": "Secure Development and Change Management",
            "policy_refs": ["ISP 4.4", "IISP 9.0"],
            "csf_refs": ["PR.PS"],
            "sox_note": "SOX §404 ITGC domains CM-1 through CM-6 and PD-1 through PD-4 require documented change management and security testing controls for financially-significant applications.",
            "questions": [
                {"q": "Is the application developed using a documented SDLC methodology?", "choices": ["Yes — with security gates", "Yes — without explicit security gates", "Informal development process", "Third-party managed / SaaS"], "weight": "High"},
                {"q": "Are SAST and/or SCA scans integrated into the CI/CD pipeline?", "choices": ["Yes — blocking on critical findings", "Yes — advisory only", "Manual scans only", "No security scanning"], "weight": "Critical"},
                {"q": "Is DAST or penetration testing performed?", "choices": ["Yes — automated DAST in CI/CD + annual pentest", "Annual penetration test only", "Ad-hoc testing", "No DAST or penetration testing"], "weight": "High"},
                {"q": "Are development, test, and production environments segregated?", "choices": ["Yes — fully segregated with access controls", "Partially segregated", "Shared environments", "N/A — SaaS application"], "weight": "High"},
                {"q": "Is there a formal change approval process for production deployments?", "choices": ["Yes — CAB/change authority approval required", "Yes — peer review only", "No formal approval process", "N/A — vendor managed"], "weight": "High"},
                {"q": "Is the application managed through the enterprise endpoint or patch management system (e.g., Intune, SCCM), or does it require an out-of-band update mechanism?", "choices": ["Fully managed via enterprise MDM/SCCM", "Partially managed — some updates out-of-band", "Entirely out-of-band (CLI, manual, or vendor-pushed)", "N/A — SaaS / vendor-managed"], "weight": "High"},
                {"q": "Are human review and approval required before application outputs are used in production or decision-making?", "choices": ["Yes — mandatory human review with sign-off", "Yes — sampling-based or risk-tiered review", "No — outputs used directly without review", "N/A — application does not generate decision outputs"], "weight": "High"},
            ]
        },
        {
            "domain": "Vulnerability and Threat Management",
            "policy_refs": ["IISP 7.0", "ISP 3.2", "ISP 5.1"],
            "csf_refs": ["ID.RA", "DE.CM"],
            "questions": [
                {"q": "Is the application included in vulnerability scanning scope?", "choices": ["Yes — authenticated scans weekly+", "Yes — unauthenticated scans", "Ad-hoc scanning only", "Not in scanning scope"], "weight": "Critical"},
                {"q": "What is the SLA for remediating critical vulnerabilities?", "choices": ["7 days or fewer", "8--30 days", "31--90 days", "> 90 days or no SLA"], "weight": "High"},
                {"q": "Is the application monitored for security events?", "choices": ["Yes — SIEM integration with alerting", "Yes — log collection without alerting", "Partial monitoring", "No security monitoring"], "weight": "High"},
                {"q": "Does the application have a web application firewall (WAF)?", "choices": ["Yes — managed WAF with tuned rules", "Yes — default WAF rules", "No WAF — network firewall only", "No protection layer"], "weight": "Medium"},
                {"q": "Are detective controls implemented to identify unauthorized or anomalous use of this application?", "choices": ["Yes — automated detection with real-time alerting", "Yes — log-based detection requiring manual review", "Partial — some detection capabilities", "No detective controls implemented"], "weight": "High"},
                {"q": "Are corrective controls defined to remediate or contain issues detected during application use?", "choices": ["Yes — automated remediation and rollback capabilities", "Yes — documented manual corrective procedures", "Partial — ad-hoc correction only", "No corrective controls defined"], "weight": "High"},
                {"q": "Is application usage monitored with defined KPIs escalated to both team-level and enterprise-level analysis?", "choices": ["Yes — dashboards with KPIs at both levels", "Yes — team-level metrics only", "Partial — ad-hoc reporting", "No usage monitoring"], "weight": "Medium"},
            ]
        },
        {
            "domain": "Incident Response and Business Continuity",
            "policy_refs": ["ISP 6.1", "ISP 6.2", "IISP 1.0", "IISP 10.0"],
            "csf_refs": ["RS.MA", "RS.AN", "RC.RP"],
            "questions": [
                {"q": "Is the application covered by the incident response plan?", "choices": ["Yes — application-specific runbook", "Yes — covered by general IRP", "Partial coverage", "Not covered"], "weight": "High"},
                {"q": "What is the Recovery Time Objective (RTO)?", "choices": ["1 hour or less", "1--4 hours", "4--24 hours", "> 24 hours or undefined"], "weight": "High"},
                {"q": "What is the Recovery Point Objective (RPO)?", "choices": ["1 hour or less", "1--4 hours", "4--24 hours", "> 24 hours or undefined"], "weight": "High"},
                {"q": "When was the last backup restoration test performed?", "choices": ["Within 6 months", "6–12 months ago", "> 12 months ago", "Never tested"], "weight": "High"},
                {"q": "Is forensic evidence preservation addressed for this application?", "choices": ["Yes — log retention and chain of custody documented", "Partial — logs retained but no formal process", "No forensic readiness", "N/A"], "weight": "Medium"},
            ]
        },
        {
            "domain": "Third-Party and Supply Chain Risk",
            "policy_refs": ["ISP 2.6"],
            "csf_refs": ["GV.SC"],
            "questions": [
                {"q": "Is the application a third-party or SaaS product?", "choices": ["Yes — SaaS / cloud-hosted", "Yes — on-premises third-party", "No — internally developed", "Hybrid"], "weight": "Info"},
                {"q": "Has a vendor security assessment been completed?", "choices": ["Yes — within 12 months", "Yes — older than 12 months", "No assessment performed", "N/A — internal application"], "weight": "High"},
                {"q": "Does the vendor contract include security requirements?", "choices": ["Yes — comprehensive security addendum", "Yes — basic security clauses", "No security requirements in contract", "N/A"], "weight": "High"},
                {"q": "Is there a defined exit strategy for vendor transition?", "choices": ["Yes — documented with data portability plan", "Partial plan", "No exit strategy", "N/A"], "weight": "Medium"},
                {"q": "Is there a phased deployment plan with maturity-gated control enhancements (e.g., crawl/walk/run)?", "choices": ["Yes — defined phases with control gates at each stage", "Yes — informal phased approach", "No — full deployment without phased controls", "N/A"], "weight": "High"},
                {"q": "Have AI-specific risks been formally assessed for this application (e.g., overreliance, output accuracy, prompt consistency, IP leakage)?", "choices": ["Yes — formal AI risk assessment completed", "Yes — partial assessment of key risks", "Not applicable — no AI/ML capabilities", "No — AI risks not assessed"], "weight": "High"},
            ]
        },
    ]
    
    tex = r"""
\documentclass[11pt,landscape]{article}
\usepackage[landscape,margin=1in]{geometry}
\usepackage{longtable,booktabs,array,tabularx,xcolor,hyperref,fancyhdr,enumitem,amssymb,amsmath}
\usepackage[T1]{fontenc}
\usepackage{helvet}
\renewcommand{\familydefault}{\sfdefault}

\definecolor{stridegreen}{HTML}{2E7D32}
\definecolor{strideblue}{HTML}{1565C0}
\definecolor{stridegray}{HTML}{757575}
\definecolor{critbg}{HTML}{FFEBEE}
\definecolor{highbg}{HTML}{FFF3E0}
\definecolor{medbg}{HTML}{E8F5E9}
\definecolor{ferpabox}{HTML}{FFF3E0}
\definecolor{soxbox}{HTML}{F3E5F5}

\hypersetup{colorlinks=true,linkcolor=strideblue,urlcolor=strideblue}

\pagestyle{fancy}
\fancyhf{}
\fancyhead[L]{\small\textcolor{stridegray}{Stride ASR Questionnaire V3}}
\fancyhead[R]{\small\textcolor{stridegray}{CONFIDENTIAL}}
\fancyfoot[C]{\thepage}
\fancyfoot[R]{\small March 2, 2026}
\renewcommand{\headrulewidth}{0.4pt}

\setlength{\parindent}{0pt}
\setlength{\parskip}{4pt}

\newcommand{\ferpabox}[1]{\colorbox{ferpabox}{\parbox{0.95\textwidth}{\small\textbf{FERPA Note:} #1}}}
\newcommand{\soxbox}[1]{\colorbox{soxbox}{\parbox{0.95\textwidth}{\small\textbf{SOX §404 Note:} #1}}}

\begin{document}

% --- Title Page ---
\begin{titlepage}
\vspace*{2cm}
\begin{center}
{\Huge\bfseries\textcolor{stridegreen}{Stride Application Security Review}}\\[0.3cm]
{\Huge\bfseries\textcolor{stridegreen}{Questionnaire}}\\[0.5cm]
{\LARGE Version 3.0}\\[1cm]
{\large Stride — K12 Inc.}\\[0.3cm]
{\large Information Security \& Governance}\\[2cm]
{\normalsize Discrete-choice questionnaire for application security risk assessment.}\\
{\normalsize Organized by policy domain with regulatory cross-references.}\\[1cm]
{\normalsize Frameworks: NIST CSF 2.0 \textbar{} FERPA (34 CFR Part 99) \textbar{} SOX §404 ITGC}\\[2cm]
{\small Document Date: March 2, 2026}\\
{\small Classification: Confidential}\\
{\small Supersedes: ASR Checklist V2}\\
\end{center}
\end{titlepage}

\tableofcontents
\newpage

% --- Instructions ---
\section{Instructions}

\subsection{Purpose}
This questionnaire is used to assess the security posture of applications within the Stride technology portfolio. Each question maps to specific Stride ISP/IISP policies, NIST CSF 2.0 subcategories, and where applicable, FERPA and SOX §404 ITGC requirements.

\subsection{How to Complete}
\begin{enumerate}
    \item For each question, select \textbf{exactly one} response that best describes the current state.
    \item Mark your selection with \textbf{$\checkmark$} or \textbf{X} in the checkbox.
    \item Questions marked \textbf{Critical} require immediate attention if the response indicates a gap.
    \item If a question is not applicable, select ``N/A'' and provide a brief justification in the notes column.
\end{enumerate}

\subsection{Scoring Model}

This questionnaire uses a \textbf{weighted scoring model} that assigns decreasing
importance to successive findings so that overall risk is dominated by the most
severe gaps rather than their count.

\subsubsection*{Per-Question Scoring}
\begin{enumerate}[leftmargin=*]
    \item Each answer choice carries an ordinal score reflecting maturity or risk.
    \item The \textbf{weight tier} of the question multiplies the raw score to
          produce a \textbf{weighted measurement} visible as a gray annotation
          next to each choice.
\end{enumerate}

\begin{tabularx}{\textwidth}{lcXl}
\toprule
\textbf{Weight Tier} & \textbf{Priority} & \textbf{Description} & \textbf{Escalation} \\
\midrule
\colorbox{critbg}{Critical} & Highest & Fundamental control --- gap requires immediate remediation & CISO notification \\
\colorbox{highbg}{High} & High & Important control --- gap requires 30-day remediation & Security Architecture review \\
\colorbox{medbg}{Medium} & Moderate & Supporting control --- address in next planning cycle & Risk acceptance option \\
Info & Low & Contextual / informational only & None \\
\bottomrule
\end{tabularx}

\subsubsection*{Composite Scoring}

Weighted measurements are combined using a \textbf{proprietary composite function}
that emphasizes the most severe finding and progressively discounts lesser ones.
This prevents score inflation from many low-severity gaps.

\begin{itemize}[leftmargin=*]
    \item \textbf{Section Score:} composite of all question measurements within a domain.
    \item \textbf{Questionnaire Score:} composite across the entire questionnaire.
    \item \textbf{Normalized Score:} mapped to a 0--100\% scale for comparison.
\end{itemize}

\vspace{0.2cm}
{\small\textbf{Interpretation:} 0--25\% = strong posture; 26--50\% = adequate; 51--75\% = elevated risk; 76--100\% = critical gaps requiring immediate action.}

\subsection{Application Information}
\begin{tabularx}{\textwidth}{lX}
\toprule
\textbf{Field} & \textbf{Value} \\
\midrule
Application Name & \\
Business Owner & \\
Technical Owner & \\
CMDB ID & \\
Risk Classification & \\
Assessment Date & \\
Assessor & \\
\bottomrule
\end{tabularx}

\newpage
"""

    # Generate domain sections
    q_num = 0
    for domain in ASR_DOMAINS:
        tex += f"\\section{{{escape_latex(domain['domain'])}}}\n\n"
        
        # Policy and CSF references
        pol_refs = ", ".join([f"STRIDE {p}" for p in domain["policy_refs"]])
        csf_refs = ", ".join(domain["csf_refs"])
        tex += f"\\textbf{{Policy References:}} {escape_latex(pol_refs)} \\hfill \\textbf{{CSF:}} {csf_refs}\n\n"
        
        # Regulatory notes
        if "ferpa_note" in domain:
            tex += f"\\ferpabox{{{escape_latex(domain['ferpa_note'])}}}\n\n\\vspace{{0.2cm}}\n\n"
        if "sox_note" in domain:
            tex += f"\\soxbox{{{escape_latex(domain['sox_note'])}}}\n\n\\vspace{{0.2cm}}\n\n"
        
        # Questions table
        for question in domain["questions"]:
            q_num += 1
            weight = question["weight"]
            if weight == "Critical":
                weight_color = "critbg"
            elif weight == "High":
                weight_color = "highbg"
            elif weight == "Medium":
                weight_color = "medbg"
            else:
                weight_color = "white"
            
            n_choices = len(question["choices"])
            scores = choice_scores(n_choices)
            w_val = WEIGHT_MAP.get(weight, 1)
            tex += f"\\noindent\\colorbox{{{weight_color}}}{{\\textbf{{Q{q_num}}} [{weight}]}}"
            tex += f" {escape_latex(question['q'])}\n\n"
            tex += "\\begin{tabularx}{\\textwidth}{cXX}\n"
            
            for i, choice in enumerate(question["choices"]):
                raw = scores[i]
                m = raw * w_val / WEIGHT_MAX
                checkbox = "$\\square$"
                # Show raw score and weight-adjusted measurement
                score_tag = f"\\textsuperscript{{\\scriptsize\\textcolor{{stridegray}}{{{raw}}}}}"
                tex += f"{checkbox} & {escape_latex(choice)} {score_tag} & "
                if i == 0:
                    tex += "Notes: \\rule{4cm}{0.4pt}"
                tex += " \\\\\n"
            
            tex += "\\end{tabularx}\n\n\\vspace{0.3cm}\n\n"
        
        tex += "\\newpage\n\n"

    # Summary / Scoring section — RSK aggregates
    # Pre-calculate max RSK per domain (all worst answers)
    domain_rsk_data = []
    all_worst_measurements = []
    all_best_measurements = []
    for domain in ASR_DOMAINS:
        worst_m = []
        best_m = []
        for q in domain["questions"]:
            n_c = len(q["choices"])
            sc = choice_scores(n_c)
            w = WEIGHT_MAP.get(q["weight"], 1)
            worst_m.append(sc[-1] * w / WEIGHT_MAX)   # worst answer
            best_m.append(sc[0] * w / WEIGHT_MAX)     # best answer
        max_rsk = rsk_aggregate(worst_m)
        min_rsk = rsk_aggregate(best_m)
        domain_rsk_data.append({
            "name": domain["domain"],
            "n_q": len(domain["questions"]),
            "max_rsk": max_rsk,
            "min_rsk": min_rsk,
            "max_norm": rsk_normalize(max_rsk),
            "min_norm": rsk_normalize(min_rsk),
        })
        all_worst_measurements.extend(worst_m)
        all_best_measurements.extend(best_m)

    total_q = sum(d["n_q"] for d in domain_rsk_data)
    total_max_rsk = rsk_aggregate(all_worst_measurements)
    total_min_rsk = rsk_aggregate(all_best_measurements)

    tex += r"""
\section{Assessment Summary}

\subsection{Domain Summary}
Complete after all sections are answered. Record each domain's risk rating below.

\begin{tabularx}{\textwidth}{lcccl}
\toprule
\textbf{Domain} & \textbf{\#\,Questions} & \textbf{Score\,\%} & \textbf{Rating} & \textbf{Notes} \\
\midrule
"""
    for d in domain_rsk_data:
        tex += (f"{escape_latex(d['name'])} & {d['n_q']} & "
                f" & & \\\\\n")

    tex += "\\midrule\n"
    tex += (f"\\textbf{{OVERALL}} & {total_q} & "
            f" & & \\\\\n")
    tex += "\\bottomrule\n\\end{tabularx}\n\n"

    tex += r"""
{\small\textit{Scores are computed by the assessor using the proprietary composite function.
Recording the normalized 0--100\% score per domain and overall enables tracking over time.}}

\subsection{Risk Rating Scale}

\begin{tabularx}{\textwidth}{lXl}
\toprule
\textbf{Norm\,\%} & \textbf{Description} & \textbf{Rating} \\
\midrule
0--25\% & Strong posture --- controls are mature and effective & \textcolor{stridegreen}{\textbf{Low}} \\
26--50\% & Adequate posture --- minor gaps with compensating controls & \textbf{Moderate} \\
51--75\% & Elevated risk --- material gaps requiring remediation plans & \textcolor{orange}{\textbf{Elevated}} \\
76--100\% & Critical risk --- fundamental controls missing or ineffective & \textcolor{red}{\textbf{Critical}} \\
\bottomrule
\end{tabularx}

\vspace{0.3cm}
{\small\textit{Domains with Norm\,\% above 50\% should trigger a remediation workstream.
The composite scoring method ensures that the single most severe gap dominates
the aggregate, reflecting operational reality.}}

\subsection{Assessor Certification}

\vspace{0.5cm}
\begin{tabularx}{\textwidth}{lX}
Assessor Signature: & \rule{6cm}{0.4pt} \\[0.5cm]
Date: & \rule{4cm}{0.4pt} \\[0.5cm]
Reviewer Signature: & \rule{6cm}{0.4pt} \\[0.5cm]
Date: & \rule{4cm}{0.4pt} \\
\end{tabularx}

\end{document}
"""

    tex_path = TEX_DIR / "asr_questionnaire_v3.tex"
    tex_path.write_text(tex)
    print(f"  LaTeX written: {tex_path}")
    return tex_path


# ============================================================
# PDF Compilation
# ============================================================

def compile_pdf(tex_path, output_name):
    """Compile LaTeX to PDF using pdflatex."""
    print(f"  Compiling {output_name}...")
    output_pdf = OUTPUT / output_name
    
    # Run pdflatex twice for TOC
    for run in range(2):
        result = subprocess.run(
            ["pdflatex", "-interaction=nonstopmode", "-output-directory", str(TEX_DIR), str(tex_path)],
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, cwd=str(TEX_DIR),
            timeout=120
        )
        if result.returncode != 0 and run == 1:
            print(f"  WARNING: pdflatex returned {result.returncode}")
            log_file = tex_path.with_suffix('.log')
            if log_file.exists():
                log_text = log_file.read_text(errors='replace')
                error_lines = [l for l in log_text.split('\n') if l.startswith('!') or 'Error' in l]
                if error_lines:
                    print(f"  Errors: {'; '.join(error_lines[:5])}")
    
    # Move PDF to output
    compiled_pdf = tex_path.with_suffix('.pdf')
    if compiled_pdf.exists():
        import shutil
        shutil.copy2(str(compiled_pdf), str(output_pdf))
        file_size = output_pdf.stat().st_size
        print(f"  SUCCESS: {output_pdf} ({file_size:,} bytes)")
        return output_pdf
    else:
        print(f"  FAILED: No PDF generated for {output_name}")
        return None


# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":
    print("=" * 60)
    print("STRIDE DELIVERABLES BUILD")
    print(f"Date: {date.today()}")
    print("=" * 60)
    
    # Build LaTeX sources
    tex1 = build_policy_cross_reference()
    tex2 = build_sra_v7()
    tex3 = build_asr_questionnaire()
    
    print("\n" + "=" * 60)
    print("COMPILING PDFs")
    print("=" * 60)
    
    pdf1 = compile_pdf(tex1, "Stride_Policy_Cross_Reference_V6.pdf")
    pdf2 = compile_pdf(tex2, "Stride_SRA_V7.pdf")
    pdf3 = compile_pdf(tex3, "Stride_ASR_Questionnaire_V3.pdf")
    
    print("\n" + "=" * 60)
    print("BUILD COMPLETE")
    print("=" * 60)
    results = [
        ("Policy Cross Reference V6", pdf1),
        ("SRA V7", pdf2),
        ("ASR Questionnaire V3", pdf3),
    ]
    for name, path in results:
        if path and path.exists():
            print(f"  ✓ {name}: {path} ({path.stat().st_size:,} bytes)")
        else:
            print(f"  ✗ {name}: FAILED")
    
    print(f"\nOutput directory: {OUTPUT}")
