# Vision / OCR endpoint quirks

Only needed when you drive the read endpoints yourself. The failure modes below all present
as "the provider is down" while the provider is fine.

## Request shape

- **Never put base64 stills in `curl` argv.** Three frames exceed `ARG_MAX` and curl dies with
  `OSError [Errno 7] Argument list too long` — which reads exactly like a provider outage.
  Stage the JSON body in a temp file and send `-d @file`.
- **Never impose a length floor on a short question.** A low `max_tokens` makes a
  reasoning-capable vision model return empty `content`; accept any non-empty answer.
- Add a mild `frequency_penalty` (≈0.4) when you ask for verbatim text — it is the real lever
  against a model restating one fact in three formats.

## Reading the response

- **`reasoning_content` may hold the whole answer with `content` empty.** Reasoning-capable
  models do this. Reading only `content` reports a working provider as dead — fall back to
  `reasoning_content`.
- **Discard scratchpad output, do not mine it.** A read can return kilobytes of
  "wait, no, maybe the second image…" with the answer buried inside. Prompt instructions do not
  enforce this; strip scaffolding and near-duplicate lines in code.
- **Same string, two spellings → the read failed.** Do not pick the more plausible one; re-read
  from a single full-size frame.

## Provider-agnostic rules

- **Probe the ladder live; do not assume a rung exists.** A configured provider may carry no
  vision model at all (a token-plan account whose listed models reject image content). A rung
  that can only fail is not a fallback, it is noise.
- **On 402/429 the dead thing is the session's vision tool, not the network.** Dispatch frame
  paths to a bounded subagent instead, and require **two models to agree** before reporting
  anatomy, injury or identity. One model is a read, not a witness.
- **Join every provider's error into the receipt.** A run that loses all rungs at once must
  report each provider's reason, not "empty answer (0 chars)" — the aggregate string is what
  makes the next probe possible.
- **Retry once with backoff per provider** before declaring it dead; transient refusals are
  common on media endpoints.
