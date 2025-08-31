# coding: utf-8

import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_classify_without_input():
  resp = client.post("/api/classify", data={})
  assert resp.status_code == 400
  assert "detail" in resp.json()

def test_classify_with_text():
  resp = client.post("/api/classify", data={"text": "Preciso saber o status da minha requisição"})
  assert resp.status_code == 200
  body = resp.json()
  assert "category" in body
  assert "probability" in body
  assert "reply" in body

def test_regenerate_reply():
  resp = client.post("/api/reply", json={"category": "Produtivo", "text": "Gostaria de abrir um chamado"})
  assert resp.status_code == 200
  body = resp.json()
  assert "reply" in body
