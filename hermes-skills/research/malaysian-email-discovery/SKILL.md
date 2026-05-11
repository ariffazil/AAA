---
name: malaysian-email-discovery
description: Deep email discovery for Malaysian persons and organizations — multi-vector search, CF email decode, WHOIS, MX lookups, verified contacts for press/political/NGO outreach
category: research
---

# Malaysian Email Discovery

Multi-vector email discovery for Malaysian persons, organizations, media, NGOs, and government bodies. Used for investigative journalism, constitutional advocacy, and media outreach campaigns.

## Trigger
Finding working email addresses for Malaysian figures (politicians, journalists, NGOs, legal bodies, policy institutes) when direct website contact forms are broken or unavailable.

## Verified Email Patterns

### Political / Former PMs
| Person | Email | Source |
|--------|-------|--------|
| Dr. Mahathir Mohamad | `drmahathir@perdana.org.my` | X/Twitter bio @chedetofficial + perdana.org.my |
| - | `plfcomms@perdana.org.my` | perdana.org.my contact page |

### Media / Publishing Houses
| Outlet | Email | Source |
|--------|-------|--------|
| **Scoop.my / Big Boom Media** | `editor@scoop.my` | bigboommedia.com.my contact page |
| - | `corporate@bigboommedia.com.my` | bigboommedia.com.my contact page |
| - | `enquiry@bigboommedia.com.my` | bigboommedia.com.my homepage |
| **Malaysiakini** | `editor@malaysiakini.com` | CF-encoded contact page (decoded) |
| **The Edge** | [email protected](mailto:Tips@theedgemarkets.com) | Tips/reporting page |

### Legal & Constitutional
| Body | Email | Source |
|------|-------|--------|
| **Malaysian Bar Council** | `council@malaysianbar.org.my` | malaysianbar.org.my footer |
| **SUHAKAM** | `humanrights@suhakam.org.my` | suhakam.org.my contact page |
| - | `complaints@suhakam.org.my` | suhakam.org.my |

### Environmental NGOs
| Org | Email | Source |
|-----|-------|--------|
| **WWF Malaysia** | `contactus@wwf.org.my` | wwf.org.my contact page |
| **SAVE Rivers** | `contact@save-rivers.org` | saverivers.net (Sarawak-specific) |

## Discovery Methodology (in order)

### 1. Website Scraping (always first)
```bash
# Direct email extraction from any website
curl -sL --max-time 15 -H "User-Agent: Mozilla/5.0" "https://TARGET-SITE.com/contact/" \
  | grep -oP '[\w.-]+@[\w.-]+\.\w+' | sort -u | head -10
```

### 2. Cloudflare Email Decode
Malaysian Bar Council and many MY sites use CF email protection. Decode with Python:
```python
import re

def decode_cfemail(hex_str):
    """Decode Cloudflare email protection (cfemail= hex XOR 100).
    hex_str: string like 'cf97f8f4e3f6f4' (prefixed with number)."""
    key = int(hex_str[0:2], 16)
    result = ''
    for i in range(2, len(hex_str)-1, 2):
        try:
            result += chr(int(hex_str[i:i+2], 16) ^ key)
        except ValueError:
            continue
    return result

# Use on data-cfemail attributes
hex_str = "6abc1234..."  # from HTML attribute
email = decode_cfemail(hex_str)
print(email)
```

### 3. WHOIS + DNS MX Lookup
```bash
# Get authoritative email from domain registrar
dig NS TARGET-DOMAIN.com +short
dig MX TARGET-DOMAIN.com +short

# WHOIS via third-party
curl -sL --max-time 15 "https://www.whatsmydns.net/whois/TARGET.com" \
  | grep -i 'email\|registrant\|admin'

# MX record pattern often reveals hosting
dig MX TARGET-DOMAIN.com +short
# If smtp.google.com → Google Workspace
# If outlook.com → Microsoft 365
```

### 4. Brave Search API (for persons)
```bash
BRAVE_KEY=$(grep BRAVE_API_KEY /root/.hermes/.env | sed 's/.*=//')
curl -s -H "Accept: application/json" \
     -H "X-Subscription-Token: $BRAVE_KEY" \
  "https://api.search.brave.com/res/v1/web/search?q=NAME+Malaysia+email+contact+official&count=10" \
  | python3 -c "
import json, sys
data = json.load(sys.stdin)
for r in data.get('web',{}).get('results',[]):
    t = r.get('title','')[:80]
    u = r.get('url','')
    d = r.get('description','')[:150]
    if d: print(t, '|', u)
    else: print(t, '|', u)
    print('---')
"
```

### 5. Nitter / Archive.org (for suspended accounts)
```bash
# Try multiple nitter instances for Twitter bio
for host in "nitter.net" "nitter.privacydev.net" "nitter.44nx.net"; do
  code=$(curl -sL --max-time 5 "https://${host}/HANDLE" -o /dev/null -w "%{http_code}")
  if [ "$code" = "200" ]; then
    curl -sL --max-time 15 "https://${host}/HANDLE" | grep -i 'email\|bio\|website'
  fi
done

# Archive.org for deleted pages
curl -sL --max-time 20 \
  "https://web.archive.org/web/2026*/https://TARGET-URL/about-us/" \
  | grep -oP 'href="[^"]*"' | grep 'about' | head -5
```

### 6. LinkedIn Company Pages
```bash
# Company page → often shows corporate email pattern
# e.g., Big Boom Media on LinkedIn → enquiry@bigboommedia.com.my
# Try: dig MX companydomain.com +short
dig MX bigboommedia.com.my +short  # → smtp.google.com
```

## Known Block Patterns
| Source | Block type | Workaround |
|--------|-----------|------------|
| Google.com | Empty results | Use Brave Search |
| Bing.com | Empty/HTTP 999 | Use Brave Search |
| LinkedIn | Bot detection 403 | Try direct DNS/WHOIS |
| nitter.net | Returns empty body | Try nitter.privacydev.net |
| scoop.my/about-us | 404 | Use bigboommedia.com.my/about |

## Pipeline: Investigative Outreach Campaign
When sending to 10+ recipients (TO + CC):
1. Discover all emails via methodology above
2. Categorize: TO (primary decision-maker), CC (secondary/witness)
3. Send single email with all in TO/CC — Gmail handles this natively
4. Attach PDF + ZKPC commitment JSON as proof of content integrity
5. Use ZKPC-SEAL prefix in subject for cryptographic anchor
6. Log ZKPC commitment to `~/.hermes/cron/output/searah_zkpc_commitment.json`

## Gotchas
1. Malaysian `.my` domains often use Cloudflare — always try CF decode
2. Small NGOs (SAVE Rivers) may not have contact form — try Facebook page admin emails
3. Bar Council uses CF encoding — decode before use
4. `pewaris.org.my` DNS resolves to Cloudflare origin — try pewaris.org.my/contact directly
5. Malaysian government domains often use `smtp.dosm.gov.my` pattern — WHOIS gives hint
