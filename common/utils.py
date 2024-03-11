from itertools import chain
from os import kill


def union_querysets(*args):
    queryset = list(chain(*args))
    return queryset


def kill_wrapper(**kwargs):
    kill(kwargs)
