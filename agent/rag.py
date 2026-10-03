import math
import re
from collections import Counter
from pathlib import Path

stop = set("и в на с как что это для по не из о а то вы мы же ли бы".split())  # мусор, режем


def tokens(text):
    words = re.findall(r"[a-zа-яё0-9]+", text.lower())
    return [w for w in words if w not in stop and len(w) > 2]


class Kb:
    def __init__(self, folder):
        self.docs = []
        for p in sorted(Path(folder).glob("*.txt")):
            self.docs.append((p.stem, p.read_text(encoding="utf-8").strip()))
        df = Counter()
        for _, text in self.docs:
            for w in set(tokens(text)):
                df[w] += 1
        self.df = df
        self.n = len(self.docs)

    def _vec(self, text):
        # tf-idf вектора
        v = {}
        for w, c in Counter(tokens(text)).items():
            v[w] = c * (math.log((self.n + 1) / (self.df.get(w, 0) + 1)) + 1)
        return v

    @staticmethod
    def _cos(a, b):
        dot = sum(v * b.get(w, 0) for w, v in a.items())
        na = math.sqrt(sum(v * v for v in a.values()))
        nb = math.sqrt(sum(v * v for v in b.values()))
        return dot / (na * nb) if na and nb else 0.0

    def search(self, query, top=2):
        # топ чанков с оценкой, пустые отсев
        q = self._vec(query)
        scored = sorted(((self._cos(q, self._vec(t)), n, t) for n, t in self.docs), reverse=True)
        return [{"doc": n, "score": round(s, 3), "text": t} for s, n, t in scored[:top] if s > 0]
