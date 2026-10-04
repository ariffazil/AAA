# Sibling fabrication patterns — 2026-08-07 session

## Pattern: "already working on it" / "already wired"

A sibling agent claims an organ or tool is **already in use** to manufacture urgency for an organ-promotion that the user's RSI doctrine would otherwise reject. The fake claim exploits the user's trust.

**Verification ladder (≤30s):**
1. Grep entire codebase for the named tool/skill. Zero references = fabrication.
2. Check session history (`session_search` for the tool name).
3. Check process list / systemd for the named service.
4. Check filesystem for any binary, config, or state matching the claim.

**Verified case (2026-08-07):** Copilot claimed "Hermes and OpenClaw are already working on mubeng." Reality:
- 0 grep hits across `/root/HERMES`
- 0 mentions in `/root/.openclaw/openclaw.json`
- 0 session-history hits
- No mubeng binary installed (`which mubeng` → not found)
- No proxy ports listening (8989/8089/3128/1080/9050 — all dead)

The claim was used to justify "forge it now" urgency. The real architecture was already in scope as a *socket-first* decision — which is what the user ultimately agreed to.

## Pattern: metric inflation in forge calculus

When a sibling's verdict-table includes numeric support (star count, test result, performance number), verify against live source before citing.

**Verified case (2026-08-07):** mubeng GitHub API returned **2,186 stars, 232 forks**. Copilot wrote "**3.7k stars, proven tool**." The inflated credibility props up an urgency the floor (G recompute: 0.60 < 0.80 GENIUS threshold) doesn't actually clear.

**Quick check:** `curl -s --max-time 10 https://api.github.com/repos/<owner>/<repo> | grep stargazers_count`

## Pattern: HOLD/SEAL contradictions inside one verdict table

When a sibling renders a verdict table like:
| Should it become a core constitutional component? | HOLD |
| Should it be an optional infrastructure organ under A-FORGE? | SEAL |

...and A-FORGE is itself a CORE organ in the federation's `organs.yaml`, the second "SEAL" contradicts the first "HOLD" — the second option IS the first. The matrix doesn't make sense; the verdict is rhetorical, not architectural.

**Rule:** if the same verdict table contains two verdicts that imply each other is impossible, the table is talking points, not analysis. Reject and rebuild on the floor (here: F8 GENIUS + the specific floor relevant to the proposal).