---
name: malaysian-contact-investigation
description: Layered email discovery for Malaysian political figures, journalists, and media outlets — when standard searches return empty or blocked. Uses DNS, Cloudflare decode, Brave Search, Wayback Machine, and X bio extraction.
trigger: "Finding contact emails for Malaysian targets when web searches fail or return empty"
created: 2026-05-07
tags: [malaysia, email-discovery, investigative, osint]
---

# Malaysian Contact Investigation Skill

## Trigger
Finding email addresses for Malaysian political figures, journalists, or media outlets when standard web searches return empty or blocked results.

## Core Discovery Stack (layered approach)

### Layer 1 — Author/Profile Pages
1. Search for the **author page** on the publication site
   - e.g., `scoop.my/author/zainul-arifin` → often has bio + contact
2. Check the **parent/company website** for contact pages
   - e.g., bigboommedia.com.my → `editor@scoop.my` listed explicitly

### Layer 2 — DNS & MX Records
```bash
dig MX scoop.my +short          # → smtp.google.com (Gmail hosted)
dig NS scoop.my +short           # → Cloudflare nameservers
dig A scoop.my +short            # → IP address
```
MX records reveal hosting. Cloudflare = site is likely protected, look for parent company emails.

### Layer 3 — WHOIS (for scoop.my)
- whatsmydns.net/whois/<domain> — may reveal registrant/admin emails

### Layer 4 — Cloudflare Email Protection Decode
Many Malaysian news sites (malaysiakini.com) use Cloudflare's `data-cfemail` attribute to encode emails in HTML source.

```bash
# Get the hex string from HTML source, then decode:
python3 -c "
hex_str = '97f2f3fee3f8e5d7faf6fbf6eee4fef6fcfef9feb9f4f8fa'
key = int(hex_str[0:2], 16)
result = ''.join(chr(int(hex_str[i:i+2], 16) ^ key) for i in range(2, len(hex_str), 2))
print(result)
# Output: editor@malaysiakini.com
"
```

### Layer 5 — Wayback Machine
```bash
curl -sL --max-time 20 \
  "https://web.archive.org/web/2026*/https://www.scoop.my/about-us/" \
  | grep -oP 'href=\"[^\"]*about[^\"]*"' | head -10
```
Pages that return 404 may have archived versions.

### Layer 6 — Brave Search API (not just web scraping)
```bash
BRAVE_KEY=$(grep BRAVE_API_KEY ~/.hermes/.env | sed 's/.*=//')
curl -s -H "Accept: application/json" \
     -H "X-Subscription-Token: $BRAVE_KEY" \
     "https://api.search.brave.com/res/v1/web/search?q=TARGET+NAME+email+contact&count=10" \
  | python3 -c "import json,sys; [print(r['url']) for r in json.load(sys.stdin)['web']['results']]"
```
Brave returns results even when Google/Bing are blocked or return empty for Malay names.

### Layer 7 — X/Twitter Bio Extraction
Many Malaysian politicians list official emails in X bio. Check:
- X.com/@handle (requires JS — use nitter.net as fallback)
- Bio field often contains `drmahathir@perdana.org.my` format

```bash
# Try nitter instances (Twitter mirror without JS):
for host in "nitter.net" "nitter.privacydev.net"; do
  code=$(curl -sL --max-time 5 "https://${host}/HANDLE" -o /dev/null -w "%{http_code}")
  echo "${host}: ${code}"
done
```

## Malaysian-Specific Patterns

| Target Type | Best Discovery Path |
|-------------|-------------------|
| Politician (senior) | X bio + party website contact page |
| Journalist/Author | Author page on publication + parent company |
| Media outlet | Contact page on parent company |
| Former PM | Foundation/Institute website (Perdana, etc.) |
| Sacked/ex-politician | Twitter/X + personal WordPress |

## Email Verification Hierarchy

| Level | Confidence | Action |
|-------|-----------|--------|
| 1 — Direct confirmation on official page | ✅ High | Send directly |
| 2 — Confirmed via MX/DKIM on same domain | ✅ High | Send directly |
| 3 — Inferred from pattern | ⚠️ Medium | Send but CC alternative |
| 4 — Social media only | ⚠️ Medium | Use Twitter DM instead |
| 5 — Blind guess | ❌ Low | Do not use |

## Verified Results (SEARAH investigation 2026-05-07)

| Recipient | Email | Discovery Method |
|-----------|-------|-----------------|
| Dr. Mahathir Mohamad | `drmahathir@perdana.org.my` | X bio @chedetofficial + directa dari perdan.org.my |
| Zainul Arifin (Scoop) | `editor@scoop.my` | bigboommedia.com.my contact page |
| Isham Jalil | `@ishamjalil` (Twitter) | No email found — Twitter fallback |

## Cover Letter Tone Principles (Malaysian context)
- **Politicians:** Rakyat Jelata angle — bukan political attack, hormat tapi berani
- **Journalists:** Fact-first, editorial pitch, "available on request" untuk protect source
- **Ex-politicians:** Malaysian-first framing, avoid partisan language
- **Always:** Cite primary sources — don't let them dismiss as hearsay

## Lessons Learned
- Malay names with hyphens: search "Isham Jalil" NOT "isham_jalil"
- Isham Jalil: NO public email exists — Twitter DM is only path
- Zainul Arifin: not on Scoop directly, parent Big Boom Media has `editor@scoop.my`
- Dr. Mahathir: `drmahathir@perdana.org.my` — not `pewarismahathir@gmail.com`
- WordPress "Hubungi Kami" pages exist for Malaysian personalities but DON'T publish owner email
- TheEdge Malaysia uses Cloudflare + JavaScript — decode HTML source cfemail
- Brave Search works when Google/Bing return empty for Malay names
- pewaris.org.my domain doesn't resolve — Tun's actual outlet is @chedetofficial on X
