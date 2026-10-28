#!/usr/bin/env python3
"""caption.py - lint the text that goes under a Reel or a Short. Russian and English.

    python3 caption.py caption.txt                                  # Instagram caption
    python3 caption.py caption.txt --keywords "акт приёмки,гарантия"
    python3 caption.py --platform shorts --title "..." description.txt
    python3 caption.py caption.txt --ai          # the video uses AI-generated people or voices

Instagram: about 125 characters show before "... more", 2,200 is the limit, and since
December 2025 a post can carry at most 5 hashtags. Captions are not clickable, so a link there
is dead text.
YouTube Shorts: title up to 100 characters (about the first 50 show in the mobile feed),
description up to 5,000 with roughly the first 100 above the fold, and more than 60 hashtags in
title and description together makes YouTube ignore all of them.

Platform numbers move. If this file disagrees with the platform, the platform is right: change
the LIMITS table below.
"""
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import ruen  # noqa: E402

LIMITS = {
    "instagram": {"visible": 125, "max": 2200, "hashtags": 5},
    "shorts": {"title": 100, "title_visible": 50, "max": 5000, "visible": 100, "hashtags": 60},
}
HASHTAG = re.compile(r"(?<!\w)#[\wЀ-ӿ]+")
URL = re.compile(r"https?://\S+|www\.\S+|\b\w+\.(ru|com|рф|io|me|net|org)/\S*", re.I)
EMOJI = re.compile("[\U0001F300-\U0001FAFF☀-➿\U0001F000-\U0001F2FF]")
DEAD_TAGS = {"#viral", "#fyp", "#foryou", "#explorepage", "#рекомендации", "#рек", "#хочуврек",
             "#вреки", "#reels", "#shorts", "#тренды"}
ASKS = {
    "ru": [r"\bнапиш\w*\s(в\s)?коммент\w*", r"\bпиши\s+\S+\s+в\sкоммент", r"\bсохран\w*\b",
           r"\bподпи[сш]\w*", r"\bперешл\w*\b", r"\bотправ\w*\s(другу|подруге|тому)", r"\bотметь\w*\b",
           r"\bссылк\w*\sв\s(шапке|профиле|описании)", r"\bнапиш\w*\sв\s(директ|личк\w*)",
           r"\bставь\w*\sлайк", r"\bжми\w*\b"],
    "en": [r"\bcomment\b", r"\bsave (this|it)\b", r"\bfollow\b", r"\bshare (this|it)\b", r"\btag\b",
           r"\blink in (bio|profile)\b", r"\bdm me\b", r"\blike (this|if)\b"],
}


def box(text, width=54, limit=125):
    shown = text.replace("\n", " ")[:limit]
    rows, line = [], ""
    for w in shown.split(" "):
        if len(line) + len(w) + 1 > width:
            rows.append(line)
            line = w
        else:
            line = (line + " " + w).strip()
    rows.append(line)
    out = ["  +" + "-" * (width + 2) + "+"]
    out += ["  | %-*s |" % (width, r) for r in rows]
    out.append("  +" + "-" * (width - 8) + " ... more +")
    return "\n".join(out)


def count_asks(text, lg):
    return sum(1 for p in ASKS[lg] if re.search(p, text, re.I))


