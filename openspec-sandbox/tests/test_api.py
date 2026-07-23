from unittest.mock import patch

from fastapi.testclient import TestClient

from text2gherkin.adapters.api import app

client = TestClient(app)

VALID_GHERKIN = "Feature: X\n\n  Scenario: Y\n    Given a\n    When b\n    Then c\n"


def test_convert_success():
    with patch("text2gherkin.adapters.api.convert", return_value=VALID_GHERKIN):
        response = client.post("/convert", json={"text": "some input text"})

    assert response.status_code == 200
    assert response.json() == {"gherkin": VALID_GHERKIN}


def test_convert_failure_returns_502():
    with patch("text2gherkin.adapters.api.convert", side_effect=ValueError("boom")):
        response = client.post("/convert", json={"text": "some input text"})

    assert response.status_code == 502
    assert response.json()["detail"] == "boom"


def test_convert_missing_text_returns_422():
    response = client.post("/convert", json={})

    assert response.status_code == 422
