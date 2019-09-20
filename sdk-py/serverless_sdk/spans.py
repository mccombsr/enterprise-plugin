import time
from datetime import datetime


class Span(object):
    def __init__(self, emmiter, span_type):
        self.emmiter = emmiter
        self.span_type = span_type
        self.tags = {}

    def set_tag(self, tag, value):
        self.tags[tag] = value

    def dump(self):
        return {
            "tags": dict(type=self.span_type, **self.tags),
            "startTime": self.start_isoformat,
            "endTime": self.end_isoformat,
            "duration": int((self.end - self.start) * 1000),
        }

    def __enter__(self):
        self.start_isoformat = datetime.utcnow().isoformat() + "Z"
        self.start = time.time()

        return self

    def __exit__(self, *args):
        self.end_isoformat = datetime.utcnow().isoformat() + "Z"
        self.end = time.time()
        self.emmiter(self.dump())
