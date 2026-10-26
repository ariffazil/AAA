// Vercel ignoreCommand: exit 0 = SKIP build. Unrelated commits must not spend a build.
import { fileURLToPath } from "node:url";

export function relevant(paths) {
  return paths.some((p) => p.startsWith("cockpit-pilot/") || p === "package.json" ||
    p === "package-lock.json" || p === "pnpm-lock.yaml" || p.startsWith("shared/"));
}

const invokedDirectly = process.argv[1] && fileURLToPath(import.meta.url) === process.argv[1];
if (invokedDirectly) {
  const changed = process.argv.slice(2);
  process.exit(relevant(changed) ? 1 : 0);
}