def lint_instagram(text, keywords=(), ai=False):
    L = LIMITS["instagram"]
    lg = ruen.lang(text)
    res = []
    first = text.strip().split("\n")[0]
    n = len(text)
    res.append(("FAIL" if n > L["max"] else "PASS", "LENGTH", "%d / %d characters" % (n, L["max"])))
    if len(first) > L["visible"]:
        res.append(("WARN", "FIRST LINE", "%d characters: the feed cuts it at %d mid-thought"
                    % (len(first), L["visible"])))
    else:
        res.append(("PASS", "FIRST LINE", "%d characters, fits before the cut" % len(first)))
    head = text[:L["visible"]]
    if first[:1] in "#@" or EMOJI.match(first[:2] or " "):
        res.append(("FAIL", "OPENING", "starts with a hashtag, a mention or an emoji"))
    if ruen.hits(" ".join(ruen.words(first)[:4]), ruen.PREAMBLE[lg]):
        res.append(("FAIL", "OPENING", "starts with a greeting or a preamble"))
    c = ruen.concrete(head, lg)
    res.append(("PASS" if c else "WARN", "CONCRETE", "%d numbers or names in the visible window" % c))
    tags = HASHTAG.findall(text)
    if len(tags) > L["hashtags"]:
        res.append(("FAIL", "HASHTAGS", "%d tags: Instagram allows %d" % (len(tags), L["hashtags"])))
    else:
        res.append(("PASS", "HASHTAGS", "%d tag(s)%s" % (len(tags), ": " + " ".join(tags) if tags else "")))
    dead = [t for t in tags if t.lower() in DEAD_TAGS]
    if dead:
        res.append(("WARN", "EMPTY TAGS", "describe nothing: " + " ".join(dead)))
    asks = count_asks(text, lg)
    res.append(("PASS" if asks == 1 else "WARN", "ONE ASK",
                "%d calls to action%s" % (asks, "" if asks == 1 else ": keep exactly one")))
    if URL.search(text):
        res.append(("WARN", "LINK", "captions are not clickable: put it in the bio, a story or the first comment"))
    e = len(EMOJI.findall(text))
    if n and e * 100.0 / n > 4:
        res.append(("WARN", "EMOJI", "%d emoji: use them as punctuation, not decoration" % e))
    if keywords:
        miss = [k for k in keywords if k.lower().replace("ё", "е") not in text.lower().replace("ё", "е")]
        res.append(("PASS" if not miss else "WARN", "SEARCH TERMS",
                    "%d/%d present%s" % (len(keywords) - len(miss), len(keywords),
                                         ". Missing: " + ", ".join(miss) if miss else "")))
    if chr(0x2014) in text:
        res.append(("WARN", "LONG DASH", "reads as generated text: run reels-clean"))
    if ai:
        res.append(("TODO", "AI LABEL", "turn on Instagram's AI label for this post before publishing"))
    return res, box(text, limit=L["visible"])


def lint_shorts(title, text, keywords=(), ai=False):
    L = LIMITS["shorts"]
    lg = ruen.lang(title + " " + text)
    res = []
    t = len(title)
    res.append(("FAIL" if t > L["title"] else "PASS", "TITLE", "%d / %d characters" % (t, L["title"])))
    if t > L["title_visible"]:
        res.append(("WARN", "TITLE CUT", "about %d show in the mobile feed: the point must be in them"
                    % L["title_visible"]))
    if ruen.hits(title, ruen.HYPE[lg]):
        res.append(("WARN", "TITLE HYPE", "adjectives where a number or a name should be: "
                    + ", ".join(ruen.hits(title, ruen.HYPE[lg]))))
    n = len(text)
    res.append(("FAIL" if n > L["max"] else "PASS", "DESCRIPTION", "%d / %d characters" % (n, L["max"])))
    if text.strip() and len(text.strip().split("\n")[0]) > L["visible"]:
        res.append(("WARN", "ABOVE THE FOLD", "first line over %d characters" % L["visible"]))
    tags = HASHTAG.findall(title + " " + text)
    if len(tags) > L["hashtags"]:
        res.append(("FAIL", "HASHTAGS", "%d tags: over %d and YouTube ignores all of them"
                    % (len(tags), L["hashtags"])))
    else:
        res.append(("PASS", "HASHTAGS", "%d tag(s); the first three may show above the title" % len(tags)))
    if keywords:
        both = (title + " " + text).lower().replace("ё", "е")
        miss = [k for k in keywords if k.lower().replace("ё", "е") not in both]
        res.append(("PASS" if not miss else "WARN", "SEARCH TERMS",
                    "%d/%d present%s" % (len(keywords) - len(miss), len(keywords),
                                         ". Missing: " + ", ".join(miss) if miss else "")))
    if ai:
        res.append(("TODO", "AI LABEL", "set 'altered or synthetic content' in YouTube Studio before publishing"))
    return res, None


def main(argv=None):
    a = list(sys.argv[1:] if argv is None else argv)
    opts = {"platform": "instagram", "keywords": "", "title": ""}
    ai = "--ai" in a
    a = [x for x in a if x != "--ai"]
    for k in list(opts):
        flag = "--" + k
        if flag in a:
            i = a.index(flag)
            opts[k] = a[i + 1]
            del a[i:i + 2]
    text = open(a[0], encoding="utf-8").read() if a and os.path.exists(a[0]) else ""
    if not text and not opts["title"]:
        print(__doc__)
        return 1
    kws = [k.strip() for k in opts["keywords"].split(",") if k.strip()]
    if opts["platform"] == "shorts":
        res, preview = lint_shorts(opts["title"], text, kws, ai)
    else:
        res, preview = lint_instagram(text, kws, ai)
        print("\n  WHAT THE FEED SHOWS\n" + preview + "\n")
    for status, name, msg in res:
        print("  %-4s  %-15s %s" % (status, name, msg))
    fails = sum(1 for r in res if r[0] == "FAIL")
    print("\n  %s" % ("READY" if not fails else "%d FAIL: fix before posting" % fails))
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
