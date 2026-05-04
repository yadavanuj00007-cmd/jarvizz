"""
iGOT Karmayogi quiz bot.

Usage:
  1. Quit Chrome, then relaunch with a remote debug port so this script can
     attach to your already-logged-in session:
        google-chrome --remote-debugging-port=9222 --user-data-dir="$HOME/.config/google-chrome"
     (On macOS: /Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --remote-debugging-port=9222)
  2. Open the Karmayogi quiz tab and reach the first question.
  3. export ANTHROPIC_API_KEY=sk-ant-...
  4. pip install playwright anthropic && playwright install
  5. python karmyogi_quiz_bot.py
"""

import os
import re
import sys
import time

from anthropic import Anthropic
from playwright.sync_api import sync_playwright

CDP_URL = os.environ.get("CDP_URL", "http://localhost:9222")
MODEL = os.environ.get("MODEL", "claude-haiku-4-5-20251001")
MAX_QUESTIONS = int(os.environ.get("MAX_QUESTIONS", "100"))
DELAY = float(os.environ.get("DELAY", "1.0"))

client = Anthropic()


def find_quiz_frame(page):
    for f in [page.main_frame, *page.frames]:
        try:
            if f.locator("text=/Question|Q\\.|Q\\s*\\d/i").first.is_visible(timeout=200):
                return f
        except Exception:
            continue
    return page.main_frame


def extract_question(frame):
    """Pull the question text + option texts from the DOM, generically."""
    js = r"""
() => {
  const root = document.querySelector('.question, [class*="question"], main, body');
  const txt = (el) => (el ? el.innerText.trim() : '');
  // question
  let qEl = document.querySelector('.question-text, [class*="question-text"], [class*="questionText"], .mcq-question, .question');
  let q = txt(qEl);
  if (!q) q = txt(document.querySelector('main')).split('\n').slice(0, 6).join('\n');
  // options
  const opts = [];
  const radios = Array.from(document.querySelectorAll('input[type=radio], input[type=checkbox]'));
  if (radios.length) {
    for (const r of radios) {
      const lbl = r.closest('label') || document.querySelector(`label[for="${r.id}"]`) || r.parentElement;
      opts.push({ text: txt(lbl), id: r.id || '' });
    }
  } else {
    const cands = Array.from(document.querySelectorAll('.option, [class*="option"], li'));
    for (const c of cands) {
      const t = txt(c);
      if (t && t.length < 400) opts.push({ text: t, id: c.id || '' });
    }
  }
  return { q, opts };
}
"""
    return frame.evaluate(js)


def ask_claude(question, options):
    opts = "\n".join(f"{i+1}. {o['text']}" for i, o in enumerate(options))
    msg = client.messages.create(
        model=MODEL,
        max_tokens=8,
        system="Answer multiple-choice questions. Reply with ONLY the option number.",
        messages=[{"role": "user", "content": f"{question}\n\n{opts}\n\nAnswer (number only):"}],
    )
    text = msg.content[0].text.strip()
    m = re.search(r"\d+", text)
    return int(m.group()) - 1 if m else 0


def click_option(frame, idx):
    radios = frame.locator("input[type=radio], input[type=checkbox]")
    if radios.count() > idx:
        radios.nth(idx).check(force=True)
        return True
    opts = frame.locator(".option, [class*='option'], li")
    if opts.count() > idx:
        opts.nth(idx).click()
        return True
    return False


def click_next(frame):
    for sel in [
        "button:has-text('Next')",
        "button:has-text('Submit')",
        "button:has-text('Save')",
        "[class*='next']",
    ]:
        try:
            btn = frame.locator(sel).first
            if btn.is_visible(timeout=300):
                btn.click()
                return True
        except Exception:
            pass
    return False


def main():
    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp(CDP_URL)
        ctx = browser.contexts[0]
        page = next((pg for pg in ctx.pages if "karmayogi" in pg.url.lower() or "igot" in pg.url.lower()), ctx.pages[0])
        page.bring_to_front()
        print(f"Attached to: {page.url}")

        seen = set()
        for i in range(MAX_QUESTIONS):
            time.sleep(DELAY)
            frame = find_quiz_frame(page)
            data = extract_question(frame)
            q, opts = data.get("q", ""), data.get("opts", [])
            if not q or not opts:
                print(f"[{i}] no question detected; stopping.")
                break
            key = q[:120]
            if key in seen:
                print("Same question detected twice; stopping.")
                break
            seen.add(key)

            idx = ask_claude(q, opts)
            print(f"[{i}] {q[:80]}... -> option {idx+1}: {opts[idx]['text'][:60]}")
            if not click_option(frame, idx):
                print("could not click option; stopping.")
                break
            time.sleep(0.4)
            if not click_next(frame):
                print("no next/submit button; stopping.")
                break


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(0)
