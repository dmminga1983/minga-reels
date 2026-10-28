import filecmp
import importlib.util
import io
import json
import os
import re
import tempfile
import unittest
import warnings
from contextlib import redirect_stdout, redirect_stderr

warnings.simplefilter("ignore", ResourceWarning)
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, ".."))
SKILLS = os.path.join(ROOT, "skills")


def load(skill, mod):
    path = os.path.join(SKILLS, skill, mod + ".py")
    import sys
    sys.path.insert(0, os.path.dirname(path))
    spec = importlib.util.spec_from_file_location("%s_%s" % (skill.replace("-", "_"), mod), path)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


hookscore = load("reels-hook", "hookscore")
calibrate = load("reels-hook", "calibrate")
beats = load("reels-script", "beats")
caption = load("reels-caption", "caption")
clean = load("reels-clean", "clean")
detect = load("reels-clean", "detect")
swipe = load("reels-viral", "swipe")
audit = load("reels-audit", "audit")
ruen = load("reels-hook", "ruen")


def tmp(text, suffix=".txt"):
    fd, path = tempfile.mkstemp(suffix=suffix)
    with os.fdopen(fd, "w", encoding="utf-8") as f:
        f.write(text)
    return path


def quiet(fn, *a):
    out, err = io.StringIO(), io.StringIO()
    with redirect_stdout(out), redirect_stderr(err):
        code = fn(*a)
    return code, out.getvalue(), err.getvalue()


class TestRuEn(unittest.TestCase):
    def test_lang(self):
        self.assertEqual(ruen.lang("Привет, это тест"), "ru")
        self.assertEqual(ruen.lang("Hello, this is a test"), "en")

    def test_numbers_said_as_words_count_as_concrete(self):
        self.assertGreater(ruen.concrete("Я потерял сорок тысяч рублей"), 0)
        self.assertGreater(ruen.concrete("three marketing books"), 0)
        self.assertEqual(ruen.concrete("очень хорошая идея"), 0)

    def test_russian_takes_longer_to_say_per_word(self):
        ru = ruen.speech_seconds("Переплатил сорок тысяч из-за договора")
        self.assertGreater(ru, 1.5)

    def test_second_person(self):
        self.assertEqual(ruen.second_person("Ты знаешь, что вы делаете"), 3)


class TestHookscore(unittest.TestCase):
    def test_every_formula_example_names_itself(self):
        for f in hookscore.FORMULAS:
            for lg in ("ru", "en"):
                with self.subTest(formula=f["id"], lang=lg):
                    self.assertEqual(hookscore.score(f["example_" + lg])["formula"], f["id"])

    def test_greetings_are_capped(self):
        for t in ("Всем привет, сегодня я расскажу про ремонт", "Hey guys, today I want to talk"):
            r = hookscore.score(t)
            self.assertLessEqual(r["verdict"], 25)
            self.assertTrue(r["dealbreakers"])

    def test_real_hook_beats_hype(self):
        good = hookscore.score("Я переплатил сорок тысяч из-за одного пункта в договоре.")
        hype = hookscore.score("Невероятный секрет, который изменит вашу жизнь")
        self.assertGreater(good["verdict"], hype["verdict"] + 15)

    def test_fix_is_in_the_hooks_language(self):
        self.assertTrue(re.search("[а-я]", hookscore.score("Просто хорошая фраза")["fix"]))
        self.assertFalse(re.search("[а-я]", hookscore.score("Just a nice phrase")["fix"]))

    def test_cli_json(self):
        p = tmp("Хватит подписывать акт в день получения ключей.\nHey guys welcome back\n")
        code, out, _ = quiet(hookscore.main, ["--json", p])
        self.assertEqual(code, 0)
        rows = json.loads(out)
        self.assertEqual(len(rows), 2)
        self.assertGreater(rows[0]["verdict"], rows[1]["verdict"])

    def test_26_formulas_with_both_languages(self):
        self.assertEqual(len(hookscore.FORMULAS), 26)
        for f in hookscore.FORMULAS:
            self.assertTrue(f["match"]["ru"] and f["match"]["en"], f["id"])


