---
name: reels-character
description: "Keep an AI-generated character consistent across videos: the character bible (fixed look, voice, world), a prompt skeleton for image and video generators, a shot list per script, and the AI labelling rules. Use for 'AI character', 'keep the face the same', 'prompt for my character', 'generate the scenes'; RU: ИИ-персонаж, сохрани внешность, промпт для персонажа, сцены для ролика, нейро-блогер."
---

# reels-character

For personas whose Kind is AI-generated character. Recognition comes from sameness: the same face,
voice, place and light in every video.

## The bible

Write `~/.claude/minga-reels/characters/<slug>.md` from `templates/character.md` in this repository
(headings: Fixed look, Voice, World, Prompt skeleton, Rules). Fill it from the persona file and
the user's approved reference images. Once approved, the fixed look does not change; a new outfit
is a new episode, not a new face.

## Per script

From a /reels-script beat sheet, write one shot per beat:

```
BEAT 2  3.1s   medium shot, kitchen, character holds the signed act, looks at camera
        prompt: <skeleton filled in>
        on screen: -40 000 ₽
```

Same reference images and the same character id or seed in every prompt, if the tool supports
them. If a generation tool is connected in this session (for example Higgsfield), offer to run the
prompts there; generation costs credits, so say how many shots before starting and wait for a yes.

## Rules

- **Never a real person's likeness or voice**, including "in the style of" a real creator.
- **Labelled every time:** Instagram's AI label, YouTube's altered-or-synthetic setting. The
  caption skill reminds; this skill puts it on the shot list too.
- **No claimed real-life credentials.** A character can have a story; it cannot claim to be a
  licensed doctor, lawyer or financial adviser giving real advice.
- **Health, money and legal niches**: the character explains and points to professionals, and never
  gives personal diagnoses, guaranteed returns or legal conclusions about someone's case.
