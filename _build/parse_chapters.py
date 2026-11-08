# -*- coding: utf-8 -*-
import os, re, json, glob

BOOK = "/home/user/Doubao/chats/38450362683561730/CPU通识课-点化学习系统/01-CPU通识课"
CH = os.path.join(BOOK, "chapters")

def parse_file(path):
    txt = open(path, encoding="utf-8").read()
    lines = txt.splitlines()
    title = next(l for l in lines if l.startswith("# ")).lstrip("# ").strip()
    m = re.search(r"\*\*难度\*\*：([★☆]+) \| \*\*学时\*\*：([\d.]+) 小时 \| \*\*前置\*\*：(.+)", txt)
    stars, hours, prev = (m.group(1), float(m.group(2)), m.group(3).strip()) if m else ("★★☆", 0.5, "")
    diff = stars.count("★")

    def section(name):
        mm = re.search(r"^## %s\n(.*?)(?=^## |\Z)" % re.escape(name), txt, re.S | re.M)
        return mm.group(1).strip() if mm else ""

    quizzes = []
    for ln in section("自测题").splitlines():
        ln = ln.strip()
        if not re.match(r"^\d+\.", ln):
            continue
        body = re.sub(r"^\d+\.\s*", "", ln)
        parts = [p.strip() for p in body.split("｜")]
        qtext = parts[0]
        opts, ans, expl = [], None, ""
        for p in parts[1:]:
            if p.startswith("答案："):
                ans = p.replace("答案：", "").strip()
            elif p.startswith("解析："):
                expl = p.replace("解析：", "").strip()
            else:
                opts.append(p)
        if ans and len(ans) >= 1 and ans[0] in "ABCD":
            ans_idx = "ABCD".index(ans[0])
            if ans_idx < len(opts):
                quizzes.append({"q": qtext, "options": opts,
                                "answer": ans_idx, "explain": expl})
            else:
                print("BAD_ANSWER", os.path.basename(path), qtext, ans, len(opts))

    cards = []
    for ln in section("抽认卡").splitlines():
        ln = ln.strip()
        if not ln.startswith("- ") or "｜" not in ln:
            continue
        f, b = ln[2:].split("｜", 1)
        cards.append({"front": f.strip(), "back": b.strip()})

    terms = []
    for ln in section("术语").splitlines():
        ln = ln.strip()
        if not ln.startswith("- ") or "：" not in ln:
            continue
        t, d = ln[2:].split("：", 1)
        terms.append({"term": t.strip(), "def": d.strip()})

    goals = [l[2:].strip() for l in section("学习目标").splitlines() if l.strip().startswith("- ")]
    core = section("一句话核心").replace("\n", " ").strip()
    return dict(title=title, difficulty=diff, hours=hours, prev=prev,
                quizzes=quizzes, cards=cards, terms=terms, goals=goals, core=core)

files = sorted(glob.glob(os.path.join(CH, "c*.md")))
data = {}
for i, f in enumerate(files, 1):
    cid = f"ch{i:02d}"
    d = parse_file(f)
    d["id"] = cid
    d["file"] = "chapters/" + os.path.basename(f)
    data[cid] = d
    print(cid, d["title"][:40], "| diff", d["difficulty"], "| q", len(d["quizzes"]),
          "| cards", len(d["cards"]), "| terms", len(d["terms"]))

print("TOTAL quizzes", sum(len(v["quizzes"]) for v in data.values()))
print("TOTAL cards", sum(len(v["cards"]) for v in data.values()))
print("TOTAL terms", sum(len(v["terms"]) for v in data.values()))
json.dump(data, open("/home/user/Doubao/chats/38450362683561730/CPU通识课-点化学习系统/_build/parsed.json", "w"),
          ensure_ascii=False, indent=1)
