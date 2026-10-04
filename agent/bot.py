import re
from pathlib import Path

from agent.rag import Kb
from agent.tools import calc

root = Path(__file__).resolve().parents[1]
kb = Kb(root / "kb")

calc_re = re.compile(r"^(посчитай|сколько будет|calc)?\s*([\d\s+\-*/().^]+)$", re.I)


def answer(text):
    # сперва калькулятор
    m = calc_re.match(text.strip().replace("^", "**"))
    if m and any(ch.isdigit() for ch in m.group(2)):
        val = calc(m.group(2))
        if val is not None:
            return f"{round(val, 4)}"
    # потом база знаний
    hits = kb.search(text)
    if not hits:
        return "не нашел в базе, напиши в поддержку: help@shop.test"
    best = hits[0]
    return f"{best['text']}\n[источник: {best['doc']}]"


if __name__ == "__main__":
    print("support-agent, пустая строка — выход")
    while True:
        try:
            q = input("you: ").strip()
        except (EOFError, KeyboardInterrupt):
            break
        if not q:
            break
        print("bot:", answer(q))
