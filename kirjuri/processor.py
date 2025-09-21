import os
import shutil

from .raw import Transcript


def hms(s):
    h = int(s // 3600)
    s -= (h * 3600)
    m = int(s // 60)
    s -= (m * 60)
    return h, m, s


def tsformat(s: int):
    h, m, s = hms(s)
    return f"{h:02d}:{m:02d}:{int(s):02d}"


def tsformatf(s: float):
    h, m, s = hms(s)
    return f"{h:02d}:{m:02d}:{s:02.3f}"



class Block(Transcript):
    pass


class Processor:
    def __init__(self, raw: Transcript):
        self.raw = raw
        self.blocks = [Block(raw.video_id, raw.snippets)]

    def dump(self, dirname="out"):
        shutil.rmtree(dirname, ignore_errors=True)
        os.mkdir(dirname)

        for block in self.blocks:
            ts = int(block.start)
            with open(f"{dirname}/{ts}.md", "w", encoding="utf-8") as f:
                f.write(f"Alkaa [{tsformat(block.start)}]({block.url}), kesto {tsformatf(block.duration)}\n\n")
                f.write(f"{block.text}\n")


        return " ".join([s.text for s in self.raw])
