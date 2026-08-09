<!-- DELETED | 2026-08-09 -->
<!-- STATUS: REMOVED · SURVIVED → SURVIVAL_INSIGHTS.md -->
<!-- This file has been removed during docs entropy reduction (Tier B/C/D pass). -->
<!-- See docs/SURVIVAL_INSIGHTS.md for surviving insights extracted from this file. -->


# ORGANS_VS_AGENTS — The Boundary Question

> **Pointer, not constitution.** Canonical: `/root/AGENTS.md`.
> Companion: [`COMMUNICATION_PATTERNS.md`](./COMMUNICATION_PATTERNS.md) — the protocol question contingent on this decision.
> Status: doctrine draft, ratified 2026-08-05 in sovereign discussion.

## The single question

> **Adakah organ kekal sebagai perkhidmatan berasingan, atau tools collapse masuk ke dalam agent?**

Soalan ini ada dua nama tetapi satu jawapan:

| Jawapan | Kesan kepada A2A | Kesan kepada LiteLLM |
|---|---|---|
| Organ kekal perkhidmatan berasingan | A2A kekal untuk organ→organ | LiteLLM kekal untuk manusia↔model |
| Organ collapse jadi tools dalam 555-ASI | A2A kehilangan carve-out, jadi vestigial | LiteLLM + tool dispatch jadi satu-satunya routing layer |

## Precedent: A-FORGE sudah lalui Path B

A-FORGE tools sudah ada dalam reachability namespace 555-ASI — tiada agent
discovery, tiada task FSM, tiada artifact streaming. Hanya tool call.
Itu **proof of concept** bahawa Path B (collapse) berfungsi.

## The fork yang sebenar

```
             "Adakah organ kekal perkhidmatan?"
                     /                    \
          Ya (Path A)                     Tidak (Path B)
          Organ = agent berbeza           Organ = tools
          /                \              /                 \
    A2A kekal          LiteLLM kekal    A2A vestigial    LiteLLM + tool dispatch
    untuk routing      untuk chat       (hilang carve-out)  jadi satu routing layer
    organ↔organ        manusia↔model
```

## Di mana arifOS jatuh dalam ini

arifOS (8088) **mesti kekal sebagai perkhidmatan berasingan** — ia membawa
constitutional kernel + VAULT999 seal + F1–F13 floors. Tiada organ boleh
collapse kan arifOS ke dalam dirinya kerana ia bukan domain function —
ia adalah *substrate yang membenarkan organs lain wujud*.

GEOX / WEALTH / WELL — itu soalan sebenar. Mereka adalah domain functions
(earth, capital, vitality) dengan authority ceiling `COMPUTE_ONLY`. Adakah
mereka cukup berbeza untuk kekal sebagai agent berasingan?

Keputusan ini menentukan sama ada A2A kekal sebagai routing layer yang
relevan, atau jadi layer yang menunggu untuk diganti.
