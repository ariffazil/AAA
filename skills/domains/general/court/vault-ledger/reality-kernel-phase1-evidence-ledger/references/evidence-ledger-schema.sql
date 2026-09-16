-- Reality Kernel Phase 1 — Evidence Ledger Schema
-- SQLite append-only with hash chain integrity
-- Created: 2026-08-19
-- Updated: 2026-08-19 — added DB-level agent write restriction trigger
-- DITEMPA BUKAN DIBERI

-- ============================================================
-- CORE TABLES
-- ============================================================

-- Event ledger: append-only factual records
CREATE TABLE IF NOT EXISTS reality_events (
    event_id        TEXT PRIMARY KEY,            -- evt_{ULID}
    prev_hash       TEXT NOT NULL,               -- SHA-256 of previous event (chain integrity)
    event_hash      TEXT NOT NULL,               -- SHA-256 of this event's canonical form
    occurred_at     TEXT NOT NULL,               -- ISO 8601 with timezone (when it happened)
    recorded_at     TEXT NOT NULL,               -- ISO 8601 with timezone (when ledger received it)
    event_type      TEXT NOT NULL,               -- e.g., 'deployment.status_observed', 'config.changed'
    subject         TEXT NOT NULL,               -- what this event is about (entity@scope)
    state           TEXT NOT NULL                -- four-state truth model
                    CHECK(state IN ('OBSERVED', 'ATTESTED', 'INFERRED', 'UNKNOWN')),
    actor_kind      TEXT NOT NULL                -- who/what created this record
                    CHECK(actor_kind IN ('connector', 'human', 'agent')),
    actor_id        TEXT NOT NULL,               -- specific actor identifier
    authority       TEXT NOT NULL,               -- 'system_receipt' | 'human_attestation' | 'agent_inference'
    source_uri      TEXT,                        -- URI of the authoritative source
    source_receipt_id TEXT,                      -- receipt ID from the source system
    source_content_hash TEXT,                    -- SHA-256 of the raw receipt
    confidence      REAL NOT NULL DEFAULT 0.5    -- [0,1] confidence in this record
                    CHECK(confidence >= 0 AND confidence <= 1),
    supersedes      TEXT,                        -- event_id this record supersedes (if correction)
    scope           TEXT NOT NULL                -- 'production' | 'staging' | 'development' | 'all'
                    CHECK(scope IN ('production', 'staging', 'development', 'all')),
    immutable       INTEGER NOT NULL DEFAULT 1   -- 1 = cannot be modified, only superseded
);

-- Evidence items: raw receipts, artifacts, proofs
CREATE TABLE IF NOT EXISTS reality_evidence (
    evidence_id     TEXT PRIMARY KEY,            -- ev_{ULID}
    event_id        TEXT NOT NULL REFERENCES reality_events(event_id),
    evidence_type   TEXT NOT NULL                -- what kind of evidence
                    CHECK(evidence_type IN (
                        'ci_receipt',           -- CI/CD pipeline output
                        'api_response',         -- API call response
                        'file_hash',            -- file content hash
                        'human_report',         -- human testimony
                        'sensor_reading',       -- sensor/IoT data
                        'database_record',      -- DB query result
                        'log_entry',            -- log file line
                        'screenshot',           -- visual evidence
                        'message_id',           -- messaging platform receipt
                        'contract_receipt'      -- external contract/system receipt
                    )),
    content_hash    TEXT NOT NULL,              -- SHA-256 of the raw evidence content
    content_type    TEXT,                       -- MIME type (application/json, text/plain, etc.)
    storage_uri     TEXT,                       -- where the full evidence is stored (file path, URL)
    captured_at     TEXT NOT NULL,              -- ISO 8601 (when evidence was captured)
    captured_by     TEXT NOT NULL,              -- actor that captured this evidence
    verified        INTEGER NOT NULL DEFAULT 0  -- 1 = independently verified by second source
);

