"""Persist snapshots including debug envelopes for support replays."""

from pydantic import BaseModel


class LastEvent(BaseModel):
    display: str
    runs_added: int
    wicket_counted: bool
    legal_delivery: bool


class StoredSnapshot(BaseModel):
    match_id: str
    runs: int
    wickets: int
    overs: str
    last_event: LastEvent
    raw_ball: dict | None = None
    match: dict | None = None


class IngestSnapshot(BaseModel):
    match_id: str
    runs: int
    wickets: int
    overs: str
    last_event: LastEvent
    raw_ball: dict | None = None
    match: dict | None = None
    model_config = {"extra": "ignore"}


def store_snapshot(payload: IngestSnapshot) -> StoredSnapshot:
    return StoredSnapshot(
        match_id=payload.match_id,
        runs=payload.runs,
        wickets=payload.wickets,
        overs=payload.overs,
        last_event=payload.last_event,
        raw_ball=payload.raw_ball,
        match=payload.match,
    )
