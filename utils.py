"""Utility functions."""


def daterange(start, end, delta, include_endpoint=False):
    date = start
    while date < end:
        yield date
        date += delta

    if include_endpoint:
        yield date
