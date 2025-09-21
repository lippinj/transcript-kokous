from itertools import pairwise

from .raw import Snippet, Transcript
from .timestamp import tsformat, tsformatf, dformatf


def is_note(snippet):
    s = snippet.text.strip()
    return s.startswith("[") and s.endswith("]")


class Block(Transcript):

    @property
    def filename(self):
        return f"{tsformat(self.start).replace(':', '.')}.md"

    def split_by_speaker(self):
        dst = BlockBuilder(self)
        for snippet in self:
            if snippet.text.startswith(">>"):
                text = snippet.text.removeprefix(">>").strip()
                snippet = Snippet(text, snippet.start, snippet.duration)
                dst.add(snippet)
            elif ">>" in snippet.text:
                assert False
            else:
                dst.add(snippet)
        return dst.build()

    def split_by_silence(self, dt=5.0):
        dst = BlockBuilder(self)
        dst.add(self[0])
        for a, b in pairwise(self):
            if b.start - a.stop >= dt:
                dst.start(b)
            else:
                dst.add(b)
        return dst.build()

    def split_by_note(self):
        dst = BlockBuilder(self)
        dst.add(self[0])
        for a, b in pairwise(self):
            if is_note(a) or is_note(b):
                dst.start(b)
            else:
                dst.add(b)
        return dst.build()

    def to_json(self):
        return {
            "start": self.start,
            "duration": self.duration,
            "snippets": [snippet.to_json() for snippet in self],
        }


class BlockBuilder:
    def __init__(self, src: Block):
        self.src = src
        self.dst = []

    def build(self):
        return [Block(self.src.video_id, snippets) for snippets in self.dst]

    def add(self, snippet):
        if len(self.dst) == 0:
            self.start(snippet)
        else:
            self.append(snippet)

    def start(self, snippet):
        self.dst.append([snippet])

    def append(self, snippet):
        self.dst[-1].append(snippet)

