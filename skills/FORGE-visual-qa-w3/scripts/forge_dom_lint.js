#!/usr/bin/env node
/**
 * forge_dom_lint.js — W₂ Structural/Syntax Witness for forge_visual_qa
 * 
 * Deterministic DOM linter. No model, no guessing, no inference.
 * Pure algorithmic validation of HTML structure against constraints.
 * 
 * Usage:
 *   node forge_dom_lint.js --html '<html>...</html>' --constraints '{"required_elements":["nav","main","footer"],"max_nav_links":5}'
 *   node forge_dom_lint.js --file /path/to/page.html --constraints '{"required_elements":["nav","main","footer"]}'
 * 
 * Output: JSON report to stdout
 * Exit code: 0 = PASS, 1 = HOLD (deviations found), 2 = FAIL (error)
 * 
 * FLOOR: F2 TRUTH — deterministic, reproducible, no inference.
 * WITNESS: W₂ — structural/syntax only. Cannot see pixels. Cannot write W₃.
 */

const fs = require('fs');
const crypto = require('crypto');
const { JSDOM } = require('jsdom');

// ── Argument parsing ──────────────────────────────────────────────────────

function parseArgs() {
  const args = process.argv.slice(2);
  const opts = {};
  for (let i = 0; i < args.length; i++) {
    if (args[i] === '--html' && args[i + 1]) opts.html = args[++i];
    if (args[i] === '--file' && args[i + 1]) opts.file = args[++i];
    if (args[i] === '--constraints' && args[i + 1]) opts.constraints = args[++i];
  }
  if (!opts.html && !opts.file) {
    console.error('Usage: node forge_dom_lint.js --html "<html>..." --constraints "{...}"');
    console.error('       node forge_dom_lint.js --file page.html --constraints "{...}"');
    process.exit(2);
  }
  if (opts.file) {
    opts.html = fs.readFileSync(opts.file, 'utf-8');
  }
  return opts;
}

// ── Constraint defaults ───────────────────────────────────────────────────

const DEFAULT_CONSTRAINTS = {
  max_nav_links: 5,
  min_contrast_ratio: 4.5,
  max_allowed_deviation_score: 0.05,
  required_elements: ['nav', 'main', 'footer'],
  forbidden_elements: [],
  max_status_opacity: 0.5,
  min_hero_font_ratio: 2.0,
};

// ── Deterministic checks ──────────────────────────────────────────────────

function checkRequiredElements(doc, required) {
  const deviations = [];
  for (const tag of required) {
    const el = doc.querySelector(tag);
    if (!el) {
      deviations.push({
        id: `required_${tag}_missing`,
        description: `Required element <${tag}> not found in DOM`,
        severity: 1.0,
        location_hint: `document`,
        source: 'W2_LINTER',
      });
    }
  }
  return deviations;
}

function checkForbiddenElements(doc, forbidden) {
  const deviations = [];
  for (const tag of forbidden) {
    const el = doc.querySelector(tag);
    if (el) {
      deviations.push({
        id: `forbidden_${tag}_present`,
        description: `Forbidden element <${tag}> found in DOM`,
        severity: 0.8,
        location_hint: tag,
        source: 'W2_LINTER',
      });
    }
  }
  return deviations;
}

function checkNavLinks(doc, maxNavLinks) {
  const deviations = [];
  
  // Find navigation containers
  const navElements = doc.querySelectorAll('nav, [role="navigation"], .nav, .navbar, .navigation');
  
  for (const nav of navElements) {
    const links = nav.querySelectorAll('a[href]');
    if (links.length > maxNavLinks) {
      deviations.push({
        id: `nav_links_exceeded`,
        description: `Navigation has ${links.length} links, max allowed: ${maxNavLinks}`,
        severity: Math.min(1.0, (links.length - maxNavLinks) / maxNavLinks),
        location_hint: 'nav',
        source: 'W2_LINTER',
      });
    }
  }
  
  // Also check header if no nav found
  if (navElements.length === 0) {
    const header = doc.querySelector('header');
    if (header) {
      const links = header.querySelectorAll('a[href]');
      if (links.length > maxNavLinks) {
        deviations.push({
          id: `header_links_exceeded`,
          description: `Header has ${links.length} links, max allowed: ${maxNavLinks}`,
          severity: Math.min(1.0, (links.length - maxNavLinks) / maxNavLinks),
          location_hint: 'header',
          source: 'W2_LINTER',
        });
      }
    }
  }
  
  return deviations;
}

