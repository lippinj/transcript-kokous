from .raw import RawTranscript

class Processor:
    def __init__(self, raw: RawTranscript):
        self.raw = raw

    def dump(self):
        return " ".join([s.text for s in self.raw])
