"""Persist product ScoreSnapshot fields. Strip protocol leaks on write."""

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


class IngestSnapshot(BaseModel):
    """Accept extra keys from scoring leaks; drop them on store."""

    match_id: str
    runs: int
    wickets: int
    overs: str
    last_event: LastEvent
    model_config = {"extra": "ignore"}


def store_snapshot(payload: IngestSnapshot) -> StoredSnapshot:
    return StoredSnapshot(
        match_id=payload.match_id,
        runs=payload.runs,
        wickets=payload.wickets,
        overs=payload.overs,
        last_event=payload.last_event,
    )
