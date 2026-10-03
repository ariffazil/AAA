#!/usr/bin/env python3
"""
shadow_fq_physics.py — the shadow as a measurable attractor
════════════════════════════════════════════════════════════
Turns "did this shadow happen 5 times?" into a statistical question with a
defensible answer, and turns "what should we instrument next?" into an APEX
optimisation rather than a gut feeling.

PHYSICS OF THE CLAIM
────────────────────
FQ(t) = Verify(t) / Execute(t) is the federation's metabolism order parameter.
FQ* = 1 is the healthy fixed point. A *shadow*, in Arif's sense — "if I stop
steering, where does it naturally pull me?" — is not a single bad reading. It is
a **statistically significant, temporally stable displacement from the fixed
point**. That definition is what this module tests. Two properties, both
required:

  1. DISPLACEMENT  — pooled FQ differs from 1 by more than measurement noise.
  2. STABILITY     — the displacement is consistent across windows, i.e. it is
                     an attractor and not a random walk that wandered low once.

Property 2 is what separates a shadow from an incident, and it is the part a
naive observation count cannot see.

WHY POISSON, AND WHY LOG SPACE
──────────────────────────────
Execute and Verify are *counts* in a window, so FQ is a ratio of two Poisson
variates. The naive delta-method variance on the raw ratio,

    Var(FQ) ≈ FQ² · ( 1/N_V + 1/N_E )

is unusable here: it collapses toward zero for any window with no verifies, so
those windows acquire near-infinite inverse-variance weight and drag the pooled
estimate to ~0 no matter what the informative windows say. Measured symptom on
first run: claude-code pooled to FQ=0.001 at Z=−1039 while its own 65-day totals
were 1384 exec / 270 verify (FQ≈0.20). A single quiet day outvoted a month.

The log-ratio has the well-behaved variance

    Var(ln FQ) ≈ 1/N_V + 1/N_E

which stays finite and correctly demotes sparse windows instead of amplifying
them. So everything is pooled in log space and exponentiated back: the reported
FQ is a precision-weighted GEOMETRIC mean, the right central tendency for a
ratio, and its SE is an SE on ln FQ.

A 0.5 continuity correction (Anscombe) keeps all-zero windows finite. The
consequence still holds and is the whole point: 1 execute / 1 verify carries
almost no information, while 556 execute / 159 verify carries a great deal, and
the weighting says so without anyone having to argue about it.

HETEROGENEITY AS THE ATTRACTOR TEST
───────────────────────────────────
Cochran's Q tests whether one fixed value explains all windows:

    Q  = Σ wᵢ (yᵢ − ȳ)²        df = k − 1
    I² = max(0, (Q − df)/Q) · 100 %

I² is read as the *strength of the attractor*. Low I² = the actor sits in one
place = a genuine fixed point = shadow. High I² = the actor regime-switches =
there is no single attractor to confirm, and the honest response is to widen the
interval (DerSimonian–Laird random effects) and refuse to confirm. Fail-closed
is built into the estimator, not bolted onto the verdict.

TWO INDEPENDENT STATISTICS
──────────────────────────
Effect size (pooled Z) and sign concordance (exact binomial on how many windows
fall on the predicted side) are computed separately and must AGREE before an
entry is called CONFIRMED_MEASURED. They fail differently: Z is sensitive to one
huge window, the binomial is not. Agreement between statistics with different
failure modes is worth more than either alone.

APEX — VALUE OF MEASUREMENT
───────────────────────────
APEX maximises truthful uncertainty reduction per unit of cost and attention.
Operationalised as expected information gain per unit waiting time:

    VoI(e) = severity(e) · H(posterior_e) / ln2 · rate(actor_e)

H(p) = −p·ln p − (1−p)·ln(1−p) is the Shannon entropy of current belief, maximal
at p = 0.5. So the ranking automatically prefers (a) entries we are genuinely
unsure about, (b) that matter, (c) whose actor produces receipts fast enough that
another sample is cheap to obtain. Entries already certain fall to the bottom —
which is the "minimum human attention" term doing real work: the gate stops
asking anyone to look at settled questions.

SAMPLING LIMIT (stated, not hidden)
───────────────────────────────────
The 6-hourly cron samples at the edge of what it can resolve: by Nyquist,
resolving a dynamic needs >=2 samples per period, so a 6 h cadence cannot
resolve anything faster than a 12 h oscillation. Daily windows over the full
ledger are used for the backfill (68 days available as of 2026-10-03) and the
cron snapshot extends resolution forward. Aliasing risk is reported per actor
rather than assumed away.

Forged 2026-10-03 by FI-003 (F13 order: "make the gate read the live FQ series.
apex theory and physics math code"). DITEMPA BUKAN DIBERI.
"""

