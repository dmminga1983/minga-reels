#!/usr/bin/env python3
"""calibrate.py - measure hookscore.py on real videos instead of trusting it.

    python3 calibrate.py corpus.tsv

corpus.tsv is tab-separated with a header row: channel, views, hook. One row per video, the hook
being the first words actually said (or the first on-screen line). Take at least eight videos per
channel, ideally from four channels or more in your niche, including your own.

For every channel the tool splits its videos into the top third and the bottom third by views,
so a big channel and a small one are compared on equal terms. Then it reports the AUC: the chance
that a random top-third hook outscores a random bottom-third hook. 0.50 is a coin flip, 0.60 is a
weak signal, 0.70 and above is useful. It does the same for every property on its own, so you can
see which ones carry signal in your niche and which ones measure nothing.

How to collect Shorts on your own computer (public data, no login):
    python3 -m yt_dlp --flat-playlist --playlist-end 40 -J "https://www.youtube.com/@HANDLE/shorts"
    python3 -m yt_dlp --skip-download --write-auto-subs --sub-langs "ru.*,en.*" \
        --sub-format json3 -o hook "https://www.youtube.com/watch?v=VIDEO_ID"
Take the caption words that start before 3.0 seconds: that is the hook as it was said.
"""
import csv
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import hookscore  # noqa: E402


def auc(pos, neg):
    if not pos or not neg:
        return None
    wins = 0.0
    for p in pos:
        for n in neg:
            wins += 1.0 if p > n else 0.5 if p == n else 0.0
    return wins / (len(pos) * len(neg))


def load(path):
    with open(path, encoding="utf-8") as f:
        rows = list(csv.DictReader(f, delimiter="\t"))
    out = []
    for r in rows:
        try:
            out.append({"channel": r["channel"].strip(), "views": float(r["views"]),
                        "hook": r["hook"].strip()})
        except (KeyError, ValueError, AttributeError):
            continue
    return [r for r in out if r["hook"]]


def split(rows, min_per_channel=6):
    top, bottom, skipped = [], [], []
    by = {}
    for r in rows:
        by.setdefault(r["channel"], []).append(r)
    for ch, rs in sorted(by.items()):
        if len(rs) < min_per_channel:
            skipped.append(ch)
            continue
        rs = sorted(rs, key=lambda r: -r["views"])
        k = len(rs) // 3
        top += rs[:k]
        bottom += rs[-k:]
    return top, bottom, skipped


def calibrate(rows):
    top, bottom, skipped = split(rows)
    st = [hookscore.score(r["hook"]) for r in top]
    sb = [hookscore.score(r["hook"]) for r in bottom]
    res = {"top": len(top), "bottom": len(bottom), "skipped_channels": skipped,
           "auc": auc([s["verdict"] for s in st], [s["verdict"] for s in sb]), "properties": {}}
    for p in hookscore.PROPS:
        res["properties"][p] = auc([s["properties"][p] for s in st], [s["properties"][p] for s in sb])
    classified = sum(1 for s in st + sb if s["formula"])
    res["classified_share"] = classified / max(1, len(st) + len(sb))
    return res


def verdict(a):
    if a is None:
        return "not enough data"
    if a >= 0.70:
        return "useful"
    if a >= 0.60:
        return "weak signal"
    return "no better than a coin flip"


def main(argv=None):
    a = sys.argv[1:] if argv is None else argv
    if not a or not os.path.exists(a[0]):
        print(__doc__)
        return 1
    res = calibrate(load(a[0]))
    print("CALIBRATION  top third %d hooks, bottom third %d" % (res["top"], res["bottom"]))
    if res["skipped_channels"]:
        print("  skipped (under 6 videos): " + ", ".join(res["skipped_channels"]))
    v = res["auc"]
    print("  overall AUC   %s  %s" % ("-" if v is None else "%.2f" % v, verdict(v)))
    for p, v in res["properties"].items():
        print("  %-12s  %s  %s" % (p, "-" if v is None else "%.2f" % v, verdict(v)))
    print("  formulas named %.0f%% of hooks" % (100 * res["classified_share"]))
    print("\n  Use what this says. A property near 0.50 in your niche is measuring nothing there.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
