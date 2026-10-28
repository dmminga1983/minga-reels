---
name: reels-persona
description: "Create or update the persona file every minga-reels skill reads: who the account or AI character is, who it talks to, how it sounds, what it may claim, what is off limits. Use for 'new persona', 'create a character', 'set up my account voice', 'write my persona from these videos'; RU: создай персонажа, новый профиль, опиши голос аккаунта, персона. Run it first for every new account."
---

# reels-persona

One file per account or character in `~/.claude/minga-reels/personas/<slug>.md`, from the template
at `templates/persona.md` in this repository (copy it from there; if the repo is not at hand, the
headings are: Who this is, How it sounds, Positions, Proof it may use, Off limits, The ask, If
this is an AI character).

## Two ways to fill it

**From examples (better).** Ask for three videos, transcripts or captions in this voice. Read them
and fill in: words it uses, sentence length, how it addresses the viewer (ты, вы, you), what it
never says, pace if there is audio. Quote the examples as evidence, do not paraphrase them.

**From questions.** If there are no examples yet (a new AI character), ask in one batch: niche in
one sentence, the one viewer it talks to, three positions, tone, what it sells or leads to, what
it must never claim. Then write the file and show it.

## Rules

- **The viewer is one person.** "Women 25 to 45" is a segment, not a viewer. Push for a situation:
  "got her keys in September and found a crack in the first week".
- **Proof is real or empty.** Only numbers and stories the user confirms. An empty section is fine:
  the other skills will leave placeholders.
- **AI characters are labelled.** If Kind is AI-generated character, the file says the AI label is
  on for every video, and the character never claims real professional experience it cannot have.
  Point to /reels-character for the look.
- **Several personas are normal.** Testing niches with three characters means three files. Never
  mix their voices: each skill reads exactly one.

## Output

The file path, the filled file, and one line on what is still thin ("Proof is empty: drafts will
carry placeholders").
