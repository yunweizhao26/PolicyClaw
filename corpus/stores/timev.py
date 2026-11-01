#!/usr/bin/env python3
import resource
import signal
import subprocess
import sys
import time

log, cmd = sys.argv[1], sys.argv[3:]
if sys.argv[2] != "--" or not cmd:
    sys.exit("usage: timev.py LOGFILE -- command args...")
t0 = time.time()
proc = subprocess.Popen(cmd)


def forward(signum, frame):
    try:
        proc.send_signal(signum)
    except ProcessLookupError:
        pass


signal.signal(signal.SIGTERM, forward)
signal.signal(signal.SIGINT, forward)
while True:
    try:
        rc = proc.wait()
        break
    except InterruptedError:
        continue
el = time.time() - t0
ru = resource.getrusage(resource.RUSAGE_CHILDREN)
h, rem = divmod(el, 3600)
m, s = divmod(rem, 60)
wall = f"{int(h)}:{int(m):02d}:{s:05.2f}" if h else f"{int(m)}:{s:05.2f}"
with open(log, "w") as f:
    f.write(f"\tCommand being timed: \"{' '.join(cmd)}\"\n")
    f.write(f"\tUser time (seconds): {ru.ru_utime:.2f}\n\tSystem time (seconds): {ru.ru_stime:.2f}\n")
    f.write(f"\tElapsed (wall clock) time (h:mm:ss or m:ss): {wall}\n")
    f.write(f"\tMaximum resident set size (kbytes): {ru.ru_maxrss}\n")
    f.write(f"\tExit status: {rc}\n")
sys.exit(rc)
