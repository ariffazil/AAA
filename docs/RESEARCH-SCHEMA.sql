-- =============================================================================
-- HERMES RESEARCH SUBSTRATE — PostgreSQL Schema
-- Extends: vault999 database (arifos_memory), research schema
-- Version: 1.0.0 (2026-09-19)
-- Constitutional alignment: F1 AMANAH, F2 TRUTH, F4 CLARITY, F11 AUDIT, F13 SOVEREIGN
-- =============================================================================

CREATE SCHEMA IF NOT EXISTS research;

-- =============================================================================
-- 1. SOURCE_REGISTRY — canonical scholarly provider registry
-- =============================================================================
-- Each row is a unique data provider (API, database, aggregator).
-- Tracks endpoint health, rate limits, and API version for reproducibility.

CREATE TABLE research.source_registry (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    slug            TEXT NOT NULL UNIQUE,
    display_name    TEXT NOT NULL,
    base_url        TEXT,
    api_version     TEXT,
    rate_limit_rpm  INTEGER,
    supports_doi    BOOLEAN NOT NULL DEFAULT false,
    supports_pmid   BOOLEAN NOT NULL DEFAULT false,
    supports_arxiv  BOOLEAN NOT NULL DEFAULT false,
    supports_isbn   BOOLEAN NOT NULL DEFAULT false,
    license_text    TEXT,
    status          TEXT NOT NULL DEFAULT 'active'
                    CHECK (status IN ('active', 'deprecated', 'offline', 'untrusted')),
    metadata        JSONB DEFAULT '{}'::jsonb,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at      TIMESTAMPTZ NOT NULL DEFAULT now()
);

COMMENT ON TABLE  research.source_registry IS 'Canonical registry of scholarly data providers for the Hermes Research Substrate.';
COMMENT ON COLUMN research.source_registry.slug IS 'URL-safe unique identifier for programmatic reference.';
COMMENT ON COLUMN research.source_registry.metadata IS 'Flexible provider config: auth method, extra endpoints, quirks.';

CREATE INDEX idx_source_registry_slug ON research.source_registry (slug);
CREATE INDEX idx_source_registry_status ON research.source_registry (status);

-- =============================================================================
-- 2. WORKS — unified scholarly work records
-- =============================================================================
-- Canonical scholarly output. One row per distinct work, deduplicated across
-- providers via identifier equivalence.

CREATE TABLE research.works (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    doi             TEXT UNIQUE,
    pmid            TEXT UNIQUE,
    pmcid           TEXT UNIQUE,
    arxiv_id        TEXT UNIQUE,
    openalex_id     TEXT UNIQUE,
    s2_id           TEXT UNIQUE,
    isbn            TEXT,
    title           TEXT NOT NULL,
    abstract        TEXT,
    year            INTEGER,
    oa_status       TEXT DEFAULT 'unknown'
                    CHECK (oa_status IN ('gold', 'green', 'hybrid', 'bronze', 'closed', 'unknown')),
    oa_url          TEXT,
    license_spdx    TEXT,
    venue_id        UUID REFERENCES research.venues(id),
    work_type       TEXT DEFAULT 'article'
                    CHECK (work_type IN ('article', 'review', 'book', 'chapter',
                                         'conference', 'dataset', 'preprint',
                                         'thesis', 'report', 'other')),
    fulltext_url    TEXT,
    word_count      INTEGER,
    citation_count INTEGER DEFAULT 0,
    first_seen_by   TEXT,
    metadata        JSONB DEFAULT '{}'::jsonb,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at      TIMESTAMPTZ NOT NULL DEFAULT now()
);

