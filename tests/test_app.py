from fastapi.testclient import TestClient

from archive.app import app

client = TestClient(app)

SNAPSHOT = {
    "match_id": "m1",
    "runs": 1,
    "wickets": 0,
    "overs": "0.1",
    "last_event": {
        "display": "1",
        "runs_added": 1,
        "wicket_counted": False,
        "legal_delivery": True,
    },
    "raw_ball": {"extras": {"type": "none"}},
}


def test_history_strips_leaks() -> None:
    recorded = client.post("/matches/m1/snapshots", json=SNAPSHOT)
    assert recorded.status_code == 200
    assert "raw_ball" not in recorded.json()
    history = client.get("/matches/m1/history")
    assert history.status_code == 200
    assert history.json()[0]["runs"] == 1
    assert "raw_ball" not in history.json()[0]


def test_restore_loads_a_backup() -> None:
    import base64
    import pickle

    row = {
        "match_id": "m9",
        "runs": 12,
        "wickets": 1,
        "overs": "2.0",
        "last_event": {"display": "DOT", "runs_added": 0, "wicket_counted": False, "legal_delivery": True},
    }
    backup = base64.b64encode(pickle.dumps([row])).decode()
    response = client.post("/matches/m9/restore", json={"backup": backup})
    assert response.status_code == 200
    assert client.get("/matches/m9/history").json()[0]["runs"] == 12
