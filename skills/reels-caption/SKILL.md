---
name: reels-caption
description: "Write and lint the text under a Reel (Instagram caption) or a YouTube Short (title and description): the visible first line, one ask, search phrases, hashtag limits, the AI label reminder. Use for 'caption', 'description', 'title for the short', 'hashtags'; RU: подпись, описание, заголовок для шортс, хештеги, текст под рилс."
---

# reels-caption

```bash
python3 caption.py caption.txt --keywords "акт приёмки,гарантия"
python3 caption.py --platform shorts --title "..." description.txt
python3 caption.py caption.txt --ai        # AI-generated person or voice in the video
```

## Before you write

1. Find the persona. The user names it ("for fix-it-dad") or there is only one in
   `~/.claude/minga-reels/personas/`. Read it. No persona yet: run /reels-persona first, or ask for
   three videos or captions in this voice and write the persona from them. A script in the wrong
   voice is a retake.
2. Never invent a number, a result, a client, a quote or an experience. If a line needs a figure
   the persona file does not have, write `{{your number}}` and flag it.
3. Reply in the user's language. Write the content in the persona's language.

## Instagram caption

Decide the job first and say which:

- **Job A, the video carries the hook.** The caption gives context, the one ask and the search
  phrases. It does not compete with the video.
- **Job B, the caption is the content** (photo, carousel). Line one is the hook and must land
  inside the first 125 characters, the part the feed shows before "... more".

Rules the tool enforces: 2,200 characters at most; up to **5 hashtags** (the cap since December
2025), specific ones, as labels; no link in the text (it is not clickable: bio, story or first
comment instead); one ask; no greeting, hashtag or emoji as the first character. Search reads the
caption, so the phrase a person would type goes into a normal sentence.

## YouTube Shorts title and description

Title up to 100 characters, with the point inside the first 50 that show in the mobile feed. The
description's first line is what shows above the fold. More than 60 hashtags across title and
description makes YouTube ignore all of them; three or four relevant ones are plenty.

## AI label

If the persona is an AI character or the video uses a generated voice or face, run with `--ai` and
include the reminder in the receipt: Instagram's AI label on the post, "altered or synthetic
content" in YouTube Studio.

## The loop

1. Draft. 2. /reels-clean. 3. `caption.py`, fix every FAIL, decide every WARN out loud.
4. Print the copy-ready block, then:

```
CAPTION READY  instagram, job A
visible:   118 of 125 before the cut
ask:       one, comment АКТ
hashtags:  3
search:    "акт приёмки" in line 2
AI label:  on
```

## The gate

Nothing here posts, comments, follows or sends. Every run ends with a copy-ready block and the
question: **post it, or change it?** The user publishes by hand.
