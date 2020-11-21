#!/usr/bin/env python3

import mre

from pydrake.systems.framework import DiagramBuilder

from pydrake.common import set_log_level
set_log_level("trace")


def traced(func, ignoredirs=None):
    """Decorates func such that its execution is traced, but filters out any
     Python code outside of the system prefix."""
    import functools
    import sys
    import trace
    if ignoredirs is None:
        ignoredirs = ["/usr", sys.prefix]
    tracer = trace.Trace(trace=1, count=0, ignoredirs=ignoredirs)

    @functools.wraps(func)
    def wrapped(*args, **kwargs):
        return tracer.runfunc(func, *args, **kwargs)

    return wrapped


@traced
def main():
    builder = DiagramBuilder()

    builder.AddSystem(mre.DoNothingSystem())


if __name__ == '__main__':
    main()
