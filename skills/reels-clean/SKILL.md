---
name: reels-clean
description: "Strip the machine fingerprint from any script, caption, comment or reply before it is shown or posted: invisible characters, long dashes, curly quotes, empty intros, stock words and bait in Russian and English, then a five-check human score. Use for 'clean this', 'does this sound like AI', 'remove dashes', 'de-slop'; RU: почисти текст, убери признаки ИИ, звучит как нейросеть, убери тире. Runs after every other reels skill."
---

# reels-clean

Two tools that run, and the minga-humanize-text skill for the part a script cannot do.

```bash
python3 clean.py draft.txt -o clean.txt --report    # fix what is safe, list what needs a human
python3 detect.py draft.txt clean.txt               # five checks, before and after
```

## Order

1. `clean.py --report`. It removes invisible characters, turns long dashes into commas or hyphens,
   straightens curly quotes (Russian guillemets stay), and deletes empty intros such as "важно
   отметить, что" and "в современном мире". URLs are never touched.
2. Read the REWRITE BY HAND list: stock words with a suggestion, bait ("подпишись", "follow for
   more"), structures ("это не просто X, это Y", one-word staged questions, preambles, emoji
   bullets, shouting, hashtag walls). Rewrite those lines yourself, keeping the meaning. If the
   minga-humanize-text skill is installed, use it for this pass.
3. Every long dash replaced in Russian: re-read that sentence. A dash between subject and
   predicate ("Москва, столица") may need rewording, not just a comma.
4. `detect.py before after`. PASS needs 70 with no check under 55. Two rounds is normal; five means
   the draft was written by formula and needs a new draft, not more passes.
5. Show the cleaned text and the score. Never the score alone.

## Honest limits

These checks run locally and are modelled on what detectors look for. They are not GPTZero or any
other service, they call nothing, and no one can promise "undetectable". What they reliably do:
remove the mechanical traces and point at the lines a reader would notice.

`slop.json` is meant to be edited. If the persona really uses a word on the list, take it out.
