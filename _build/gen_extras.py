# -*- coding: utf-8 -*-
import json, re, os
B = "/home/user/Doubao/chats/38450362683561730/CPU通识课-点化学习系统/01-CPU通识课"
p = json.load(open(os.path.join("/home/user/Doubao/chats/38450362683561730/CPU通识课-点化学习系统/_build", "parsed.json"), encoding="utf-8"))

# ---------- glossary ----------
rows, seen = [], {}
for cid in sorted(p):
    for t in p[cid]["terms"]:
        key = re.sub(r"\s+", "", t["term"]).lower()
        if key in seen:
            continue
        seen[key] = cid
        rows.append((t["term"], t["def"], cid))
num = {cid: int(cid[2:]) for cid in p}
rows.sort(key=lambda r: (num[r[2]], r[0]))
with open(os.path.join(B, "glossary.md"), "w", encoding="utf-8") as f:
    f.write("# 术语表\n\n")
    f.write("按章节顺序排列，共 %d 条。术语在正文首次出现处即有白话定义，本表用于集中查阅。\n\n" % len(rows))
    f.write("| 术语 | 白话定义 | 章节 |\n|---|---|---|\n")
    for t, d, cid in rows:
        f.write(f"| {t} | {d} | 第 {num[cid]} 章 |\n")

# ---------- quiz ----------
with open(os.path.join(B, "quiz.md"), "w", encoding="utf-8") as f:
    f.write("# 《CPU 通识课》测验\n\n")
    f.write("每章 3—4 题，答案与解析紧随其后。建议先合上讲义作答，再对照解析；正确率低于 80% 就回去重读对应小节。\n")
    for cid in sorted(p):
        c = p[cid]
        f.write(f"\n## 第 {num[cid]} 章：{c['title'].split('：',1)[-1]}\n\n")
        for i, q in enumerate(c["quizzes"], 1):
            letters = "ABCD"
            f.write(f"{i}. （单选）{q['q']}\n")
            for oi, o in enumerate(q["options"]):
                f.write(f"   - {letters[oi]}. {o}\n")
            f.write(f"   - **答案**：{letters[q['answer']]}\n")
            f.write(f"   - **解析**：{q['explain']}\n")

# ---------- flashcards ----------
with open(os.path.join(B, "flashcards.md"), "w", encoding="utf-8") as f:
    f.write("# 《CPU 通识课》抽认卡\n\n")
    f.write("正面只放问题与线索，答案在背面。共 %d 张。\n" % sum(len(v["cards"]) for v in p.values()))
    for cid in sorted(p):
        c = p[cid]
        f.write(f"\n## 第 {num[cid]} 章：{c['title'].split('：',1)[-1]}\n\n")
        for i, card in enumerate(c["cards"], 1):
            f.write(f"### 卡片 {i}：{card['front']}\n")
            f.write(f"- **背面**：{card['back']}\n")
            f.write(f"- **标签**：第 {num[cid]} 章\n")
            f.write(f"- **章节**：{cid}\n\n")
print("glossary rows", len(rows), "ok")