-- Conflict log: when two records contradict each other
CREATE TABLE IF NOT EXISTS reality_conflicts (
    conflict_id     TEXT PRIMARY KEY,           -- cfx_{ULID}
    event_id_a      TEXT NOT NULL REFERENCES reality_events(event_id),
    event_id_b      TEXT NOT NULL REFERENCES reality_events(event_id),
    conflict_type   TEXT NOT NULL               -- what kind of contradiction
                    CHECK(conflict_type IN (
                        'contradiction',        -- A says X, B says not X
                        'temporal_impossible',  -- timestamps violate causality
                        'scope_overlap',        -- same subject, overlapping scope
                        'state_upgrade',        -- OBSERVED from non-connector actor
                        'chain_break'           -- hash chain integrity failure
                    )),
    detected_at     TEXT NOT NULL,              -- ISO 8601 (when conflict was detected)
    resolved        INTEGER NOT NULL DEFAULT 0, -- 1 = conflict has been resolved
    resolution      TEXT,                       -- how it was resolved
    resolved_by     TEXT,                       -- who resolved it
    resolved_at     TEXT                        -- when it was resolved
);

-- Action state machine: track planned/executed/verified actions
CREATE TABLE IF NOT EXISTS reality_actions (
    action_id       TEXT PRIMARY KEY,           -- act_{ULID}
    event_id        TEXT REFERENCES reality_events(event_id),
    action_type     TEXT NOT NULL,              -- what kind of action
    subject         TEXT NOT NULL,              -- what system/component is affected
    state           TEXT NOT NULL               -- action state machine
                    CHECK(state IN (
                        'PROPOSED',             -- agent suggests
                        'REQUESTED',            -- formal request submitted
                        'AUTHORIZED',           -- human/F13 approved
                        'EXECUTED',             -- action performed
                        'VERIFIED',             -- outcome confirmed via read-back
                        'ROLLED_BACK',          -- action reversed
                        'FAILED'                -- action could not complete
                    )),
    proposed_at     TEXT,
    requested_at    TEXT,
    authorized_at   TEXT,
    authorized_by   TEXT,                       -- who authorized (F13 or connector)
    executed_at     TEXT,
    executed_by     TEXT,                       -- who/what executed
    verified_at     TEXT,
    verified_by     TEXT,                       -- who/what verified outcome
    rolled_back_at  TEXT,
    failure_reason  TEXT
);

-- ============================================================
-- INDEXES
-- ============================================================

-- Timeline queries: "what happened to subject X between time A and B?"
CREATE INDEX IF NOT EXISTS idx_events_subject_time
    ON reality_events(subject, occurred_at);

-- State queries: "show me all INFERRED records" or "show me all OBSERVED"
CREATE INDEX IF NOT EXISTS idx_events_state
    ON reality_events(state);

-- Actor queries: "what did connector X write?"
CREATE INDEX IF NOT EXISTS idx_events_actor
    ON reality_events(actor_kind, actor_id);

-- Conflict queries: "what unresolved conflicts exist?"
CREATE INDEX IF NOT EXISTS idx_conflicts_unresolved
    ON reality_conflicts(resolved, detected_at);

-- Evidence queries: "what evidence supports event X?"
CREATE INDEX IF NOT EXISTS idx_evidence_event
    ON reality_evidence(event_id);

-- Chain verification: ordered traversal
CREATE INDEX IF NOT EXISTS idx_events_chain
    ON reality_events(event_id);

-- ============================================================
-- APPEND-ONLY ENFORCEMENT (SQLite triggers)
-- ============================================================

-- Prevent UPDATE on events (append-only)
CREATE TRIGGER IF NOT EXISTS trg_events_no_update
BEFORE UPDATE ON reality_events
BEGIN
    SELECT RAISE(ABORT, 'reality_events is append-only; use supersedes to correct');
END;

-- Prevent DELETE on events (append-only)
CREATE TRIGGER IF NOT EXISTS trg_events_no_delete
BEFORE DELETE ON reality_events
BEGIN
    SELECT RAISE(ABORT, 'reality_events is append-only; records cannot be deleted');
