from playwright.sync_api import sync_playwright
import os
idx = "file://" + os.path.abspath("index.html")
with sync_playwright() as p:
    b = p.chromium.launch(executable_path="/usr/local/bin/chromium", args=["--no-sandbox","--disable-gpu"])
    pg = b.new_page()
    errs=[]; pg.on("console", lambda m: errs.append(m.text) if m.type=="error" else None)
    pg.goto(idx); pg.wait_for_timeout(800)
    for c in ("ch01","ch02","ch03"):
        pg.evaluate(f"location.hash='#/book/cpu-tongshi/chapter/{c}'"); pg.wait_for_timeout(500)
    pg.evaluate("location.hash='#/book/cpu-tongshi/path'"); pg.wait_for_timeout(600)
    txt = pg.inner_text("#view")
    print("含已完成:", "已完成" in txt, "| 已通过步骤:", txt.count("已完成"))
    pg.evaluate("location.hash='#/book/cpu-tongshi/quiz/ch01'"); pg.wait_for_timeout(500)
    # 答第一题
    pg.click(".quiz-item:first-child .quiz-opt:first-child input")
    pg.click(".quiz-item:first-child .quiz-check")
    pg.wait_for_timeout(300)
    print("答题反馈:", pg.inner_text(".quiz-item:first-child .quiz-feedback"))
    print("解析存在:", "解析" in pg.inner_text(".quiz-item:first-child"))
    print("控制台错误:", errs[:3])
    b.close()