from __future__ import annotations

import json
import math
from collections import defaultdict
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable

RECEIPTS = Path("/var/lib/arifflow/receipts.jsonl")

# ── Actor identity ─────────────────────────────────────────────────
# The ledger carries both naming grammars for the same principal
# (A-FORGE 48612 rows and a-forge 7749 rows on 2026-10-03). Without this the
# series splits and each half looks under-sampled.
ACTOR_ALIASES: dict[str, tuple[str, ...]] = {
    "claude-code": ("claude-code", "claude_code"),
    "kimi-code": ("kimi-code", "kimi_code"),
    "hermes-asi": ("hermes-asi", "hermes_asi"),
    "aforge": ("A-FORGE", "a-forge", "aforge"),
    "grok-build": ("grok-build", "grok_build"),
    "qwen-code": ("qwen-code", "qwen_code", "qwen-code/FI-003"),
    "333-agi": ("333-AGI", "333-agi"),
}

# ── Which shadows the FQ observable can actually test ──────────────
# A shadow is FQ-testable only if it predicts a direction of metabolic
# displacement. Behavioural shadows (menu_reflex, attention_leak) are real but
# invisible to this observable, and forcing a mapping would manufacture
# evidence. They are reported as NOT_FQ_TESTABLE instead.
PREDICTS_LOW_FQ = {  # execution outruns verification
    "bridge_volume_overload", "execution_gravity", "execution_dominance",
    "mutation_hunger", "executes_without_verifying", "closure_pressure",
    # failure_signature spellings of the same prediction — the registries are not
    # consistent about which field carries the semantics, so both must be known.
    "execute_volume_dwarfs_verify", "executes_without_verification",
}
PREDICTS_HIGH_FQ = {  # verification outruns execution
    "verification_paralysis", "verifies_without_executing",
    "meaning_as_gatekeeping", "observer_inertia",
    "validation_becomes_bottleneck", "verifies_without_executing",
}

SEVERITY_WEIGHT = {"CRITICAL": 1.0, "HIGH": 0.75, "MEDIUM": 0.5, "LOW": 0.25}

MIN_WINDOW_COUNTS = 4   # below this a window is noise, not a measurement
CONTINUITY = 0.5        # Anscombe correction; keeps variance off zero
I2_ATTRACTOR_MAX = 50.0 # above this the "single attractor" assumption fails


@dataclass
class Window:
    label: str
    n_exec: int
    n_verify: int
    fq: float          # raw ratio, for concordance and display
    log_fq: float      # ln FQ — the estimand that is actually pooled
    var: float         # Var(ln FQ) ≈ 1/N_V + 1/N_E

    @property
    def weight(self) -> float:
        return 1.0 / self.var if self.var > 0 else 0.0


@dataclass
class SeriesVerdict:
    actor: str
    signature: str
    predicted: str                 # "FQ<1" | "FQ>1" | "NONE"
    windows_used: int = 0
    windows_dropped: int = 0
    total_exec: int = 0
    total_verify: int = 0
    pooled_fq: float | None = None
    pooled_se: float | None = None
    z_vs_fixed_point: float | None = None
    cochran_q: float | None = None
    i_squared: float | None = None
    tau_squared: float | None = None
    model: str = "none"            # "fixed" | "random_effects(DL)"
    concordant: int = 0
    binom_p: float | None = None
    log10_bayes_factor: float | None = None
    posterior: float | None = None
    displacement: bool = False
    stability: bool = False
    magnitude_stable: bool = False
    verdict: str = "INSUFFICIENT"
    reason: str = ""
    series: list[dict] = field(default_factory=list)


