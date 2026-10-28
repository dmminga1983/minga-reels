---
name: reels-audit
description: "Post-mortem on what a persona already posted: ranks videos by outlier multiple and sends per reach instead of views, finds what separates hits from misses, compares personas or platforms in a niche test, and says when the problem is the profile rather than the hooks. Use for 'what's working', 'why did this flop', 'read my stats', 'audit my reels', 'which niche won'; RU: разбор статистики, почему не залетело, что работает, какая ниша выиграла."
---

# reels-audit

The only honest evidence about an account is that account. Every rule in every guide, including
this pack, is a prior.

```bash
python3 audit.py posts.csv
python3 audit.py posts.csv --by persona      # niche test
python3 audit.py posts.csv --by platform     # Instagram against Shorts
```

## Input

Ask for whatever the user has, as a table or screenshots you turn into `posts.csv`: views, reach,
non-follower share, hold at 3 seconds, average watch time, length, shares, saves, comments,
follows, plus persona, platform, the formula and the hook if known (`~/.claude/minga-reels/log.md`
has them for videos written with this pack). Only views is required.

## What to look at

- **Outlier multiple** (views over the account's median) instead of views.
- **Hold at 3 seconds** is the hook's grade. If the top and bottom differ here, it is the hook and
  nothing else.
- **Sends per 1,000 reach**: the strongest signal a viewer can give.
- **Follows per 1,000 reach**: whether the profile converts attention.
- Formula, format, length, theme. Day and time last, and only if nothing else shows anything.

**Views without follows is a profile problem, not a hook problem.** If non-follower reach is high
and follows are low, stop rewriting hooks and fix the profile: name field, bio line one, pinned
videos, highlights.

## Niche test

With `--by persona`, compare only groups of 8 or more posts over the same period and platforms.
Report medians, not the one lucky video. Say which persona wins on which measure, and if they are
within noise, say that too: "no winner yet" is a result.

## Output

The tool's ranking, then three or four findings, each a claim with its evidence and confidence,
then STOP (one thing to stop making) and DO MORE (one thing to make more of). Hand the conclusions
to /reels-plan and /reels-viral.
