# Arxiv API as Web-Search Fallback

When `web_search` / `web_extract` return HTTP 432 (Tavily backend down), pivot to direct arxiv API via `curl`. Faster than browser exploration for academic sources.

## Query URL

```
curl -sL --max-time 15 \
  'https://export.arxiv.org/api/query?search_query=all:TERM+TERM+TERM&start=0&max_results=5'
```

## Rules

- `all:term1+term2+term3` → implicit OR. Avoid `AND`/`OR` keywords — arxiv parses them as search terms.
- `ti:` for title, `abs:` for abstract. `id_list=X,Y` for known paper IDs.
- Rate limit: ~8 rapid queries before "Rate exceeded." Wait 10-15s.
- Extract: `grep -E "<title>|<id>|<summary>|<arxiv:doi>" | head -30`

## Proven query templates

| Domain | Query |
|---|---|
| MoE / routing | `all:mixture+of+experts+efficiency+LLM` |
| LLM ensemble | `all:LLM+routing+ensemble+cost+optimization` |
| AI governance | `all:AI+governance+constitutional+maps+oversight` |
| Trust / XAI | `all:trust+AI+empirical+user` |
| Brain modularity | `all:brain+modularity+deep+learning` |
| Distributed cognition | `all:distributed+cognition+multi-agent` |

## Counterparty fallbacks

When arxiv is also exhausted: Semantic Scholar API (rate-limited, 429), Google Scholar via browser, or cite known foundational texts from memory with `type: analogical_foundation`.