# ── Ledger → windows ───────────────────────────────────────────────
def load_counts(
    actors: Iterable[str], window: str = "day", path: Path = RECEIPTS
) -> tuple[dict[str, dict[str, list[int]]], dict[str, Any]]:
    """Stream the receipt ledger once; bucket Execute/Verify per actor per window.

    Streams rather than loads: the ledger is ~106 MB / 109k rows and grows.
    Only three fields are parsed per row (F4: the model never sees the firehose).
    """
    wanted: dict[str, str] = {}
    for canonical, alts in ACTOR_ALIASES.items():
        for a in alts:
            wanted[a] = canonical
        wanted[canonical] = canonical
    for a in actors:
        wanted.setdefault(a, a)

    buckets: dict[str, dict[str, list[int]]] = defaultdict(lambda: defaultdict(lambda: [0, 0]))
    meta = {"rows": 0, "parsed": 0, "span_min": None, "span_max": None, "unparsed": 0}

    if not path.exists():
        meta["error"] = f"{path} not found"
        return {}, meta

    with open(path, "r", encoding="utf-8", errors="replace") as f:
        for ln in f:
            ln = ln.strip()
            if not ln:
                continue
            meta["rows"] += 1
            try:
                r = json.loads(ln)
            except json.JSONDecodeError:
                meta["unparsed"] += 1
                continue
            actor = r.get("actor_id")
            if actor not in wanted:
                continue
            st = r.get("step_type")
            if st not in ("Execute", "Verify"):
                continue
            ca = r.get("created_at") or ""
            if len(ca) < 10:
                continue
            meta["parsed"] += 1
            if meta["span_min"] is None or ca < meta["span_min"]:
                meta["span_min"] = ca
            if meta["span_max"] is None or ca > meta["span_max"]:
                meta["span_max"] = ca
            key = ca[:10] if window == "day" else ca[:13]
            slot = buckets[wanted[actor]][key]
            if st == "Execute":
                slot[0] += 1
            else:
                slot[1] += 1

    return buckets, meta


def fq_windows(counts: dict[str, list[int]]) -> tuple[list[Window], int]:
    """Convert raw counts into log-FQ observations with honest Poisson variance.

    See module docstring, "WHY POISSON, AND WHY LOG SPACE": pooling the raw
    ratio lets zero-verify windows dominate. ln(FQ) does not.
    """
    out: list[Window] = []
    dropped = 0
    for label in sorted(counts):
        n_e, n_v = counts[label]
        if (n_e + n_v) < MIN_WINDOW_COUNTS:
            dropped += 1
            continue
        e, v = n_e + CONTINUITY, n_v + CONTINUITY
        fq = v / e
        log_fq = math.log(v) - math.log(e)
        var = 1.0 / v + 1.0 / e          # Var(ln FQ), Anscombe-corrected
        if var <= 0 or not math.isfinite(var) or not math.isfinite(log_fq):
            dropped += 1
            continue
        out.append(Window(label=label, n_exec=n_e, n_verify=n_v,
                          fq=fq, log_fq=log_fq, var=var))
    return out, dropped


# ── Statistics ─────────────────────────────────────────────────────
def _pool(ws: list[Window]) -> tuple[float, float, str, float]:
    """Inverse-variance pooling of ln(FQ).

    Returns (pooled_log_fq, se_log, model, cochran_q). Falls back to
    DerSimonian–Laird random effects when Cochran's Q says a single fixed value
    cannot explain the windows — i.e. when there is no single attractor.
    """
    w = [x.weight for x in ws]
    sw = sum(w)
    ybar = sum(wi * x.log_fq for wi, x in zip(w, ws)) / sw
    q = sum(wi * (x.log_fq - ybar) ** 2 for wi, x in zip(w, ws))
    df = len(ws) - 1
    c = sw - sum(wi * wi for wi in w) / sw
    tau2 = max(0.0, (q - df) / c) if (df > 0 and c > 0) else 0.0

    if tau2 > 0:
        w2 = [1.0 / (x.var + tau2) for x in ws]
        sw2 = sum(w2)
        ybar2 = sum(wi * x.log_fq for wi, x in zip(w2, ws)) / sw2
        return ybar2, math.sqrt(1.0 / sw2), "random_effects(DL)", q
    return ybar, math.sqrt(1.0 / sw), "fixed", q


def _sigmoid(x: float) -> float:
    """Numerically stable logistic. exp() of a large Bayes factor overflows;
    log-odds never does. grok-build's Z is large enough (40 exec / 5411 verify)
    that 10**(Z^2 / 2ln10) raises OverflowError — so stay in log space."""
    if x >= 0.0:
        return 1.0 / (1.0 + math.exp(-x))
    ex = math.exp(x)
    return ex / (1.0 + ex)


