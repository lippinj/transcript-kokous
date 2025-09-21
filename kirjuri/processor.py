import os
import shutil
from itertools import pairwise

from .raw import Snippet, Transcript
from .timestamp import tsformat, tsformatf


def is_note(x):
    s = x.text.strip()
    return s.startswith("[") and s.endswith("]")


class Block(Transcript):

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



class Processor:
    def __init__(self, raw: Transcript):
        self.raw = raw
        self.blocks = [Block(raw.video_id, raw.snippets)]

    def split_by_speaker(self):
        self.grind(lambda block: block.split_by_speaker())

    def split_by_silence(self, *args):
        self.grind(lambda block: block.split_by_silence(*args))

    def split_by_note(self, *args):
        self.grind(lambda block: block.split_by_note(*args))

    def grind(self, predicate):
        self.blocks, old_blocks = [], self.blocks
        for block in old_blocks:
            self.blocks += predicate(block)

    def dump(self, dirname="out"):
        shutil.rmtree(dirname, ignore_errors=True)
        os.mkdir(dirname)

        for block in self.blocks:
            ts = int(block.start)
            with open(f"{dirname}/{ts}.md", "w", encoding="utf-8") as f:
                f.write(f"Alkaa [{tsformat(block.start)}]({block.url}), kesto {tsformatf(block.duration)}\n\n")
                f.write(f"{block.text}\n")

        return " ".join([s.text for s in self.raw])
