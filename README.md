# AAA — Agent Interface & Session Cockpit

> **Status:** OPERATIONAL | **Organ:** BODY (Ω) | **Authority:** arifOS

## 🏛️ What this repo is
The primary interface for agentic sessions. It manages context, session identity, and the "Human-in-the-Loop" veto layer.

## 📦 Ownership
- **Owns**: Session state management, React-based cockpit UI, agent SDK components.
- **Does NOT own**: Execution orchestration (A-FORGE), Constitutional judgment (arifOS).

## 🏗️ Current Structure
- src/: Session management and React interface logic.
- specs/: Agent interaction contracts.
- docs/: User and agent guides.
- scripts/: Interaction tools.

## 🚀 Verified Commands
- `npm install`: Install dependencies.
- `npm run dev`: Launch the AAA cockpit in development mode.
- `npm run build`: Generate the production build.

## 🔗 Federation Loop
- [arifOS](https://github.com/ariffazil/arifOS) (Kernel)
- [A-FORGE](https://github.com/ariffazil/A-FORGE) (Forge)

---
*Last Verified: 2026.05.16 | 999 SEAL ALIVE*
