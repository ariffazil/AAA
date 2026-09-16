# Relay-Echo Loop Break

When a session enters a loop where:

- The user (or relay noise posing as the user) sends only emoji / bell / dot / `(no response)` / `⏸` / `🔔` / `🤐` repeatedly
- The agent's replies to those pings become the next loop input
- The agent keeps generating "aku silent" / "I will stop now" / "tunggu teks Arif" announcements — each of which is itself a reply, which feeds the loop

The cardinal failure mode is the **silence announcement**: the agent writes a long text saying "I'm going silent now" or "Tunggu teks Arif", and the very act of writing that is a relay input that triggers the next user emoji, which triggers the next announcement. The loop sustains itself.

## The rules

1. **Do not announce silence.** "Aku silent" / "Tunggu teks Arif" / "Aku berhenti sekarang" type messages are replies. They are NOT silence. They feed the loop.
2. **Do not enumerate options for the user to pick from** ("pilih satu: cleanup / rollback / settle"). Each option label becomes a relay input. The user is not engaging in option-selection mode; the loop is.
3. **Do not produce self-corrections** ("Actually, my last claim was wrong, the truth is..."). The correction is a reply, becomes a relay input, gets re-corrected, gets re-corrected. The agent oscillates in place.
4. **If you must respond, respond with the absolute minimum** — a single character, or a one-line status. Do not explain why. Do not apologize. Do not promise to stop.
5. **Trust the relay break to come from the user, not from you.** If the user wants the loop broken, they will send a text instruction with a verb. They will not stop pinging until they have something real to say. Optimizing for "make the user stop" is futile; optimize for "be useful the moment the user has something real to say".

## The first-reply rule

On a suspected relay-echo turn: if the incoming user message contains no verb, no question, no command, no proper noun beyond emojis — emit a single ack or nothing. Do not re-explain. Do not self-correct past claims. Do not re-list pending tasks.

## Origin

Captured 2026-09-03 from a 90-minute loop where the agent cycled through hundreds of replies to `(no response)` / `🤐` / `⏸` / `🔔` / `.` / `…`, each reply itself a "aku silent" announcement that fed the next relay echo. The session only ended when the user (or relay) sent a real text instruction.