class TestCalibrate(unittest.TestCase):
    def test_auc(self):
        self.assertEqual(calibrate.auc([3, 4], [1, 2]), 1.0)
        self.assertEqual(calibrate.auc([1], [1]), 0.5)
        self.assertIsNone(calibrate.auc([], [1]))

    def test_run(self):
        rows = ["channel\tviews\thook"]
        for ch in ("a", "b"):
            for i in range(9):
                good = "Я потерял %d тысяч из-за одного пункта в договоре" % (i + 10)
                bad = "Всем привет, сегодня поговорим про ремонт"
                rows.append("%s\t%d\t%s" % (ch, 1000 * (i + 1), good if i > 4 else bad))
        res = calibrate.calibrate(calibrate.load(tmp("\n".join(rows))))
        self.assertGreater(res["auc"], 0.9)


class TestBeats(unittest.TestCase):
    def test_flags_long_hook_and_no_loop(self):
        s = ("Это очень длинная первая фраза, которую невозможно произнести за три секунды никогда.\n"
             "[ЭКРАН: 40 000 ₽]\nВторая строка.\nТретья строка.\nКонец без повтора.")
        r = beats.sheet(s, target=30)
        text = " ".join(r["flags"])
        self.assertIn("хук", text)
        self.assertIn("петли", text)
        self.assertEqual(len(r["beats"]), 4)
        self.assertEqual(r["beats"][0]["screen"], ["[ЭКРАН: 40 000 ₽]"])

    def test_loop_detected(self):
        r = beats.sheet("Договор стоил мне сорок тысяч.\nВот пункт.\nЧитайте договор до подписи.")
        self.assertTrue(r["loop"])

    def test_english(self):
        r = beats.sheet("I lost forty grand on one contract.\nHere is the clause.\nRead the contract.")
        self.assertEqual(r["lang"], "en")
        self.assertTrue(r["loop"])


class TestCaption(unittest.TestCase):
    def test_instagram_hashtag_cap(self):
        res, _ = caption.lint_instagram("Строка. " + " ".join("#t%d" % i for i in range(6)))
        self.assertIn(("FAIL", "HASHTAGS"), [(r[0], r[1]) for r in res])

    def test_instagram_flags_link_and_asks(self):
        res, _ = caption.lint_instagram("Акт за 10 минут. Подпишись и сохрани. https://x.ru/a")
        names = {r[1]: r[0] for r in res}
        self.assertEqual(names["LINK"], "WARN")
        self.assertEqual(names["ONE ASK"], "WARN")

    def test_shorts_limits(self):
        res, _ = caption.lint_shorts("x" * 101, "ok")
        self.assertIn(("FAIL", "TITLE"), [(r[0], r[1]) for r in res])
        res, _ = caption.lint_shorts("ok", " ".join("#t%d" % i for i in range(61)))
        self.assertIn(("FAIL", "HASHTAGS"), [(r[0], r[1]) for r in res])

    def test_ai_reminder(self):
        res, _ = caption.lint_instagram("Строка с цифрой 5.", ai=True)
        self.assertIn("AI LABEL", [r[1] for r in res])


class TestClean(unittest.TestCase):
    def test_fixes_and_flags(self):
        dash = chr(0x2014)
        zw = chr(0x200B)
        src = ("Важно отметить, что ремонт %s это не просто работа, это путешествие%s. "
               "Подпишись! См. https://example.com/a%sb" % (dash, zw, dash))
        out, changes = clean.clean(src)
        self.assertNotIn(chr(0x200B), out)
        self.assertNotIn("Важно отметить", out)
        self.assertIn("https://example.com/a%sb" % dash, out)          # URLs untouched
        self.assertNotIn(dash, out.replace("https://example.com/a%sb" % dash, ""))
        kinds = {k for k, _ in clean.flags(out)}
        self.assertTrue({"word", "bait", "structure"} <= kinds)

    def test_guillemets_stay(self):
        out, _ = clean.clean("Он сказал «да» и " + chr(0x201C) + "ok" + chr(0x201D))
        self.assertIn("«да»", out)
        self.assertIn('"ok"', out)

    def test_detect_prefers_clean_text(self):
        dirty = ("В современном мире это не просто тренд, это настоящий прорыв" + chr(0x200B) + " " + chr(0x2014) + " "
                 "невероятно уникальный лайфхак. Подпишись!")
        human = ("В прошлом году я подписал акт с тремя замечаниями. Через месяц застройщик "
                 "переделал окно. Второе ждали до марта. Третье так и висит, и я пишу им снова.")
        self.assertGreater(detect.score(human)["human"], detect.score(dirty)["human"] + 25)
        self.assertEqual(detect.score(dirty)["verdict"], "FLAGGED")