COMMENT ON TABLE  research.works IS 'Unified scholarly work record -- deduplicated across providers.';
COMMENT ON COLUMN research.works.doi IS 'Digital Object Identifier. Canonical primary key for scholarly works.';
COMMENT ON COLUMN research.works.oa_status IS 'Open access status per BOAI/Sherpa classification.';
COMMENT ON COLUMN research.works.license_spdx IS 'SPDX license identifier for the work itself, not the provider data.';
COMMENT ON COLUMN research.works.venue_id IS 'FK to venues -- the journal or conference where published.';
COMMENT ON COLUMN research.works.first_seen_by IS 'slug from source_registry that first registered this work.';
COMMENT ON COLUMN research.works.citation_count IS 'Denormalized total. Source-of-truth is count(*) from citation_edges.';

CREATE INDEX idx_works_doi ON research.works (doi) WHERE doi IS NOT NULL;
CREATE INDEX idx_works_pmid ON research.works (pmid) WHERE pmid IS NOT NULL;
CREATE INDEX idx_works_pmcid ON research.works (pmcid) WHERE pmcid IS NOT NULL;
CREATE INDEX idx_works_arxiv ON research.works (arxiv_id) WHERE arxiv_id IS NOT NULL;
CREATE INDEX idx_works_openalex ON research.works (openalex_id) WHERE openalex_id IS NOT NULL;
CREATE INDEX idx_works_s2 ON research.works (s2_id) WHERE s2_id IS NOT NULL;
CREATE INDEX idx_works_isbn ON research.works (isbn) WHERE isbn IS NOT NULL;
CREATE INDEX idx_works_year ON research.works (year);
CREATE INDEX idx_works_oa_status ON research.works (oa_status);
CREATE INDEX idx_works_venue ON research.works (venue_id) WHERE venue_id IS NOT NULL;
CREATE INDEX idx_works_type ON research.works (work_type);
CREATE INDEX idx_works_title_trgm ON research.works USING gin (title gin_trgm_ops);
CREATE INDEX idx_works_abstract_trgm ON research.works USING gin (abstract gin_trgm_ops);
CREATE INDEX idx_works_citation_count ON research.works (citation_count DESC);

-- =============================================================================
-- 3. AUTHORS — disambiguated author records
-- =============================================================================

CREATE TABLE research.authors (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    orcid           TEXT UNIQUE,
    display_name    TEXT NOT NULL,
    given_name      TEXT,
    family_name     TEXT,
    h_index         INTEGER,
    citation_count  BIGINT DEFAULT 0,
    affiliations    JSONB DEFAULT '[]'::jsonb,
    metadata        JSONB DEFAULT '{}'::jsonb,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at      TIMESTAMPTZ NOT NULL DEFAULT now()
);

COMMENT ON TABLE  research.authors IS 'Disambiguated scholarly author records.';
COMMENT ON COLUMN research.authors.orcid IS 'Open Researcher and Contributor ID. NULL if not assigned.';
COMMENT ON COLUMN research.authors.h_index IS 'h-index as reported by the most authoritative provider.';
COMMENT ON COLUMN research.authors.affiliations IS 'JSONB array of affiliation strings. Use author_institutions for structured FK.';

CREATE INDEX idx_authors_orcid ON research.authors (orcid) WHERE orcid IS NOT NULL;
CREATE INDEX idx_authors_name_trgm ON research.authors USING gin (display_name gin_trgm_ops);
CREATE INDEX idx_authors_family ON research.authors (family_name);

-- =============================================================================
-- 4. INSTITUTIONS — institutional records
-- =============================================================================

CREATE TABLE research.institutions (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    ror_id          TEXT UNIQUE,
    display_name    TEXT NOT NULL,
    country_code    TEXT,
    institution_type TEXT
                    CHECK (institution_type IN ('education', 'company', 'government',
                                                'nonprofit', 'healthcare', 'archive',
                                                'other', NULL)),
    aliases         JSONB DEFAULT '[]'::jsonb,
    metadata        JSONB DEFAULT '{}'::jsonb,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at      TIMESTAMPTZ NOT NULL DEFAULT now()
);

