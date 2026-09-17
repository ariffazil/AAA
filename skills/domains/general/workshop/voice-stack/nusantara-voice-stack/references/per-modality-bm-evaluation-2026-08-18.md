# Per-Modality BM Fluency Evaluation — 2026-08-18

## Trigger

External analysis presented (2026-08-18 18:34 MYT) claimed: *"Antara Qwen, MiniMax, dan MiMo, Qwen (Alibaba) adalah pilihan yang paling solid dan fasih untuk Bahasa Melayu."*

This was presented as a blanket verdict across all modalities. Falsified by live probe data + nusantara-voice-stack lane map.

## Where the verdict was right

For **LLM BM reasoning/copywriting**:
- Qwen2.5/Qwen3 trained on substantial SEA corpus including BM
- BM output reads native, code-switches naturally
- Qwen beats MiMo-V2.5 on BM creative tasks
- Qwen beats MiniMax on BM reasoning depth

→ **Qwen wins LLM BM. Confirmed.**

## Where the verdict was wrong

For **BM TTS / voice output**:
- Qwen qwen-audio-3.0-tts-plus has **597 base voices, ALL Chinese/English, ZERO Malay**
- The only Qwen path to Malay voice is **voice cloning** (upload 10-20s sample, requires URL hosting)
- For base-voice TTS, **MiniMax Indonesian voices outperform Qwen for BM** because Indonesian and Malay are mutually intelligible at the phoneme/intonation level
- Live probe (2026-08-18): `Indonesian_CaringMan`, `Indonesian_BossyLeader`, `Indonesian_SweetGirl` all render BM text naturally; Qwen `longanlufeng` reading BM produces Chinese-accented English where BM words exist

→ **Qwen loses BM TTS. Falsified.**

## Verdict by modality (live probe + nusantara-voice-stack §3)

| Modality | Winner | Runner-up | Why |
|---|---|---|---|
| BM LLM reasoning / copywriting | **Qwen** | MiniMax | Qwen SEA-trained; MiniMax is CN-EN oriented |
| BM TTS base voices | **MiniMax Indonesian** | Qwen voice clone (setup heavier) | MiniMax has 9 Indonesian voices that read BM naturally; Qwen has zero Malay base voices |
| BM custom voice clone | **MiniMax TTV** (free, persistent) | Qwen voice cloning (free, URL-hosted) | MiniMax simpler; both free within quota |
| BM STT / falsification | **Groq Whisper-large-v3-turbo** | faster-whisper local | Groq 216× realtime, free, supports `language=ms` |
| Codebase crunch (large context) | **MiMo-V2.5** | Qwen | MiMo 1M context, cost-efficient on technical text |
| BM-native F5-TTS finetune | **Malaysian-F5-TTS-v3** | (none) | 15,631 hrs Malaysian speech; CC-BY-NC-4.0; needs Runpod GPU + F13 GO |

## The doctrine

> Never generalize "best BM model" across modalities. Voice ≠ text ≠ code ≠ vision. Ask "best for what?" before any verdict. If the question is unanswered, refuse to rank.

## Anti-pattern caught

The external analysis made these errors:
1. Generalized Qwen's LLM strength across all BM tasks
2. Did not probe TTS base voice catalog (would have found zero Malay in Qwen)
3. Did not compare MiniMax Indonesian voices for BM phoneme mapping
4. Did not separate MiMo's use cases (cost-efficient technical text ≠ fluent BM creative)

## Note on Qwen voice cloning path

Still relevant for custom voices (Syed voice clone, Arif voice clone). But this is a SEPARATE capability from "Qwen speaks BM by default." The two should not be conflated.

## Reference

- Live probe transcript: `/root/.hermes/skills/media/nusantara-voice-stack/references/tts-provider-lane-map.md`
- Voice table: `references/minimax-indonesian-voices-2026-08-18.md`
- Qwen cloning: `references/qwen-voice-cloning-2026-08-18.md`
- Doctrine source: nusantara-voice-stack SKILL.md §11