---
name: reels-hook
description: "Write and score hooks for Reels and YouTube Shorts in Russian or English: options from 26 formulas, scored by a local tool, the weakest property named with the fix. Use for 'hook', 'first line', 'opening', 'how do I start this video', 'score my hook'; RU: хук, первая фраза, начало ролика, зацепка, оцени хук. Also calibrates the scorer on the user's own videos."
---

# reels-hook

The first three seconds decide the video. This skill writes hook options and scores them with
a tool that actually runs:

```bash
python3 hookscore.py hooks.txt              # one per line, ranked
python3 hookscore.py --hook "одна строка"
python3 hookscore.py --pace 5.5 hooks.txt   # the persona's pace
python3 calibrate.py corpus.tsv             # how well the score predicts in your niche
```

## Before you write

1. Find the persona. The user names it ("for fix-it-dad") or there is only one in
   `~/.claude/minga-reels/personas/`. Read it. No persona yet: run /reels-persona first, or ask for
   three videos or captions in this voice and write the persona from them. A script in the wrong
   voice is a retake.
2. Never invent a number, a result, a client, a quote or an experience. If a line needs a figure
   the persona file does not have, write `{{your number}}` and flag it.
3. Reply in the user's language. Write the content in the persona's language.

## The loop

1. Read `hooks.json`: 26 formulas, each with its shape, an example, the on-screen line, what it is
   good for and how it gets ruined. The examples illustrate the shape; never reuse their numbers.
2. If `~/.claude/minga-reels/swipe.md` exists, read it first: formulas working in this niche now
   outrank the defaults.
3. Pick **three different formulas** that fit the idea and write the spoken line and the on-screen
   line for each. Three formulas, not three rewrites of one.
4. Score them. Show the ranking with each one's weakest property and fix.
5. If the best is under 48, you do not have the hook yet. Ask one question that gets the specific
   true thing (what happened, to whom, what it cost) and write again.

## What the score means

It reliably catches weak hooks: greetings, preambles, hype words instead of facts, more than three
seconds to say. It cannot pick the winner between two decent hooks; the face, the edit, the sound
and the platform decide that. Say so when you show the scores.

Once the user has 30 or more of their own videos, offer `calibrate.py`: it measures whether the
score separates their own hits from their own misses, property by property, and tells them which
properties mean nothing in their niche.

## Output

```
HOOKS  (scored)
  61  OK    #2 Цена ошибки      "Я переплатил сорок тысяч из-за одного пункта в договоре."
                                 on screen: -40 000 ₽
  ...
Shooting #2: the number is the persona's own, and it reads in one glance.
```

Then hand the winner to /reels-script.
