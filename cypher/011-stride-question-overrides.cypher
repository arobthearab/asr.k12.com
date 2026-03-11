// ════════════════════════════════════════════════════════════════════
// Stride (k12.com) — ASR Client Overlay: Question Overrides
// ════════════════════════════════════════════════════════════════════
// Overrides generic question text and answer choices with
// Stride-specific wording (FERPA, Entra ID, SCCM, CMDB).
// Runs after 002-seed-questionnaire.cypher — MERGE ensures safety.
// ════════════════════════════════════════════════════════════════════

// ─── D0Q1: CMDB-specific answer choice ──────────────────────────

MATCH (q:Question {domainIndex: 0, questionIndex: 0})
  SET q.choices = ['Yes — named owner in CMDB', 'Yes — informal ownership', 'No — ownership not established'];

// ─── D1Q1: Entra ID as enterprise IdP ───────────────────────────

MATCH (q:Question {domainIndex: 1, questionIndex: 0})
  SET q.choices = ['SSO with MFA (Entra ID)', 'SSO without MFA', 'Local authentication with MFA', 'Local authentication without MFA'];

// ─── D2Q1: FERPA-specific data protection question ──────────────

MATCH (q:Question {domainIndex: 2, questionIndex: 0})
  SET q.text    = 'Does the application process, store, or transmit student education records (FERPA-protected data)?',
      q.choices = ['No — no education records', 'Yes — incidental processing', 'Yes — primary function', 'Unknown / Not assessed'];

// ─── D2Q6: FERPA §99.32 disclosure records ──────────────────────

MATCH (q:Question {domainIndex: 2, questionIndex: 5})
  SET q.text = 'Does the application maintain disclosure records as required by FERPA §99.32?';

// ─── D3Q6: SCCM-specific endpoint management ────────────────────

MATCH (q:Question {domainIndex: 3, questionIndex: 5})
  SET q.choices = ['Fully managed via enterprise MDM/SCCM', 'Partially managed — some updates out-of-band', 'Entirely out-of-band (CLI / manual / vendor-pushed)'];
