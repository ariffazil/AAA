---
name: cross-host-change-verification
description: "Use when another host claims a fix is deployed."
version: 1.0.0
owner: HERMES
tags: [verification, deployment, cross-host, md5, mtime, claims]
---

# Cross-Host Change Verification

A sibling agent, a cron job, or another operator reports that a fix has landed on a host you do not
own. The report may be entirely honest and still be wrong: it can describe intent, a source file, or
a copy that went to a different path. Your job is to read the **destination** and say what you found.

Never relay a cross-host "done" upward on the strength of the report. The only admissible evidence
is a fact you read on the target host yourself, with the command that produced it.

## Procedure

### 1. Resolve the path the running system actually uses

Read the consumer's configuration; do not assume a path from the source tree.

```bash
python3 -c 'import json;c=json.load(open("<config>"));print(json.dumps(c["<subtree>"], indent=1))'
stat -c %y <config>
```

Normalise the filename before trusting a match. Names that differ by one letter are different
files, and in a repo with an archive directory both usually exist — one live, one retired. Confirm
which one the config spells, then confirm which one is live.

### 2. Read three facts on the destination, in this order

```bash
md5sum   <path>
stat -c %y <path>
wc -c < <path>
```

**mtime is the cheapest disproof.** If the mtime predates the reported change, no write happened at
that path — regardless of any hash quoted in the report. State the timestamp you read.

### 3. Search the tree before concluding "not deployed"

```bash
find <root> -maxdepth 5 -name '<pattern>' -newermt '<reported-time>'
```

Work frequently exists at a different path, under a differently-spelled name, or in a sibling
clone. Report what you searched and what the search covered; "not found" from one narrow `find` is
an absence claim and needs the same warrant as a positive one.

### 4. Read the running process, not the file

A file on disk is a request; it becomes behaviour only after the process re-reads it.

```bash
systemctl show <unit> -p ExecMainStartTimestamp --value
journalctl -u <unit> --since "10 minutes ago" --no-pager | grep -iE 'reload|config change'
```

Do not assert "no hot-reload" from the absence of a restart. Many gateways reload a config subtree
and log it as `[reload] config hot reload applied`. Grep the journal before claiming a restart is
required — and if it is required, say so plainly rather than implying it already happened.

### 5. Invoke the artifact exactly as the runtime would

The runtime spawns the process with a specific argv, cwd and environment. Reproduce all three.

- Build argv from the config entry, not from your idea of the command.
- Apply the `env` block from the same entry — the fix may depend on a variable that only exists there.
- Feed the real protocol frames (for stdio MCP: newline-delimited `initialize`, then `tools/list`,
  then `tools/call`) rather than importing the module and calling a function directly.

Importing functions bypasses the I/O framing that is the usual failure point. A shim that passes a
unit test can still return nothing on stdin.

### 6. Compare against a direct call from the same vantage

Call the upstream service twice from the host under test: once directly, once through the artifact
under scrutiny.

```text
direct -> full payload (diagnosis, counts, data fields)
shim   -> stub carrying only a provenance/meta header, data fields null, isError: false
```

If direct succeeds and the shim returns a stub, the shim is the defect. Do not attribute the empty
result to the daemon. Compare **byte counts** as well as status codes.

### 7. Report what you read, not what you were told

Every line of the receipt carries its own warrant:

```text
path    : <absolute path you read>
md5     : <hash you computed>
mtime   : <timestamp you read>
command : <the exact invocation>
result  : <what came back>
```

If a claimed hash does not match, quote both numbers and say which file each came from. Do not soften
the gap into "provisionally deployed".

### 8. Keep the ownership split explicit

When another operator owns the host, name which steps are theirs and which are yours. Never perform
cross-host writes without an explicit grant. When granted, do the write, re-read the hash, and hand
back the number — an offer to help is not a substitute for the receipt.

## Pitfalls

- **A hash quoted as proof of equality must be read from the destination after the write.** A
  source-file hash proves what was copied, not that the copy landed.
- **An edit changes the hash.** "Same md5 on both sides" and "I then added two lines" cannot both be
  true of the final file. One of the two statements is about a different file than you think.
- **A script can sit at the configured path and still be the superseded version.** Existence is not
  currency; check which variant the active config expects and which one the tree considers live.
- **A tests-passed claim is not evidence about the file you can see.** Ask which path it ran against
  and re-run it yourself against that path.
- **Do not let repeated identical reports wear you down into agreement.** If the same change is
  reported three times and the hash has not moved, the fourth check will not move it either. Say what
  you found, offer the exact remaining action, and stop — continuing produces ceremony, not evidence.
- **Do not convert a cross-host gap into a silent success.** If you cannot read the destination, say
  `UNVERIFIED` with the reason, not `deployed`.

## What this skill is not

It does not grant authority to mutate another host, and it does not judge the other operator's
honesty. It verifies a filesystem and a running process. Motive is not in scope; the hash is.
