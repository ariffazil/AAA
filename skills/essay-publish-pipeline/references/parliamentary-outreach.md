# Parliamentary Outreach — MP Email Research & One-Shot Distribution

Workflow for compiling verified Malaysian MP email lists for advocacy campaigns (open letters, petitions, audit requests). Proven 2026-08-09 on the PETRONAS governance open letter.

## Canonical sources

| Source | URL | What it gives |
|---|---|---|
| **Parlimen MP list** | `https://www.parlimen.gov.my/ahli-dewan.html?uweb=dr` | All 222 MPs, filter by state (`&p=Johor`, `&p=Sarawak`) |
| **MP profile pages** | `https://www.parlimen.gov.my/profile-ahli.html?uweb=dr&id=<ID>` | Name, constituency, party, **email**, phone, office address |
| **PAC members** | `https://www.parlimen.gov.my/pac/ahli-jawatankuasa-pac.html` | Current PAC committee roster + `pacparlimen@parlimen.my` |
| **Wikipedia** | `Members of the Dewan Rakyat, 15th Malaysian Parliament` | Full roster with parties — good for cross-checking vacancies/by-elections |
| **Google search** | `site:parlimen.gov.my profile-ahli <name>` | Find the profile ID when the directory is slow |

## Email patterns

- Official ministry emails: `<name>@<ministry>.gov.my` (e.g. `anwaribrahim@pmo.gov.my`, `liewchintong@mof.gov.my`, `zahid@jpm.gov.my`)
- PAC: `pacparlimen@parlimen.my` (committee inbox — highest priority target)
- Personal gmail/office emails on profile pages (e.g. `syedsaddiq92@gmail.com`, `fadillah194@gmail.com`, `tebrauparlimen@gmail.com`, `mp@wongchen.com`)
- Many MPs list NO public email — the profile page shows `-`. For those, use the service center phone/fax or the party channel.

## Tiering logic (who gets the letter)

1. **PAC members** — the only body that can order a special audit of a GLC. Pengerusi first.
2. **State-relevant MPs** — for Petronas: Johor (Pengerang petrochemical, SEARAH) + Sarawak (Petronas-Petros gas rights, GPS bloc).
3. **Opposition voices** who have publicly questioned GLC governance (Syed Saddiq — 650+ parliamentary interventions; Wong Chen — fiscal transparency).
4. **Media amplifiers** — podcast hosts who can make it viral (Khairy Jamaluddin + Shahril Hamdan, *Keluar Sekejap*). NOT MPs — separate tier.
5. **Ministers** — CC only, not primary: PMX (also Minister of Finance — the sole shareholder of Petronas), DPM, Finance Minister II.

## The 33-email target

Arif's explicit requirement: **at least 33 verified emails in one shot.** Composition that worked:

| Tier | Count | Example |
|---|---|---|
| PAC (chair + VC + members) | 9 | pacparlimen@parlimen.my, teresakok@parlimen.my |
| Sarawak GPS | 8 | fadillah194@gmail.com, alexlinggi@kkr.gov.my |
| Johor | 5 | tebrauparlimen@gmail.com, liewchintong@mof.gov.my |
| Opposition | 3 | syedsaddiq92@gmail.com |
| Media (KJ, Shahril) | 2 | shahril.hamdan@gmail.com |
| Ministers | 3 | anwaribrahim@pmo.gov.my |
| Selangor | 3 | mp@wongchen.com |
| Others (PN backup) | 3 | ronald@parlimen.my |
| PMX | 1 | anwaribrahim@pmo.gov.my (CC) |

## Verification discipline

- **Cross-check every email** against the parlimen.gov.my profile page — a single wrong address in a 35-recipient blast is an embarrassment.
- **Check for recent resignations/vacancies.** Rafizi Ramli (Pandan) resigned May 2026; Wong Chen (Subang) announced resignation intent Aug 2026. Wikipedia's roster page flags vacancies — read it before finalizing.
- **CSV output columns:** `No,Nama,Kawasan,Parti,Email,Tier,Sebab` — the "Sebab" (reason) column is what makes the list usable by whoever sends the blast.

## Cloudflare email routing check (arifos@arif-fazil.com)

If asked whether a domain email works:
1. `dig MX <domain> +short` → if `route1/2/3.mx.cloudflare.net`, Cloudflare Email Routing is active.
2. `dig TXT <domain> +short | grep spf` → expect `v=spf1 include:_spf.mx.cloudflare.net ~all`.
3. API verification: `GET https://api.cloudflare.com/client/v4/zones/<ZONE_ID>/email/routing/rules` — the zone API token may 401 (token scope/expiry); fall back to telling the user to check the Cloudflare dashboard → Email → Routing Rules.
4. `ss -tlnp | grep -E ":25|:587|:465"` — empty means no local MTA; mail is fully handled by Cloudflare.
