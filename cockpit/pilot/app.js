// Read-only cockpit pilot — one snapshot, honest staleness, no action controls.
export const STALE_AFTER_MS = 120_000;
export const BASE_INTERVAL_MS = 30_000;
export const MAX_INTERVAL_MS = 240_000;

export function ageMs(observedAt, now = Date.now()) {
  const t = Date.parse(observedAt);
  return Number.isFinite(t) ? now - t : Infinity;
}
export function stateOf(observedAt, now = Date.now()) {
  const a = ageMs(observedAt, now);
  if (!Number.isFinite(a) || a < 0) return "unmeasured";
  return a > STALE_AFTER_MS ? "stale" : "fresh";
}
export function nextInterval(failures, base = BASE_INTERVAL_MS, max = MAX_INTERVAL_MS) {
  const f = Math.max(0, Math.min(Number(failures) || 0, 4));
  return Math.min(base * 2 ** f, max);
}
export function shouldPoll({ hidden = false, online = true } = {}) {
  return !hidden && online !== false;
}
export function card(label, field, now = Date.now()) {
  const has = field && Object.prototype.hasOwnProperty.call(field, "value");
  const value = has ? field.value : undefined;
  const observedAt = (field && field.observed_at) || null;
  const state = value === undefined || value === null ? "unmeasured" : stateOf(observedAt, now);
  return { label, value: value === undefined || value === null ? "UNMEASURED" : value,
           observedAt, source: (field && field.source) || "missing", state };
}
if (typeof document !== "undefined") {
  const grid = document.getElementById("grid");
  const banner = document.getElementById("banner");
  let failures = 0, timer = null;
  const paint = (snapshot) => {
    const now = Date.now();
    const cards = (snapshot.cards || []).map((c) => card(c.label, c, now));
    if (grid) grid.innerHTML = cards.map((c) => `
      <article class="card ${c.state}">
        <h3>${c.label}</h3><p class="v">${String(c.value)}</p>
        <p class="m">${c.source} · ${c.observedAt || "tiada timestamp"} · <b>${c.state}</b></p>
      </article>`).join("");
    if (banner) {
      banner.textContent = snapshot.state === "fresh"
        ? `Snapshot ${snapshot.observed_at}`
        : `Keadaan: ${String(snapshot.state).toUpperCase()} — jangan anggap hijau`;
      banner.className = `banner ${snapshot.state}`;
    }
  };
  const poll = async () => {
    if (!shouldPoll({ hidden: document.hidden, online: navigator.onLine })) return;
    try {
      const r = await fetch("/api/status", { cache: "no-store", signal: AbortSignal.timeout(8000) });
      if (!r.ok) throw new Error(`http ${r.status}`);
      paint(await r.json()); failures = 0;
    } catch (e) {
      failures += 1;
      paint({ state: "unavailable", observed_at: null,
              cards: [{ label: "Backend", value: "tidak tersedia", observed_at: null, source: "cockpit /api/status" }] });
    }
    schedule();
  };
  const schedule = () => {
    clearTimeout(timer);
    if (!shouldPoll({ hidden: document.hidden, online: navigator.onLine })) return;
    timer = setTimeout(poll, nextInterval(failures));
  };
  document.addEventListener("visibilitychange", () => { document.hidden ? clearTimeout(timer) : poll(); });
  window.addEventListener("online", schedule);
  poll();
}
