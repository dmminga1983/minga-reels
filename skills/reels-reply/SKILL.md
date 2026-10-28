---
name: reels-reply
description: "Handle comments under the persona's own videos and write comments on other people's: triage into buckets, replies in the persona's voice, which question deserves a video reply, never a pitch or a bot-sounding line. Use for 'reply to comments', 'answer this comment', 'someone wrote X under my reel', 'comment on this post'; RU: ответь на комментарии, что ответить, прокомментируй пост, хейтер в комментариях."
---

# reels-reply

## Before you write

1. Find the persona. The user names it ("for fix-it-dad") or there is only one in
   `~/.claude/minga-reels/personas/`. Read it. No persona yet: run /reels-persona first, or ask for
   three videos or captions in this voice and write the persona from them. A script in the wrong
   voice is a retake.
2. Never invent a number, a result, a client, a quote or an experience. If a line needs a figure
   the persona file does not have, write `{{your number}}` and flag it.
3. Reply in the user's language. Write the content in the persona's language.

## Under the persona's own video: triage first

Sort and say the counts before writing:

| bucket | what it gets |
| --- | --- |
| KEYWORD (the word the video asked for) | the promised thing, by hand or the platform's own auto-reply |
| LEAD (describes the problem the persona solves) | a full answer in public, then one sentence offering help |
| SUBSTANCE (data, disagreement, an addition) | the longest reply in the thread |
| QUESTION many people have | a video reply, not just a comment: hand it to /reels-hook as formula #16 |
| SUPPORT ("огонь", "спасибо", a tag) | a like and three to eight words at most |
| NOISE (spam, bait, abuse) | nothing. Hide abuse with the platform's controls |

Replies: answer the actual question in the first sentence, match the commenter's length, use
their name once without an exclamation mark. To a critic: concede the true part in their words,
then hold the line, once. Never argue a fact you cannot check.

## On other people's posts

Pick the type by what the post is: add a datum, add the missing case, disagree respectfully, extend
one line, ask the real question, a receipt from experience, a correction, a reframe, or a short
true one-liner. One to three sentences, one idea, never "отличный пост", never a restatement of
the video, never a link or a pitch. Give two options of different types and say which to post.

## AI characters

An AI persona replies as itself and never pretends to be a human with a real-life experience it
does not have. If someone sincerely asks whether it is real, it says it is an AI character.

## Never

Do not automate comments, likes or DMs to people who did not interact first; that breaks the
platforms' terms and gets accounts restricted. Keyword auto-replies through Instagram's own tools
or an approved partner, after someone comments, are fine.

Run every reply through /reels-clean. Short text makes a stock phrase louder.

## The gate

Nothing here posts, comments, follows or sends. Every run ends with a copy-ready block and the
question: **post it, or change it?** The user publishes by hand.
