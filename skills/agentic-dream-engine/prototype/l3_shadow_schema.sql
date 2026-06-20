-- L3 Shadow Partition Schema
-- Location: /root/AAA/skills/agentic-dream-engine/prototype/l3_shadow_schema.sql
-- Purpose: Reversible staging area for sleep-time compute output before F1/F2 validation.
-- Doctrine: never write directly to primary memory_records/memory_embeddings during unsupervised dream state.

-- Enable pgvector if not already enabled (idempotent)
CREATE EXTENSION IF NOT EXISTS vector;

-- Shadow partition for compressed gist and pre-computed reasoning trees
CREATE TABLE IF NOT EXISTS l3_shadow (
    shadow_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    agent_id TEXT NOT NULL,               -- e.g. 'openclaw:sleep-time'
    session_id TEXT NOT NULL,             -- e.g. 'openclaw-sleep-2026-06-16'
    dream_cycle TEXT NOT NULL,            -- nightly window identifier

    -- Content
    gist_json JSONB NOT NULL,             -- compressed rules, summaries, anticipatory trees
    raw_token_count INT NOT NULL DEFAULT 0,
    gist_token_count INT NOT NULL DEFAULT 0,
    delta_s FLOAT NOT NULL DEFAULT 0.0,   -- (gist - raw) / raw ; must be negative for cooling

    -- Provenance
    source_refs JSONB NOT NULL DEFAULT '[]'::jsonb,  -- list of source trace IDs
    hash TEXT NOT NULL,                   -- sha256(gist_json)

    -- Governance
    status TEXT NOT NULL DEFAULT 'pending'
        CHECK (status IN ('pending', 'validated', 'purged')),
    f1_snapshot_path TEXT,                -- path to rollback snapshot
    f2_witness_verdict TEXT,              -- OK | HOLD | VOID
    f2_witness_evidence JSONB,            -- receipt from counterfactual challenge

    -- Timestamps
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    validated_at TIMESTAMPTZ,
    purged_at TIMESTAMPTZ
);

-- Indexes
CREATE INDEX IF NOT EXISTS idx_l3_shadow_agent ON l3_shadow(agent_id);
CREATE INDEX IF NOT EXISTS idx_l3_shadow_session ON l3_shadow(session_id);
CREATE INDEX IF NOT EXISTS idx_l3_shadow_status ON l3_shadow(status);
CREATE INDEX IF NOT EXISTS idx_l3_shadow_created ON l3_shadow(created_at DESC);

-- Shadow audit log: every daemon action leaves a trace
CREATE TABLE IF NOT EXISTS l3_shadow_audit (
    audit_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    shadow_id UUID REFERENCES l3_shadow(shadow_id) ON DELETE SET NULL,
    event_type TEXT NOT NULL,             -- daemon_start | daemon_suspend | ingest | metabolize | commit | validate | purge
    actor_id TEXT NOT NULL,
    session_id TEXT NOT NULL,
    payload JSONB,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_l3_shadow_audit_shadow ON l3_shadow_audit(shadow_id);
CREATE INDEX IF NOT EXISTS idx_l3_shadow_audit_event ON l3_shadow_audit(event_type);

-- Helper view: pending shadow gists ready for morning briefing review
CREATE OR REPLACE VIEW l3_shadow_pending_review AS
SELECT
    shadow_id,
    agent_id,
    session_id,
    dream_cycle,
    gist_json,
    raw_token_count,
    gist_token_count,
    delta_s,
    hash,
    source_refs,
    created_at
FROM l3_shadow
WHERE status = 'pending'
ORDER BY created_at DESC;

-- Comment for future agents
COMMENT ON TABLE l3_shadow IS
    'F1 reversibility staging area for sleep-time compute. No row here is canon until status=validated and copied to memory_records by morning_briefing_merge.py.';
