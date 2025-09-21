from dataclasses import dataclass

from .video import Video


@dataclass
class Snippet:
    text: str
    start: float
    duration: float

    @property
    def stop(self):
        return self.start + self.duration

    @property
    def lower(self):
        return self.text.lower()

    @staticmethod
    def from_json(j: dict):
        return Snippet(j["text"], j["start"], j["duration"])

    @staticmethod
    def from_json_list(jj: list):
        return [Snippet.from_json(j) for j in jj]

    def to_json(self):
        return {
            "start": self.start,
            "duration": self.duration,
            "text": self.text,
        }


@dataclass
class Transcript:
    video: Video
    snippets: list[Snippet]

    def __len__(self):
        return len(self.snippets)

    def __iter__(self):
        return iter(self.snippets)

    def __getitem__(self, i):
        return self.snippets[i]

    @property
    def url(self):
        return self.video.url(int(self.start))

    @property
    def start(self):
        return self[0].start

    @property
    def stop(self):
        return self[-1].stop

    @property
    def duration(self):
        return self.stop - self.start

    @property
    def text(self):
        return " ".join([s.text for s in self])