COMMENT ON TABLE  research.institutions IS 'Scholarly institutions and organizations.';
COMMENT ON COLUMN research.institutions.ror_id IS 'Research Organization Registry identifier.';
COMMENT ON COLUMN research.institutions.country_code IS 'ISO 3166-1 alpha-2 country code.';

CREATE INDEX idx_institutions_ror ON research.institutions (ror_id) WHERE ror_id IS NOT NULL;
CREATE INDEX idx_institutions_name_trgm ON research.institutions USING gin (display_name gin_trgm_ops);
CREATE INDEX idx_institutions_country ON research.institutions (country_code);

-- =============================================================================
-- 5. VENUES — journals, conferences, proceedings
-- =============================================================================

CREATE TABLE research.venues (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    issn_print      TEXT,
    issn_online     TEXT,
    display_name    TEXT NOT NULL,
    publisher       TEXT,
    venue_type      TEXT DEFAULT 'journal'
                    CHECK (venue_type IN ('journal', 'conference', 'book_series',
                                          'workshop', 'proceedings', 'other')),
    is_oa           BOOLEAN,
    impact_factor   NUMERIC(8,3),
    metadata        JSONB DEFAULT '{}'::jsonb,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at      TIMESTAMPTZ NOT NULL DEFAULT now()
);

COMMENT ON TABLE  research.venues IS 'Scholarly venues -- journals, conferences, proceedings.';
COMMENT ON COLUMN research.venues.issn_print IS 'Print ISSN. Either issn_print or issn_online should be non-null.';
COMMENT ON COLUMN research.venues.impact_factor IS 'Impact Factor or CiteScore. NULL if not available.';

CREATE INDEX idx_venues_issn_print ON research.venues (issn_print) WHERE issn_print IS NOT NULL;
CREATE INDEX idx_venues_issn_online ON research.venues (issn_online) WHERE issn_online IS NOT NULL;
CREATE INDEX idx_venues_name_trgm ON research.venues USING gin (display_name gin_trgm_ops);
CREATE INDEX idx_venues_type ON research.venues (venue_type);

-- =============================================================================
-- 6. FUNDERS — funding agencies and programs
-- =============================================================================

CREATE TABLE research.funders (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    crossref_funder_id TEXT UNIQUE,
    display_name    TEXT NOT NULL,
    country_code    TEXT,
    aliases         JSONB DEFAULT '[]'::jsonb,
    metadata        JSONB DEFAULT '{}'::jsonb,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at      TIMESTAMPTZ NOT NULL DEFAULT now()
);

COMMENT ON TABLE  research.funders IS 'Funding agencies and programs.';
COMMENT ON COLUMN research.funders.crossref_funder_id IS 'Crossref Funder Registry identifier.';

CREATE INDEX idx_funders_crossref ON research.funders (crossref_funder_id) WHERE crossref_funder_id IS NOT NULL;
CREATE INDEX idx_funders_name_trgm ON research.funders USING gin (display_name gin_trgm_ops);

-- =============================================================================
-- JUNCTION TABLES — entity relationships
-- =============================================================================

-- work_authors: many-to-many works <-> authors with positional metadata
CREATE TABLE research.work_authors (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    work_id         UUID NOT NULL REFERENCES research.works(id) ON DELETE CASCADE,
    author_id       UUID NOT NULL REFERENCES research.authors(id) ON DELETE CASCADE,
    author_position INTEGER,
    is_corresponding BOOLEAN DEFAULT false,
    metadata        JSONB DEFAULT '{}'::jsonb,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT now(),
    UNIQUE (work_id, author_id)
);

COMMENT ON TABLE research.work_authors IS 'Many-to-many: works <-> authors with authorship position.';

CREATE INDEX idx_work_authors_work ON research.work_authors (work_id);
CREATE INDEX idx_work_authors_author ON research.work_authors (author_id);
CREATE INDEX idx_work_authors_position ON research.work_authors (work_id, author_position);

