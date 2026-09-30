---
name: model-artifact-integrity
description: "Use when fetching or verifying a model checkpoint."
version: 1.0.0
floors: [F1, F2]
triggers:
  - "download a checkpoint"
  - "model weights"
  - "huggingface checkpoint"
  - "finetune checkpoint"
  - "load a .pt / .safetensors"
  - "is this download complete"
  - "sha256 the model file"
---

# Model Artifact Integrity

Fetching a multi-gigabyte artifact from a vendor is a **trust decision**, and everything about it is
silent when it goes wrong: a corrupted file has the right name, the right size, and loads far enough
to produce plausible garbage. The deliverable is an artifact you have *proven* is the publisher's
bytes, in the shape the loader expects, before anything downstream consumes it.

## Rule 0 — size is not integrity

**A matching byte count proves a transfer finished, not that it transferred the right bytes.** A
`curl -C -` resume against a redirecting CDN can splice a partial download at the wrong offset and
produce a file of *exactly* the expected size with corrupted content. That file will load, and the
model will be blamed for the output.

Always verify against the **publisher's own digest**, never your local expectation of size.

## Procedure

### 1. Get the publisher's truth before the first byte

```bash
# HuggingFace: ?blobs=true exposes the LFS oid (sha256) and size per file
curl -s 'https://huggingface.co/api/models/<org>/<repo>?blobs=true' \
  | python3 -c "import sys,json;d=json.load(sys.stdin);[print(f['rfilename'],f['lfs']['sha256'],f['lfs']['size']) for f in d['siblings']]"

curl -sL 'https://huggingface.co/<org>/<repo>/raw/main/README.md'   # usage + licence + which checkpoint
```

Record the expected digest next to the download. Fetching before you know the target makes every
later check unfalsifiable.

### 2. Fetch with retries, and never resume onto a suspect partial

```bash
curl -L --retry 5 --retry-delay 5 -o <name> "<resolved-url>"
```

- Omit `-C -` unless you are certain the existing partial is the same object (same URL, same
  revision). When a resume is suspected of corruption, **delete and re-fetch from zero** — a wrong
  resume cannot be repaired, only replaced.
- Check the artifact, never a wrapper's exit code. A fetch detached with `nohup ... &` inside a
  script leaves the script exiting 0 while the fetch is dead; a child in the parent's process group
  also dies with it. Confirm with `stat`/`sha256sum` **and** `pgrep` before calling a download done.

### 3. Verify, and stop on mismatch

```bash
sha256sum <file>
```

Mismatch = delete and re-fetch. Do not "try loading it anyway" — a corrupted checkpoint's failure
mode is bad output, not a clean error, and it will be attributed to the model.

### 4. Classify the artifact's shape before loading it

Vendor "checkpoints" are frequently **training** artifacts (weights + optimizer + scheduler) rather
than inference artifacts. Read the top-level structure **without materialising the tensors** — a
torch `.pt` is a zip, so stub the unpickler and read only the key tree:

```python
import io, pickle, zipfile
PATH = "model.pt"; PREFIX = PATH.rsplit("/", 1)[-1][:-3]   # zip entry dir == basename without .pt

class Stub:
    def __init__(self, *a, **k): pass
    def __setitem__(self, k, v): pass

class U(pickle.Unpickler):
    def persistent_load(self, pid): return Stub()
    def find_class(self, module, name):
        if module.startswith("torch"): return Stub
        return super().find_class(module, name)

obj = U(io.BytesIO(zipfile.ZipFile(PATH).read(f"{PREFIX}/data.pkl"))).load()
for k, v in obj.items():
    print(k, type(v).__name__, len(v) if hasattr(v, "__len__") else "-")
```

This costs seconds on a multi-GB file and answers the questions that decide everything downstream:
is there an `ema_model_state_dict`, is it prefixed, is there an optimizer blob you do not need.

### 5. Extract the subset you actually need, memory-mapped

Loading a whole training checkpoint to use one sub-state costs RAM and time for nothing, and can
exceed a session's memory cgroup. `mmap=True` keeps the source file-backed so the extraction peaks
near the *output* size, not the input:

```python
ck = torch.load(PATH, map_location="cpu", weights_only=True, mmap=True)
keep = {k: v for k, v in ck["<sub_state_dict>"].items() if k not in ("initted", "step")}
torch.save({"<sub_state_dict>": keep}, OUT)
```

Measured shape of the win: a 5.4 GB training checkpoint extracted to a **1.35 GB** inference
checkpoint with peak RSS **1.49 GB**, versus a 4.2 GB peak and an OOM kill when loading it whole.
Name the output so its role is obvious (`*_infer_ema.pt`, not a copy of the vendor filename).

### 6. Confirm the tokenizer/vocab by shape, not by filename

A finetune of a base model normally keeps the base tokenizer. Setting a custom vocab "because a
vocab file shipped alongside" invites junk tokens. Confirm from the embedding width instead:

```python
model.<text_embed>.weight.shape     # vocab_size + 1, e.g. (2546, 512) for a 2545-token vocab
```

**Trap:** a `vocab.txt` beside a checkpoint is often the upstream vocab re-saved with CRLF line
endings — same tokens, +1 byte per line (11,255 B vs 13,800 B for identical content). Diff it against
the copy inside the installed package before trusting it; prefer the default.

### 7. Run heavy loads outside the session's memory cgroup

```bash
cg=$(cat /proc/self/cgroup | cut -d: -f3); cat /sys/fs/cgroup${cg}/memory.max
systemd-run --scope --slice=system.slice -p MemoryMax=24G --quiet <command>
```

`free` reports the host, not your ceiling. A killed process leaves no trace in its own log — check
`dmesg -T | grep -iE 'killed process|out of memory'` before blaming the library. Prefer shrinking the
job over raising the cap.

## Pitfalls

- **A "completed" download is a claim about the fetcher, not the file.** Verify the digest yourself;
  an exit code from a detached child describes the wrapper.
- **Do not resume blind.** `-C -` onto a partial whose provenance you cannot vouch for produces a
  right-sized, wrong-content file — the worst outcome, because every cheap check passes.
- **Never report a model as bad before the artifact is verified.** Weight corruption, wrong revision
  and wrong-loading-code all present identically as "the model is worse than advertised".
- **Vendor model-card claims are hypotheses.** Capability statements in a README (emotion, fillers,
  code-switch, benchmark scores) are the publisher's measurement on their data. Reproduce on your own
  reference before repeating them as fact — and judge A/B by changing exactly one variable
  (the checkpoint), keeping reference, reference text and input text fixed.
- **Do not hold a lane behind hardware it does not need.** Before gating work on a GPU rental or a
  paid top-up, check whether the same model already runs on the box you are on; a lane can sit
  "pending" for weeks behind a cost that was never necessary.
- **Keep the original until the derivative is proven.** Delete the multi-GB source only after a
  downstream run has actually consumed the extracted artifact successfully.

## Reporting shape

State: source URL + revision, expected digest, measured digest, byte size, the artifact's shape
(training vs inference, sub-state used), the extraction result, and what was **not** verified. A
loader that returns a tensor does not prove the weights are the publisher's — only the digest does.
