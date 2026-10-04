# Taufiq Shadow — Web Page Implementation

## Source
- URL: https://arif-fazil.com/world/economics/petronas/shadow/
- Published: 2026-08-09
- Source file: `/root/arif-fazil.com/sites/arif-fazil.com/public/world/economics/petronas/shadow/index.html`

## Design Language
Follows PM Bayang (`/politics/shadow/`) pattern:
- Dark theme (`#07070d`), gold accents (`#c9a84c`), IBM Plex Mono + Sans
- Card-based layout with numbered shadows
- Color-coded legend: MECHANICAL (cyan), STRUCTURAL (amber), CRITICAL (red), HIDDEN (purple)
- YouTube embed as hero element
- Contrast bar linking to PM Bayang page

## Content Structure
13 shadow cards, each with:
- DATA section (verifiable facts)
- TRANSCRIPT PATTERN section (linguistic analysis)
- QUALIA section (emotional/felt sense)

Plus MBTI analysis section (ISTJ vs INTJ).

## Contrast with PM Bayang
- PM Bayang = Jung Shadow of political leaders (9 PMs)
- Taufiq Shadow = Institutional Shadow of corporate power (1 CEO)
- Same design language, different analytical frame
- Cross-linked via nav bar and contrast bar

## CSP Requirement
Pages with YouTube iframe embeds require `frame-src` directive in Caddy CSP:
```
frame-src https://www.youtube.com https://www.youtube-nocookie.com;
```
Added to `/etc/caddy/Caddyfile` line 45 on 2026-08-09.
