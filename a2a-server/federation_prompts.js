#!/usr/bin/env node
/**
 * Federation Orchestration Prompts — AAA Control Plane
 *
 * Three multi-organ workflow prompts. Each pre-resolves cross-organ
 * resource URIs via the federation gateway before returning messages[].
 *
 * DITEMPA BUKAN DIBERI — Orchestration is forged, not given.
 */

'use strict';

const FED_CAPITAL_JUDGE_DESC = 'FEDERATION: WEALTH Capital -> arifOS Judge -> VAULT999 Seal. Routes any capital decision through constitutional judgment. Pre-loads WEALTH tools + arifOS floor status. Use for: investment decisions, allocation judgments, fiscal analysis.';

const FED_EARTH_CAPITAL_DESC = 'FEDERATION: GEOX Earth -> WEALTH Capital -> arifOS Judge. Routes subsurface prospect evaluation through capital computation to constitutional judgment. Pre-loads GEOX + WEALTH tool catalogs. Use for: prospect screening, bid round evaluation, basin economics.';

const FED_READINESS_DESC = 'FEDERATION: WELL Vitality -> Decision Gate. Routes human readiness assessment through constitutional decision context. Pre-loads WELL state. Use for: any task where operator fatigue matters, T3+ action gates.';

function getFederationPrompts(gateway) {
  return [
    {
      name: 'federation_capital_judge',
      description: FED_CAPITAL_JUDGE_DESC,
      args: [
        { name: 'query', description: 'The capital question or decision being evaluated', required: true },
        { name: 'capital_context', description: 'Financial context: numbers, scenarios, constraints', required: false },
        { name: 'blast_radius', description: 'LOW / MEDIUM / HIGH / CRITICAL', required: false },
        { name: 'reversibility', description: 'FULL / PARTIAL / NONE', required: false },
      ],
      async handler(params) {
        const query = params.query || '';
        const capital_context = params.capital_context || '';
        const blast_radius = params.blast_radius || 'MEDIUM';
        const reversibility = params.reversibility || 'PARTIAL';

        const wealthRes = gateway.resolveResource
          ? await gateway.resolveResource('wealth://capabilities')
          : { ok: false };

        var pipelineText = '# Federation: Capital -> Judge Pipeline\n\n';
        pipelineText += '## Capital Query\n' + query + '\n\n';
        pipelineText += '## Context\n' + capital_context + '\n\n';
        pipelineText += '## Pipeline (5 steps)\n\n';
        pipelineText += '**STEP 1 — WEALTH Reality Intake**\n';
        pipelineText += 'Use /prompt wealth_reality_intake_loop on WEALTH (:18082)\n\n';
        pipelineText += '**STEP 2 — WEALTH Compute**\n';
        pipelineText += 'wealth_compute_npv / wealth_compute_emv / wealth_compute_irr\n';
        pipelineText += 'ALWAYS compute downside before upside. F2 TRUTH.\n\n';
        pipelineText += '**STEP 3 — WEALTH Handoff**\n';
        pipelineText += 'Use /prompt wealth_arifos_handoff_loop OR wealth_judge_handoff(mode=prepare)\n\n';
        pipelineText += '**STEP 4 — arifOS Judge (:8088)**\n';
        pipelineText += 'arif_judge -> SEAL / SABAR / HOLD / VOID\n\n';
        pipelineText += '**STEP 5 — arifOS Seal (if SEAL)**\n';
        pipelineText += 'arif_seal -> VAULT999 immutable ledger\n\n';
        pipelineText += '## Federation Gateway\n';
        pipelineText += 'POST /federation/pipeline to execute this chain atomically.\n';
        pipelineText += 'GET /federation/status to check organ health.\n\n';
        pipelineText += '## Authority\n';
        pipelineText += 'Blast: ' + blast_radius + ' | Reversible: ' + reversibility + '\n';
        pipelineText += 'WEALTH computes. arifOS judges. Arif decides.';

        var resourceText = wealthRes.ok
          ? JSON.stringify({ tools: wealthRes.content.tool_names.slice(0, 15), count: wealthRes.content.tools })
          : JSON.stringify({ note: 'WEALTH unavailable — probe organ health first' });

        return {
          messages: [
            { role: 'user', content: { type: 'text', text: pipelineText } },
            { role: 'user', content: { type: 'resource', resource: { uri: 'wealth://capabilities', mimeType: 'application/json', text: resourceText } } },
          ],
        };
      },
    },

    {
      name: 'federation_earth_capital',
      description: FED_EARTH_CAPITAL_DESC,
      args: [
        { name: 'prospect_ref', description: 'Prospect name or reference', required: true },
        { name: 'basin', description: 'Basin name for context', required: false },
        { name: 'lat', description: 'Latitude (EPSG:4326)', required: false },
        { name: 'lng', description: 'Longitude (EPSG:4326)', required: false },
      ],
      async handler(params) {
        var prospect_ref = params.prospect_ref || '';
        var basin = params.basin || '';
        var lat = params.lat || '?';
        var lng = params.lng || '?';

        const geoxRes = gateway.resolveResource
          ? await gateway.resolveResource('geox://prospect/catalog')
          : { ok: false };

        var pipelineText = '# Federation: Earth -> Capital Pipeline\n\n';
        pipelineText += '## Prospect\n' + prospect_ref + '\n\n';
        pipelineText += '## Basin\n' + basin + '\n\n';
        pipelineText += '## Location\nlat=' + lat + ', lng=' + lng + '\n\n';
        pipelineText += '## Pipeline (5 steps)\n\n';
        pipelineText += '**STEP 1 — GEOX Basin Context (:8081)**\n';
        pipelineText += 'geox_basin(mode=profile, name=' + basin + ')\n\n';
        pipelineText += '**STEP 2 — GEOX Prospect Evaluation**\n';
        pipelineText += 'geox_prospect(mode=screen, prospect_ref=' + prospect_ref + ')\n\n';
        pipelineText += '**STEP 3 — WEALTH Capital Bridge (:18082)**\n';
        pipelineText += 'geox_wealth_bridge_run -> GEOX->WEALTH handoff\n\n';
        pipelineText += '**STEP 4 — WEALTH Risk + Fiscal**\n';
        pipelineText += '/prompt wealth_risk_downside_loop + wealth_fiscal_breakeven (if Malaysia)\n\n';
        pipelineText += '**STEP 5 — arifOS Judge (:8088)**\n';
        pipelineText += 'Only if POS > 0.25 or EMV > well_cost. Otherwise OBSERVE only.\n\n';
        pipelineText += '## Authority\n';
        pipelineText += 'GEOX computes earth. WEALTH computes capital. arifOS judges. Arif decides.\n';
        pipelineText += 'No drilling without well tie (GEOX Benchmark 001). No capital without SEAL.';

        var resourceText = geoxRes.ok
          ? JSON.stringify({ tools: (geoxRes.content.tool_names || []).slice(0, 15), count: geoxRes.content.tools })
          : JSON.stringify({ note: 'GEOX unavailable — probe organ health first' });

        return {
          messages: [
            { role: 'user', content: { type: 'text', text: pipelineText } },
            { role: 'user', content: { type: 'resource', resource: { uri: 'geox://prospect/catalog', mimeType: 'application/json', text: resourceText } } },
          ],
        };
      },
    },

    {
      name: 'federation_readiness_check',
      description: FED_READINESS_DESC,
      args: [
        { name: 'task_context', description: 'What task is being evaluated for readiness', required: true },
        { name: 'decision_class', description: 'C1-C5 decision threshold (default C3)', required: false },
        { name: 'subject_id', description: 'Subject being observed (default arif)', required: false },
      ],
      async handler(params) {
        var task_context = params.task_context || '';
        var decision_class = params.decision_class || 'C3';
        var subject_id = params.subject_id || 'arif';

        const wellRes = gateway.resolveResource
          ? await gateway.resolveResource('well://state/current')
          : { ok: false };

        var pipelineText = '# Federation: Human Readiness Check\n\n';
        pipelineText += '## Task\n' + task_context + '\n\n';
        pipelineText += '## Decision Class: ' + decision_class + '\n';
        pipelineText += '## Subject: ' + subject_id + '\n\n';
        pipelineText += '## Pipeline (4 steps)\n\n';
        pipelineText += '**STEP 1 — WELL Sense (:18083)**\n';
        pipelineText += 'well_assess_homeostasis(mode=fatigue, decision_class=' + decision_class + ')\n\n';
        pipelineText += '**STEP 2 — WELL Interpret**\n';
        pipelineText += 'well_validate_vitality(mode=readiness, decision_class=' + decision_class + ')\n\n';
        pipelineText += '**STEP 3 — Decision Gate (C-class matrix)**\n';
        pipelineText += 'C1/C2: proceed unless CRITICAL\n';
        pipelineText += 'C3: proceed if STABLE or better\n';
        pipelineText += 'C4: proceed only if OPTIMAL; DEFER if STABLE\n';
        pipelineText += 'C5: proceed only if OPTIMAL + no chronic fatigue\n\n';
        pipelineText += '**STEP 4 — arifOS Context (:8088)**\n';
        pipelineText += 'Pass readiness verdict as evidence to arif_judge for T3+ actions\n\n';
        pipelineText += '## Authority\n';
        pipelineText += 'WELL reflects. The sovereign decides. WELL never blocks, diagnoses, or treats.';

        var resourceText = wellRes.ok
          ? JSON.stringify({ tools: (wellRes.content.tool_names || []).slice(0, 15), count: wellRes.content.tools })
          : JSON.stringify({ note: 'WELL state unavailable — probe organ health first' });

        return {
          messages: [
            { role: 'user', content: { type: 'text', text: pipelineText } },
            { role: 'user', content: { type: 'resource', resource: { uri: 'well://state/current', mimeType: 'application/json', text: resourceText } } },
          ],
        };
      },
    },
  ];
}

function mountFederationPrompts(app, gateway) {
  const prompts = getFederationPrompts(gateway);

  app.get('/federation/prompts', function(req, res) {
    res.json({
      prompts: prompts.map(function(p) {
        return { name: p.name, description: p.description, args: p.args || [] };
      }),
    });
  });

  prompts.forEach(function(prompt) {
    app.post('/federation/prompts/' + prompt.name, async function(req, res) {
      try {
        var result = await prompt.handler(req.body || {});
        res.json({ messages: result.messages });
      } catch (e) {
        res.status(500).json({ error: e.message });
      }
    });

    app.get('/federation/prompts/' + prompt.name, async function(req, res) {
      try {
        var result = await prompt.handler(req.query || {});
        res.json({ messages: result.messages });
      } catch (e) {
        res.status(500).json({ error: e.message });
      }
    });
  });

  console.log('[federation_prompts] Mounted ' + prompts.length + ' prompts: ' + prompts.map(function(p) { return p.name; }).join(', '));
}

module.exports = { getFederationPrompts: getFederationPrompts, mountFederationPrompts: mountFederationPrompts };
