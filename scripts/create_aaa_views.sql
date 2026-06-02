-- ============================================================
-- AAA Read-Only Views — Phase 3A
-- Security: SECURITY DEFINER runs as table owner (postgres)
--          Bypasses RLS so anon key can read.
-- Views are SELECT-only — no INSERT/UPDATE/DELETE allowed.
-- ============================================================

-- 1. aaa.recent_seals
--    Shows the 50 most recent vault seals for AAA cockpit.
CREATE OR REPLACE VIEW aaa.recent_seals
WITH (security_barrier = false)
AS
SELECT
    id,
    event_id,
    event_type,
    actor_id,
    verdict,
    risk_tier,
    merkle_leaf,
    prev_leaf,
    sealed_by,
    signed_by,
    sealed_at,
    created_at,
    payload
FROM vault_sealed_events
ORDER BY sealed_at DESC NULLS LAST, created_at DESC
LIMIT 50;

-- 2. aaa.pending_approvals
--    Shows all unresolved approval tickets.
CREATE OR REPLACE VIEW aaa.pending_approvals
WITH (security_barrier = false)
AS
SELECT
    id,
    ticket_id,
    action_plan,
    human_verdict,
    requested_at,
    resolved_at,
    jsonb_build_object(
        'ticket_id', ticket_id,
        'verdict', human_verdict,
        'requested_at', requested_at
    ) AS summary
FROM arifosmcp_approval_tickets
WHERE human_verdict = 'PENDING'
ORDER BY requested_at DESC;

-- 3. aaa.mcp_surface
--    Shows tool call counts grouped by organ and tool name.
CREATE OR REPLACE VIEW aaa.mcp_surface
WITH (security_barrier = false)
AS
SELECT
    organ,
    tool_name,
    COUNT(*) AS call_count,
    COUNT(CASE WHEN verdict = 'SEAL' THEN 1 END) AS seal_count,
    COUNT(CASE WHEN verdict = 'SABAR' THEN 1 END) AS sabar_count,
    COUNT(CASE WHEN verdict = 'VOID' THEN 1 END) AS void_count,
    AVG(duration_ms) AS avg_duration_ms,
    COUNT(CASE WHEN error_msg IS NOT NULL THEN 1 END) AS error_count,
    MAX(epoch) AS last_called
FROM arifosmcp_tool_calls
GROUP BY organ, tool_name
ORDER BY call_count DESC;

-- 4. aaa.evidence_index
--    Shows canon records of type 'evidence_item'.
CREATE OR REPLACE VIEW aaa.evidence_index
WITH (security_barrier = false)
AS
SELECT
    id,
    record_type,
    reference_id,
    body,
    verdict,
    sealed_by,
    epoch,
    witness
FROM arifosmcp_canon_records
WHERE record_type IN ('evidence_item', 'interpretation', 'fact')
ORDER BY epoch DESC
LIMIT 100;

-- 5. aaa.artifact_index
--    Shows canon records of type 'artifact' or 'build_artifact'.
CREATE OR REPLACE VIEW aaa.artifact_index
WITH (security_barrier = false)
AS
SELECT
    id,
    record_type,
    reference_id,
    body,
    verdict,
    epoch
FROM arifosmcp_canon_records
WHERE record_type IN ('artifact', 'build_artifact', 'execution_receipt')
ORDER BY epoch DESC
LIMIT 100;

-- 6. aaa.risk_dashboard
--    Shows high-risk (tier >= 3) tool calls and their approval status.
CREATE OR REPLACE VIEW aaa.risk_dashboard
WITH (security_barrier = false)
AS
SELECT
    tc.id,
    tc.organ,
    tc.tool_name,
    tc.epoch,
    tc.verdict,
    tc.floor_triggered,
    tc.error_msg,
    tc.peace2,
    at.ticket_id,
    at.human_verdict AS approval_status,
    at.requested_at AS ticket_requested_at,
    at.resolved_at AS ticket_resolved_at
FROM arifosmcp_tool_calls tc
LEFT JOIN arifosmcp_approval_tickets at
    ON tc.session_id = at.ticket_id
    OR tc.id::text = at.ticket_id
WHERE tc.verdict IN ('HOLD', 'SABAR', 'VOID', 'SEAL')
ORDER BY tc.epoch DESC
LIMIT 100;

-- 7. aaa.memory_health
--    Shows row counts per Supabase table as a health check.
CREATE OR REPLACE VIEW aaa.memory_health
WITH (security_barrier = false)
AS
SELECT
    'arifosmcp_tool_calls' AS table_name,
    COUNT(*) AS row_count,
    MAX(epoch) AS last_activity,
    'ok' AS status
FROM arifosmcp_tool_calls
UNION ALL
SELECT
    'arifosmcp_approval_tickets' AS table_name,
    COUNT(*) AS row_count,
    MAX(requested_at) AS last_activity,
    CASE WHEN COUNT(*) > 0 AND MAX(CASE WHEN human_verdict = 'PENDING' THEN 1 END) > 0 THEN 'attention' ELSE 'ok' END AS status
FROM arifosmcp_approval_tickets
UNION ALL
SELECT
    'arifosmcp_canon_records' AS table_name,
    COUNT(*) AS row_count,
    MAX(epoch) AS last_activity,
    'ok' AS status
FROM arifosmcp_canon_records
UNION ALL
SELECT
    'vault_sealed_events' AS table_name,
    COUNT(*) AS row_count,
    MAX(sealed_at) AS last_activity,
    'ok' AS status
FROM vault_sealed_events
UNION ALL
SELECT
    'arifosmcp_sessions' AS table_name,
    COUNT(*) AS row_count,
    MAX(epoch) AS last_activity,
    'ok' AS status
FROM arifosmcp_sessions
ORDER BY table_name;

-- ============================================================
-- GRANT SELECT to anon role (for Supabase JS anon key access)
-- ============================================================
GRANT SELECT ON aaa.recent_seals TO anon;
GRANT SELECT ON aaa.pending_approvals TO anon;
GRANT SELECT ON aaa.mcp_surface TO anon;
GRANT SELECT ON aaa.evidence_index TO anon;
GRANT SELECT ON aaa.artifact_index TO anon;
GRANT SELECT ON aaa.risk_dashboard TO anon;
GRANT SELECT ON aaa.memory_health TO anon;
