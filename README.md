# minga-reels

**Eleven Claude skills for Instagram Reels and YouTube Shorts, in Russian and English: personas and AI characters, hooks scored by a tool that runs, timed scripts, captions checked against the platforms' limits, research, cleanup, plans, audits and replies.**

Part of the [Minga](https://github.com/dmminga1983/minga) ecosystem. One pack for both platforms, built around persona files, so one person can run several accounts or test several AI characters without their voices bleeding into each other. Free, MIT, no API key, nothing to connect. **Nothing is posted for you:** every skill ends with a copy-ready block and the question "post it, or change it?".

[Русская версия →](README.ru.md)

## The eleven

| command | what it does |
| --- | --- |
| `/reels-persona` | The persona file every skill reads: who it talks to, how it sounds, what it may claim. A real creator or an AI character. |
| `/reels-hook` | Hook options from [26 formulas](skills/reels-hook/hooks.json), scored by `hookscore.py`, weakest property named with the fix. Calibrates on your own videos. |
| `/reels-script` | One idea into a script: spoken lines, a separate on-screen track, a beat sheet timed by `beats.py`. Carousels too. |
| `/reels-caption` | Instagram caption or Shorts title and description, linted by `caption.py`: the 125 visible characters, 5 hashtags, one ask, the AI label. |
| `/reels-viral` | What works in the niche now, ranked by each video's multiple over its own account's median, with the formula named. |
| `/reels-clean` | Removes invisible characters, long dashes and empty intros, flags stock words and bait, scores the text with five local checks. |
| `/reels-plan` | The week for one persona, or a fair niche test across several: same count, same days, same platforms, the rule decided in advance. |
| `/reels-audit` | Your own numbers: outlier multiple, hold at 3 seconds, sends and follows per 1,000 reach, comparison by persona or platform. |
| `/reels-reply` | Comment triage under your videos and comments on other people's, in the persona's voice. |
| `/reels-repurpose` | One long video, podcast or document into standalone shorts, cut from your own footage where possible. |
| `/reels-character` | For AI characters: the character bible, a prompt skeleton, a shot per beat, and the labelling rules. |

## Install

**Claude Code**, as a plugin:

```
/plugin marketplace add dmminga1983/minga-reels
/plugin install minga-reels@minga-reels
```

Or copy the folders to get plain `/reels-hook` and so on:

```bash
git clone https://github.com/dmminga1983/minga-reels.git
cp -r minga-reels/skills/reels-* ~/.claude/skills/
```

**claude.ai**: zip one skill folder and upload it under Settings, Capabilities, Skills. The method works without Claude Code; the tools need a session that can run Python.

The tools need Python 3.8 or newer and nothing else.

Then create the first persona: `/reels-persona`, or send Claude three of your videos and say "write the persona from these". Files live in `~/.claude/minga-reels/`.

## The tools

All standard-library Python, no network, nothing uploaded. Russian or English is detected per text.

```bash
python3 skills/reels-hook/hookscore.py hooks.txt               # six-property hook panel
python3 skills/reels-hook/calibrate.py corpus.tsv              # does the score work in your niche?
python3 skills/reels-script/beats.py script.txt --target 30    # timed beat sheet
python3 skills/reels-caption/caption.py caption.txt --ai       # caption linter
python3 skills/reels-caption/caption.py --platform shorts --title "..." desc.txt
python3 skills/reels-clean/clean.py draft.txt -o clean.txt --report
python3 skills/reels-clean/detect.py draft.txt clean.txt       # five checks, before and after
python3 skills/reels-viral/swipe.py captured.tsv               # outliers by own-account multiple
python3 skills/reels-audit/audit.py posts.csv --by persona     # what worked, which persona won
```

**Speaking time is counted in syllables**, because Russian packs more syllables into a word and a words-per-minute pace from English guides overestimates what fits into three seconds. **Numbers said as words count as concrete**: "сорок тысяч" is as specific as "40 000". **The formula classifier knows every one of its 26 examples in both languages**, and a test checks it.

```bash
python3 -m unittest discover -s tests -v
```

## The fine print

- **It does not post, comment, like, follow or DM.** Automating those through a browser or a third-party tool breaks Instagram's terms and gets accounts restricted. The one exception the skills mention is keyword auto-replies through Instagram's own tools or an approved partner, after someone comments first.
- **`hookscore.py` is a heuristic.** It reliably catches weak hooks: greetings, preambles, hype instead of facts, more than three seconds to say. It cannot pick the winner between two decent hooks; your face, edit, sound and the platform decide that. `calibrate.py` measures how well it works on your own videos, property by property, and tells you which ones mean nothing in your niche.
- **The five text checks are local heuristics**, not GPTZero or any other detector. Nobody can honestly promise "undetectable".
- **Nothing is invented.** No numbers, clients, results or experiences under a persona's name. A missing figure comes back as `{{your number}}` and a flag.
- **AI characters are labelled.** Instagram's AI label and YouTube's altered-or-synthetic setting on every video, no real person's likeness or voice, no claimed professional credentials.
- **Platform numbers move.** The limits in `caption.py` were checked in October 2026 (Instagram's 5-hashtag cap dates from December 2025). If the platform says otherwise, the platform is right: edit the `LIMITS` table.
- **Research reads, it does not scrape.** Public Shorts data with `yt-dlp` on your own computer; Instagram in your own browser, at human speed, with you there.

## Credit

Made by [dmminga1983](https://github.com/dmminga1983). Inspired by Jake Schincariol's [instagram-agent-skill](https://github.com/Jakeschincariol/instagram-agent-skill); the formulas, lexicon, tools and skills here are written from scratch, for Russian and English.

## License

MIT.
