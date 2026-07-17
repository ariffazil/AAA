/**
 * AAA → Supabase Approval Routes
 * Pre-seal approval records. AAA warga agents write approval judgments
 * before vault999-writer seals. Linked post-seal via /link_approval.
 *
 * DITEMPA BUKAN DIBERI — Forged, Not Given.
 */
const express = require('express');
const { createClient } = require('@supabase/supabase-js');
const crypto = require('crypto');
const router = express.Router();

// === SUPABASE CLIENT (service_role — bypasses RLS for server-side writes) ===
const SUPA_URL = process.env.SUPABASE_URL || process.env.VITE_SUPABASE_URL || '';
const SUPA_KEY = process.env.SUPABASE_SERVICE_ROLE_KEY || process.env.SUPABASE_SERVICE_KEY || '';
let supabase = null;
if (SUPA_URL && SUPA_KEY) {
  supabase = createClient(SUPA_URL, SUPA_KEY, {
    auth: { persistSession: false },
  });
}

// === AAA WARGA — agents authorised to write pre-seal approvals ===
const AAA_WARGA = Object.freeze([
  '333-AGI',
  '555-ASI',
  '888-APEX',
  // A-AUDIT, A-ARCHIVE — COLLAPSED 2026-07-15 (absorbed into arifOS + VAULT999)
  'aaa-gateway',             // AAA A2A gateway itself
  'Claude-AAA-Governed',     // Claude Code via AAA warga identity
]);

const VALID_STATUSES = ['APPROVED', 'REJECTED', 'ABSTAIN'];

// === ROUTES ===

/**
 * POST /approvals
 * Write a pre-seal approval record to Supabase aaa_approvals.
 * Body: { aaa_actor_id, approval_status, approval_payload?, aaa_signature }
 * Returns: 201 { approval_id, aaa_actor_id, approval_status, ... }
 */
router.post('/approvals', async (req, res) => {
  if (!supabase) {
    return res.status(503).json({
      error: 'supabase_unavailable',
      detail: 'SUPABASE_URL or SUPABASE_SERVICE_ROLE_KEY not configured',
    });
  }

  const { aaa_actor_id, approval_status, approval_payload = {}, aaa_signature } = req.body || {};

  // F11 AUTH: warga-only boundary
  if (!aaa_actor_id || !AAA_WARGA.includes(aaa_actor_id)) {
    return res.status(403).json({
      error: 'F11_AUTH',
      detail: `Actor '${aaa_actor_id || 'unknown'}' not in AAA warga. Allowed: ${AAA_WARGA.join(', ')}`,
    });
  }

  if (!VALID_STATUSES.includes(approval_status)) {
    return res.status(400).json({
      error: 'invalid_status',
      detail: `approval_status must be one of: ${VALID_STATUSES.join(', ')}`,
    });
  }

  if (!aaa_signature || typeof aaa_signature !== 'string' || aaa_signature.length < 8) {
    return res.status(400).json({
      error: 'F11_AUTH',
      detail: 'aaa_signature required (ed25519 signature over approval payload, v1 = trust+audit)',
    });
  }

  const approval_id = crypto.randomUUID();
  const { data, error } = await supabase
    .from('aaa_approvals')
    .insert({
      approval_id,
      aaa_actor_id,
      approval_status,
      approval_payload: typeof approval_payload === 'string'
        ? JSON.parse(approval_payload)
        : approval_payload,
      aaa_signature,
    })
    .select('approval_id, aaa_actor_id, approval_status, approved_at')
    .single();

  if (error) {
    console.error(`[approvals] Supabase insert failed: ${error.message}`);
    return res.status(500).json({ error: 'supabase_write_failed', detail: error.message });
  }

  console.log(
    `[approvals] ${aaa_actor_id} → ${approval_status} | approval_id=${approval_id}`
  );
  res.status(201).json(data);
});

/**
 * GET /approvals/:event_id
 * Query pre-seal approvals linked to a sealed event.
 * Returns: array of approval records
 */
router.get('/approvals/:event_id', async (req, res) => {
  if (!supabase) {
    return res.status(503).json({
      error: 'supabase_unavailable',
      detail: 'SUPABASE_URL or SUPABASE_SERVICE_ROLE_KEY not configured',
    });
  }

  const { event_id } = req.params;
  if (!event_id || event_id.length < 32) {
    return res.status(400).json({ error: 'invalid_event_id' });
  }

  const { data, error } = await supabase
    .from('aaa_approvals')
    .select('*')
    .eq('event_id', event_id)
    .order('approved_at', { ascending: false });

  if (error) {
    return res.status(500).json({ error: 'supabase_query_failed', detail: error.message });
  }

  res.json(data || []);
});

/**
 * GET /approvals/pending
 * List all unlinked approvals (pre-seal, event_id IS NULL).
 * For cockpit visibility.
 */
router.get('/approvals/pending', async (req, res) => {
  if (!supabase) {
    return res.status(503).json({
      error: 'supabase_unavailable',
    });
  }

  const { data, error } = await supabase
    .from('aaa_approvals')
    .select('*')
    .is('event_id', null)
    .order('approved_at', { ascending: false })
    .limit(100);

  if (error) {
    return res.status(500).json({ error: 'supabase_query_failed', detail: error.message });
  }

  res.json({ pending: data || [], count: (data || []).length });
});

module.exports = router;
