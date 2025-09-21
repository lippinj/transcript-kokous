import json
import os
import shutil

from . import timestamp
from .block import Block
from .transcript import Transcript


class Processor:
    def __init__(self, raw: Transcript):
        self.raw = raw
        self.blocks = [Block(raw.video, raw.snippets)]

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

    def to_json(self):
        return {
            "video_id": self.raw.video.id,
            "blocks": [b.to_json() for b in self.blocks],
        }

    def to_file(self, filename):
        with open(filename, "w", encoding="utf-8") as f:
            f.write(json.dumps(self.to_json(), ensure_ascii=False, indent=2))

    def dump(self, dirname="out"):
        shutil.rmtree(dirname, ignore_errors=True)
        os.mkdir(dirname)

        for block in self.blocks:
            with open(f"{dirname}/{block.filename}", "w", encoding="utf-8") as f:
                f.write(f"Alkaa {timestamp.tsformat(block.start)}, ")
                f.write(f"kesto {timestamp.dformatf(block.duration)} ")
                f.write(f"([video]({block.url}))\n\n")
                f.write(f"{block.text}\n")

        with open(f"{dirname}/index.md", "w", encoding="utf-8") as f:
            for block in self.blocks:
                f.write(f"Alkaa {timestamp.tsformat(block.start)}, ")
                f.write(f"kesto {timestamp.dformatf(block.duration)} ")
                f.write(f"([teksti]({block.filename}), [video]({block.url}))\n\n")
                if len(block.text) < 300:
                    f.write(f"_{block.text}_\n\n")
                else:
                    f.write(f"_{block.text[:296]} ..._\n\n")


        return " ".join([s.text for s in self.raw])
