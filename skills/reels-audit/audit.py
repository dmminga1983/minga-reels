#!/usr/bin/env python3
"""audit.py - what actually worked on your own account, from the numbers.

    python3 audit.py posts.csv
    python3 audit.py posts.csv --by persona       # compare characters or niches
    python3 audit.py posts.csv --by platform      # compare Instagram with Shorts

posts.csv, comma-separated with a header row. Only views is required; every other column that
is present gets used:
    date, persona, platform, format, views, reach, nonfollower_pct, hold3s_pct,
    avg_watch_s, length_s, shares, saves, comments, follows, formula, hook

Raw views mostly measure how many people already follow you. This ranks by the outlier multiple
(views over the account's own median) and by sends per reach (shares / reach), the strongest
signal a viewer can give. A video with reach and no follows is a profile problem, not a hook
problem: it says so when it sees it.
"""
import csv
import os
import sys


def f(x):
    try:
        return float(str(x).replace(" ", "").replace("%", "").replace(",", "."))
    except (TypeError, ValueError):
        return None


def median(xs):
    xs = sorted(x for x in xs if x is not None)
    if not xs:
        return None
    m = len(xs) // 2
    return xs[m] if len(xs) % 2 else (xs[m - 1] + xs[m]) / 2


def load(path):
    with open(path, encoding="utf-8") as fh:
        rows = list(csv.DictReader(fh))
    out = []
    for r in rows:
        v = f(r.get("views"))
        if v is None:
            continue
        d = {k: (r.get(k) or "").strip() for k in ("date", "persona", "platform", "format",
                                                    "formula", "hook")}
        for k in ("views", "reach", "nonfollower_pct", "hold3s_pct", "avg_watch_s", "length_s",
                  "shares", "saves", "comments", "follows"):
            d[k] = f(r.get(k))
        d["views"] = v
        out.append(d)
    return out


def enrich(rows, group=None):
    groups = {}
    for r in rows:
        groups.setdefault(r.get(group) or "all" if group else "all", []).append(r)
    for key, rs in groups.items():
        med = median([r["views"] for r in rs]) or 1
        for r in rs:
            r["multiple"] = round(r["views"] / med, 2)
            reach = r["reach"] or r["views"]
            r["sends_per_1k"] = round(1000 * r["shares"] / reach, 1) if r["shares"] is not None and reach else None
            r["follows_per_1k"] = round(1000 * r["follows"] / reach, 1) if r["follows"] is not None and reach else None
    return groups


def findings(rows):
    out = []
    ranked = sorted(rows, key=lambda r: (-r["multiple"], -(r["sends_per_1k"] or 0)))
    k = min(5, max(1, len(rows) // 3))
    top, bottom = ranked[:k], ranked[-k:]
    ht, hb = median([r["hold3s_pct"] for r in top]), median([r["hold3s_pct"] for r in bottom])
    if ht is not None and hb is not None and ht - hb >= 10:
        out.append("Hold at 3 seconds separates them: %.0f%% up top, %.0f%% at the bottom. It is the hook; "
                   "everything downstream is a distraction." % (ht, hb))
    ft = {}
    for r in top:
        if r["formula"]:
            ft[r["formula"]] = ft.get(r["formula"], 0) + 1
    for name, c in sorted(ft.items(), key=lambda kv: -kv[1]):
        if c >= 2:
            out.append("Formula %s is in the top %d times." % (name, c))
    lt, lb = median([r["length_s"] for r in top]), median([r["length_s"] for r in bottom])
    if lt and lb and abs(lt - lb) >= 8:
        out.append("Length: the top ones are about %.0fs, the bottom ones %.0fs." % (lt, lb))
    nf = median([r["nonfollower_pct"] for r in rows])
    fol = median([r["follows_per_1k"] for r in rows])
    if nf is not None and fol is not None and nf >= 50 and fol < 2:
        out.append("Reach travels (%.0f%% non-followers) but follows are %.1f per 1,000: that is a "
                   "profile problem, not a hook problem. Fix the profile before the hooks." % (nf, fol))
    if not out:
        out.append("No pattern strong enough to state. That is a finding too: keep posting and re-run.")
    conf = "enough to see a pattern" if len(rows) >= 20 else "too few posts for a confident claim (%d)" % len(rows)
    return top, bottom, out, conf


def line(r):
    bits = ["%6.1fx" % r["multiple"], "%9d views" % r["views"]]
    if r["hold3s_pct"] is not None:
        bits.append("hold@3s %3.0f%%" % r["hold3s_pct"])
    if r["sends_per_1k"] is not None:
        bits.append("sends %5.1f/1k" % r["sends_per_1k"])
    if r["formula"]:
        bits.append(r["formula"])
    lbl = " ".join(x for x in (r["date"], r["persona"], r["platform"]) if x)
    return "  " + "  ".join(bits) + ("  " + lbl if lbl else "") + ("\n          " + r["hook"][:64] if r["hook"] else "")


def compare(groups):
    out = ["COMPARISON (each group against its own median)",
           "  %-20s %5s %12s %10s %12s %12s" % ("group", "posts", "median views", "best", "sends/1k", "follows/1k")]
    for key, rs in sorted(groups.items(), key=lambda kv: -(median([r["views"] for r in kv[1]]) or 0)):
        out.append("  %-20s %5d %12.0f %9.1fx %12s %12s" % (
            key[:20], len(rs), median([r["views"] for r in rs]) or 0, max(r["multiple"] for r in rs),
            "-" if median([r["sends_per_1k"] for r in rs]) is None else "%.1f" % median([r["sends_per_1k"] for r in rs]),
            "-" if median([r["follows_per_1k"] for r in rs]) is None else "%.1f" % median([r["follows_per_1k"] for r in rs])))
    out.append("  Groups with under 8 posts are noise, whatever the numbers say.")
    return "\n".join(out)


def main(argv=None):
    a = list(sys.argv[1:] if argv is None else argv)
    by = None
    if "--by" in a:
        i = a.index("--by")
        by = a[i + 1]
        del a[i:i + 2]
    if not a or not os.path.exists(a[0]):
        print(__doc__)
        return 1
    rows = load(a[0])
    if not rows:
        print("no rows with a views value")
        return 1
    groups = enrich(rows, by)
    if by:
        print(compare(groups) + "\n")
    top, bottom, notes, conf = findings(rows)
    print("AUDIT  %d posts  median views %.0f" % (len(rows), median([r["views"] for r in rows])))
    print("\nTOP BY OUTLIER MULTIPLE")
    print("\n".join(line(r) for r in top))
    print("\nBOTTOM")
    print("\n".join(line(r) for r in bottom))
    print("\nWHAT THE DATA SAYS")
    for i, n in enumerate(notes, 1):
        print("  %d. %s" % (i, n))
    print("\nCONFIDENCE  " + conf)
    return 0


if __name__ == "__main__":
    sys.exit(main())