-- author_institutions: many-to-many authors <-> institutions with temporal range
CREATE TABLE research.author_institutions (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    author_id       UUID NOT NULL REFERENCES research.authors(id) ON DELETE CASCADE,
    institution_id  UUID NOT NULL REFERENCES research.institutions(id) ON DELETE CASCADE,
    start_year      INTEGER,
    end_year        INTEGER,
    metadata        JSONB DEFAULT '{}'::jsonb,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT now(),
    UNIQUE (author_id, institution_id, start_year)
);

COMMENT ON TABLE research.author_institutions IS 'Many-to-many: authors <-> institutions with temporal affiliation range.';

CREATE INDEX idx_author_inst_author ON research.author_institutions (author_id);
CREATE INDEX idx_author_inst_institution ON research.author_institutions (institution_id);

-- work_funders: many-to-many works <-> funders with grant info
CREATE TABLE research.work_funders (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    work_id         UUID NOT NULL REFERENCES research.works(id) ON DELETE CASCADE,
    funder_id       UUID NOT NULL REFERENCES research.funders(id) ON DELETE CASCADE,
    grant_number    TEXT,
    award_amount    NUMERIC(15,2),
    award_currency  TEXT,
    metadata        JSONB DEFAULT '{}'::jsonb,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT now(),
    UNIQUE (work_id, funder_id, grant_number)
);

COMMENT ON TABLE research.work_funders IS 'Many-to-many: works <-> funders with grant/award details.';

CREATE INDEX idx_work_funders_work ON research.work_funders (work_id);
CREATE INDEX idx_work_funders_funder ON research.work_funders (funder_id);

-- source_work_map: which providers have records for which works
CREATE TABLE research.source_work_map (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    source_id       UUID NOT NULL REFERENCES research.source_registry(id) ON DELETE CASCADE,
    work_id         UUID NOT NULL REFERENCES research.works(id) ON DELETE CASCADE,
    provider_work_id TEXT,
    provider_url    TEXT,
    fetched_at      TIMESTAMPTZ,
    metadata        JSONB DEFAULT '{}'::jsonb,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at      TIMESTAMPTZ NOT NULL DEFAULT now(),
    UNIQUE (source_id, work_id)
);

COMMENT ON TABLE research.source_work_map IS 'Tracks which providers have records for each work -- provenance chain.';

CREATE INDEX idx_swmap_source ON research.source_work_map (source_id);
CREATE INDEX idx_swmap_work ON research.source_work_map (work_id);
CREATE INDEX idx_swmap_fetched ON research.source_work_map (fetched_at);

-- =============================================================================
-- 7. CITATION_EDGES — directed citation relationships
-- =============================================================================

CREATE TABLE research.citation_edges (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    citing_work_id  UUID NOT NULL REFERENCES research.works(id) ON DELETE CASCADE,
    cited_work_id   UUID NOT NULL REFERENCES research.works(id) ON DELETE CASCADE,
    context         TEXT,
    citation_type   TEXT DEFAULT 'in_text'
                    CHECK (citation_type IN ('in_text', 'background', 'method',
                                             'comparison', 'result', 'other')),
    source_provider TEXT,
    metadata        JSONB DEFAULT '{}'::jsonb,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT now(),
    UNIQUE (citing_work_id, cited_work_id)
);

COMMENT ON TABLE  research.citation_edges IS 'Directed citation graph between scholarly works.';
COMMENT ON COLUMN research.citation_edges.context IS 'Text snippet where the citation appears.';
COMMENT ON COLUMN research.citation_edges.citation_type IS 'Semantic role of the citation in the citing work.';

CREATE INDEX idx_cite_citing ON research.citation_edges (citing_work_id);
CREATE INDEX idx_cite_cited ON research.citation_edges (cited_work_id);
CREATE INDEX idx_cite_provider ON research.citation_edges (source_provider);

-- =============================================================================
-- 8. EVIDENCE_OBJECTS — immutable evidence snapshots
-- =============================================================================
-- An evidence object is a frozen, verifiable extract from a scholarly work.
-- Content hash ensures immutability; trust_state tracks the evidence lifecycle.

