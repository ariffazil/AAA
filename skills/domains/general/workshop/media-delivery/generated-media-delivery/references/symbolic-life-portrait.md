# Symbolic life-portrait (no faces)

When the ask is "picture my life", "how would you portray me", or any portrait-of-a-person request
where no reference photograph exists and none is wanted. The deliverable is a symbolic still life that
could only be *this* person's — not a generic moody room.

## Procedure

1. **Read before drawing.** Collect the elements from what the subject actually disclosed: the working
   surface, the objects of the trade, the people-adjacent facts (no names, no faces), the recurring
   want. Lane memory and the session are the only sources; nothing is inferred to fill a gap.
2. **Write the element ledger first.** Two columns — *drawn element* → *the disclosure it comes from*.
   Any candidate whose right column is empty gets cut, however good it would look. This single step is
   what keeps the image honest.
3. **Decide the blanks deliberately.** Name which territory stays out of frame (the parts never shared)
   and say so in the delivery — that pane is a window, not a mirror. Filling it invents a life the
   subject did not hand over.
4. **Stage it as a still life.** Zero people, faces or hands. One key light, one working surface, the
   background element in near darkness with a single cold accent.
5. **Prompt in positional order.** Load-bearing object first, each background element given an explicit
   location ("lower-left foreground", "upper-right background"), then the negative clause set.
6. **Generate two takes on the primary lane** (same prompt, two seeds, pinned absolute `--out` paths)
   plus one cheaper cross-check lane. More takes buy little once the ledger is fixed.
7. **QC each take on elements** (checklist below), then deliver with one line naming the lane and
   stating the frame is synthetic and contains no real person.

## Prompt shape

```
<camera / angle>. <light source, and what it lights>.
<foreground: load-bearing object, then the supporting objects, described concretely>.
<background: the quiet element, in near darkness, cut by one accent of cold light>.
Everything between them falls into black.
Cinematic chiaroscuro, photographic realism, muted <warm> and deep <cool>, shallow depth of field,
35mm film grain. No people, no faces, no hands, no text, no lettering.
```

The negative clause set is mandatory — an unstated negative lets the render place an anonymous figure
in the frame, which collapses the symbolic composition back into a portrait.

## Element QC checklist

Never ask "describe the image" — an open question returns mood prose and hides which elements dropped.
Ask the enumerated form instead:

```
Describe exactly what is present. Which of these landed: <element 1>, <element 2>, <element 3>,
<element 4>? Any people, faces, hands, or text/lettering?
```

- Read every take. A take that looks beautiful while dropping two named elements is a **reject**.
- Check the light source explicitly: in low-key night frames the key light is the element most often
  lost while the frame still reads as successful.
- Where two takes pass, say which one you would pick and why, in one line.
- Never describe an element as present because the prompt asked for it — only what the read-back
  confirmed. Presenting a partial as complete is a truth failure, not a delivery detail.