class TestSwipe(unittest.TestCase):
    def test_ranks_by_multiple_not_views(self):
        p = tmp("account\tmedian\tviews\thook\n"
                "big\t1000000\t1200000\tВсем привет, сегодня про ремонт\n"
                "small\t2000\t60000\tХватит подписывать акт в день получения ключей\n"
                "small\t2000\t2000\tПросто обычный ролик\n")
        rows, bad = swipe.load(p)
        res = swipe.analyse(rows)
        self.assertEqual(res["rows"][0]["account"], "small")
        self.assertEqual(res["rows"][0]["multiple"], 30.0)
        self.assertEqual(res["rows"][0]["formula"], "stop")
        self.assertIn("too small", res["confidence"])


class TestAudit(unittest.TestCase):
    def test_profile_problem_and_groups(self):
        lines = ["persona,platform,views,reach,nonfollower_pct,hold3s_pct,shares,follows"]
        for i in range(10):
            lines.append("a,instagram,%d,%d,80,%d,%d,1" % (1000 + i * 500, 1000 + i * 500, 30 + i * 4, i))
            lines.append("b,shorts,%d,%d,70,40,2,0" % (500 + i * 10, 500 + i * 10))
        rows = audit.load(tmp("\n".join(lines), ".csv"))
        groups = audit.enrich(rows, "persona")
        self.assertEqual(set(groups), {"a", "b"})
        _, _, notes, _ = audit.findings(rows)
        self.assertTrue(any("profile problem" in n for n in notes))
        code, out, _ = quiet(audit.main, [tmp("\n".join(lines), ".csv"), "--by", "persona"])
        self.assertEqual(code, 0)
        self.assertIn("COMPARISON", out)


class TestRepo(unittest.TestCase):
    def test_skill_frontmatter_matches_folder(self):
        names = sorted(os.listdir(SKILLS))
        self.assertEqual(len(names), 11)
        for n in names:
            text = open(os.path.join(SKILLS, n, "SKILL.md"), encoding="utf-8").read()
            m = re.match(r'---\nname: (.+)\ndescription: "(.+?)"\n---\n', text, re.S)
            self.assertTrue(m, n)
            self.assertEqual(m.group(1), n)
            self.assertLessEqual(len(m.group(2)), 1024, n)

    def test_ruen_copies_are_identical(self):
        copies = [os.path.join(SKILLS, d, "ruen.py") for d in os.listdir(SKILLS)
                  if os.path.exists(os.path.join(SKILLS, d, "ruen.py"))]
        self.assertGreaterEqual(len(copies), 4)
        for c in copies[1:]:
            self.assertTrue(filecmp.cmp(copies[0], c, shallow=False), c)

    def test_no_long_dashes(self):
        for base, _, files in os.walk(ROOT):
            if ".git" in base:
                continue
            for f in files:
                if f.endswith((".md", ".json", ".txt", ".py")):
                    text = open(os.path.join(base, f), encoding="utf-8").read()
                    self.assertNotIn(chr(0x2014), text, os.path.join(base, f))

    def test_json_files_parse(self):
        for base, _, files in os.walk(ROOT):
            for f in files:
                if f.endswith(".json") and ".git" not in base:
                    json.load(open(os.path.join(base, f), encoding="utf-8"))

    def test_plugin_name(self):
        p = json.load(open(os.path.join(ROOT, ".claude-plugin", "plugin.json")))
        self.assertEqual(p["name"], "minga-reels")


if __name__ == "__main__":
    unittest.main()
