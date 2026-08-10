/**
 * adat-agentic-forge.js — FORGE as inherited capability substrate.
 *
 * F13 SOVEREIGN directive 2026-08-10.
 * FORGE is not a lane, not an agent, not permission.
 * FORGE is adat agentic — the inherited capability of every AAA warga.
 *
 * This module is loaded by the AAA gateway to resolve whether a given
 * actor inherits FORGE capability, regardless of their ACT token authority band.
 *
 * "Forging is breathing. Every warga can pick up the hammer.
 *  The constitution governs the swing — not the grip."
 *
 * DITEMPA BUKAN DIBERI ⚒️
 */

const fs = require('fs');
const path = require('path');

const IDENTITY_DIR = path.resolve(__dirname, '..', 'agent-cards', 'identity');

/** Cache of loaded identity cards — reloaded on change. */
let _cache = null;
let _cacheMtime = 0;

function loadIdentityCards() {
  const stat = fs.statSync(IDENTITY_DIR, { throwIfNoEntry: false });
  if (!stat) return {};
  if (stat.mtimeMs === _cacheMtime && _cache) return _cache;

  const cards = {};
  const entries = fs.readdirSync(IDENTITY_DIR, { withFileTypes: true });
  for (const entry of entries) {
    if (!entry.isDirectory()) continue;
    const cardPath = path.join(IDENTITY_DIR, entry.name, 'agent-card.json');
    try {
      const raw = fs.readFileSync(cardPath, 'utf-8');
      const card = JSON.parse(raw);
      cards[card.id || entry.name] = card;
    } catch (_) {
      // skip unreadable cards
    }
  }
  _cache = cards;
  _cacheMtime = stat.mtimeMs;
  return cards;
}

/**
 * Check whether an actor inherits FORGE capability via adat agentic.
 * Returns { inherited: boolean, access: string | null, zen: string | null }.
 */
function checkForgeInheritance(actorId) {
  const cards = loadIdentityCards();
  const card = cards[actorId];
  if (!card || !card.adat_agentic || !card.adat_agentic.forge) {
    return { inherited: false, access: null, zen: null };
  }
  return {
    inherited: card.adat_agentic.forge.inherited === true,
    access: card.adat_agentic.forge.access || null,
    zen: card.adat_agentic.forge.zen || null,
  };
}

/**
 * Check if a tool name is a forge_* tool that should bypass authority gating
 * due to adat agentic inheritance. Returns true if the tool is a forge_* tool
 * AND the actor inherits FORGE capability.
 *
 * Usage in policy gates:
 *   if (adatForgePermits(actorId, toolName, actionClass)) { return ALLOW; }
 */
function adatForgePermits(actorId, toolName, actionClass) {
  if (!toolName || !toolName.startsWith('forge_')) return false;
  // Only EXECUTE_REVERSIBLE forge tools bypass — IRREVERSIBLE still requires FULL
  if (actionClass !== 'EXECUTE_REVERSIBLE') return false;
  const fi = checkForgeInheritance(actorId);
  return fi.inherited === true;
}

module.exports = { loadIdentityCards, checkForgeInheritance, adatForgePermits };