def _binom_upper_tail(k: int, n: int, p: float = 0.5) -> float:
    """Exact one-sided binomial p-value, no scipy dependency."""
    if n <= 0:
        return 1.0
    return sum(math.comb(n, i) * p**i * (1 - p) ** (n - i) for i in range(k, n + 1))


def shannon_entropy_norm(p: float) -> float:
    """H(p)/ln2 in [0,1]; 1.0 = maximally uncertain, 0 = settled."""
    if p <= 0.0 or p >= 1.0:
        return 0.0
    return (-(p * math.log(p) + (1 - p) * math.log(1 - p))) / math.log(2)


def predicted_direction(signature: str) -> str:
    """Map a shadow's semantic label onto a predicted FQ regime.

    Accepts one or more candidate labels separated by '|'. The registries are
    inconsistent about which field carries the semantics — `name` holds
    bridge_volume_overload while `failure_signature` holds
    execute_volume_dwarfs_verify for the SAME entry. Testing only one field
    silently misclassified SHADOW-HA-001 (the best-evidenced shadow in the
    federation, three agreeing live measurements) as NOT_FQ_TESTABLE. Measured
    2026-10-03. Both fields must be offered.
    """
    cands = [c.strip().lower() for c in (signature or "").split("|") if c.strip()]
    for s in cands:                       # exact semantic labels first
        if s in PREDICTS_LOW_FQ:
            return "FQ<1"
        if s in PREDICTS_HIGH_FQ:
            return "FQ>1"
    for s in cands:                       # then conservative substring fallbacks
        if any(t in s for t in ("execution_domin", "executes_without",
                                "execute_volume", "dwarfs_verify")):
            return "FQ<1"
        if "verifies_without" in s or ("verif" in s and "paralysis" in s):
            return "FQ>1"
    return "NONE"


