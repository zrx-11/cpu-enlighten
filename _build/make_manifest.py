# -*- coding: utf-8 -*-
import json, os, re, glob
P = "/home/user/Doubao/chats/38450362683561730/CPU通识课-点化学习系统"
B = os.path.join(P, "01-CPU通识课")
p = json.load(open(os.path.join(P, "_build", "parsed.json"), encoding="utf-8"))
n = {cid: int(cid[2:]) for cid in p}

PIAN = [
 ("01", "概览篇：CPU 是什么", ["ch01","ch02","ch03"]),
 ("02", "术语篇：CPU 的语汇", ["ch04","ch05","ch06","ch07","ch08","ch09","ch10"]),
 ("03", "原理篇：CPU 怎么算", ["ch11","ch12","ch13","ch14","ch15","ch16","ch17","ch18"]),
 ("04", "系统篇：CPU 与外部世界", ["ch19","ch20","ch21","ch22","ch23"]),
 ("05", "生产制造篇：从设计到实物", ["ch24","ch25","ch26","ch27","ch28"]),
 ("06", "家族篇：厂商与架构的兴衰", ["ch29","ch30","ch31"]),
 ("07", "生态篇：为什么生态比芯片难", ["ch32","ch33","ch34"]),
 ("08", "中国 CPU 篇：自主路线", ["ch35","ch36","ch37","ch38"]),
]

concepts = [
 ("c-isa", "指令集（ISA）", "concepts/isa.md", ["ch04","ch05","ch06","ch37"]),
 ("c-uarch", "微结构", "concepts/microarchitecture.md", ["ch06","ch15","ch16"]),
 ("c-pipeline", "流水线", "concepts/pipeline.md", ["ch15","ch16"]),
 ("c-cache", "缓存与存储层次", "concepts/cache.md", ["ch17"]),
 ("c-syscall", "系统调用", "concepts/system-call.md", ["ch18","ch19"]),
 ("c-perf", "性能度量", "concepts/performance.md", ["ch02","ch36"]),
 ("c-eco", "软件生态", "concepts/ecology.md", ["ch32","ch33","ch34"]),
 ("c-ownisa", "自主指令集", "concepts/autonomous-isa.md", ["ch04","ch37","ch38"]),
]

manifest = {
 "slug": "cpu-tongshi",
 "title": "CPU 通识课",
 "subtitle": "从一块硅片到一整套生态：零基础学透 CPU",
 "book": {
   "title": "CPU 通识课",
   "author": "靳国杰、张戈",
   "source": ["CPU通识课.pdf（310 页）"],
 },
 "audience": "零基础",
 "goal": "读完能看懂 CPU 的关键参数、说清从指令到芯片的完整链路、理解生态与自主路线的产业逻辑",
 "companion": "cpu-tongshi-companion.html",
 "learningPath": [
   {"step": s, "title": t, "chapterIds": ids, "checkpoint": "该篇各章自测题正确率 ≥ 80%"}
   for s, t, ids in PIAN
 ],
 "chapters": [],
 "concepts": [],
 "glossary": [],
 "patterns": {"file": "patterns.md"},
 "cheatsheet": {"file": "cheatsheet.md"},
 "quizzes": [],
 "flashcards": [],
}

for cid in sorted(p):
    c = p[cid]
    manifest["chapters"].append({
        "id": cid,
        "title": c["title"],
        "file": c["file"],
        "difficulty": c["difficulty"],
        "hours": c["hours"],
        "prerequisite": c["prev"],
        "core": c["core"],
        "objectives": c["goals"],
    })

for cid, title, file, chs in concepts:
    manifest["concepts"].append({"id": cid, "title": title, "file": file, "chapterIds": chs})

# glossary：按章首次出现，去重
seen = {}
rows = []
for cid in sorted(p):
    for t in p[cid]["terms"]:
        key = re.sub(r"\s+", "", t["term"]).lower()
        if key in seen:
            continue
        seen[key] = 1
        rows.append({"term": t["term"], "def": t["def"], "chapterId": cid})
rows.sort(key=lambda r: (n[r["chapterId"]], r["term"]))
manifest["glossary"] = rows

# quizzes
qi = 0
for cid in sorted(p):
    for k, q in enumerate(p[cid]["quizzes"], 1):
        qi += 1
        manifest["quizzes"].append({
            "id": "q%02d-%d" % (n[cid], k),
            "chapterId": cid,
            "type": "single",
            "question": q["q"],
            "options": q["options"],
            "answer": q["answer"],
            "explain": q["explain"],
        })

# flashcards
fi = 0
for cid in sorted(p):
    for k, c in enumerate(p[cid]["cards"], 1):
        fi += 1
        manifest["flashcards"].append({
            "id": "f%02d-%d" % (n[cid], k),
            "chapterId": cid,
            "front": c["front"],
            "back": c["back"],
            "tags": ["第 %d 章" % n[cid]],
        })

json.dump(manifest, open(os.path.join(B, "manifest.json"), "w", encoding="utf-8"),
          ensure_ascii=False, indent=1)
print("chapters", len(manifest["chapters"]), "concepts", len(manifest["concepts"]),
      "glossary", len(manifest["glossary"]), "quizzes", len(manifest["quizzes"]),
      "cards", len(manifest["flashcards"]))
ids = [q["id"] for q in manifest["quizzes"]]
print("dup quiz ids", len(ids) - len(set(ids)))
