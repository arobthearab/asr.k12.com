// ════════════════════════════════════════════════════════════════════
// Stride (k12.com) — ASR Client Overlay: ISP/IISP Policies
// ════════════════════════════════════════════════════════════════════
// Seeds Stride-specific Policy nodes, Domain→Policy relationships,
// policyRefs, FERPA notes, and SOX compliance notes.
//
// Usage: set ASR_OVERLAY_CYPHER_DIR to this directory before running
//   npm run cypher:setup -w api
// ════════════════════════════════════════════════════════════════════

// ─── ISP Policy Nodes ────────────────────────────────────────────

MERGE (p:Policy {reference: 'ISP 1.0'})  SET p.title = 'Information Security Program', p.updated = datetime();
MERGE (p:Policy {reference: 'ISP 2.1'})  SET p.title = 'Risk Assessment', p.updated = datetime();
MERGE (p:Policy {reference: 'ISP 2.3'})  SET p.title = 'Access Management Policy', p.updated = datetime();
MERGE (p:Policy {reference: 'ISP 2.4'})  SET p.title = 'Security Awareness', p.updated = datetime();
MERGE (p:Policy {reference: 'ISP 2.5'})  SET p.title = 'Security Documentation', p.updated = datetime();
MERGE (p:Policy {reference: 'ISP 2.6'})  SET p.title = 'Third-Party Risk Management', p.updated = datetime();
MERGE (p:Policy {reference: 'ISP 3.2'})  SET p.title = 'Vulnerability Management', p.updated = datetime();
MERGE (p:Policy {reference: 'ISP 4.1'})  SET p.title = 'Identity and Access Management', p.updated = datetime();
MERGE (p:Policy {reference: 'ISP 4.3'})  SET p.title = 'Data Protection', p.updated = datetime();
MERGE (p:Policy {reference: 'ISP 4.4'})  SET p.title = 'Secure Development', p.updated = datetime();
MERGE (p:Policy {reference: 'ISP 5.1'})  SET p.title = 'Threat Detection', p.updated = datetime();
MERGE (p:Policy {reference: 'ISP 6.1'})  SET p.title = 'Incident Response', p.updated = datetime();
MERGE (p:Policy {reference: 'ISP 6.2'})  SET p.title = 'Business Continuity', p.updated = datetime();

// ─── IISP Policy Nodes ──────────────────────────────────────────

MERGE (p:Policy {reference: 'IISP 1.0'}) SET p.title = 'Information Security Implementation Standard', p.updated = datetime();
MERGE (p:Policy {reference: 'IISP 2.0'}) SET p.title = 'Data Classification Implementation', p.updated = datetime();
MERGE (p:Policy {reference: 'IISP 3.0'}) SET p.title = 'Data Handling Implementation', p.updated = datetime();
MERGE (p:Policy {reference: 'IISP 7.0'}) SET p.title = 'Vulnerability Scanning Implementation', p.updated = datetime();
MERGE (p:Policy {reference: 'IISP 8.0'}) SET p.title = 'Access Control Implementation', p.updated = datetime();
MERGE (p:Policy {reference: 'IISP 9.0'}) SET p.title = 'Secure Development Implementation', p.updated = datetime();
MERGE (p:Policy {reference: 'IISP 10.0'}) SET p.title = 'Business Continuity Implementation', p.updated = datetime();

// ─── Domain policyRefs and Compliance Notes ─────────────────────

MATCH (d0:Domain {domainIndex: 0})
  SET d0.policyRefs = ['ISP 1.0', 'ISP 2.1', 'ISP 2.4', 'ISP 2.5'];

MATCH (d1:Domain {domainIndex: 1})
  SET d1.policyRefs = ['ISP 4.1', 'ISP 2.3', 'IISP 8.0'];

MATCH (d2:Domain {domainIndex: 2})
  SET d2.policyRefs = ['ISP 4.3', 'IISP 2.0', 'IISP 3.0'],
      d2.ferpaNote  = 'Applications processing student education records must comply with FERPA §99.30 (consent), §99.31 (exceptions), and §99.37 (directory information).';

MATCH (d3:Domain {domainIndex: 3})
  SET d3.policyRefs = ['ISP 4.4', 'IISP 9.0'],
      d3.soxNote    = 'SOX §404 ITGC domains CM-1 through CM-6 and PD-1 through PD-4 require documented change management and security testing controls.';

MATCH (d4:Domain {domainIndex: 4})
  SET d4.policyRefs = ['IISP 7.0', 'ISP 3.2', 'ISP 5.1'];

MATCH (d5:Domain {domainIndex: 5})
  SET d5.policyRefs = ['ISP 6.1', 'ISP 6.2', 'IISP 1.0', 'IISP 10.0'];

MATCH (d6:Domain {domainIndex: 6})
  SET d6.policyRefs = ['ISP 2.6'];

// ─── Domain → Policy Relationships ──────────────────────────────

// D0: Governance
MATCH (d:Domain {domainIndex: 0})
UNWIND ['ISP 1.0', 'ISP 2.1', 'ISP 2.4', 'ISP 2.5'] AS ref
MATCH (p:Policy {reference: ref})
MERGE (d)-[:REFERENCES_POLICY]->(p);

// D1: IAM
MATCH (d:Domain {domainIndex: 1})
UNWIND ['ISP 4.1', 'ISP 2.3', 'IISP 8.0'] AS ref
MATCH (p:Policy {reference: ref})
MERGE (d)-[:REFERENCES_POLICY]->(p);

// D2: Data Protection
MATCH (d:Domain {domainIndex: 2})
UNWIND ['ISP 4.3', 'IISP 2.0', 'IISP 3.0'] AS ref
MATCH (p:Policy {reference: ref})
MERGE (d)-[:REFERENCES_POLICY]->(p);

// D3: Secure Development
MATCH (d:Domain {domainIndex: 3})
UNWIND ['ISP 4.4', 'IISP 9.0'] AS ref
MATCH (p:Policy {reference: ref})
MERGE (d)-[:REFERENCES_POLICY]->(p);

// D4: Vulnerability Mgmt
MATCH (d:Domain {domainIndex: 4})
UNWIND ['IISP 7.0', 'ISP 3.2', 'ISP 5.1'] AS ref
MATCH (p:Policy {reference: ref})
MERGE (d)-[:REFERENCES_POLICY]->(p);

// D5: Incident Response
MATCH (d:Domain {domainIndex: 5})
UNWIND ['ISP 6.1', 'ISP 6.2', 'IISP 1.0', 'IISP 10.0'] AS ref
MATCH (p:Policy {reference: ref})
MERGE (d)-[:REFERENCES_POLICY]->(p);

// D6: Third-Party
MATCH (d:Domain {domainIndex: 6})
UNWIND ['ISP 2.6'] AS ref
MATCH (p:Policy {reference: ref})
MERGE (d)-[:REFERENCES_POLICY]->(p);
