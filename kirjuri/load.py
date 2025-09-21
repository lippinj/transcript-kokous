import json
import os

from youtube_transcript_api import YouTubeTranscriptApi

from .raw import Transcript


CACHE_DIR = ".kirjuri-cache"


def load_raw(video_id: str, languages: list[str] | None = None) -> list | dict:
    languages = languages or ["fi"]
    os.makedirs(CACHE_DIR, exist_ok=True)
    filepath = f"{CACHE_DIR}/{video_id}-{'-'.join(languages)}.json"
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)
    except OSError:
        api = YouTubeTranscriptApi()
        result = api.fetch(video_id, languages=languages)
        raw = result.to_raw_data()
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(raw, f, ensure_ascii=False, indent=2)
        return raw


def load(video_id: str) -> Transcript:
    return Transcript.from_json(video_id, load_raw(video_id))