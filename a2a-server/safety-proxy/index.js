#!/usr/bin/env node
/**
 * safety-proxy/index.js — hermes_safety_proxy Entry Point
 * ========================================================
 * Constitutional middleware for the arifOS federation.
 *
 * Usage:
 *   const { createSafetyProxy, getStats, TIERS } = require('./safety-proxy');
 *   app.use(createSafetyProxy({ dry_run: false }));
 *   app.get('/safety-proxy/stats', (req, res) => res.json(getStats()));
 *
 * DITEMPA BUKAN DIBERI — Forged, Not Given.
 */

'use strict';

const { createSafetyProxy, extractActionMetadata, auditDecision, getStats, stats } = require('./middleware');
const { classifyAction, isReadOnlyMode, TIERS, DENY_PATTERNS, JITU_PATTERNS, FORCE_DENY_PATTERNS, TOOL_TIER_MAP } = require('./policy');
const { createJituToken, validateJituToken, hashPayload, DEFAULT_TTL_SECONDS, SOVEREIGN_TTL_SECONDS } = require('./jitu_token');

module.exports = {
  // Middleware
  createSafetyProxy,

  // Policy engine
  classifyAction,
  isReadOnlyMode,
  TIERS,
  DENY_PATTERNS,
  JITU_PATTERNS,
  FORCE_DENY_PATTERNS,
  TOOL_TIER_MAP,

  // JITU tokens
  createJituToken,
  validateJituToken,
  hashPayload,
  DEFAULT_TTL_SECONDS,
  SOVEREIGN_TTL_SECONDS,

  // Utilities
  extractActionMetadata,
  auditDecision,
  getStats,
  stats,
};