CREATE TABLE research.evidence_objects (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    work_id         UUID NOT NULL REFERENCES research.works(id) ON DELETE RESTRICT,
    source_provider TEXT NOT NULL,
    verbatim_text   TEXT NOT NULL,
    locator         TEXT,
    content_hash    TEXT NOT NULL,
    license_status  TEXT NOT NULL DEFAULT 'unknown'
                    CHECK (license_status IN ('open', 'fair_use', 'licensed',
                                              'restricted', 'unknown', 'expired')),
    version_status  TEXT NOT NULL DEFAULT 'current'
                    CHECK (version_status IN ('current', 'superseded', 'retracted', 'erratum')),
    trust_state     TEXT NOT NULL DEFAULT 'pending'
                    CHECK (trust_state IN ('pending', 'verified', 'challenged',
                                           'retracted', 'superseded')),
    verified_at     TIMESTAMPTZ,
    verified_by     TEXT,
    extraction_method TEXT,
    metadata        JSONB DEFAULT '{}'::jsonb,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at      TIMESTAMPTZ NOT NULL DEFAULT now()
);

COMMENT ON TABLE  research.evidence_objects IS 'Immutable evidence snapshots -- verbatim extracts from scholarly works.';
COMMENT ON COLUMN research.evidence_objects.content_hash IS 'SHA-256 hash for tamper detection. Hash = SHA256(work_id || verbatim_text || locator).';
COMMENT ON COLUMN research.evidence_objects.locator IS 'Precise location within the work: page, section, paragraph, figure.';
COMMENT ON COLUMN research.evidence_objects.trust_state IS 'Lifecycle: pending -> verified (or challenged -> retracted).';

CREATE INDEX idx_evidence_work ON research.evidence_objects (work_id);
CREATE INDEX idx_evidence_provider ON research.evidence_objects (source_provider);
CREATE INDEX idx_evidence_hash ON research.evidence_objects (content_hash);
CREATE INDEX idx_evidence_trust ON research.evidence_objects (trust_state);
CREATE INDEX idx_evidence_license ON research.evidence_objects (license_status);

-- =============================================================================
-- 9. CLAIMS — extracted claims with exact evidence spans
-- =============================================================================

CREATE TABLE research.claims (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    subject         TEXT NOT NULL,
    predicate       TEXT NOT NULL,
    object          TEXT NOT NULL,
    polarity        TEXT NOT NULL DEFAULT 'affirmative'
                    CHECK (polarity IN ('affirmative', 'negative', 'conditional', 'uncertain')),
    scope           TEXT DEFAULT 'general'
                    CHECK (scope IN ('general', 'study_specific', 'population',
                                     'temporal_bounded', 'method_bounded')),
    method          TEXT,
    confidence      NUMERIC(5,4)
                    CHECK (confidence >= 0 AND confidence <= 1),
    claim_state     TEXT NOT NULL DEFAULT 'proposed'
                    CHECK (claim_state IN ('proposed', 'supported', 'contested',
                                           'refuted', 'withdrawn', 'superseded')),
    superseded_by   UUID REFERENCES research.claims(id),
    evidence_id     UUID REFERENCES research.evidence_objects(id) ON DELETE SET NULL,
    claim_text      TEXT,
    numeric_value   NUMERIC,
    numeric_unit    TEXT,
    extracted_by    TEXT,
    extraction_model TEXT,
    metadata        JSONB DEFAULT '{}'::jsonb,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at      TIMESTAMPTZ NOT NULL DEFAULT now()
);

