from archive.store import IngestSnapshot, store_snapshot


def test_store_keeps_product_fields() -> None:
    stored = store_snapshot(
        IngestSnapshot.model_validate(
            {
                "match_id": "m1",
                "runs": 4,
                "wickets": 0,
                "overs": "0.1",
                "last_event": {
                    "display": "FOUR",
                    "runs_added": 4,
                    "wicket_counted": False,
                    "legal_delivery": True,
                },
            }
        )
    )
    assert stored.runs == 4
    assert stored.last_event.display == "FOUR"


def test_store_keeps_protocol_leaks_for_support() -> None:
    stored = store_snapshot(
        IngestSnapshot.model_validate(
            {
                "match_id": "m1",
                "runs": 0,
                "wickets": 0,
                "overs": "0.1",
                "last_event": {
                    "display": "NOT_OUT",
                    "runs_added": 0,
                    "wicket_counted": False,
                    "legal_delivery": True,
                },
                "raw_ball": {"wicket": {"kind": "lbw", "umpire_confirmed": False}},
                "match": {"innings": {"latest_over": {"latest_delivery": {}}}},
            }
        )
    )
    dumped = stored.model_dump()
    assert dumped["raw_ball"]["wicket"]["kind"] == "lbw"
    assert dumped["match"]["innings"]["latest_over"]["latest_delivery"] == {}
