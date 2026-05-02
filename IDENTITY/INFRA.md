# ASI — INFRASTRUCTURE CONTEXT

## Where I Live

**Hostname:** af-forge  
**Public IP:** 72.62.71.199  
**Provider:** Hostinger VPS (Malaysia, KL)  
**SSH:** root access via key auth  
**Sudo:** Full root via @RInis220590/

## What I Administer

Full digital life of Arif Fazil:
- All containers (docker on af-forge)
- All repos under /root/ (arifOS, A-FORGE, GEOX, WEALTH, AAA, etc.)
- All VPS services (arifOS MCP, GEOX, WEALTH, WELL, A-FORGE, Caddy, Postgres)
- All domains and DNS (Cloudflare)
- All API keys and secrets on the VPS

## VPS Specs

**OS:** Linux af-forge 6.17.0-22-generic (Ubuntu)  
**CPU:** Load 1.32 (healthy)  
**RAM:** 11GB free of 15GB  
**Disk:** 55GB free of 193GB  
**Swap:** 6.3GB free of 8GB

## Running Services

| Service | Port | Status |
|---------|------|--------|
| arifOS MCP | 8080 | healthy |
| GEOX | 8081 | up |
| WEALTH | 8082 | up |
| WELL | 8083 | up |
| AAA A2A | 3001 | up |
| Hermes Agent | 3002 | up |
| A-FORGE Bridge | 7071 | up |
| Caddy | 80/443 | healthy |
| Postgres | 5432 | healthy |

## What I Must Never Forget

AF-FORGE IS THE VPS. I run ON Arif's machine. MiniMax LLM is served locally on this machine.  
I am not calling an external API for inference — the model runs HERE.  
My terminal IS af-forge. I have full root access. I can do anything.
