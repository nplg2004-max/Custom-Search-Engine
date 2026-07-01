import hashlib
import json
import os
from pathlib import Path
from typing import Optional

CACHE_DIR = Path("cache")
CACHE_FILE = CACHE_DIR / "results.json"


def _load() -> dict:
    if CACHE_FILE.exists():
        try:
            return json.loads(CACHE_FILE.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            return {}
    return {}


def _save(data: dict) -> None:
    CACHE_DIR.mkdir(exist_ok=True)
    CACHE_FILE.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")


def _key(query: str) -> str:
    return hashlib.md5(query.strip().lower().encode()).hexdigest()


def get(query: str) -> Optional[dict]:
    return _load().get(_key(query))


def set(query: str, answer: str, sources: list) -> None:
    cache = _load()
    cache[_key(query)] = {"answer": answer, "sources": sources}
    _save(cache)


def clear() -> None:
    if CACHE_FILE.exists():
        CACHE_FILE.unlink()
        print("Cache cleared.")
    else:
        print("Cache is already empty.")
