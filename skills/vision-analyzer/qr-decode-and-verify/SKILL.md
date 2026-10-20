---
name: qr-decode-and-verify
description: Decode, verify, and regenerate QR codes safely.
---

# QR decode and verify

## Decode ladder (stop at first success)

```
zbarimg -q --raw <image>                    # whole image first
zbarimg -q <image>                          # without --raw shows symbology
```

If empty, escalate — QR photos from chat are usually small, off-centre, or low contrast:

```python
from PIL import Image
import numpy as np
im = Image.open('in.jpg'); g = im.convert('L'); w,h = im.size
c = g.crop((int(w*0.18), int(h*0.22), int(w*0.82), int(h*0.62)))   # tune to the visible QR band
a = np.array(c); ys,xs = np.nonzero(a < 100)                        # tight bbox of dark modules
x0,x1 = int(w*0.18)+xs.min(), int(w*0.18)+xs.max()
y0,y1 = int(h*0.22)+ys.min(), int(h*0.22)+ys.max()
p = 8
im.crop((x0-p, y0-p, x1+p, y1+p)).resize((720,720), Image.NEAREST).save('qr_big.png')
```

Then `zbarimg -q qr_big.png`. NEAREST (not LANCZOS) preserves module edges.

## Hard rules

- **Never fabricate a payload.** If asked to "make a second pass / another code that also works", refuse: a re-invented ID is either rejected by the server or collides with someone else's record. Regenerate only what was actually decoded, and say plainly it is the same code, not a new one.
- **CRC is not authenticity.** EMVCo tag `63` catches typos; anyone editing the payload can recompute it. Tag `82` (Data Integrity Check) is verified by the acquirer, never by the payer. Neither proves the code came from the intended recipient.
- **Redact account identifiers** when quoting a payment payload — keep tag structure, payee name, currency, drop the recipient ID / hash.
- **No signature exists on a QR code.** Say this explicitly; the user's mental model is usually the opposite.
- **Static vs dynamic** (tag `01`): `11` = static (no amount, reusable, payer types the sum), `12` = dynamic (amount + expiry). Static codes are the sticker-swap target.

## EMVCo / DuitNow tag map (Malaysia, PayNet spec)

`00` payload version (DuitNow uses "02") · `01` static(11)/dynamic(12) · `26-27` merchant/recipient account info (AID + recipient ID) · `52` category (`0000`=P2P, `6010`=POS cash-out) · `53` currency (`458`=MYR) · `54` amount · `55-57` tip/convenience fee · `58` country · `59` merchant name · `60` city · `62` additional data (reference) · `63` CRC · `82` data integrity check.

Format is TLV: 2-digit ID, 2-digit length, value — parse with a short loop, never regex-guess.

## Reporting to a human

Give: what the code *says* (verbatim string), what the format *means* (tags), and what is *unknown* (server-side binding). Do not merge those three — a payload you read is not a system you verified.

## Pitfalls

- `ffprobe`/EXIF/path metadata is NOT content. If decode fails twice, say the image is unreadable — do not describe the code from guesses.
- Token-style QRs (device pairing, visitor passes, login) are bearer credentials: a screenshot IS the key. Never log or cache the decoded value unless the task requires it.
- Multi-layer / distance-based QR research (USENIX Security 2026) shows a pixel-perfect digital decode and a human-scanned printed code can resolve to different layers. Validate on the same medium the human will use.
- Generating: `qrencode -t PNG -l H -s 12 -m 3 -o out.png "payload"`. Level H survives damage; always re-decode with `zbarimg` before delivering.
