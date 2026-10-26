// Vercel ignoreCommand: exit 0 = SKIP build, exit 1 = BUILD.
// Evidence-bound skipping: a build is skipped ONLY when the changed paths are
// provably irrelevant. Vercel invokes this script with NO argv — changed paths
// come from git diff VERCEL_GIT_PREVIOUS_SHA..VERCEL_GIT_COMMIT_SHA. No
// evidence → build (fail-safe: a silent skip is a dead site).
//
// Fixed 2026-10-26 (two witnessed defects):
//   1. no-argv invocation made relevant([]) === false → exit 0 → skipped
//      EVERY build, including pilot changes.
//   2. the filter matched "cockpit-pilot/" but the real repo path is
//      "cockpit/pilot/" — even with paths, every build would be skipped.
import { fileURLToPath } from "node:url";
import { execFileSync } from "node:child_process";

const RELEVANT_PREFIXES = ["cockpit/pilot/", "cockpit-pilot/", "shared/"];
const RELEVANT_FILES = new Set(["package.json", "package-lock.json", "pnpm-lock.yaml"]);

export function relevant(paths) {
  return paths.some(
    (p) => RELEVANT_FILES.has(p) || RELEVANT_PREFIXES.some((pre) => p.startsWith(pre))
  );
}

export function gitChangedPaths(prev, head) {
  try {
    const out = execFileSync("git", ["diff", "--name-only", `${prev}..${head}`], {
      encoding: "utf8",
      timeout: 15000,
    });
    return out.split("\n").map((s) => s.trim()).filter(Boolean);
  } catch {
    return null; // git unavailable or SHAs unknown — no evidence, not "no changes"
  }
}

export function decide({ argvPaths = [], env = {} }) {
  if (argvPaths.length) {
    return relevant(argvPaths)
      ? { action: "build", reason: "argv-relevant" }
      : { action: "skip", reason: "argv-irrelevant" };
  }
  const prev = env.VERCEL_GIT_PREVIOUS_SHA;
  const head = env.VERCEL_GIT_COMMIT_SHA;
  if (prev && head) {
    const paths = gitChangedPaths(prev, head);
    if (paths === null) return { action: "build", reason: "git-diff-unavailable" };
    return relevant(paths)
      ? { action: "build", reason: "git-diff-relevant" }
      : { action: "skip", reason: "git-diff-irrelevant" };
  }
  // No change evidence at all → never skip.
  return { action: "build", reason: "no-change-evidence" };
}

const invokedDirectly = process.argv[1] && fileURLToPath(import.meta.url) === process.argv[1];
if (invokedDirectly) {
  const d = decide({ argvPaths: process.argv.slice(2), env: process.env });
  console.log(`ignore-build: ${d.action} (${d.reason})`);
  process.exit(d.action === "build" ? 1 : 0);
}
