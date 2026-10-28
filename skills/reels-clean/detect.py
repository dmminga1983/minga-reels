#!/usr/bin/env python3
"""detect.py - score how human a draft reads, five local checks. Russian and English.

    python3 detect.py draft.txt                 # score one text
    python3 detect.py before.txt after.txt      # show the difference
    python3 detect.py draft.txt --json

    BURSTINESS    sentence lengths vary the way people write; generated text is even
    SPECIFICITY   numbers, names, money, durations per 100 words
    STOCK         stock phrases and bait from slop.json per 100 words (higher is cleaner)
    FINGERPRINT   invisible characters, long dashes, curly quotes, the ellipsis character
    VOICE         structural tells: "not just X, it's Y", staged one-word questions, preambles

The verdict is 60% the mean and 40% the weakest check, because one signal is enough to give a
text away. PASS needs 70 or more with no check under 55.

These are heuristics that run on your machine. They are not GPTZero, Originality or any other
detector, they call no service, and nobody can honestly promise "undetectable".
"""
import json
import math
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import ruen  # noqa: E402

LEX = json.load(open(os.path.join(HERE, "slop.json"), encoding="utf-8"))


def burstiness(text):
    lens = [len(ruen.words(s)) for s in ruen.sentences(text) if ruen.words(s)]
    if len(lens) < 3:
        return 70.0, "too few sentences to judge"
    mean = sum(lens) / len(lens)
    sd = math.sqrt(sum((x - mean) ** 2 for x in lens) / len(lens))
    cv = sd / mean if mean else 0
    return round(max(0, min(100, cv * 160)), 1), "variation %.2f across %d sentences" % (cv, len(lens))


def specificity(text, lg):
    n = max(1, len(ruen.words(text)))
    per100 = ruen.concrete(text, lg) * 100.0 / n
    return round(max(0, min(100, 30 + per100 * 12)), 1), "%.1f concrete markers per 100 words" % per100


def stock(text, lg):
    n = max(1, len(ruen.words(text)))
    k = ruen.count(text, LEX["delete"][lg]) + ruen.count(text, list(LEX["flag"][lg])) \
        + ruen.count(text, LEX["bait"][lg])
    per100 = k * 100.0 / n
    return round(max(0, 100 - per100 * 22), 1), "%d stock terms, %.1f per 100 words" % (k, per100)


def fingerprint(text):
    inv = sum(text.count(chr(int(cp, 16))) for cp, _ in LEX["invisible"])
    dash = text.count(chr(0x2014))
    curly = sum(text.count(c) for c in "“”‘’")
    ell = text.count("…")
    k = len(text) or 1
    per1k = (inv * 3 + dash * 2 + curly + ell) * 1000.0 / k
    s = max(0, 100 - per1k * 12 - (40 if inv else 0))
    return round(s, 1), "%d invisible, %d long dash, %d curly quote, %d ellipsis" % (inv, dash, curly, ell)


def voice(text, lg):
    tells = 0
    for s in LEX["structures"][lg]:
        if s["id"] == "triad":
            continue
        tells += len(re.findall(s["pattern"], text))
    triads = len(re.findall(next(s["pattern"] for s in LEX["structures"][lg] if s["id"] == "triad"), text))
    sents = max(1, len(ruen.sentences(text)))
    tells += max(0, triads - sents // 4)
    return round(max(0, 100 - tells * 15), 1), "%d structural tell(s)" % tells


def score(text):
    lg = ruen.lang(text)
    parts = {}
    parts["BURSTINESS"] = burstiness(text)
    parts["SPECIFICITY"] = specificity(text, lg)
    parts["STOCK"] = stock(text, lg)
    parts["FINGERPRINT"] = fingerprint(text)
    parts["VOICE"] = voice(text, lg)
    vals = [v[0] for v in parts.values()]
    total = round(0.6 * sum(vals) / len(vals) + 0.4 * min(vals), 1)
    verdict = "PASS" if total >= 70 and min(vals) >= 55 else "REVIEW" if total >= 55 else "FLAGGED"
    weakest = min(parts, key=lambda k: parts[k][0])
    return {"lang": lg, "checks": {k: {"score": v[0], "detail": v[1]} for k, v in parts.items()},
            "human": total, "verdict": verdict, "weakest": weakest}


def bar(v):
    k = int(round(v / 100 * 24))
    return "#" * k + "." * (24 - k)


def show(r, label=""):
    if label:
        print("\n  " + label)
    for k, v in r["checks"].items():
        print("  %-12s %s %5.1f   %s" % (k, bar(v["score"]), v["score"], v["detail"]))
    print("  " + "-" * 60)
    print("  %-12s %s %5.1f   %s" % ("HUMAN", bar(r["human"]), r["human"], r["verdict"]))


def main(argv=None):
    a = list(sys.argv[1:] if argv is None else argv)
    as_json = "--json" in a
    a = [x for x in a if x != "--json"]
    files = [x for x in a if os.path.exists(x)]
    if not files:
        print(__doc__)
        return 1
    res = [score(open(f, encoding="utf-8").read()) for f in files]
    if as_json:
        print(json.dumps(res if len(res) > 1 else res[0], ensure_ascii=False, indent=1))
        return 0
    for f, r in zip(files, res):
        show(r, f)
    if len(res) == 2:
        print("\n  delta %+.1f" % (res[1]["human"] - res[0]["human"]))
    print("\n  Weakest: %s. Fix that first." % res[-1]["weakest"])
    return 0


if __name__ == "__main__":
    sys.exit(main())
