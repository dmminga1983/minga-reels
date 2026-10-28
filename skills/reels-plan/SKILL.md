---
name: reels-plan
description: "Plan the week of Reels and Shorts for one persona or a niche test across several, sized to the hours the user has: what to post, which format, which hook formula, which platform, and who to engage with. Use for 'plan my week', 'content plan', 'what should I post', 'test niches', 'compare characters'; RU: контент-план, план на неделю, что постить, тест ниш, сравнить персонажей."
---

# reels-plan

## Before you write

1. Find the persona. The user names it ("for fix-it-dad") or there is only one in
   `~/.claude/minga-reels/personas/`. Read it. No persona yet: run /reels-persona first, or ask for
   three videos or captions in this voice and write the persona from them. A script in the wrong
   voice is a retake.
2. Never invent a number, a result, a client, a quote or an experience. If a line needs a figure
   the persona file does not have, write `{{your number}}` and flag it.
3. Reply in the user's language. Write the content in the persona's language.

Also read, if they exist: `~/.claude/minga-reels/swipe.md` (what works in the niche now),
`log.md` (what was posted, so themes do not repeat) and the latest /reels-audit result.

## Ask two things first

How many hours this week, and what is already half made. A plan that does not fit the week is a
list of regrets.

## One persona: the week

Four or five posts, at least three of them short videos, never two of the same type in a row:

| type | per week | job |
| --- | --- | --- |
| proof | 1 | something real that happened, with a number |
| teach | 1 to 2 | one thing the viewer can do today |
| opinion | 1 | a position from the persona file that could cost followers |
| story | every other week | a scene with a cost |
| offer | every other week | what it sells, said plainly |

For each slot: day, platform (Instagram, Shorts or both), type, the specific angle (not a topic:
an angle), the hook formula number, and what exists for it already.

The same video can go to Reels and Shorts. Change the on-screen text and the caption per platform,
and keep the platform's own watermark off the other one.

## Several personas: a niche test

When the user is testing characters or niches against each other, make the test fair, or the
result means nothing:

- the same number of videos per persona (10 is a reasonable first batch), posted over the same
  days, at the same time of day in the audience's time zone
- the same platforms for everyone
- formulas spread evenly, so one persona does not win on formula alone
- decide the comparison now: median views, outlier multiple, sends and follows per 1,000 reach,
  read with `audit.py --by persona` after 10 to 14 days
- write the rule for what happens next before the data comes in: which persona continues, which
  stops

## When to post

Evening in the audience's time zone for most consumer niches, early morning for business. Say it
plainly: the hour matters far less than the first two seconds. If the hooks are weak, timing is
polishing the wrong thing.

## Engagement

Twenty minutes a day, before posting: 5 large accounts in the niche (comment early), 3 peers, 2
potential buyers. Comments come from /reels-reply rules: specific, one idea, never a pitch.

## Output

A table per persona, the hours it costs, what to drop first if the week goes wrong, and "say
'write Tuesday' and I will draft it". Save it to `~/.claude/minga-reels/plan.md`.
