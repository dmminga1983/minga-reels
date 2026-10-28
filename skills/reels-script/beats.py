#!/usr/bin/env python3
"""beats.py - time a Reel or Shorts script before you shoot it. Russian and English.

    python3 beats.py script.txt --target 30
    python3 beats.py script.txt --target 45 --pace 5.5     # your pace, syllables per second
    python3 beats.py script.txt --json

One spoken line is one beat. Lines in square brackets, or starting with "ЭКРАН:" or "SCREEN:",
are on-screen notes: shown in the sheet, not timed. Speaking time is counted in syllables,
because Russian packs more syllables into a word and a words-per-minute pace from English guides
overestimates how much fits.

It flags the five things that kill a short video in the edit:
    the hook takes longer than 3 seconds to say
    one beat runs longer than 4 seconds: a static frame is where people leave
    three beats in a row with nothing concrete in them
    no loop: the last line shares no word with the first, so the replay does not land
    the total is far from the target length
"""
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import ruen  # noqa: E402

NOTE = re.compile(r"^\s*(\[.*\]|(экран|screen|on screen|на экране)\s*:.*)$", re.I)
STOP = set(("и в во не на с со что как а но это то же за к ко по из у о об от для до так "
            "the a an and or but to of in on at for is it this that with you i we").split())


def content_words(text):
    return {w for w in ruen.words(text) if len(w) > 3 and w not in STOP}


def stem(w):
    return w[:5] if ruen.CYR.search(w) else w[:6]


def sheet(text, target=None, pace=None):
    lines = [l.rstrip() for l in text.splitlines() if l.strip()]
    beats, notes = [], []
    lg = ruen.lang(text)
    t = 0.0
    for l in lines:
        if NOTE.match(l):
            notes.append({"at": round(t, 1), "text": l.strip()})
            if beats:
                beats[-1]["screen"].append(l.strip())
            continue
        sec = ruen.speech_seconds(l, lg, pace)
        beats.append({"start": round(t, 1), "seconds": round(sec, 1), "text": l.strip(),
                      "concrete": ruen.concrete(l, lg) > 0, "screen": []})
        t += sec
    flags = []
    if not beats:
        return {"lang": lg, "beats": [], "total": 0, "flags": ["no spoken lines found"],
                "words": 0}
    beats[0]["role"] = "HOOK"
    beats[-1]["role"] = "END"
    if len(beats) > 2:
        beats[1]["role"] = "STAKE"
    if beats[0]["seconds"] > 3.0:
        flags.append({"ru": "хук звучит %.1f с: больше трёх секунд, сократите" % beats[0]["seconds"],
                      "en": "the hook takes %.1fs to say: over three seconds, cut it" % beats[0]["seconds"]}[lg])
    for i, b in enumerate(beats):
        if b["seconds"] > 4.0:
            flags.append({"ru": "бит %d длится %.1f с: разбейте строку или смените кадр внутри неё" % (i + 1, b["seconds"]),
                          "en": "beat %d runs %.1fs: split the line or change the frame inside it" % (i + 1, b["seconds"])}[lg])
    run = 0
    for i, b in enumerate(beats):
        run = 0 if b["concrete"] else run + 1
        if run == 3:
            flags.append({"ru": "биты %d-%d без единой конкретики: добавьте цифру, имя или пример" % (i - 1, i + 1),
                          "en": "beats %d-%d have nothing concrete: add a number, a name or an example" % (i - 1, i + 1)}[lg])
    first = {stem(w) for w in content_words(beats[0]["text"])}
    last = {stem(w) for w in content_words(beats[-1]["text"])}
    loop = bool(first & last) and len(beats) > 1
    if not loop and len(beats) > 1:
        flags.append({"ru": "нет петли: повторите в последней строке слово из хука, тогда повторный просмотр сработает",
                      "en": "no loop: echo a word from the hook in the last line so the replay lands"}[lg])
    if target:
        diff = t - target
        if abs(diff) > max(3.0, target * 0.15):
            more = "длиннее" if diff > 0 else "короче"
            flags.append({"ru": "на %.1f с %s цели в %d с" % (abs(diff), more, target),
                          "en": "%.1fs %s than the %ds target" % (abs(diff), "longer" if diff > 0 else "shorter", target)}[lg])
    return {"lang": lg, "beats": beats, "total": round(t, 1), "flags": flags, "loop": loop,
            "words": sum(len(ruen.words(b["text"])) for b in beats), "target": target}


def fmt(s):
    m, sec = divmod(s, 60)
    return "%d:%04.1f" % (m, sec)


def main(argv=None):
    a = list(sys.argv[1:] if argv is None else argv)
    as_json = "--json" in a
    a = [x for x in a if x != "--json"]
    target = pace = None
    if "--target" in a:
        i = a.index("--target")
        target = float(a[i + 1])
        del a[i:i + 2]
    if "--pace" in a:
        i = a.index("--pace")
        pace = float(a[i + 1])
        del a[i:i + 2]
    if not a or not os.path.exists(a[0]):
        print(__doc__)
        return 1
    r = sheet(open(a[0], encoding="utf-8").read(), target, pace)
    if as_json:
        print(json.dumps(r, ensure_ascii=False, indent=1))
        return 0
    print("BEAT SHEET  %d words  ~%.1fs%s" % (r["words"], r["total"],
                                             "  target %ds" % target if target else ""))
    print("=" * 72)
    for b in r["beats"]:
        print("  %s  %4.1fs  %-6s %s" % (fmt(b["start"]), b["seconds"], b.get("role", ""), b["text"][:56]))
        for s in b["screen"]:
            print("  %s  %5s  %-6s %s" % (" " * 6, "", "", s[:56]))
    print("-" * 72)
    for f in r["flags"]:
        print("  - " + f)
    if not r["flags"]:
        print("  clean")
    return 0


if __name__ == "__main__":
    sys.exit(main())