END;

-- Prevent UPDATE on evidence (append-only)
CREATE TRIGGER IF NOT EXISTS trg_evidence_no_update
BEFORE UPDATE ON reality_evidence
BEGIN
    SELECT RAISE(ABORT, 'reality_evidence is append-only');
END;

-- Prevent DELETE on evidence (append-only)
CREATE TRIGGER IF NOT EXISTS trg_evidence_no_delete
BEFORE DELETE ON reality_evidence
BEGIN
    SELECT RAISE(ABORT, 'reality_evidence is append-only; records cannot be deleted');
END;

-- ============================================================
-- LLM WRITE RESTRICTION (database-level enforcement)
-- ============================================================

-- Agent cannot create OBSERVED events. Only connectors and humans can.
-- This is the database-level enforcement that backs the application gate.
-- SQLite trigger checks column values at INSERT time.
-- NOTE: SQLite does not support stored procedures or role-based access.
--       A determined attacker controlling the application layer could bypass
--       this by setting actor_kind='connector'. For production enforcement,
--       migrate to PostgreSQL with role-based access and stored procedures:
--         append_agent_inference() — agent credential, INFERRED/PROPOSED/UNKNOWN only
--         append_connector_observation() — connector credential, OBSERVED/ATTESTED only
--         append_human_attestation() — human credential, ATTESTED only

CREATE TRIGGER IF NOT EXISTS trg_deny_agent_observed
BEFORE INSERT ON reality_events
FOR EACH ROW
BEGIN
    SELECT CASE
        WHEN NEW.actor_kind = 'agent' AND NEW.state = 'OBSERVED'
        THEN RAISE(ABORT, 'Agent cannot create OBSERVED events; use INFERRED or UNKNOWN')
    END;
END;

-- Agent cannot self-promote: UPDATE that changes state to OBSERVED is blocked
CREATE TRIGGER IF NOT EXISTS trg_deny_agent_self_promote
BEFORE UPDATE ON reality_events
FOR EACH ROW
BEGIN
    SELECT CASE
        WHEN NEW.state = 'OBSERVED' AND OLD.state != 'OBSERVED'
        THEN RAISE(ABORT, 'Cannot promote state to OBSERVED; only connectors/humans may observe')
    END;
END;

-- ============================================================
-- GENESIS EVENT
-- ============================================================
-- The first event in every ledger. hash = sha256("genesis")
-- prev_hash = "0" * 64 (no previous event)

-- INSERT INTO reality_events (
--     event_id, prev_hash, event_hash, occurred_at, recorded_at,
--     event_type, subject, state, actor_kind, actor_id, authority,
--     source_uri, source_receipt_id, source_content_hash,
--     confidence, supersedes, scope, immutable
-- ) VALUES (
--     'evt_genesis_001',
--     '0000000000000000000000000000000000000000000000000000000000000000',
--     'sha256:...',
--     '2026-08-19T00:00:00+08:00',
--     '2026-08-19T00:00:00+08:00',
--     'system.genesis',
--     'evidence_ledger',
--     'OBSERVED',
--     'human',
--     'arif-fazil',
--     'human_attestation',
--     NULL, NULL, NULL,
--     1.0, NULL, 'all', 1
-- );

-- ============================================================
-- SCHEMA VERSION
-- ============================================================

CREATE TABLE IF NOT EXISTS reality_schema_version (
    version         TEXT PRIMARY KEY,            -- '1.0.0'
    applied_at      TEXT NOT NULL,              -- ISO 8601
    applied_by      TEXT NOT NULL,              -- who applied this migration
    description     TEXT                        -- what changed
);

INSERT OR IGNORE INTO reality_schema_version (version, applied_at, applied_by, description)
VALUES ('1.0.0', '2026-08-19T00:00:00+08:00', 'reality-kernel-phase1', 'Initial schema: events, evidence, conflicts, actions, DB-level agent write restriction');
