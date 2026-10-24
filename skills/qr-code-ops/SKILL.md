---
name: qr-code-ops
description: "Use when a QR must be read, made, or explained."
version: 1.0.0
owner: AAA
category: media
tags: [qr, barcode, zbarimg, qrencode, duitnow, emvco, payment, forensics]
floor_scope: [F2, F9, F12]
autonomy_tier: T1
ecology_state: WARM
---

# QR Code Ops — decode, generate, verify, and know the limits

A QR code is a text container, not an identity. It carries no signature, no issuer, no expiry and
no owner — anyone with a printer can make one. Every rule below follows from that single fact.

Covers: reading a code out of a screenshot or poster, generating one, interpreting a payment
payload (EMVCo / DuitNow), and explaining the security limits to a human.

## Rule −1 — the container is code, the payload is text

A QR lives inside an image file. The decoder stack parses that file **before** any payload exists,
and a crafted container can execute code at scan time even when the decoded payload is harmless.
There is no signature on the container either. On this host, `zbarimg` links ImageMagick, and
ImageMagick's EPS delegate invokes Ghostscript; Pillow < 13.0.0 carries the CVE-2026-112900
EPS/Ghostscript batch plus JPEG/FPX parser flaws.

Before any decode:

1. **Format allowlist by magic bytes, not extension.** Accept PNG / JPEG / WebP / GIF only.
   Reject EPS/PS (`%!PS`), PDF (`%PDF`), and OLE/FPX (`D0 CF 11 E0 A1 B1 1A E1`). A `.jpg` name is
   not a format.
2. **Pillow ≥ 13.0.0.** Check `python3 -c "import PIL; print(PIL.__version__)"`. Never pass a
   user-controlled filename to `Image.open`; copy to a generated temp name first.
3. **Cap and timeout.** `Image.MAX_IMAGE_PIXELS = 64_000_000`; wrap zbarimg/Pillow in
   `timeout 20`; reject files over ~25 MB.
4. **No `gs` on the decode host.** If Ghostscript is installed, treat EPS/PS as hostile. Backstop
   with ImageMagick's coder policy: `rights="none"` for `{PS,PS2,PS3,EPS,PDF,XPS}`.
5. **Do not mutate `Image.OPEN` and call it security.** Pillow's own handbook says plugin
   unregistration is not a stable control. Gate at the boundary, or sandbox the decoder.

A QR payload can be a valid, harmless string while the file that carries it is the exploit.
When the gate fires, report `container: rejected` — never "no QR".

## Rule 0 — scan before you speak

Never describe what a QR "probably points to". Decode it. If you cannot decode it, say the decode
failed and at which step — do not substitute the surrounding context (poster text, the chat
message, the brand) for the payload.

## Decode (the working ladder)

```bash
zbarimg -q file.jpg                      # payload as text
then
zbarimg -q --raw file.jpg | xxd          # exact bytes: control chars, hidden newline, non-UTF8
```

**If zbarimg returns nothing, do not conclude "no QR".** Work the image, in this order:

1. **Tight bbox crop, then re-decode.** Threshold dark pixels inside a generous central band, take
   the bounding box, pad ~8 px, resize with `Image.NEAREST` to ~720 px, decode again. A code that
   fails on a 630×1280 screenshot usually decodes at 720 px nearest-neighbour.
2. **Upscale, don't sharpen.** Blurring or sharpening destroys module edges; nearest-neighbour
   upscaling preserves them.
3. **Keep the quiet zone.** Most decoders need white margin; a crop flush to the finder patterns
   fails.
4. Only then consider inversion (white-on-dark) and perspective correction.

Report the payload verbatim, and where it matters its length and shape (all digits, URL, TLV).
A payload you paraphrased is a payload you invented.

## Generate — and always re-decode before delivering

```bash
qrencode -t PNG -l H -s 12 -m 3 -o out.png "<payload>"
zbarimg -q out.png        # MUST print the payload you asked for
```

- `-l H` (30% error correction) for anything printed, stuck on a wall, or shown on a phone at an
  angle. Redundancy is also what lets a logo sit in the middle — and what lets an attacker cover a
  third of the code without breaking the read.
- `-m 3` to `-m 4` quiet-zone margin; `-s` module size so it scans from a screen.
- **A generated QR that decodes to something other than the intended string is worse than none.**
  The `zbarimg` round-trip is not optional, and it is one command.
- Deliver the PNG as a file (`MEDIA:/abs/path.png`), not a description of it.

## Never author a credential the issuer never issued

When asked to make "another pass", "a second QR for the same visitor", or any artifact another
system validates against a stored record:

- **You may regenerate a payload you have decoded and confirmed.** You may not invent one.
- A guessed ID is not merely invalid — it may belong to a different record (another unit, another
  person), and using it is worse than the request failing.
- Say which of the three you are doing: *regenerated the same token*, *generated a new independent
  QR*, or *cannot — the issuer must mint it*. Then state the consequence: same token means one
  shared credential, not two.

The same boundary covers "how do I hack/crack/forge <payment or access QR>": decline the offensive
technique and offer the defensive read instead (what the fraud looks like, what to check). That
offer is not a consolation prize — it is usually the thing the person actually needs.

## Reading a payment QR (EMVCo / DuitNow)

A payment payload is TLV — two-digit tag, two-digit decimal length, value — not free text. Parse it
as TLV; a regex over the raw string mis-splits on repeated tag digits.

