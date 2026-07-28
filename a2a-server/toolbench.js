/**
 * AAA TOOLBENCH ROUTER — Skill-to-A2A Bridge
 * ═══════════════════════════════════════════════
 * 
 * Exposes the 150-skill federation catalog as discoverable,
 * searchable, and hydratable tools via the AAA A2A Gateway.
 * 
 * Modes:
 *   - manifest  → full skill catalog by layer
 *   - search    → intent-based skill discovery
 *   - hydrate   → load full SKILL.md for execution
 * 
 * DITEMPA BUKAN DIBERI — Forged 2026-07-28
 */

const fs = require('fs');
const path = require('path');

const MANIFEST_PATH = path.join(__dirname, '..', 'public', 'toolbench', 'manifest.json');
const SKILLS_ROOT = '/root/.agents/skills';

// ── Load manifest ──────────────────────────────────────────────────────────
function loadManifest() {
  try {
    return JSON.parse(fs.readFileSync(MANIFEST_PATH, 'utf8'));
  } catch (e) {
    return { error: 'MANIFEST_NOT_FOUND', message: e.message };
  }
}

// ── Search skills by intent ────────────────────────────────────────────────
function searchSkills(manifest, intent, layer, maxResults = 5) {
  const results = [];
  const query = (intent || '').toLowerCase();
  
  const searchLayer = (layerName, layerData) => {
    if (layer && layerName !== layer) return;
    
    for (const skill of (layerData.skills || [])) {
      const text = `${skill.id} ${skill.name} ${skill.description || ''} ${(skill.functional_tags || []).join(' ')}`.toLowerCase();
      let score = 0;
      
      // Token-based scoring
      const tokens = query.split(/\s+/).filter(t => t.length > 1);
      for (const token of tokens) {
        if (skill.id.toLowerCase().includes(token)) score += 10;
        if (skill.name.toLowerCase().includes(token)) score += 8;
        if ((skill.description || '').toLowerCase().includes(token)) score += 3;
        if ((skill.functional_tags || []).some(t => t.toLowerCase().includes(token))) score += 5;
        if ((skill.subcategory || '').toLowerCase().includes(token)) score += 6;
      }
      
      if (score > 0) {
        results.push({ ...skill, layer: layerName, score });
      }
    }
  };
  
  for (const [layerName, layerData] of Object.entries(manifest.layers || {})) {
    searchLayer(layerName, layerData);
  }
  
  // Sort by score, deduplicate, limit
  results.sort((a, b) => b.score - a.score);
  
  const seen = new Set();
  const unique = [];
  for (const r of results) {
    if (!seen.has(r.id)) {
      seen.add(r.id);
      unique.push(r);
    }
  }
  
  return unique.slice(0, maxResults);
}

// ── List skills by layer ───────────────────────────────────────────────────
function listLayer(manifest, layer) {
  if (!layer) {
    // Return layer summary
    const summary = {};
    for (const [lname, ldata] of Object.entries(manifest.layers || {})) {
      summary[lname] = {
        count: ldata.count,
        description: ldata.description,
        skillNames: (ldata.skills || []).slice(0, 3).map(s => s.name)
      };
      if (ldata.subcategories) {
        summary[lname].subcategories = {};
        for (const [sc, scd] of Object.entries(ldata.subcategories)) {
          summary[lname].subcategories[sc] = scd.count;
        }
      }
    }
    return { layers: summary, total: manifest.total_skills };
  }
  
  const layerData = manifest.layers[layer];
  if (!layerData) return { error: 'LAYER_NOT_FOUND', available: Object.keys(manifest.layers || {}) };
  
  return {
    layer,
    description: layerData.description,
    count: layerData.count,
    skills: layerData.skills,
    subcategories: layerData.subcategories || null
  };
}

// ── Hydrate a skill (load SKILL.md) ────────────────────────────────────────
function hydrateSkill(skillName) {
  const safeName = path.basename(skillName); // prevent path traversal
  const skillPath = path.join(SKILLS_ROOT, safeName, 'SKILL.md');
  
  try {
    if (!fs.existsSync(skillPath)) {
      return { error: 'SKILL_NOT_FOUND', path: skillPath };
    }
    
    const content = fs.readFileSync(skillPath, 'utf8');
    
    // Parse YAML frontmatter
    const fmMatch = content.match(/^---\n([\s\S]*?)\n---\n([\s\S]*)$/);
    let frontmatter = {};
    let body = content;
    
    if (fmMatch) {
      // Simple YAML parser for name, description, trigger_phrases
      const fmText = fmMatch[1];
      body = fmMatch[2];
      
      for (const line of fmText.split('\n')) {
        const m = line.match(/^(\w[\w-]*):\s*(.*)/);
        if (m) frontmatter[m[1]] = m[2].trim();
      }
    }
    
    return {
      skill: safeName,
      path: skillPath,
      frontmatter,
      body_preview: body.substring(0, 2000),
      body_length: body.length
    };
  } catch (e) {
    return { error: 'HYDRATION_FAILED', message: e.message };
  }
}

// ── Mount routes on Express app ────────────────────────────────────────────
function mountToolbenchRoutes(app, { requireAuth = false, prefix = '' } = {}) {
  const manifest = loadManifest();
  const p = prefix;
  
  app.get(`${p}/toolbench/manifest.json`, (req, res) => { res.json(manifest); });
  app.get(`${p}/toolbench/search`, (req, res) => {
    const { intent, layer, max } = req.query;
    if (!intent) return res.status(400).json({ error: 'intent query parameter required' });
    const results = searchSkills(manifest, intent, layer, parseInt(max) || 5);
    res.json({ query: intent, layer: layer || 'all', results, count: results.length });
  });
  app.get(`${p}/toolbench/list`, (req, res) => {
    const { layer } = req.query;
    res.json(listLayer(manifest, layer));
  });
  app.get(`${p}/toolbench/hydrate/:skillName`, (req, res) => {
    res.json(hydrateSkill(req.params.skillName));
  });
  app.get(`${p}/toolbench/layers`, (req, res) => {
    res.json(listLayer(manifest, null));
  });
  app.get(`${p}/toolbench/health`, (req, res) => {
    const m = loadManifest();
    res.json({ status: 'healthy', manifest_version: m.version || 'unknown', total_skills: m.total_skills || 0, layers: Object.keys(m.layers || {}).length, manifest_path: MANIFEST_PATH });
  });
  
  console.log(`[TOOLBENCH] Mounted 6 routes on ${p}/toolbench/* (${manifest.total_skills || '?'} skills)`);
}

module.exports = { mountToolbenchRoutes, searchSkills, listLayer, hydrateSkill, loadManifest };
