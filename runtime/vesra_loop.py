"""
vesra_loop.py — Vesra Loop Orchestrator (Phase-1+ skeleton)

Variation → Evaluation → Selection → Retention → [ZEN INVOICE] → Adaptation loop.

DITEMPA BUKAN DIBERI ⚒️
Status: SKELETON — see /root/AAA/canon/GENESIS-062-VESRA-LOOP.md
                                 /root/AAA/canon/GENESIS-063-SUBSTRATE-INTELLIGENCE.md

This module is INTENTIONALLY a pure orchestrator:
- It does NOT call arif_judge directly. It receives verdicts.
- It does NOT call arif_seal directly. It emits cohort records for sealing.
- It does NOT mutate live state. All cohort records are append-only.

The five stages plus ZEN membrane bind to existing canonical primitives:
- V → arif_think(mode=variate)  [TBD Phase-2]
- E → arif_judge(mode=judge) + arif_observe(mode=reality_probe)  [exists]
- S → arif_judge verdict mapping  [exists]
- R → arif_seal + lineage_receipt.LineageReceipt  [exists]
- Z → ZEN reality-invoice (this file)  [scaffold — see §ZEN_INVOICE below]
- A → arif_think(mode=metabolize) + scar ingestion  [exists]

The PURPOSE of this skeleton is to give the closed-loop topology a single,
auditable surface. Each method's TODO comment names the canonical primitive
it will bind to in the next phase.

=== ZEN_INVOICE ===
ZEN is the MEMBRANE between Selection (S) and Adaptation (A). It asks:
"Did reality accept the selection?" Default invoice = OPEN.

States: PAID | OPEN | VOID | DOUBTFUL
Default: OPEN. Never assume reality agrees until proven.

Without ZEN, the loop runs V→E→S→R→A but never bills reality. Adaptation
commits before the invoice arrives — a fossilization risk. ZEN closes that.
"""

from __future__ import annotations

import json
import time
from dataclasses import dataclass, field, asdict
from pathlib import Path
from typing import Any

# ─── Constants (canonical SOT) ───────────────────────────────────────────────

VESRA_VERSION = "0.2.0-skeleton-zen"
COHORT_TRACKER_PATH = Path("/root/.local/share/arifos/cohorts.jsonl")
VESRA_CANON_PATH = Path("/root/AAA/canon/GENESIS-062-VESRA-LOOP.md")
SUBSTRATE_CANON_PATH = Path("/root/AAA/canon/GENESIS-063-SUBSTRATE-INTELLIGENCE.md")
ZEN_INVOICE_LOG_PATH = Path("/root/.local/share/arifos/zen_invoices.jsonl")

# Fitness thresholds — bound to GENESIS-062 §4 (F8 GENIUS, F3 TRI-WITNESS)
G_FLOOR = 0.80  # F8 — variant must clear this to enter next generation
W3_FLOOR = 0.70  # F3 — cohort survival requires W³ ≥ 0.7 (Phase 5)
REALITY_PROBE_MIN = 1  # at least one reality probe per variant (Phase 5)


# ─── Data structures ────────────────────────────────────────────────────────


@dataclass
class Variant:
    """A single candidate in the cohort."""

    variant_id: str
    parent_variant_id: str | None
    strategy: str
    payload: dict[str, Any]
    created_at: str = field(default_factory=lambda: time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()))


@dataclass
class Evaluation:
    """Fitness signal for one variant. Bound to JudgeSealContract + W³ + reality probes."""

    variant_id: str
    g_score: float  # F8 — constitutional genius score
    w3_score: float  # F3 — tri-witness (Human × AI × Earth)
    reality_probe_count: int
    scar_pressure: float  # accumulated scar weight from past failures
    judge_verdict: str  # SEAL | HOLD | VOID
    epistemic_label: str  # OBS | DER | INT | SPEC
    notes: str = ""


@dataclass
class Selection:
    """Which variants survive, which archive. The judge verdict IS the selection."""

    cohort_id: str
    survivors: list[str]  # variant_ids
    archived: list[str]
    retire_reasons: dict[str, str]
    selection_criteria: str = "G×W³×reality, F8+F3+F5 floors"


