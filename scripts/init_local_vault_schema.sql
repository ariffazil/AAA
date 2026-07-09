-- ============================================================
-- vault999 local schema initialization script
-- ============================================================

CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Table 1: vault_seals
CREATE TABLE IF NOT EXISTS vault_seals (
    id SERIAL PRIMARY KEY,
    record_id UUID NOT NULL UNIQUE DEFAULT gen_random_uuid(),
    event_type VARCHAR(50),
    session_id VARCHAR(100),
    actor_id VARCHAR(100),
    agent_id VARCHAR(100),
    action_type VARCHAR(100),
    seal_hash VARCHAR(100) UNIQUE,
    chain_hash VARCHAR(100),
    prev_seal_id VARCHAR(100),
    action TEXT,
    payload JSONB,
    verdict VARCHAR(50),
    epoch TIMESTAMPTZ,
    witness JSONB,
    signature TEXT,
    signed_by TEXT,
    sealed_at TIMESTAMPTZ DEFAULT NOW(),
    confidence    NUMERIC(4,3),
    created_at    TIMESTAMPTZ DEFAULT NOW(),
    timestamp     TIMESTAMPTZ,
    floors_triggered JSONB,
    data          JSONB,
    cooling_id    VARCHAR(100),
    aaa_surface          TEXT    DEFAULT 'AAA-HF',
    aaa_doctrine_version TEXT,
    aaa_canon_refs       TEXT[],
    floor_refs           TEXT[],
    record_class         TEXT    DEFAULT 'constitutional_receipt'
);

-- Table 2: cooling_queue
CREATE TABLE IF NOT EXISTS cooling_queue (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    session_id VARCHAR(100),
    agent_id VARCHAR(100),
    action_type VARCHAR(100),
    prospect_id VARCHAR(100),
    proposal_hash VARCHAR(100),
    judge_verdict VARCHAR(50),
    risk_class VARCHAR(50),
    status VARCHAR(50),
    payload JSONB,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    hold_initiated_at TIMESTAMPTZ DEFAULT NOW(),
    reviewed_by VARCHAR(100),
    reviewed_at TIMESTAMPTZ,
    review_notes TEXT,
    human_signature TEXT
);

-- Table 3: human_reviews
CREATE TABLE IF NOT EXISTS human_reviews (
    review_id SERIAL PRIMARY KEY,
    cooling_id UUID REFERENCES cooling_queue(id),
    reviewer_id VARCHAR(100),
    decision VARCHAR(50),
    reason TEXT,
    human_signature TEXT,
    reviewed_at TIMESTAMPTZ DEFAULT NOW()
);

-- Table 4: vault999_witness
CREATE TABLE IF NOT EXISTS vault999_witness (
    id SERIAL PRIMARY KEY,
    ledger_id INTEGER REFERENCES vault_seals(id),
    human_witness BOOLEAN,
    ai_witness BOOLEAN,
    evidence_witness BOOLEAN,
    w_score NUMERIC(4,2),
    metadata JSONB
);
