# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

The first time I ran it, the UI looked like a normal guessing game, but gameplay behavior felt inconsistent right away. I expected the hint system to guide me correctly, but when my guess was too high it told me to go higher, and when my guess was too low it told me to go lower. I expected difficulty settings and attempt counters to be accurate, but the game always told me to guess between 1 and 100, started attempts in a way that reduced the real number of tries, and New Game reset the secret to 1-100 instead of the selected difficulty range. I expected New Game to fully restart the session, but after winning or losing, pressing New Game did not reliably reset status/history/score, so I could still be stuck in an ended game state. I also expected numeric comparisons to stay stable, but the app sometimes converted the secret number to a string on even attempts, which can produce incorrect comparison behavior.

---

## 2. How did you use AI as a teammate?

I used Codex as my AI teammate in the terminal to inspect bugs, refactor shared logic, and add regression tests. One correct suggestion was to move `check_guess`, `parse_guess`, and range logic into `logic_utils.py` and import them in `app.py` so behavior is consistent in one place; this was correct because the app now uses one source of truth and tests run directly against those functions. Another correct suggestion was to add a targeted test for the reversed hint bug (`test_hint_direction_regression_for_too_high_guess`) so we do not reintroduce the wrong hint direction. A misleading suggestion from earlier AI-generated code was the old fallback in `check_guess` that converted values to strings and compared them lexicographically, which can produce wrong results in number games. I verified this was misleading by reading the code path and confirming we removed string comparisons so `check_guess` always compares integers.

---

## 3. Debugging and testing your fixes

I treated a bug as fixed only after both code-path inspection and repeatable tests showed the expected behavior. I ran `pytest` and confirmed the targeted regression test for hint direction passes, specifically proving a too-high guess returns a message containing `LOWER`. I also verified parsing behavior with a test that rejects decimal input (`12.5`) as not a whole number, which closes a confusing input edge case from the original implementation. On the app side, I verified that New Game resets `status`, `score`, `history`, and `attempts`, and that the secret is regenerated within the selected difficulty range. AI helped design the regression tests by translating each user-visible bug into a precise assertion we can keep in the suite.

---

## 4. What did you learn about Streamlit and state?

The secret changed because Streamlit reruns the script on each interaction, so values not protected in `st.session_state` can reset or drift. I would explain reruns as “the whole script re-executes every click,” and session state as “the small memory that survives those reruns.” The key fix was centralizing initialization/reset logic and only changing the secret when starting a new game or changing difficulty.

---

## 5. Looking ahead: your developer habits

One habit I will reuse is writing a regression test immediately after finding a user-visible bug. Next time, I will ask AI for smaller, testable changes instead of broad rewrites so mistakes are easier to catch. I rejected one bad AI pattern (string-based number comparison fallback) because it could return wrong results, and this project reinforced that AI code is a draft I must verify, not trust by default.
