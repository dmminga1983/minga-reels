#!/usr/bin/env python3
"""swipe.py - rank short videos by how far each beat its own account, and name the hook formula.

    python3 swipe.py captured.tsv
    python3 swipe.py captured.tsv --out ~/.claude/minga-reels/swipe.md
    python3 swipe.py captured.tsv --min 3

captured.tsv is tab-separated with a header row:
    account  median  views  hook            (required)
    platform followers length cta url       (optional)

median is that account's typical views: eyeball its last 12 videos and take the middle one.
Raw views rank account size, not ideas. The outlier multiple, views over the account's own
median, is the only version of the question that is about the video. Above 3x is a signal.
Below 1.5x is that account's normal day and teaches nothing.

Formula names and hook scores come from ../reels-hook. If that folder is not installed next to
this one, the ranking still works and those two columns stay empty.
"""
import csv
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
HOOK_DIR = os.path.join(HERE, "..", "reels-hook")
try:
    sys.path.insert(0, HOOK_DIR)
    import hookscore  # noqa: E402
except Exception:  # pragma: no cover - only when the sibling skill is missing
    hookscore = None


def num(x):
    try:
        return float(str(x).replace(" ", "").replace(",", "").replace(" ", ""))
    except ValueError:
        return None


def load(path):
    with open(path, encoding="utf-8") as f:
        rows = list(csv.DictReader(f, delimiter="\t"))
    out, bad = [], 0
    for r in rows:
        med, views = num(r.get("median", "")), num(r.get("views", ""))
        hook = (r.get("hook") or "").strip()
        if not med or views is None or not hook:
            bad += 1
            continue
        out.append({"account": (r.get("account") or "?").strip(), "median": med, "views": views,
                    "hook": hook, "platform": (r.get("platform") or "").strip(),
                    "length": num(r.get("length", "")) if r.get("length") else None,
                    "url": (r.get("url") or "").strip()})
    return out, bad


def analyse(rows, min_multiple=3.0):
    for r in rows:
        r["multiple"] = round(r["views"] / r["median"], 1)
        if hookscore:
            s = hookscore.score(r["hook"])
            r["score"], r["formula"], r["formula_name"] = s["verdict"], s["formula"], s["formula_name"]
            r["words"] = len(s["hook"].split())
        else:
            r["score"] = r["formula"] = r["formula_name"] = None
            r["words"] = len(r["hook"].split())
    rows.sort(key=lambda r: -r["multiple"])
    k = max(1, len(rows) // 3)
    top, bottom = rows[:k], rows[-k:]

    def counts(rs):
        c = {}
        for r in rs:
            if r["formula"]:
                c[r["formula_name"]] = c.get(r["formula_name"], 0) + 1
        return c

    def median(xs):
        xs = sorted(x for x in xs if x is not None)
        return xs[len(xs) // 2] if xs else None

    accounts = sorted({r["account"] for r in rows})
    return {
        "rows": rows, "outliers": [r for r in rows if r["multiple"] >= min_multiple],
        "top_formulas": counts(top), "bottom_formulas": counts(bottom),
        "top_words": median([r["words"] for r in top]),
        "bottom_words": median([r["words"] for r in bottom]),
        "top_length": median([r["length"] for r in top]),
        "bottom_length": median([r["length"] for r in bottom]),
        "unclassified": [r for r in rows if not r["formula"]],
        "accounts": accounts,
        "confidence": "enough to support a claim" if len(rows) >= 30 and len(accounts) >= 5
        else "too small for a claim, treat as hints",
    }


def render(res):
    rows = res["rows"]
    out = ["SWIPE  %d videos  %d accounts  baseline: each account's own median" % (
        len(rows), len(res["accounts"])), "=" * 78, "", "OUTLIERS"]
    for r in res["outliers"] or rows[:5]:
        out.append("  %6.1fx  hook %5s  %-22s %-16s %10d" % (
            r["multiple"], "-" if r["score"] is None else "%.0f" % r["score"],
            (r["formula_name"] or "unclassified")[:22], r["account"][:16], r["views"]))
        out.append('          "%s"' % r["hook"][:68])
    out += ["", "WHAT IS OVER-INDEXING (top third vs bottom third)"]
    for name, c in sorted(res["top_formulas"].items(), key=lambda kv: -kv[1]):
        out.append("  %-24s x%d up top, x%d at the bottom" % (name, c, res["bottom_formulas"].get(name, 0)))
    if res["top_words"] is not None:
        out.append("  hook length            %s words up top, %s at the bottom" % (
            res["top_words"], res["bottom_words"]))
    if res["top_length"] is not None:
        out.append("  video length           %ss up top, %ss at the bottom" % (
            res["top_length"], res["bottom_length"]))
    out += ["", "UNCLASSIFIED (%d): read these by hand, a new formula may be hiding here" % len(res["unclassified"])]
    for r in res["unclassified"][:10]:
        out.append('  %5.1fx  %s: "%s"' % (r["multiple"], r["account"], r["hook"][:60]))
    out += ["", "SAMPLE  %d videos across %d accounts: %s" % (len(rows), len(res["accounts"]), res["confidence"])]
    return "\n".join(out)


def main(argv=None):
    a = list(sys.argv[1:] if argv is None else argv)
    out_path, mn = None, 3.0
    if "--out" in a:
        i = a.index("--out")
        out_path = os.path.expanduser(a[i + 1])
        del a[i:i + 2]
    if "--min" in a:
        i = a.index("--min")
        mn = float(a[i + 1])
        del a[i:i + 2]
    if not a or not os.path.exists(a[0]):
        print(__doc__)
        return 1
    rows, bad = load(a[0])
    if not rows:
        print("no usable rows: each needs account, median, views and hook")
        return 1
    text = render(analyse(rows, mn))
    if bad:
        text += "\n%d row(s) skipped: missing median, views or hook" % bad
    print(text)
    if out_path:
        os.makedirs(os.path.dirname(out_path) or ".", exist_ok=True)
        open(out_path, "w", encoding="utf-8").write(text + "\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
