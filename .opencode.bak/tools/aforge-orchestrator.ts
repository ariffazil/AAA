import { tool } from "@opencode-ai/plugin"
import { z } from "zod"

export default tool({
  description: "Run A-FORGE CLI commands in the AAA workspace to deploy/update arifOS organs and surfaces. Wraps whatever A-FORGE CLI exposes (deploy, status, plan, etc.)",
  schema: z.object({
    subcommand: z.string().describe("A-FORGE CLI subcommand: deploy, status, plan, rollback, logs"),
    args: z.array(z.string()).default([]).describe("Additional arguments"),
    cwd: z.string().default("/root/A-FORGE").describe("Working directory for A-FORGE"),
  }),
  async execute({ subcommand, args, cwd }, ctx) {
    const { $ } = await import("bun")

    const cmd = ["npx", "aforge", subcommand, ...args]
    const result = await $`cd ${cwd} && ${cmd}`.nothrow().text()

    return {
      command: cmd.join(" "),
      cwd,
      output: result,
      success: !result.includes("error") && !result.includes("failed")
    }
  }
})