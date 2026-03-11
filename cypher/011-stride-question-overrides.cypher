// ════════════════════════════════════════════════════════════════════
// Stride (k12.com) — ASR Client Overlay: Question Overrides
// ════════════════════════════════════════════════════════════════════
// Overrides generic question text and answer choices with
// Stride-specific tool names (Entra ID, CMDB).
//
// Runs AFTER configureFromYaml.mjs — MATCH ensures it only applies
// when the target questions exist (safe to re-run).
//
// Only tool-name overrides belong here.  Content that is part of the
// Stride questionnaire (FERPA, SCCM, SOX references) belongs in the
// YAML source of truth (build/asr_questions.yaml).
// ════════════════════════════════════════════════════════════════════

// ─── D0Q0: CMDB-specific answer choice ──────────────────────────

MATCH (q:Question {domainIndex: 0, questionIndex: 0})
  SET q.choices = ['Yes — named owner in CMDB', 'Yes — informal ownership', 'No — ownership not established'];

// ─── D1Q0: Entra ID as enterprise IdP ───────────────────────────

MATCH (q:Question {domainIndex: 1, questionIndex: 0})
  SET q.choices = ['Passwordless (FIDO2/passkey/client certificate)', 'SSO with MFA (Entra ID)', 'SSO without MFA', 'Local authentication with MFA', 'Local authentication without MFA'];
