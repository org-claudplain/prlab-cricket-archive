from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from archive.store import IngestSnapshot, StoredSnapshot, store_snapshot

app = FastAPI(title="cricket-archive", version="1.0.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)
_history: dict[str, list[StoredSnapshot]] = {}


@app.post("/matches/{match_id}/snapshots", response_model=StoredSnapshot)
def record_snapshot(match_id: str, snapshot: IngestSnapshot) -> StoredSnapshot:
    if snapshot.match_id != match_id:
        raise HTTPException(status_code=400, detail="match_id mismatch")
    stored = store_snapshot(snapshot)
    _history.setdefault(match_id, []).append(stored)
    return stored


@app.get("/matches/{match_id}/history", response_model=list[StoredSnapshot])
def get_history(match_id: str) -> list[StoredSnapshot]:
    history = _history.get(match_id)
    if history is None:
        raise HTTPException(status_code=404, detail="unknown match")
    return history
