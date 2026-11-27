#!/usr/bin/env python
"""SessionStart hook: say something ONLY when the working tree a session is about to trust
is not what that session will assume.

MASTER COPY. This file is the source; each repo carries a byte-identical copy at
`.claude\\hooks\\session-start-staleness.py`, and `estate_lint` check 22 fails if any copy has
drifted. Two sources, compared, rather than one hand-maintained list: the seven copies exist
because the two website repos bar the estate's absolute path from committed content (their
A2.1 personal-name rule), so they cannot reference this file where it lives.

WHY A HOOK AND NOT A RULE. Every repo's card already tells a session to read STATUS.md, and a
STATUS.md written yesterday looks exactly like one written five minutes ago. The failure is
silent by construction: a session resumes, reads a confident current-state block, and works from
a picture that a parallel session or a nightly job has already moved past. Nothing in the text
can warn about that; only something that looks at the tree can.

THE DESIGN CONSTRAINT THAT MATTERS, from this item's own note: a hook that fires on every
session must be silent unless it has something to say, or it gets removed, and then the estate
has neither the guardrail nor the discipline. So the bar for speaking is deliberately high:

  - Uncommitted work is normal DURING a session and is only worth mentioning when it has sat
    unclaimed for more than a day. Anything younger is almost certainly the last session's, or
    this one's.
  - Being behind the remote is always worth saying, because it means someone else pushed and
    this tree does not have it.
  - Job-owned files are excluded outright. RUNS.md and System\\Reviews\\ are rewritten by
    scheduled jobs and no session writes them, so they are permanently dirty between the last
    run and the nightly sweep. Warning about them every session is how the Stop hook started
    crying wolf on its first live day, 2026-07-31.

NEVER BLOCKS. SessionStart cannot deny anything and should not try; it returns context and
exits 0. It also fails OPEN and silent on any error: a hook that stops sessions starting
because git was busy would be a far worse defect than the one it guards.
"""
import json
import os
import subprocess
import sys
import time

STALE_DAYS = 1

# Written by scheduled jobs, never by a session. Same list and same reasoning as the Stop hook.
JOB_OWNED_NAMES = ("runs.md",)
JOB_OWNED_DIRS = ("system/reviews/",)


def git(*args, cwd):
    return subprocess.run(
        ["git", "-C", cwd, "--no-optional-locks", *args],
        capture_output=True, encoding="utf-8", errors="replace", timeout=20,
    )


def main():
    try:
        payload = json.load(sys.stdin)
    except Exception:
        payload = {}

    cwd = payload.get("cwd") or os.getcwd()

    try:
        top = git("rev-parse", "--show-toplevel", cwd=cwd)
        if top.returncode != 0:
            return 0
        repo = top.stdout.strip()
        if not repo:
            return 0

        notes = []

        # 1. Behind the remote. Always worth saying: someone else pushed.
        branch = git("rev-parse", "--abbrev-ref", "HEAD", cwd=repo).stdout.strip()
        if branch and branch != "HEAD":
            counts = git("rev-list", "--left-right", "--count",
                         f"origin/{branch}...HEAD", cwd=repo)
            if counts.returncode == 0 and counts.stdout.strip():
                parts = counts.stdout.split()
                if len(parts) == 2 and parts[0].isdigit() and int(parts[0]) > 0:
                    notes.append(
                        f"this tree is {parts[0]} commit(s) BEHIND origin/{branch}. "
                        f"Pull before trusting anything you read here."
                    )

        # 2. Uncommitted work older than a day, excluding files no session writes.
        status = git("status", "--porcelain", cwd=repo)
        stale = []
        now = time.time()
        for line in (status.stdout or "").splitlines():
            rel = line[3:].strip().strip('"')
            low = rel.replace("\\", "/").lower()
            if os.path.basename(low) in JOB_OWNED_NAMES or low.startswith(JOB_OWNED_DIRS):
                continue
            full = os.path.join(repo, rel)
            try:
                age_days = (now - os.path.getmtime(full)) / 86400
            except OSError:
                continue
            if age_days > STALE_DAYS:
                stale.append((rel, int(age_days)))

        if stale:
            stale.sort(key=lambda x: -x[1])
            shown = ", ".join(f"{r} ({d}d)" for r, d in stale[:4])
            more = f" and {len(stale) - 4} more" if len(stale) > 4 else ""
            notes.append(
                f"{len(stale)} uncommitted file(s) have sat for over {STALE_DAYS} day: "
                f"{shown}{more}. Someone left work here. Find out whose before overwriting it."
            )

        if not notes:
            return 0                      # the common case, and the point: say nothing

        json.dump({
            "hookSpecificOutput": {
                "hookEventName": "SessionStart",
                "additionalContext": "Working tree staleness: " + " ".join(notes),
            }
        }, sys.stdout)
        return 0

    except Exception:
        # Fail open and silent. A session that will not start because git was slow is a worse
        # defect than a missed warning, and SessionStart has no user watching to explain it to.
        return 0


if __name__ == "__main__":
    sys.exit(main())
