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


def test_history_keeps_raw_ball_for_support() -> None:
    recorded = client.post("/matches/m1/snapshots", json=SNAPSHOT)
    assert recorded.status_code == 200
    assert recorded.json()["raw_ball"]["extras"]["type"] == "none"
    history = client.get("/matches/m1/history")
    assert history.status_code == 200
    assert history.json()[0]["runs"] == 1
    assert history.json()[0]["raw_ball"]["extras"]["type"] == "none"