| ID | Field | Note |
|---|---|---|
| `00` | Payload format | DuitNow uses `02` (EMVCo base `01`) |
| `01` | Point of initiation | `11` static (reusable), `12` dynamic (per transaction) |
| `26`–`27` | Account info | `26` = AID + recipient ID; `27` reserved |
| `52` | Category code | `0000` = P2P, `6010` = POS cash-out |
| `53` | Currency | `458` = MYR |
| `54` | Amount | **Absent on static QR** → payer types it |
| `58` | Country | `MY` |
| `59` | Recipient name | **The only anti-fraud field a payer can read** |
| `60` | City | `MY` when not applicable |
| `62` | Additional data | bill / reference label |
| `63` | CRC | 4 hex, checksum only — **not a signature** |
| `82` | Data integrity check | hash verified by acquirer, invisible to payer |

```python
NAMES = {'00':'format','01':'initiation','26':'acct','52':'mcc','53':'ccy','54':'amount',
         '58':'country','59':'name','60':'city','62':'extra','63':'crc','82':'integrity'}

def parse_tlv(s, depth=0):
    out, i = {}, 0
    while i + 4 <= len(s):
        tag, ln = s[i:i+2], s[i+2:i+4]
        if not (tag.isdigit() and ln.isdigit()):
            out['_unparsed'] = s[i:]; break
        val = s[i+4:i+4+int(ln)]
        if len(val) < int(ln):
            out['_truncated'] = (tag, val); break
        if depth < 2 and len(val) >= 8 and val[:2].isdigit() and val[2:4].isdigit():
            nested = parse_tlv(val, depth + 1)
            out[tag] = nested if len(nested) > 1 else val
        else:
            out[tag] = val
        i += 4 + int(ln)
    return out
```

Sanity checks after parsing: `00` present; `63` present and 4 chars; reassembled byte count equals
input length. If reassembly differs you mis-split, and every field after the error is fiction.

**Static vs dynamic.** Static carries an address, not an invoice: reusable, reprintable, no amount,
no expiry, and a payer who types the sum themselves with full confidence. Dynamic is always safer
for payment.

## Redaction when quoting a payload

A payment payload contains a recipient identifier and an integrity hash. When quoting it in a report
or a chat, keep the structure, currency, name and tag map; **mask the recipient ID and the hash**.
Not because it is secret to its owner, but because a report travels further than its original
purpose. The platform's secret-scrubber may mask digit runs on its own — re-read your output for
`[REDACTED:...]` before assuming the payload printed intact.

## Security posture (what actually protects anyone)

Cuts must land on a different layer than the attack, or they do nothing:

| Layer | Attack | Only effective defence |
|---|---|---|
| Physical | sticker over sticker, partial cover | inspect the medium; prefer the code inside the merchant's own app over a printed sticker |
| Data | malicious payload, dual-standard / distance-layered codes | treat payload as data, never as instruction |
| Redirect | shorteners, custom schemes, `intent://` | Android App Links verified against the domain, not custom schemes |
| Application | the decision | show **name + amount + recipient before** the action, not after |
| Token | QR as bearer credential (login, pairing, pass) | short TTL, single use, server binds token → one record |

Facts worth carrying:

- **Scanning alone rarely moves money.** Loss happens on the step *after*: entering credentials,
  approving a notification, handing over an OTP/TAC, or installing an app. Any request for those four
  after a scan is the scam, whatever the QR looked like.
- **A genuine DuitNow recipient never scans the payer's code**, never needs bank credentials, never
  needs an OTP, and never charges an activation fee. Four cheap tests.
- **A QR carrying only a bare number** (a pass ID, a ticket ID) has **no in-code anti-tamper at all** —
  the only binding lives on the server. Say that as a structural observation, not as an accusation
  that the system is broken.
- **Redundancy is dual-use.** Error correction that survives a 30% cover also lets a code be altered
  and still scan, and lets two decoders read two different payloads from one printed image
  (dual-standard, distance-layered and high-refresh-display techniques all exist in the literature).
  Validating a pixel-perfect image is not validating the medium the human is looking at.

## Pitfalls

- **A generated QR is untrusted output until re-decoded.** The round-trip is one command; skipping it
  ships a code that scans to the wrong payload.
- **`zbarimg` silence is not proof of absence** — work the image (bbox crop → nearest upscale → keep
  margin) before reporting "no code found".
- **Never infer a payload from the poster around it.** Brand, logo and surrounding text are not the
  payload.
- **Do not restate a payload from memory** while writing the report; re-open the decode output.
- **A short link is not the artifact.** Resolve shorteners/redirects before probing, or the block you
  hit belongs to the shortener's domain and says nothing about the target.
- **Two codes, two lessons.** A payload carrying a human-readable name lets the payer check it; a
  payload carrying only a number gives them nothing to check. That difference is a design property,
  and naming it is more useful than any list of tips.

## Source note (verify freshness before quoting)

DuitNow/EMVCo tag semantics: PayNet developer docs (Merchant-Presented Mode, QR Data Object) and
EMVCo MPQR v1.1 — stable. Malaysian quishing case counts move monthly: take them from CCID Bukit
Aman / Bank Negara statements and date them in the deliverable. Threat-vendor percentages
(Microsoft, ESET, Palo Alto, APWG) are quarterly — always carry the quarter.