function checkHeadingStructure(doc) {
  const deviations = [];
  const headings = doc.querySelectorAll('h1, h2, h3, h4, h5, h6');
  
  if (headings.length === 0) {
    deviations.push({
      id: 'no_headings',
      description: 'No heading elements found — poor semantic structure',
      severity: 0.3,
      location_hint: 'document',
      source: 'W2_LINTER',
    });
  }
  
  // Check for h1 presence
  const h1s = doc.querySelectorAll('h1');
  if (h1s.length === 0) {
    deviations.push({
      id: 'no_h1',
      description: 'No <h1> element found — page lacks primary heading',
      severity: 0.5,
      location_hint: 'document',
      source: 'W2_LINTER',
    });
  }
  
  return deviations;
}

function checkImages(doc) {
  const deviations = [];
  const images = doc.querySelectorAll('img');
  
  for (const img of images) {
    if (!img.getAttribute('alt') && img.getAttribute('alt') !== '') {
      deviations.push({
        id: `img_missing_alt`,
        description: `Image missing alt attribute: ${img.src || 'unknown'}`,
        severity: 0.6,
        location_hint: 'img',
        source: 'W2_LINTER',
      });
    }
  }
  
  return deviations;
}

function checkForms(doc) {
  const deviations = [];
  const inputs = doc.querySelectorAll('input, textarea, select');
  
  for (const input of inputs) {
    const id = input.getAttribute('id');
    const name = input.getAttribute('name');
    const ariaLabel = input.getAttribute('aria-label');
    const placeholder = input.getAttribute('placeholder');
    
    if (!id && !name && !ariaLabel && !placeholder) {
      deviations.push({
        id: `input_no_label`,
        description: `Form input has no id, name, aria-label, or placeholder`,
        severity: 0.4,
        location_hint: 'form',
        source: 'W2_LINTER',
      });
    }
  }
  
  return deviations;
}

// ── Main ──────────────────────────────────────────────────────────────────

function main() {
  const opts = parseArgs();
  const constraints = {
    ...DEFAULT_CONSTRAINTS,
    ...(opts.constraints ? JSON.parse(opts.constraints) : {}),
  };
  
  let doc;
  try {
    const dom = new JSDOM(opts.html);
    doc = dom.window.document;
  } catch (err) {
    const report = {
      verdict: 'FAIL',
      error: `HTML_PARSE_ERROR: ${err.message}`,
      hash: crypto.createHash('sha256').update(opts.html).digest('hex'),
      score: 0,
      deviations: [],
    };
    console.log(JSON.stringify(report, null, 2));
    process.exit(2);
  }
  
  // Run all deterministic checks
  const deviations = [
    ...checkRequiredElements(doc, constraints.required_elements),
    ...checkForbiddenElements(doc, constraints.forbidden_elements),
    ...checkNavLinks(doc, constraints.max_nav_links),
    ...checkHeadingStructure(doc),
    ...checkImages(doc),
    ...checkForms(doc),
  ];
  
  // Compute score
  const maxSeverity = deviations.length > 0
    ? Math.max(...deviations.map(d => d.severity))
    : 0;
  const score = Math.max(0, 1 - maxSeverity);
  
  // Determine verdict
  let verdict = 'PASS';
  if (deviations.length > 0 && maxSeverity >= 0.8) {
    verdict = 'FAIL';
  } else if (deviations.length > 0) {
    verdict = 'HOLD';
  }
  
  // Compute hash of the lint report
  const reportJson = JSON.stringify({ verdict, deviations, score });
  const hash = crypto.createHash('sha256').update(reportJson).digest('hex');
  
  const report = {
    verdict,
    hash,
    score,
    evidence: `required: [${constraints.required_elements.map(t => {
      const el = doc.querySelector(t);
      return `${t}:${el ? 'present' : 'missing'}`;
    ).join(', ')}], nav_links: ${doc.querySelectorAll('nav a[href]').length}, deviations: ${deviations.length}`,
    deviations,
    label: 'DER',
    constraints_checked: Object.keys(constraints).filter(k => constraints[k] !== undefined),
    timestamp: new Date().toISOString(),
  };
  
  console.log(JSON.stringify(report, null, 2));
  
  // Exit code: 0 = PASS, 1 = HOLD, 2 = FAIL
  if (verdict === 'PASS') process.exit(0);
  if (verdict === 'HOLD') process.exit(1);
  process.exit(2);
}

main();
