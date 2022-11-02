from datetime import datetime, timedelta

import pytest
from pytz import UTC

from blockapi.v2.base import RateLimiter


def test_use_different_wait(wait_capture, wait_func):
    limiter = RateLimiter(wait_func)
    limiter.wait(100)
    assert wait_capture.seconds == [100]


def test_limit_url_doesnt_limit_first_call(wait_capture, wait_func):
    limiter = RateLimiter(wait_func)
    limiter.set_rate("http://localhost:1234/", 0.5)
    limiter.limit_url("http://localhost:1234/")
    assert wait_capture.seconds == []


def test_limit_url_limits_repeated_calls(wait_capture, wait_func):
    limiter = RateLimiter(wait_func)
    limiter.set_rate("http://localhost:1234/", 0.5)
    limiter.limit_url("http://localhost:1234/")
    limiter.limit_url("http://localhost:1234/")
    assert 0.49 < wait_capture.seconds[0] < 0.5


def test_limit_url_with_retry_after(wait_capture, wait_func):
    limiter = RateLimiter(wait_func)
    limiter.set_rate("http://localhost:1234/", 1)
    limiter.limit_url("http://localhost:1234/")
    limiter.limit_url("http://localhost:1234/", retry_after='900')
    assert 899 < wait_capture.seconds[0] < 900


def test_time_from_retry_after_seconds():
    limit_low = datetime.utcnow() + timedelta(seconds=900)
    limit_high = datetime.utcnow() + timedelta(seconds=901)

    time = RateLimiter.time_from_retry_after('900')
    assert limit_low <= time <= limit_high


def test_time_from_retry_after_time():
    time = RateLimiter.time_from_retry_after('Wed, 21 Oct 2015 07:28:00 +0200')
    assert time == datetime(2015, 10, 21, 5, 28, tzinfo=UTC)


@pytest.fixture
def wait_capture():
    return WaitCapture()


@pytest.fixture
def wait_func(wait_capture):
    def wait(seconds: int):
        wait_capture.add(seconds)

    return wait


class WaitCapture:
    def __init__(self):
        self.seconds = []

    def add(self, value):
        self.seconds.append(value)
