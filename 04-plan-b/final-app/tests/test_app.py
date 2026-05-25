"""Acceptance tests for Shortly — derived from spec.md scenarios."""
from __future__ import annotations

from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from app import db
from app.main import app, db_conn


@pytest.fixture()
def client(tmp_path: Path):
    db_file = tmp_path / "test.db"
    db.init_db(db_file)

    def _override():
        with db.get_conn(db_file) as conn:
            yield conn

    app.dependency_overrides[db_conn] = _override
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()


def _shorten(client: TestClient, url: str = "https://example.com/foo") -> str:
    resp = client.post("/shorten", data={"url": url})
    assert resp.status_code == 200, resp.text
    # extract the freshly created code from the success banner
    needle = '<a href="/'
    body = resp.text
    idx = body.find(needle)
    assert idx > 0, body
    end = body.find('"', idx + len(needle))
    return body[idx + len(needle):end]


def test_shorten_creates_code(client: TestClient):
    code = _shorten(client)
    assert len(code) == 6
    assert code.isalnum()


def test_redirect_increments_clicks(client: TestClient):
    code = _shorten(client, "https://example.com/target")

    resp = client.get(f"/{code}", follow_redirects=False)
    assert resp.status_code == 307
    assert resp.headers["location"] == "https://example.com/target"

    # second click
    client.get(f"/{code}", follow_redirects=False)

    stats = client.get(f"/stats/{code}")
    assert stats.status_code == 200
    assert "<kbd" in stats.text  # the click counter widget
    assert ">2<" in stats.text   # 2 clicks recorded


def test_stats_shows_count(client: TestClient):
    code = _shorten(client, "https://example.com/x")
    resp = client.get(f"/stats/{code}")
    assert resp.status_code == 200
    assert "https://example.com/x" in resp.text
    assert ">0<" in resp.text


def test_unknown_code_returns_404(client: TestClient):
    assert client.get("/nope42", follow_redirects=False).status_code == 404
    assert client.get("/stats/nope42").status_code == 404


def test_invalid_url_returns_400(client: TestClient):
    resp = client.post("/shorten", data={"url": "javascript:alert(1)"})
    assert resp.status_code == 400
    assert "http://" in resp.text  # error message mentions valid scheme
