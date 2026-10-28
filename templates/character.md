# Character bible: {{name}}

For an AI-generated character. Copy to `~/.claude/minga-reels/characters/<slug>.md`. Every image
or video prompt for this character starts from this file, so the face, the voice and the world
stay the same from video to video.

## Fixed look (never changes)

- **Age range, build, skin, hair:**
- **Face: three features that make it recognisable:**
- **Signature item:** (glasses, a scarf, a mug, a colour)
- **Default outfit:**
- **Reference images:** (paths or links to the 3 to 5 approved images; reuse them every time)

## Voice

- **Voice description:** (pitch, speed, accent, warmth)
- **Voice id in the tool you use:**
- **Catchphrase, if any:** (one, used rarely)

## World

- **Where it is usually filmed:** (kitchen, workshop, office: the same place builds recognition)
- **Lighting and colour:**
- **Camera:** handheld selfie / tripod / over the shoulder

## Prompt skeleton

```
{{fixed look}}, {{default outfit}}, in {{usual place}}, {{lighting}}, {{camera}},
{{action for this video}}, vertical 9:16, natural skin texture, no text on screen
```

## Rules

- Same reference images, same seed or character id where the tool supports it.
- Never the likeness of a real person, and never a real person's voice.
- Labelled as AI on every platform, every time.
