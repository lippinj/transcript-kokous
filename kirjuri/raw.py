from dataclasses import dataclass


@dataclass
class RawSnippet:
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
        return RawSnippet(j["text"], j["start"], j["duration"])


@dataclass
class RawTranscript:
    snippets: list[RawSnippet]

    def __len__(self):
        return len(self.snippets)

    def __iter__(self):
        return iter(self.snippets)

    def __getitem__(self, *args):
        return self.snippets[*args]

    def start(self):
        return self[0].start

    def stop(self):
        return self[-1].stop

    def duration(self):
        return self.stop - self.start

    @staticmethod
    def from_json(j: list):
        return RawTranscript([RawSnippet.from_json(s) for s in j])
