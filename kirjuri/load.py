import json
import os

from dataclasses import dataclass

from youtube_transcript_api import YouTubeTranscriptApi

from .raw import Snippet, Transcript
from .video import Video


def load(video_id: str) -> Transcript:
    """Load a raw transcript (from cache if possible)"""
    spec = FetchSpec(video_id, ["fi"])
    snippets = Snippet.from_json_list(_load_raw(spec))
    return Transcript.from_json(Video(video_id), snippets)


# Implementation details below

_CACHE_DIR = ".kirjuri-cache"


@dataclass
class FetchSpec:
    id: str
    languages: list[str]

    @property
    def basename(self):
        return "-".join([self.id] + self.languages)

    @property
    def filename(self):
        return f"{self.basename}.json"

    @property
    def cache_path(self):
        return f"{_CACHE_DIR}/{self.filename}"


def _load_raw(spec: FetchSpec):
    try:
        return _load_from_cache(spec)
    except OSError:
        raw = _fetch(spec)
        _store_to_cache(raw, spec)
        return raw


def _load_from_cache(spec: FetchSpec):
    with open(spec.cache_path, "r", encoding="utf-8") as f:
        return json.load(f)


def _store_to_cache(j, spec: FetchSpec):
    os.makedirs(_CACHE_DIR, exist_ok=True)
    with open(spec.cache_path, "w", encoding="utf-8") as f:
        json.dump(j, f, ensure_ascii=False, indent=2)


def _fetch(spec: FetchSpec):
    api = YouTubeTranscriptApi()
    result = api.fetch(spec.id, languages=spec.languages)
    return result.to_raw_data()