@dataclass
class Retention:
    """VAULT999-bound lineage of one cycle."""

    cohort_id: str
    seal_ids: list[str]
    parent_seal_ids: list[str]
    generation: int
    fitness_score: float  # cohort-level median
    fitness_delta: float  # change from previous generation
    delta_s: float  # entropy impact (F4)


@dataclass
class ZenInvoice:
    """
    Reality-invoice emitted by ZEN membrane after Retention, before Adaptation.

    State semantics (canonical — GENESIS/063 §4):
    - PAID:      reality accepted; selection is load-bearing; decrement exploration budget
    - OPEN:      reality pending; default state; selection conditional; wait 90d, re-invoice
    - VOID:      reality rejected; selection is dead; archive + increment scar_pressure
    - DOUBTFUL:  mixed signal; selection unstable; re-evaluate with new evidence

    Default state: OPEN. Never assume reality agrees until proven.
    """

    invoice_id: str
    cohort_id: str
    selection_ref: str  # which selection this invoices
    state: str = "OPEN"  # PAID | OPEN | VOID | DOUBTFUL
    reality_signal: dict[str, Any] = field(default_factory=dict)
    w3_score: float = 0.0
    evidence_refs: list[str] = field(default_factory=list)
    opened_at: str = field(default_factory=lambda: time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()))
    resolved_at: str | None = None
    notes: str = ""


@dataclass
class Adaptation:
    """Mutations derived from archived failures. These feed next cycle's V."""

    cohort_id: str
    mutation_operators: list[str]
    scar_nudges: list[dict[str, Any]]
    next_exploration_budget: float


@dataclass
class CohortResult:
    """Closed-loop return. One complete V-E-S-R-Z-A cycle (with ZEN membrane)."""

    cohort_id: str
    generation: int
    variants: list[Variant]
    evaluations: list[Evaluation]
    selection: Selection
    retention: Retention
    invoice: ZenInvoice  # ZEN membrane — was missing in v0.1.0
    adaptation: Adaptation
    closed: bool = False  # True only when invoice=PAID and A's mutations become V's input next cycle
    invoice_pending: bool = True  # True until invoice resolves (PAID/VOID/DOUBTFUL→re-evaluate)


# ─── Orchestrator ───────────────────────────────────────────────────────────