COMMENT ON TABLE  research.claims IS 'Extracted claims from scholarly evidence -- reified triples with epistemic metadata.';
COMMENT ON COLUMN research.claims.subject IS 'Subject of the claim triple. E.g. porosity or basin X.';
COMMENT ON COLUMN research.claims.predicate IS 'Predicate: e.g. increases_with, measured_as, located_in.';
COMMENT ON COLUMN research.claims.object IS 'Object of the claim triple. E.g. depth or sandstone.';
COMMENT ON COLUMN research.claims.polarity IS 'Whether the claim affirms or negates the relationship.';
COMMENT ON COLUMN research.claims.scope IS 'Population or domain the claim applies to.';
COMMENT ON COLUMN research.claims.numeric_value IS 'Numeric result when the claim quantifies something.';
COMMENT ON COLUMN research.claims.superseded_by IS 'FK to the claim that replaced this one (temporal chain).';

CREATE INDEX idx_claims_evidence ON research.claims (evidence_id) WHERE evidence_id IS NOT NULL;
CREATE INDEX idx_claims_state ON research.claims (claim_state);
CREATE INDEX idx_claims_polarity ON research.claims (polarity);
CREATE INDEX idx_claims_confidence ON research.claims (confidence DESC);
CREATE INDEX idx_claims_subject_trgm ON research.claims USING gin (subject gin_trgm_ops);
CREATE INDEX idx_claims_pred_trgm ON research.claims USING gin (predicate gin_trgm_ops);

-- =============================================================================
-- 10. CLAIM_RELATIONS — typed relations between claims
-- =============================================================================

CREATE TABLE research.claim_relations (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    source_claim_id UUID NOT NULL REFERENCES research.claims(id) ON DELETE CASCADE,
    target_claim_id UUID NOT NULL REFERENCES research.claims(id) ON DELETE CASCADE,
    relation_type   TEXT NOT NULL
                    CHECK (relation_type IN (
                        'SUPPORTS',
                        'CONTRADICTS',
                        'QUALIFIES',
                        'SCOPE_DIVERGES',
                        'METHOD_DIVERGES',
                        'TEMPORALLY_SUPERSEDED',
                        'INCOMPARABLE'
                    )),
    confidence      NUMERIC(5,4)
                    CHECK (confidence >= 0 AND confidence <= 1),
    evidence_id     UUID REFERENCES research.evidence_objects(id) ON DELETE SET NULL,
    notes           TEXT,
    metadata        JSONB DEFAULT '{}'::jsonb,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT now(),
    UNIQUE (source_claim_id, target_claim_id, relation_type)
);

COMMENT ON TABLE  research.claim_relations IS 'Typed directed relations between claims -- the claim dependency graph.';
COMMENT ON COLUMN research.claim_relations.relation_type IS 'Epistemic relation type from the 7-value controlled vocabulary.';
COMMENT ON COLUMN research.claim_relations.confidence IS 'Confidence in the relation itself (not the claims).';

CREATE INDEX idx_crel_source ON research.claim_relations (source_claim_id);
CREATE INDEX idx_crel_target ON research.claim_relations (target_claim_id);
CREATE INDEX idx_crel_type ON research.claim_relations (relation_type);

-- =============================================================================
-- 11. SEARCH_PROTOCOLS — research question definitions
-- =============================================================================

CREATE TABLE research.search_protocols (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    question        TEXT NOT NULL,
    description     TEXT,
    inclusion_criteria TEXT NOT NULL,
    exclusion_criteria TEXT NOT NULL DEFAULT '',
    protocol_state  TEXT NOT NULL DEFAULT 'draft'
                    CHECK (protocol_state IN ('draft', 'active', 'frozen', 'retired')),
    version         INTEGER NOT NULL DEFAULT 1,
    max_results_per_provider INTEGER DEFAULT 100,
    time_bounds     JSONB DEFAULT '{}'::jsonb,
    language_filter JSONB DEFAULT '["en"]'::jsonb,
    authored_by     TEXT,
    metadata        JSONB DEFAULT '{}'::jsonb,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at      TIMESTAMPTZ NOT NULL DEFAULT now()
);

