class Video:
    def __init__(self, id: str):
        self.id = id

    def __str__(self):
        return self.id

    def __repr__(self):
        return self.id

    @property
    def base_url(self):
        return f"https://www.youtube.com/watch?v={self.id}"

    def url(self, timestamp: int | None = None):
        if timestamp:
            return f"{self.base_url}&t={timestamp}"
        else:
            return self.base_url
