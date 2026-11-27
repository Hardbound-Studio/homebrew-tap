#!/usr/bin/env python
"""Run a sibling hook script if it exists here; exit 0 if it does not.

Most hooks a dev repo's settings wire are gitignored copies that exist only on the machine that
installed them. In a fresh clone (a cloud session) `python missing.py` exits 2, and exit 2 from a
PreToolUse or UserPromptSubmit hook blocks the call, so the pilot's first cloud session was
refused at its first prompt (P11 cloud pilot, 2026-09-29). Where the script exists, it runs
exactly as before: same stdin, same stdout, same exit code.

The master lives in the estate's System/tools and is deployed, TRACKED, into every dev repo by
sync_dev_settings.py, which also wires every hook through it. It holds no path, so it is safe on
a remote. Edit the master and re-run the generator; never edit a repo's copy.
"""
import os
import runpy
import sys

if len(sys.argv) < 2:
    sys.exit(0)
name = sys.argv[1]
# A bare sibling filename only. Anything else is a wiring error, reported without blocking.
if os.path.basename(name) != name or not name.endswith(".py"):
    print(f"run-if-present: refusing non-sibling target {name!r}", file=sys.stderr)
    sys.exit(1)
target = os.path.join(os.path.dirname(os.path.abspath(__file__)), name)
if not os.path.isfile(target):
    sys.exit(0)
sys.argv = [target] + sys.argv[2:]
runpy.run_path(target, run_name="__main__")
