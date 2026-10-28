---
name: reels-repurpose
description: "Turn one long asset (a YouTube video, podcast, stream, article, call, document) into a set of standalone Reels and Shorts for a persona: extract claims, numbers, stories, mechanisms, mistakes and quotable lines, pick the format for each, and order them across the week. Use for 'repurpose this', 'cut this into shorts', 'turn this video into reels', 'clips from this podcast'; RU: нарежь на шортс, сделай рилсы из видео, переупаковать, клипы из подкаста."
---

# reels-repurpose

One good long asset holds four to six short videos. Most people take one and throw the rest away.

## Before you write

1. Find the persona. The user names it ("for fix-it-dad") or there is only one in
   `~/.claude/minga-reels/personas/`. Read it. No persona yet: run /reels-persona first, or ask for
   three videos or captions in this voice and write the persona from them. A script in the wrong
   voice is a retake.
2. Never invent a number, a result, a client, a quote or an experience. If a line needs a figure
   the persona file does not have, write `{{your number}}` and flag it.
3. Reply in the user's language. Write the content in the persona's language.

## Extract, do not summarise

Read the whole thing first. Pull out, with counts:

| pull | becomes |
| --- | --- |
| claims that would start an argument | a video (opinion) |
| numbers: costs, durations, percentages | a video hook or a carousel slide |
| stories with a person, a scene and a cost | a video (story) |
| mechanisms: "the way this actually works is" | a carousel |
| mistakes someone admitted | a video (cost) |
| lines quotable as they are | a story frame or an on-screen card |

Fewer than four items means the source is thin, and four videos squeezed out of it will be thin
too. Say so.

## Cutting from the user's own footage

If the source is the user's video, use the real clip: the moment they said it, with the real
reaction, beats a re-record. A clip qualifies only if it opens on a complete thought (no "as I said
before"), has a turn in it, and ends on a line, 20 to 55 seconds. Give timecodes and write a NEW
first line or on-screen card for each, scored with /reels-hook, because the original line assumes
context this viewer does not have.

## Then

Vary the formulas across the set: five videos with the same hook shape read as a content mill.
Order: the strongest claim first, the story midweek, the mechanism last. Draft one at a time on
request through /reels-script, never four finished scripts at once.
