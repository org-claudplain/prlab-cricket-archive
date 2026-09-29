# cricket-archive

Snapshot store. Persists product `ScoreSnapshot` fields for later replay.

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
pytest
uvicorn archive.app:app --port 8003
```
