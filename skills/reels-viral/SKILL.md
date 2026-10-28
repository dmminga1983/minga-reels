---
name: reels-viral
description: "Find what is working right now in the persona's niche on Reels and Shorts, rank each video by how far it beat its own account's median, name the hook formula, and turn it into a swipe file and hooks the persona could say tomorrow. Use for 'what's working', 'find viral reels', 'competitor research', 'swipe file', 'why did this blow up'; RU: что сейчас заходит, найди вирусные ролики, разбор конкурентов, почему этот ролик залетел."
---

# reels-viral

The research skill. Run it monthly, not daily: formulas last a season.

```bash
python3 swipe.py captured.tsv --out ~/.claude/minga-reels/swipe.md
```

Needs `../reels-hook` next to it for formula names and scores.

## The idea

Raw views rank account size. Rank by the **outlier multiple**: views over that account's own
median. Above 3x is a signal; under 1.5x is a normal day and teaches nothing. Pick accounts within
about 10x of the persona's size: a format that works at two million followers often works because
of the two million.

## Step 1: accounts

6 to 12, proposed and approved: 4 in the niche, 4 adjacent (same audience, different topic, where
formats arrive first), 2 to 4 much bigger ones for format only.

## Step 2: collect, reading not scraping

- **Shorts** have public view counts and captions. On the user's own computer:
  `python3 -m yt_dlp --flat-playlist --playlist-end 40 -J "https://www.youtube.com/@HANDLE/shorts"`
  for views, and auto-captions (`--write-auto-subs --sub-langs "ru.*,en.*"`) for the spoken first
  line. The cloud session usually cannot reach YouTube; say so and ask the user to run it locally.
- **Instagram** has no public API for this. Read reels in the user's own browser at human speed,
  with the user present, a dozen per account. Never log in for them, never ask for a password,
  never loop it in the background or use a scraping service: that gets accounts blocked and breaks
  the platform's terms.

Per video: account, median (middle of its last 12), views, hook (verbatim, as said), optional
platform, length, url. Write `captured.tsv` with a header row.

## Step 3: read it carefully

Report three things: formulas over-indexing in the top third (with counts), what the top third
share structurally (hook length, video length, where the ask sits), and the unclassified hooks,
read by hand, because a formula missing from `hooks.json` hides there. State the sample size: 40
videos across 6 accounts supports a claim, 12 does not.

## Step 4: the persona's version

For the top three formulas, write the persona's own hook in that shape, with its own facts. Never
"make one like this": copy the shape, never the script, the voice or the edit, and attribute every
row in the swipe file.

Nothing is followed, liked or messaged by this skill. It reads.
