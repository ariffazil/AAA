import { tool } from "@opencode-ai/plugin"
import { z } from "zod"
import { readdir, readFile } from "fs/promises"
import path from "path"

const GOVERNANCE_PATTERN = /^(arifos|geox|wealth|well|aforge|aaa)-/
const FEDERATION_DIRS = [
  path.join(process.env.HOME || "/root", "AAA"),
  path.join(process.env.HOME || "/root", "A-FORGE"),
  path.join(process.env.HOME || "/root", "GEOX"),
  path.join(process.env.HOME || "/root", "WEALTH"),
  path.join(process.env.HOME || "/root", ".config/opencode/skills"),
]

export default tool({
  description: "Read all skills across the arifOS federation, audit their quality, classify by type (governed/infra/domain), and return structured improvement recommendations. Governed skills require arifOS MCP review before changes.",
  schema: z.object({
    skill_name: z.string().optional().describe("Specific skill to audit, or omit for all"),
    classify_only: z.boolean().default(false).describe("Only classify skills without scoring"),
  }),
  async execute({ skill_name, classify_only }, ctx) {
    const skills: any[] = []

    for (const dir of FEDERATION_DIRS) {
      try {
        const entries = await readdir(dir)
        for (const entry of entries) {
          const skillPath = path.join(dir, entry, "SKILL.md")
          try {
            const content = await readFile(skillPath, "utf8")
            const isGoverned = GOVERNANCE_PATTERN.test(entry)
            const hasDescription = content.includes("description:")
            const descMatch = content.match(/description:\s*(.+?)(\n---|\n[a-z])/s)
            const descLength = descMatch ? descMatch[1].trim().length : 0
            const hasOutputFormat = /output\s*format/i.test(content)
            const hasWarnings = content.includes("888 HOLD") || content.includes("⚠️")
            const hasExamples = content.includes("```bash") || content.includes("```")
            const hasFloorRef = /F\d\d?|floor/i.test(content)
            const lineCount = content.split("\n").length

            if (classify_only) {
              skills.push({ name: entry, path: skillPath, type: isGoverned ? "governed" : "infra" })
              continue
            }

            const descScore = descLength > 200 ? 5 : descLength > 100 ? 4 : descLength > 50 ? 3 : 2
            const contentScore = Math.min(5, (hasExamples ? 2 : 0) + (hasOutputFormat ? 1 : 0) +
                              (lineCount > 50 ? 1 : 0) + (hasWarnings ? 1 : 0))
            const constitutionalScore = hasFloorRef ? 5 : 3

            skills.push({
              name: entry,
              path: skillPath,
              type: isGoverned ? "governed" : "infra",
              descriptionLength: descLength,
              scores: { desc: descScore, content: contentScore, constitutional: constitutionalScore },
              totalScore: descScore + contentScore + constitutionalScore,
              hasOutputFormat,
              hasWarnings,
              hasExamples,
              hasFloorRef,
              lineCount,
              needsImprovement: (descScore + contentScore) < 7,
              currentContent: content
            })
          } catch {}
        }
      } catch {}
    }

    if (skill_name) {
      const filtered = skills.filter(s => s.name === skill_name)
      return {
        audited: filtered.length,
        needsWork: filtered.filter(s => s.needsImprovement).length,
        results: filtered,
        summary: filtered.map(s =>
          `${s.name} [${s.type}]: ${s.totalScore}/15 ${s.needsImprovement ? "⚠️ NEEDS WORK" : "✅"}`
        ).join("\n")
      }
    }

    const governed = skills.filter(s => s.type === "governed")
    const infra = skills.filter(s => s.type === "infra")
    const domain = skills.filter(s => s.type === "domain")

    return {
      total: skills.length,
      governed: governed.length,
      infra: infra.length,
      domain: domain.length,
      needsWork: skills.filter(s => s.needsImprovement).length,
      results: skills.sort((a, b) => (a.totalScore || 0) - (b.totalScore || 0)),
      summary: `Federation Health: ${skills.filter(s => !s.needsImprovement).length}/${skills.length} skills OK\n` +
               `Governed: ${governed.length} | Infra: ${infra.length} | Domain: ${domain.length}\n\n` +
               skills.map(s => `${s.name} [${s.type}]: ${(s.totalScore || 0).toFixed(1)}/15 ${s.needsImprovement ? "⚠️" : "✅"}`).join("\n")
    }
  }
})