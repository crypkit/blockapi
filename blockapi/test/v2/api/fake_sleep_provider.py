from blockapi.v2.base import ISleepProvider


class FakeSleepProvider(ISleepProvider):
    def __init__(self):
        self._calls = []

    def sleep(self, url: str, seconds: float):
        self._calls.append((url, seconds))

    @property
    def calls(self):
        return self._calls
