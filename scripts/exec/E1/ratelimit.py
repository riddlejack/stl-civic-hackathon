"""One clock for every E1 process that calls www.stlouis-mo.gov: at most one request per GAP seconds.

Processes take an exclusive lock on build/E1/private/.host_clock, wait until GAP has passed since
the last recorded request start, record the new start, and release.
"""
import fcntl, pathlib, time

CLOCK = pathlib.Path(__file__).resolve().parents[3] / 'build' / 'E1' / 'private' / '.host_clock'
GAP = 1.05


def wait_turn():
    CLOCK.parent.mkdir(parents=True, exist_ok=True)
    with open(CLOCK, 'a+') as f:
        fcntl.flock(f, fcntl.LOCK_EX)
        f.seek(0)
        try:
            last = float(f.read().strip() or 0)
        except ValueError:
            last = 0.0
        wait = last + GAP - time.time()
        if wait > 0:
            time.sleep(wait)
        f.seek(0); f.truncate(); f.write(repr(time.time())); f.flush()
        fcntl.flock(f, fcntl.LOCK_UN)
