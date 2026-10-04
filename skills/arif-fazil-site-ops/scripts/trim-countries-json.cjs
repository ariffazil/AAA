#!/usr/bin/env node
/**
 * trim-countries-json.cjs
 *
 * Fetches the mledoze/world-countries dataset (1.4 MB) and trims it to
 * the fields the SOT Atlas needs (~74 KB). Writes to a target path.
 *
 * Usage:
 *   node trim-countries-json.cjs [output-path]
 *
 * Default output: ./countries-min.json
 * Cache: ./.cache/countries.json (30 days)
 *
 * Why this exists: REST Countries v3.1 is deprecated as of 2026-08-06,
 * v5 requires an API key. Embedding a static, trimmed dataset removes
 * the live dependency and keeps the dossier UI offline-capable.
 */
const fs = require("fs");
const path = require("path");
const https = require("https");

const SRC = "https://cdn.jsdelivr.net/npm/world-countries@5.1.0/countries.json";
const OUT = path.resolve(process.argv[2] || "./countries-min.json");
const CACHE_DIR = path.resolve("./.cache");
const CACHE = path.join(CACHE_DIR, "countries.json");
const CACHE_TTL_MS = 30 * 24 * 60 * 60 * 1000;

function fetch(url) {
  return new Promise((resolve, reject) => {
    const req = https.get(url, { timeout: 30000 }, (res) => {
      if (res.statusCode === 301 || res.statusCode === 302) {
        return fetch(res.headers.location).then(resolve, reject);
      }
      if (res.statusCode !== 200) return reject(new Error(`HTTP ${res.statusCode} for ${url}`));
      let body = "";
      res.on("data", (c) => (body += c));
      res.on("end", () => resolve(body));
    });
    req.on("error", reject);
    req.on("timeout", () => req.destroy(new Error("timeout")));
  });
}

async function main() {
  fs.mkdirSync(CACHE_DIR, { recursive: true });
  let raw;
  const cacheFresh = fs.existsSync(CACHE) && Date.now() - fs.statSync(CACHE).mtimeMs < CACHE_TTL_MS;
  if (cacheFresh) {
    raw = fs.readFileSync(CACHE, "utf8");
    console.log(`[trim] using cache ${CACHE} (${(raw.length / 1024).toFixed(1)} KB)`);
  } else {
    console.log(`[trim] fetching ${SRC} ...`);
    raw = await fetch(SRC);
    fs.writeFileSync(CACHE, raw);
    console.log(`[trim] cached ${CACHE} (${(raw.length / 1024).toFixed(1)} KB)`);
  }

  const full = JSON.parse(raw);
  const MIN = full.map((c) => ({
    cca3: c.cca3,
    cca2: c.cca2,
    name: c.name?.common ?? "",
    official: c.name?.official ?? "",
    capital: Array.isArray(c.capital) ? c.capital[0] : "",
    region: c.region ?? "",
    subregion: c.subregion ?? "",
    population: c.population ?? 0,
    area: c.area ?? 0,
    latlng: c.latlng ?? [0, 0],
    languages: c.languages ? Object.values(c.languages) : [],
    currencies: c.currencies ? Object.keys(c.currencies) : [],
    flag: c.flag ?? "",
    unMember: c.unMember ?? false,
    independent: c.independent ?? false,
  }));

  fs.mkdirSync(path.dirname(OUT), { recursive: true });
  fs.writeFileSync(OUT, JSON.stringify(MIN));
  const outSize = fs.statSync(OUT).size;
  console.log(
    `[trim] wrote ${MIN.length} countries → ${OUT} (${(outSize / 1024).toFixed(1)} KB, ${(
      (outSize / raw.length) *
      100
    ).toFixed(1)}% of original)`
  );
}

main().catch((e) => {
  console.error(`[trim] FAILED: ${e.message}`);
  process.exit(1);
});