class VesraLoop:
    """
    The closed-loop orchestrator.

    Usage:
        loop = VesraLoop(cohort_id="cohort-2026-09-11-AAA-cleanup-v1")
        result = loop.cycle(
            intent={"text": "AAA dirty 73 files → clean main"},
            parent_cohort=None,
            n_variants=5,
            strategy_set=["squash", "atomic", "semantic", "test-first", "risk-first"],
        )
        # → CohortResult, fully traced

    The orchestrator does NOT execute anything itself. It coordinates evidence.
    """

    def __init__(self, cohort_id: str):
        self.cohort_id = cohort_id
        self.generation = 1
        self.lineage: list[str] = []
        self.history: list[CohortResult] = []

    # ── V — Variation ──────────────────────────────────────────────────────
    def variate(
        self,
        parent_variant_id: str | None,
        n: int,
        strategy_set: list[str],
        mutations: list[str] | None = None,
    ) -> list[Variant]:
        """
        Generate N variants from a parent.

        TODO Phase-2: bind to arif_think(mode=variate) + GEPA self-evolution skill.
        For now: skeleton returns N synthetic variants tagged with parent + strategy.
        """
        variants = []
        for i, strategy in enumerate(strategy_set[:n]):
            vid = f"{self.cohort_id}-gen{self.generation}-v{i + 1}-{strategy}"
            variants.append(
                Variant(
                    variant_id=vid,
                    parent_variant_id=parent_variant_id,
                    strategy=strategy,
                    payload={
                        "strategy": strategy,
                        "mutation_operators": mutations or [],
                        "exploration_budget": 1.0 / max(1, n),
                    },
                )
            )
        return variants

    # ── E — Evaluation ─────────────────────────────────────────────────────
    def evaluate(self, variants: list[Variant]) -> list[Evaluation]:
        """
        Measure each variant's fitness.

        TODO Phase-2: bind to arif_judge(mode=judge) + arif_observe(mode=reality_probe).
        For now: skeleton returns a stub evaluation per variant (fitness = 0 by default).
        In Phase-3 pilot, this will receive real judge verdicts + reality probe counts.
        """
        evals = []
        for v in variants:
            evals.append(
                Evaluation(
                    variant_id=v.variant_id,
                    g_score=0.0,  # placeholder; populated by real judge call
                    w3_score=0.0,  # placeholder; populated by real W³
                    reality_probe_count=0,  # placeholder; populated by arif_observe
                    scar_pressure=0.0,
                    judge_verdict="HOLD",  # default conservative
                    epistemic_label="DER",
                    notes="skeleton — awaiting Phase-2 wiring",
                )
            )
        return evals

    # ── S — Selection ──────────────────────────────────────────────────────
    def select(
        self,
        evaluations: list[Evaluation],
        g_floor: float = G_FLOOR,
        w3_floor: float = W3_FLOOR,
    ) -> Selection:
        """
        Promote survivors, archive losers.

        Bound to: arif_judge verdict mapping.
        - SEAL verdict → survive
        - HOLD verdict → observe-90d (treated as survivor for now)
        - VOID verdict → archive immediately
        """
        survivors, archived = [], []
        retire_reasons = {}
        for ev in evaluations:
            if ev.judge_verdict == "VOID":
                archived.append(ev.variant_id)
                retire_reasons[ev.variant_id] = "judge=VOID"
            elif ev.g_score < g_floor and ev.g_score > 0:
                archived.append(ev.variant_id)
                retire_reasons[ev.variant_id] = f"g_score={ev.g_score:.2f} < {g_floor}"
            else:
                survivors.append(ev.variant_id)
        return Selection(
            cohort_id=self.cohort_id,
            survivors=survivors,
            archived=archived,
            retire_reasons=retire_reasons,
        )

    # ── R — Retention ──────────────────────────────────────────────────────
    def retain(self, selection: Selection, fitness_score: float, delta_s: float) -> Retention:
        """
        Emit cohort record for VAULT999 sealing.

        TODO Phase-2: bind to arif_seal(mode=seal) + lineage_receipt.LineageReceipt.
        For now: skeleton appends to cohorts.jsonl (regenerable from log).
        """
        fitness_delta = fitness_score - (self.history[-1].retention.fitness_score if self.history else 0.0)
        retention = Retention(
            cohort_id=self.cohort_id,
            seal_ids=[f"seal-stub-{self.cohort_id}-gen{self.generation}"],  # stub
            parent_seal_ids=self.lineage[-3:] if self.lineage else [],
            generation=self.generation,
            fitness_score=fitness_score,
            fitness_delta=fitness_delta,
            delta_s=delta_s,
        )
        # Append to local cohort tracker (NOT VAULT999 — that needs arif_seal)
        COHORT_TRACKER_PATH.parent.mkdir(parents=True, exist_ok=True)
        with COHORT_TRACKER_PATH.open("a") as f:
            f.write(
                json.dumps(
                    {
                        "ts": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                        "cohort_id": self.cohort_id,
                        "generation": self.generation,
                        "selection": asdict(selection),
                        "retention": asdict(retention),
                    }
                )
                + "\n"
            )
        return retention

    # ── Z — ZEN Reality-Invoice (membrane) ─────────────────────────────────
    def zen_invoice(
        self,
        retention: Retention,
        w3_score: float = 0.0,
        reality_signal: dict[str, Any] | None = None,
    ) -> ZenInvoice:
        """
        Emit a reality-invoice after Retention, before Adaptation.

        Default state = OPEN. The selection is conditional until reality bills.

        TODO Phase-2: bind to arif_observe(mode=reality_probe) + FRAME observer.
        For now: skeleton returns OPEN invoice with stub W³ score.

        The invoice is appended to ZEN_INVOICE_LOG_PATH (regenerable).
        When W³ ≥ W3_FLOOR and reality_signal is non-empty, transition OPEN→PAID.
        When reality_signal is empty after 90d, OPEN→VOID (selection dies).
        """
        invoice_id = f"inv-{self.cohort_id}-gen{self.generation}"
        inv = ZenInvoice(
            invoice_id=invoice_id,
            cohort_id=self.cohort_id,
            selection_ref=f"selection-gen{self.generation}",
            state="OPEN",
            reality_signal=reality_signal or {},
            w3_score=w3_score,
            evidence_refs=[],
            notes="ZEN membrane — default OPEN; reality-bill pending",
        )
        # State transition logic — only PAID when W³ clears floor and signal present
        if w3_score >= W3_FLOOR and reality_signal:
            inv.state = "PAID"
            inv.resolved_at = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
            inv.notes = "auto-PAID: W³ cleared floor and reality_signal non-empty"
        # Append to ZEN invoice log (regenerable)
        ZEN_INVOICE_LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
        with ZEN_INVOICE_LOG_PATH.open("a") as f:
            f.write(
                json.dumps(
                    {
                        "ts": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                        "vesra_version": VESRA_VERSION,
                        "invoice": asdict(inv),
                    }
                )
                + "\n"
            )
        return inv

    # ── A — Adaptation ─────────────────────────────────────────────────────
    def adapt(self, archived: list[str], scar_pressure: float = 0.0) -> Adaptation:
        """
        Mutate losing strategies, evolve winners.

        TODO Phase-4: bind to arif_think(mode=metabolize) + scar ingestion.
        For now: skeleton returns stub mutation operators derived from archived ids.
        """
        mutations = [f"inverse-of-{vid}" for vid in archived[:3]]
        return Adaptation(
            cohort_id=self.cohort_id,
            mutation_operators=mutations,
            scar_nudges=[{"pressure": scar_pressure, "kind": "stub"}],
            next_exploration_budget=0.5 if scar_pressure < 0.6 else 1.0,
        )

    # ── The closed cycle ───────────────────────────────────────────────────
    def cycle(
        self,
        intent: dict[str, Any],
        parent_cohort: "CohortResult | None" = None,
        n_variants: int = 5,
        strategy_set: list[str] | None = None,
        mutations: list[str] | None = None,
        fitness_score: float = 0.0,
        delta_s: float = 0.0,
        scar_pressure: float = 0.0,
    ) -> CohortResult:
        """
        One closed V-E-S-R-A cycle. The loop is closed only when this returns
        CohortResult.closed=True, which happens when the next cycle's variate()
        consumes this cycle's adapt() output as mutations.
        """
        strategy_set = strategy_set or [f"strategy-{i}" for i in range(n_variants)]
        parent_variant = parent_cohort.variants[0].variant_id if parent_cohort else None

        # V
        variants = self.variate(parent_variant, n_variants, strategy_set, mutations)
        # E
        evaluations = self.evaluate(variants)
        # S
        selection = self.select(evaluations)
        # R
        retention = self.retain(selection, fitness_score, delta_s)
        # Z — ZEN membrane: invoice reality before committing adaptation
        invoice = self.zen_invoice(retention, w3_score=0.0, reality_signal=None)
        # A — only commit adaptation if invoice is PAID or OPEN-with-pressure
        adaptation = self.adapt(selection.archived, scar_pressure)

        # Closure is true ONLY when invoice is PAID. OPEN means loop pauses.
        closed = invoice.state == "PAID"

        result = CohortResult(
            cohort_id=self.cohort_id,
            generation=self.generation,
            variants=variants,
            evaluations=evaluations,
            selection=selection,
            retention=retention,
            invoice=invoice,
            adaptation=adaptation,
            closed=closed,
            invoice_pending=(invoice.state == "OPEN"),
        )

        self.history.append(result)
        self.lineage.extend(retention.seal_ids)
        self.generation += 1
        return result

    # ── Cohort fitness aggregator ──────────────────────────────────────────
    def cohort_fitness(self, evaluations: list[Evaluation]) -> dict[str, float]:
        """Aggregate G + W³ + reality into a single cohort fitness score."""
        if not evaluations:
            return {"median_g": 0.0, "median_w3": 0.0, "reality_avg": 0.0, "fitness": 0.0}
        gs = sorted([e.g_score for e in evaluations])
        w3s = sorted([e.w3_score for e in evaluations])
        reals = [e.reality_probe_count for e in evaluations]
        med_g = gs[len(gs) // 2]
        med_w3 = w3s[len(w3s) // 2]
        avg_real = sum(reals) / len(reals)
        # Fitness = geometric mean × reality-saturation
        fitness = (med_g * med_w3) ** 0.5 * min(1.0, avg_real / REALITY_PROBE_MIN)
        return {"median_g": med_g, "median_w3": med_w3, "reality_avg": avg_real, "fitness": fitness}


# ─── Convenience: smoke test ────────────────────────────────────────────────

if __name__ == "__main__":
    print(f"VesraLoop skeleton v{VESRA_VERSION}")
    print(f"Canon: {VESRA_CANON_PATH}")
    print(f"Substrate: {SUBSTRATE_CANON_PATH}")
    print(f"Cohort tracker: {COHORT_TRACKER_PATH}")
    print(f"ZEN invoice log: {ZEN_INVOICE_LOG_PATH}")
    print(f"Floors: G≥{G_FLOOR}, W³≥{W3_FLOOR}, reality_probes≥{REALITY_PROBE_MIN}")
    # Smoke test: closed loop on synthetic data
    loop = VesraLoop(cohort_id="smoke-test-zen-gen0")
    strategies = ["squash", "atomic", "semantic", "test-first", "risk-first"]
    # G1: no reality signal yet → invoice stays OPEN → loop NOT closed
    result_g1 = loop.cycle(
        intent={"text": "smoke test — does the loop close?"},
        n_variants=5,
        strategy_set=strategies,
        fitness_score=0.0,
        delta_s=0.0,
    )
    print(
        f"G1 closed={result_g1.closed} invoice={result_g1.invoice.state} survivors={len(result_g1.selection.survivors)}"
    )
    assert not result_g1.closed, "G1 must NOT close with OPEN invoice (ZEN invariant)"
    assert result_g1.invoice_pending, "G1 invoice must be pending"
    # G2: feed adaptation mutations back into variate + provide reality_signal
    result_g2 = loop.cycle(
        intent={"text": "G2 — using G1 mutations + reality signal"},
        parent_cohort=result_g1,
        n_variants=3,
        strategy_set=["m1", "m2", "m3"],
        mutations=result_g1.adaptation.mutation_operators,
        fitness_score=0.65,
        delta_s=-0.02,
    )
    # Reality signal arrives AFTER G2 cycle — simulate reality acceptance post-hoc
    # This is the real-world pattern: invoice resolves asynchronously
    result_g2.invoice = loop.zen_invoice(
        result_g2.retention,
        w3_score=0.85,
        reality_signal={"earth_observation": "ok", "human_signal": "ok"},
    )
    # Re-derive closed from invoice state (semantic invariant: closed ⟺ PAID)
    result_g2.closed = result_g2.invoice.state == "PAID"
    result_g2.invoice_pending = result_g2.invoice.state == "OPEN"
    print(f"G2 closed={result_g2.closed} invoice={result_g2.invoice.state} lineage_len={len(loop.lineage)}")
    assert result_g2.closed, "G2 must close after PAID invoice"
    print("✓ V-E-S-R-Z-A loop closed across 2 generations (G1 OPEN-pause, G2 PAID-close)")
    print(f"  ZEN invoices logged to: {ZEN_INVOICE_LOG_PATH}")
    print(f"  Cohort records logged to: {COHORT_TRACKER_PATH}")