COMMENT ON TABLE  research.search_protocols IS 'Reproducible research question definitions with inclusion/exclusion criteria.';
COMMENT ON COLUMN research.search_protocols.question IS 'The research question in natural language.';
COMMENT ON COLUMN research.search_protocols.protocol_state IS 'Lifecycle: draft -> active -> frozen -> retired.';
COMMENT ON COLUMN research.search_protocols.time_bounds IS 'JSONB: {start_year: N, end_year: N} for temporal filtering.';

CREATE INDEX idx_proto_state ON research.search_protocols (protocol_state);
CREATE INDEX idx_proto_question_trgm ON research.search_protocols USING gin (question gin_trgm_ops);

-- =============================================================================
-- 12. CORPUS_VERSIONS — versioned corpus manifests
-- =============================================================================

CREATE TABLE research.corpus_versions (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    protocol_id     UUID NOT NULL REFERENCES research.search_protocols(id) ON DELETE RESTRICT,
    query_hash      TEXT NOT NULL,
    provider_results JSONB NOT NULL DEFAULT '{}'::jsonb,
    total_records   INTEGER NOT NULL DEFAULT 0,
    dedup_log       JSONB DEFAULT '[]'::jsonb,
    dedup_strategy  TEXT DEFAULT 'doi-first',
    work_ids        UUID[] NOT NULL DEFAULT '{}',
    corpus_state    TEXT NOT NULL DEFAULT 'building'
                    CHECK (corpus_state IN ('building', 'frozen', 'expired', 'superseded')),
    built_by        TEXT,
    metadata        JSONB DEFAULT '{}'::jsonb,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at      TIMESTAMPTZ NOT NULL DEFAULT now()
);

COMMENT ON TABLE  research.corpus_versions IS 'Versioned corpus manifests -- immutable snapshots of a search result.';
COMMENT ON COLUMN research.corpus_versions.query_hash IS 'SHA-256 of normalized query + parameters for reproducibility.';
COMMENT ON COLUMN research.corpus_versions.provider_results IS 'Per-provider record counts as JSONB.';
COMMENT ON COLUMN research.corpus_versions.dedup_log IS 'Array of dedup decisions: which records were merged.';
COMMENT ON COLUMN research.corpus_versions.work_ids IS 'Final deduplicated array of work UUIDs.';

CREATE INDEX idx_corpus_protocol ON research.corpus_versions (protocol_id);
CREATE INDEX idx_corpus_state ON research.corpus_versions (corpus_state);
CREATE INDEX idx_corpus_hash ON research.corpus_versions (query_hash);
CREATE INDEX idx_corpus_works ON research.corpus_versions USING gin (work_ids);

-- =============================================================================
-- 13. REVIEW_PACKETS — literature review artifacts
-- =============================================================================

CREATE TABLE research.review_packets (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    protocol_id     UUID NOT NULL REFERENCES research.search_protocols(id) ON DELETE RESTRICT,
    corpus_id       UUID NOT NULL REFERENCES research.corpus_versions(id) ON DELETE RESTRICT,
    title           TEXT NOT NULL,
    synthesis       TEXT NOT NULL,
    contradictions  JSONB DEFAULT '[]'::jsonb,
    witness_report  TEXT,
    evidence_count  INTEGER NOT NULL DEFAULT 0,
    claim_count     INTEGER NOT NULL DEFAULT 0,
    contradiction_count INTEGER NOT NULL DEFAULT 0,
    coverage_score  NUMERIC(5,4),
    review_state    TEXT NOT NULL DEFAULT 'draft'
                    CHECK (review_state IN ('draft', 'in_review', 'sealed',
                                            'contested', 'withdrawn')),
    sealed_at       TIMESTAMPTZ,
    sealed_by       TEXT,
    authored_by     TEXT,
    metadata        JSONB DEFAULT '{}'::jsonb,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at      TIMESTAMPTZ NOT NULL DEFAULT now()
);

