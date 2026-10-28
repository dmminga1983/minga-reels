---
name: reels-script
description: "Turn one idea into a full Reel or YouTube Short script for a named persona: the hook, the spoken lines, a separate on-screen text track, and a timed beat sheet checked by a local tool. Use for 'write a reel', 'script a short', 'make a video about X', 'what do I say in this video'; RU: напиши сценарий, сделай рилс, сценарий для шортс, что говорить в ролике."
---

# reels-script

One idea in, one script somebody finishes out.

```bash
python3 beats.py script.txt --target 30
python3 beats.py script.txt --target 45 --pace 5.5
```

## Before you write

1. Find the persona. The user names it ("for fix-it-dad") or there is only one in
   `~/.claude/minga-reels/personas/`. Read it. No persona yet: run /reels-persona first, or ask for
   three videos or captions in this voice and write the persona from them. A script in the wrong
   voice is a retake.
2. Never invent a number, a result, a client, a quote or an experience. If a line needs a figure
   the persona file does not have, write `{{your number}}` and flag it.
3. Reply in the user's language. Write the content in the persona's language.

## The shape

```
0-3s      HOOK     the claim. Spoken line and on-screen line written separately.
3-7s      STAKE    why this matters to the one viewer. One line.
7s-end    BODY     one idea per beat, and the frame changes every beat.
last 3s   PAYOFF   deliver what the hook promised, then one ask.
last line LOOP     echo a word from the hook so the replay lands.
```

Length: 15 to 45 seconds for most ideas. Shorts and Reels both allow up to 3 minutes; almost nothing
needs it.

## The loop

1. **Hook.** If none is chosen yet, run /reels-hook and take the winner.
2. **Write** in the persona's voice: short lines, the words it uses, none it never says. One idea
   per video: if the script has two, it is two videos. Say so.
3. **On-screen track** as its own list: six words or fewer per card, the hook card from frame one,
   inside the safe zone (on 1080x1920 keep text between y=250 and y=1450 and clear of the right
   220 px, where the buttons sit). Burned-in captions for the body: most people watch muted first.
4. **Time it** with `beats.py`. Fix every flag: a hook over 3 seconds, a beat over 4, three beats
   with nothing concrete, no loop, far from the target. Re-run until clean.
5. **Clean it** with /reels-clean before showing it. A written-sounding line is obvious the moment
   someone says it.
6. **Carousels**: if the idea is steps to re-read rather than something to watch, write it as a
   carousel instead: 6 to 10 slides, cover of six words or fewer, one idea per slide, a recap slide
   people screenshot, one ask on the last.

## Output

The script in a fenced block, the on-screen cards with timings, then:

```
REEL READY  (persona: <slug>)
hook:       #2 Цена ошибки, 61 OK
length:     27.4s, 9 beats
on-screen:  6 cards
clean:      3 fixes, human score 78 PASS
next:       /reels-caption
```

On "yes", append a line to `~/.claude/minga-reels/log.md`: date, persona, formula, first line. The
audit uses it later.

## The gate

Nothing here posts, comments, follows or sends. Every run ends with a copy-ready block and the
question: **post it, or change it?** The user publishes by hand.
