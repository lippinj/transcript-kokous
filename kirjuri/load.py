import json
import os

from youtube_transcript_api import YouTubeTranscriptApi

from .raw import RawTranscript


CACHE_DIR = ".kirjuri-cache"
LANGS = ["fi", "se", "en"]


def load_raw(video_id: str) -> list | dict:
    os.makedirs(CACHE_DIR, exist_ok=True)
    filepath = f"{CACHE_DIR}/{video_id}.json"
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)
    except OSError:
        api = YouTubeTranscriptApi()
        raw = api.fetch(video_id, languages=LANGS).to_raw_data()
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(raw, f, ensure_ascii=False, indent=2)
        return raw


def load(video_id: str) -> RawTranscript:
    return RawTranscript.from_json(load_raw(video_id))