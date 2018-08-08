import datetime as dt

MIN_DATETIME = dt.datetime(1, 1, 1)

class ScoredSentence:
    def __init__(self, text):
        self.text = text
        self.last_used = MIN_DATETIME
        self.score = 0

    def compare(self, other):
        if not other or \
                self.last_used < other.last_used or \
                (self.last_used == other.last_used and self.score > other.score):
            return self
        else:
            return other
