from playwright.sync_api import sync_playwright
import os
url = "file://" + os.path.abspath("01-CPU通识课/cpu-tongshi-companion.html")
with sync_playwright() as p:
    b = p.chromium.launch(executable_path="/usr/local/bin/chromium", args=["--no-sandbox","--disable-gpu"])
    pg = b.new_page(); errs=[]
    pg.on("console", lambda m: errs.append(m.text) if m.type=="error" else None)
    pg.goto(url); pg.wait_for_timeout(800)
    print("标题:", pg.title())
    print("章节导航数:", pg.eval_on_selector_all("nav a", "e=>e.length"))
    pg.evaluate("location.hash='#/chapter/ch38'"); pg.wait_for_timeout(600)
    print("末章正文长度:", len(pg.inner_text("#view")))
    pg.evaluate("location.hash='#/cards'"); pg.wait_for_timeout(500)
    print("卡片正面:", pg.inner_text(".fc-front"))
    pg.click("#flashcard"); pg.wait_for_timeout(400)
    print("翻面后背面:", pg.inner_text(".fc-back"))
    pg.evaluate("location.hash='#/glossary'"); pg.wait_for_timeout(500)
    print("术语条数:", pg.eval_on_selector_all("#glossary-list li", "e=>e.length"))
    pg.fill("#q", "TLB"); pg.wait_for_timeout(600)
    print("搜索命中:", pg.eval_on_selector_all(".search-hit", "e=>e.length"))
    print("控制台错误:", errs[:3])
    b.close()
