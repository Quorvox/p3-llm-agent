from fastapi.testclient import TestClient

from agent.bot import answer, kb
from api import app

api = TestClient(app)


def test_calc():
    assert answer("2+2") == "4"


def test_calc_word():
    assert answer("сколько будет (10+5)*2") == "30"


def test_calc_bad():
    assert "поддержку" in answer("2++")


def test_pay():
    assert "сбп" in answer("как оплатить заказ").lower()


def test_delivery():
    assert "трек" in answer("где трек номер")


def test_return():
    assert "14 дней" in answer("как вернуть товар")


def test_unknown():
    assert "поддержку" in answer("абырвалг хррр")


def test_kb_size():
    assert len(kb.docs) == 4


def test_api_chat():
    r = api.post("/api/chat", json={"text": "как оплатить заказ"})
    assert r.status_code == 200
    assert "сбп" in r.json()["answer"].lower()
    assert r.json()["hits"][0]["doc"] == "pay"


def test_api_empty():
    assert api.post("/api/chat", json={"text": ""}).status_code == 422


def test_health():
    assert api.get("/api/health").json() == {"ok": True, "docs": 4}