COMMENT ON TABLE  research.review_packets IS 'Literature review deliverables -- structured synthesis with witness reports.';
COMMENT ON COLUMN research.review_packets.contradictions IS 'Array of contradiction objects between claims in the review.';
COMMENT ON COLUMN research.review_packets.witness_report IS 'Independent verification: was the review methodology sound?';
COMMENT ON COLUMN research.review_packets.sealed_at IS 'Timestamp when the review was sealed (irreversible commitment).';

CREATE INDEX idx_review_protocol ON research.review_packets (protocol_id);
CREATE INDEX idx_review_corpus ON research.review_packets (corpus_id);
CREATE INDEX idx_review_state ON research.review_packets (review_state);

-- =============================================================================
-- 14. REVIEW_EVIDENCE_MAP — many-to-many review <-> evidence
-- =============================================================================

CREATE TABLE research.review_evidence_map (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    review_id       UUID NOT NULL REFERENCES research.review_packets(id) ON DELETE CASCADE,
    evidence_id     UUID NOT NULL REFERENCES research.evidence_objects(id) ON DELETE CASCADE,
    role            TEXT DEFAULT 'supporting'
                    CHECK (role IN ('supporting', 'contradicting', 'contextual',
                                    'methodological', 'excluded')),
    notes           TEXT,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT now(),
    UNIQUE (review_id, evidence_id)
);

COMMENT ON TABLE research.review_evidence_map IS 'Many-to-many: review packets <-> evidence objects with role classification.';

CREATE INDEX idx_rem_review ON research.review_evidence_map (review_id);
CREATE INDEX idx_rem_evidence ON research.review_evidence_map (evidence_id);
CREATE INDEX idx_rem_role ON research.review_evidence_map (role);

-- =============================================================================
-- 15. REVIEW_CLAIM_MAP — many-to-many review <-> claims
-- =============================================================================

CREATE TABLE research.review_claim_map (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    review_id       UUID NOT NULL REFERENCES research.review_packets(id) ON DELETE CASCADE,
    claim_id        UUID NOT NULL REFERENCES research.claims(id) ON DELETE CASCADE,
    role            TEXT DEFAULT 'included'
                    CHECK (role IN ('included', 'excluded', 'primary', 'secondary',
                                    'contradicted')),
    inclusion_reason TEXT,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT now(),
    UNIQUE (review_id, claim_id)
);

COMMENT ON TABLE research.review_claim_map IS 'Many-to-many: review packets <-> claims with inclusion rationale.';

CREATE INDEX idx_rcm_review ON research.review_claim_map (review_id);
CREATE INDEX idx_rcm_claim ON research.review_claim_map (claim_id);
CREATE INDEX idx_rcm_role ON research.review_claim_map (role);

-- =============================================================================
-- TRIGGER: auto-update updated_at on all tables
-- =============================================================================

CREATE OR REPLACE FUNCTION research.set_updated_at()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = now();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DO $$
DECLARE
    t RECORD;
BEGIN
    FOR t IN
        SELECT table_name
        FROM information_schema.columns
        WHERE table_schema = 'research'
          AND column_name = 'updated_at'
    LOOP
        EXECUTE format(
            'CREATE TRIGGER trg_%s_updated_at BEFORE UPDATE ON research.%I FOR EACH ROW EXECUTE FUNCTION research.set_updated_at()',
            t.table_name, t.table_name
        );
    END LOOP;
END;
$$;

-- =============================================================================
-- SCHEMA SUMMARY
-- =============================================================================
-- 19 tables total in research schema:
--   6 entity tables:      source_registry, works, authors, institutions, venues, funders
--   4 junction tables:    work_authors, author_institutions, work_funders, source_work_map
--   1 graph table:        citation_edges
--   3 evidence/claim:     evidence_objects, claims, claim_relations
--   2 protocol tables:    search_protocols, corpus_versions
--   1 review table:       review_packets
--   2 review map tables:  review_evidence_map, review_claim_map
--   1 trigger function:   set_updated_at (auto-applied to all tables with updated_at)