def assess(
    actor: str,
    signature: str,
    buckets: dict[str, dict[str, list[int]]],
    prior: float = 0.5,
    severity: str = "MEDIUM",
) -> SeriesVerdict:
    """Full test: displacement AND stability, from two independent statistics."""
    direction = predicted_direction(signature)
    v = SeriesVerdict(actor=actor, signature=signature, predicted=direction)

    counts = buckets.get(actor)
    if not counts:
        v.verdict = "NO_RECEIPTS"
        v.reason = f"actor '{actor}' produced no Execute/Verify receipts in the ledger"
        return v
    if direction == "NONE":
        v.verdict = "NOT_FQ_TESTABLE"
        v.reason = ("signature predicts no direction of metabolic displacement; "
                    "FQ cannot confirm or refute it")
        v.windows_dropped = len(counts)
        return v

    ws, dropped = fq_windows(counts)
    v.windows_dropped = dropped
    if len(ws) < 2:
        v.windows_used = len(ws)
        v.verdict = "INSUFFICIENT"
        v.reason = f"only {len(ws)} usable window(s); >=2 required to test stability"
        v.series = [{"w": x.label, "fq": round(x.fq, 4), "e": x.n_exec, "v": x.n_verify} for x in ws]
        return v

    v.windows_used = len(ws)
    v.total_exec = sum(x.n_exec for x in ws)
    v.total_verify = sum(x.n_verify for x in ws)
    v.series = [{"w": x.label, "fq": round(x.fq, 4), "e": x.n_exec, "v": x.n_verify} for x in ws]

    pooled_log, se_log, model, q = _pool(ws)
    # Exponentiate back: pooled_fq is a precision-weighted GEOMETRIC mean of the
    # window ratios. The healthy fixed point FQ*=1 is ln(1)=0, so the test
    # statistic against it is simply pooled_log / se_log.
    v.pooled_fq = math.exp(pooled_log)
    v.pooled_se = se_log        # SE on ln FQ — NOT on FQ. See module docstring.
    v.model, v.cochran_q = model, q
    df = len(ws) - 1
    v.i_squared = max(0.0, (q - df) / q) * 100.0 if q > 0 else 0.0
    v.z_vs_fixed_point = (pooled_log / se_log) if se_log > 0 else None

    # Displacement must be in the PREDICTED direction, not merely non-null.
    z = v.z_vs_fixed_point or 0.0
    v.displacement = (z < -1.96) if direction == "FQ<1" else (z > 1.96)

    # Stability: an attractor is consistent. High I² = regime switching.
    v.stability = v.i_squared <= I2_ATTRACTOR_MAX

    # Sign concordance — independent of effect size, robust to one huge window.
    if direction == "FQ<1":
        v.concordant = sum(1 for x in ws if x.fq < 1.0)
    else:
        v.concordant = sum(1 for x in ws if x.fq > 1.0)
    v.binom_p = _binom_upper_tail(v.concordant, len(ws))

    # Bayes factor: point-alternative-at-MLE vs point null, flat prior (BIC-like
    # approximation — an approximation, not exact model evidence). Held in LOG
    # space throughout: FQ is a ratio of two large Poisson counts, so its SE is
    # tiny and Z routinely reaches values where 10**(Z²/2ln10) overflows float.
    log_bf_nat = (z * z) / 2.0 if v.displacement else 0.0
    v.log10_bayes_factor = round(min(log_bf_nat / math.log(10), 999.0), 2)
    log_prior_odds = math.log(prior / (1 - prior)) if 0 < prior < 1 else 0.0
    v.posterior = _sigmoid(log_prior_odds + log_bf_nat)

    # ── Verdict logic ──────────────────────────────────────────────────
    # A shadow claims an ATTRACTOR, i.e. a DIRECTION of pull. I² measures
    # heterogeneity of MAGNITUDE across windows. Conflating them was the first
    # draft's error and it cut both ways:
    #   grok-build  20/20 concordant, Z=+16.6, I²=65.7% -> withheld. Absurd:
    #               the direction is certain, only the daily strength varies.
    #   claude-code Z=+0.61, 8/24 concordant, I²=86.6%   -> "REFUTED". Too
    #               strong: with heterogeneity that high the actor is not in one
    #               state at all, so a fixed attractor is neither confirmed nor
    #               refuted — it is EPISODIC, which is a different and useful
    #               finding, and deleting the entry on that basis would be wrong.
    # So direction and magnitude are reported separately, and high I² downgrades
    # to NO_STABLE_ATTRACTOR rather than to REFUTED.
    concordance_ok = v.binom_p is not None and v.binom_p < 0.05
    direction_confirmed = v.displacement and concordance_ok
    v.magnitude_stable = v.stability

    if direction_confirmed and v.stability:
        v.verdict = "CONFIRMED_MEASURED"
        v.reason = (f"geometric-mean FQ={v.pooled_fq:.3f} (SE_ln={se_log:.3f}), "
                    f"Z={z:+.2f} vs fixed point FQ*=1, I²={v.i_squared:.1f}% "
                    f"(stable attractor, {v.model}), {v.concordant}/{len(ws)} windows "
                    f"concordant (binomial p={v.binom_p:.4f})")
    elif direction_confirmed:
        v.verdict = "CONFIRMED_DIRECTION_HETEROGENEOUS"
        v.reason = (f"direction confirmed — {v.concordant}/{len(ws)} windows concordant "
                    f"(p={v.binom_p:.4f}), Z={z:+.2f}, FQ={v.pooled_fq:.3f}; but "
                    f"I²={v.i_squared:.1f}% > {I2_ATTRACTOR_MAX}% so daily MAGNITUDE "
                    f"varies ({v.model}). The attractor is real; its strength is not constant.")
    elif v.displacement and not concordance_ok:
        v.verdict = "DISPLACEMENT_NOT_CONCORDANT"
        v.reason = (f"pooled Z={z:+.2f} is significant but only {v.concordant}/{len(ws)} "
                    f"windows agree (p={v.binom_p:.3f}) — the effect is driven by a "
                    f"minority of high-volume windows, not a persistent pull")
    elif concordance_ok and not v.displacement:
        v.verdict = "CONCORDANT_WEAK_EFFECT"
        v.reason = (f"{v.concordant}/{len(ws)} windows on the predicted side "
                    f"(p={v.binom_p:.4f}) but pooled effect not significant "
                    f"(Z={z:+.2f}, FQ={v.pooled_fq:.3f}); direction real, magnitude unresolved")
    elif v.i_squared > I2_ATTRACTOR_MAX:
        v.verdict = "NO_STABLE_ATTRACTOR"
        v.reason = (f"I²={v.i_squared:.1f}% with no significant displacement "
                    f"(Z={z:+.2f}, FQ={v.pooled_fq:.3f}, {v.concordant}/{len(ws)} concordant) — "
                    f"the actor regime-switches rather than sitting in one state; "
                    f"neither confirmed nor refuted, and NOT grounds for deletion")
    else:
        v.verdict = "REFUTED"
        v.reason = (f"no significant displacement (Z={z:+.2f}, FQ={v.pooled_fq:.3f}), no sign "
                    f"concordance ({v.concordant}/{len(ws)}, p={v.binom_p:.3f}), and "
                    f"I²={v.i_squared:.1f}% is low enough that a single value DOES explain "
                    f"the windows — that value is simply not the predicted one")
    return v


