#!/usr/bin/env python3
"""clean.py - strip the machine fingerprint out of a draft. Russian and English.

    python3 clean.py draft.txt                    # print the cleaned text
    python3 clean.py draft.txt -o clean.txt --report
    python3 clean.py draft.txt --keep-quotes      # keep curly quotes

Fixed automatically:
    invisible characters  zero-width spaces and joiners, word joiners, soft hyphens, byte-order
                          marks, direction marks; odd spaces become plain spaces
    typography            long dash to a comma (between words) or a hyphen, en dash to a hyphen,
                          the ellipsis character to three dots, curly quotes to straight ones.
                          Russian guillemets stay, they are normal Russian typography
    empty intros          "важно отметить, что", "в современном мире", "let's dive in" and the
                          rest of the 'delete' list in slop.json

Flagged, not fixed, because changing them needs judgement: stock words with a suggestion, bait
("подпишись", "follow for more"), and structures such as "это не просто X, это Y". Rewrite those
by hand, or with the minga-humanize-text skill, then run detect.py.
URLs are never touched.
"""
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import ruen  # noqa: E402

LEX = json.load(open(os.path.join(HERE, "slop.json"), encoding="utf-8"))
URL = re.compile(r"https?://\S+|www\.\S+")


def _protect(text):
    urls = URL.findall(text)
    for i, u in enumerate(urls):
        text = text.replace(u, "\x00%d\x00" % i, 1)
    return text, urls


def _restore(text, urls):
    for i, u in enumerate(urls):
        text = text.replace("\x00%d\x00" % i, u)
    return text


def clean(text, keep_quotes=False):
    changes = []
    text, urls = _protect(text)
    n = 0
    for cp, _name in LEX["invisible"]:
        ch = chr(int(cp, 16))
        n += text.count(ch)
        text = text.replace(ch, "")
    other = [c for c in text if ord(c) > 127 and __import__("unicodedata").category(c) == "Cf"]
    for c in set(other):
        n += text.count(c)
        text = text.replace(c, "")
    if n:
        changes.append(("invisible", "%d invisible character(s) removed" % n))
    sp = 0
    for cp, _name in LEX["spaces"]:
        ch = chr(int(cp, 16))
        sp += text.count(ch)
        text = text.replace(ch, " ")
    if sp:
        changes.append(("spaces", "%d unusual space(s) made plain" % sp))
    dash = chr(0x2014)
    nd = text.count(dash)
    if nd:
        text = re.sub(r"\s*%s\s*(?=\d)" % dash, "-", text)          # 1990 - 2000
        text = re.sub(r"(?m)^(\s*)%s\s*" % dash, r"\1- ", text)       # dialogue or list line
        text = re.sub(r"\s+%s\s+" % dash, ", ", text)                 # between words
        text = text.replace(dash, "-")
        changes.append(("dash", "%d long dash(es) replaced: check each sentence still reads right" % nd))
    for cp, to in LEX["typographic"]:
        ch = chr(int(cp, 16))
        if ch == dash or (keep_quotes and to in ("\"", "'")):
            continue
        k = text.count(ch)
        if k:
            text = text.replace(ch, to)
            changes.append(("typography", "%d x U+%s -> %r" % (k, cp, to)))
    lg = ruen.lang(text)
    for p in LEX["delete"][lg]:
        body = "".join("[её]" if ch in "её" else re.escape(ch) for ch in p)
        pat = re.compile(r"(?i)(?<![\wЀ-ӿ])" + body + r"\s*")
        k = len(pat.findall(text))
        if k:
            text = pat.sub("", text)
            changes.append(("intro", "removed %r x%d" % (p, k)))
    # tidy what the removals leave behind and recapitalise sentence starts
    text = re.sub(r" ,", ",", text)
    text = re.sub(r",\s*,", ",", text)
    text = re.sub(r"([.!?])\s*,\s*", r"\1 ", text)
    text = re.sub(r"[ \t]{2,}", " ", text)
    text = re.sub(r"(^|[.!?]\s+|\n)([a-zа-яё])", lambda m: m.group(1) + m.group(2).upper(), text)
    text = _restore(text, urls)
    return text, changes


def flags(text):
    lg = ruen.lang(text)
    out = []
    for w, tip in LEX["flag"][lg].items():
        k = ruen.count(text, [w])
        if k:
            out.append(("word", "%r x%d: %s" % (w, k, tip)))
    for b in LEX["bait"][lg]:
        if ruen.hits(text, [b]):
            out.append(("bait", "%r: reflex bait, cut it or replace with one real ask" % b))
    for s in LEX["structures"][lg]:
        for m in re.finditer(s["pattern"], text):
            out.append(("structure", "%s: \"%s\"" % (s["message"], m.group(0).strip()[:60])))
    return out


def main(argv=None):
    a = list(sys.argv[1:] if argv is None else argv)
    report = "--report" in a
    keep = "--keep-quotes" in a
    a = [x for x in a if x not in ("--report", "--keep-quotes")]
    out = None
    if "-o" in a:
        i = a.index("-o")
        out = a[i + 1]
        del a[i:i + 2]
    if not a or not os.path.exists(a[0]):
        print(__doc__)
        return 1
    text = open(a[0], encoding="utf-8").read()
    cleaned, changes = clean(text, keep)
    if out:
        open(out, "w", encoding="utf-8").write(cleaned)
    else:
        print(cleaned)
    if report or out:
        print("\nCHANGED", file=sys.stderr)
        for kind, msg in changes or [("none", "nothing to fix automatically")]:
            print("  %-11s %s" % (kind, msg), file=sys.stderr)
        fl = flags(cleaned)
        print("\nREWRITE BY HAND (%d)" % len(fl), file=sys.stderr)
        for kind, msg in fl:
            print("  %-11s %s" % (kind, msg), file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