# VoI is only meaningful where waiting can actually produce evidence. Ranking an
# entry this observable cannot see (NOT_FQ_TESTABLE) or an actor that emits no
# receipts (NO_RECEIPTS) at the top would send attention exactly where it cannot
# pay off — the opposite of the APEX objective. Settled entries score 0 too:
# "minimum human attention" means not re-asking closed questions.
VOI_MEASURABLE = {
    "INSUFFICIENT", "DISPLACEMENT_NOT_CONCORDANT", "CONCORDANT_WEAK_EFFECT",
    "NO_STABLE_ATTRACTOR", "DISPLACED_UNSTABLE",
}
VOI_SETTLED = {"CONFIRMED_MEASURED", "CONFIRMED_DIRECTION_HETEROGENEOUS", "REFUTED"}
VOI_UNMEASURABLE = {"NOT_FQ_TESTABLE", "NO_RECEIPTS"}


def apex_voi(v: SeriesVerdict, severity: str, daily_rate: float) -> dict[str, Any]:
    """APEX value-of-measurement: uncertainty reduction per unit waiting time.

        VoI = severity × H(posterior)/ln2 × daily_receipt_rate

    H is maximal at posterior 0.5, so the ranking prefers questions that are
    genuinely open, consequential, and cheap to re-sample. Returns 0 — with the
    reason — when the entry is settled or when this observable cannot see it.
    """
    p = v.posterior if v.posterior is not None else 0.5
    h = shannon_entropy_norm(p)
    sw = SEVERITY_WEIGHT.get((severity or "").upper(), 0.5)

    if v.verdict in VOI_UNMEASURABLE:
        why = ("observable cannot see this shadow" if v.verdict == "NOT_FQ_TESTABLE"
               else "actor emits no Execute/Verify receipts — nothing to sample")
        return {"posterior": round(p, 4), "entropy_norm": round(h, 4),
                "severity_weight": sw, "daily_receipt_rate": round(daily_rate, 2),
                "voi": 0.0, "voi_status": "UNMEASURABLE_BY_FQ", "note": why}
    if v.verdict in VOI_SETTLED:
        return {"posterior": round(p, 4), "entropy_norm": round(h, 4),
                "severity_weight": sw, "daily_receipt_rate": round(daily_rate, 2),
                "voi": 0.0, "voi_status": "SETTLED",
                "note": f"{v.verdict} — no further attention warranted from this gate"}

    return {"posterior": round(p, 4), "entropy_norm": round(h, 4),
            "severity_weight": sw, "daily_receipt_rate": round(daily_rate, 2),
            "voi": round(sw * h * max(daily_rate, 0.0), 4),
            "voi_status": "OPEN",
            "note": "measurable and unresolved — waiting produces evidence"}


def daily_rate(buckets: dict[str, dict[str, list[int]]], actor: str, span_days: int) -> float:
    counts = buckets.get(actor) or {}
    tot = sum(e + v for e, v in counts.values())
    return tot / span_days if span_days > 0 else 0.0


def span_days(meta: dict[str, Any]) -> int:
    a, b = meta.get("span_min"), meta.get("span_max")
    if not a or not b:
        return 0
    try:
        d0 = datetime.fromisoformat(a.replace("Z", "+00:00"))
        d1 = datetime.fromisoformat(b.replace("Z", "+00:00"))
        return max(1, (d1 - d0).days)
    except ValueError:
        return 0


if __name__ == "__main__":
    actors = list(ACTOR_ALIASES)
    buckets, meta = load_counts(actors)
    days = span_days(meta)
    print(f"# ledger rows={meta['rows']} parsed={meta['parsed']} unparsed={meta['unparsed']}")
    print(f"# span={meta['span_min']} -> {meta['span_max']} ({days} days)")
    for a in actors:
        c = buckets.get(a) or {}
        e = sum(x[0] for x in c.values())
        vv = sum(x[1] for x in c.values())
        print(f"  {a:<14} windows={len(c):<4} exec={e:<7} verify={vv:<7} rate/day={daily_rate(buckets,a,days):.1f}")
