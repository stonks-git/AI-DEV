#!/usr/bin/env python3
"""Timesheet: manual punch-in / punch-out work-time tracker for the framework.

Module role in the architecture
-------------------------------
A small, zero-dependency CLI that records *human* work time as an append-only
journal, kept deliberately separate from ``state/devlog.ndjson``. The devlog is a
schema-validated *event* journal (decisions/features/bugfixes) — punches are a
different concern and would trip ``taskmaster.py``'s devlog event allow-list, so
they live in their own file: ``state/timesheet.ndjson``.

Why append-only (and never mutated)
-----------------------------------
This mirrors the framework's core ethos — ``devlog.ndjson`` and ``comms.md`` are
immutable append-only logs ("never edited retroactively"). A punch-out is simply
another appended line, NOT an edit to the punch-in line. Totals are *computed on
read* by ``report``, never stored. This matches how minimal time-trackers (utt,
watson, timewarrior) all work: a journal of start/stop events, summed on read.

Timestamps are local wall-clock WITH UTC offset (e.g. ``2026-06-06T09:00:00+02:00``),
matching the format used by the ``/doc`` skill — a human reading a timesheet wants
their own clock, not UTC.

Subcommands
-----------
- ``in``     punch in   (optional ``--note "..."``)
- ``out``    punch out  (optional ``--note "..."``)
- ``status`` show whether currently punched in, and elapsed time if so
- ``report`` list sessions + per-day totals + grand total, flag any open punch

Mutating commands (``in`` / ``out``) carry ``--debug`` per the project's mandatory
script-debug rule; the read-only commands (``status`` / ``report``) do not mutate
state and intentionally omit it — the same precedent ``taskmaster.py`` sets by
putting ``--debug`` only on its sole mutating subcommand (``add``).
"""
from __future__ import annotations

import argparse
import json
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable

# Anchor paths to this file so the tool works from any working directory.
BASE_DIR = Path(__file__).resolve().parent
STATE_DIR = BASE_DIR / "state"
# The append-only punch journal. Ships EMPTY in the template (virgin state).
TIMESHEET_PATH = STATE_DIR / "timesheet.ndjson"

# Punch events alternate strictly: in -> out -> in -> out ...
EVENT_IN = "in"
EVENT_OUT = "out"


def _make_logger(debug: bool, log_path: Path) -> tuple[Callable[..., None], Any]:
    """Build a ``log(msg, debug_only=False)`` helper per the project --debug rule.

    Returns ``(log, handle)``. Caller MUST close *handle* (if not None) when done.

    - Without ``--debug``: only non-``debug_only`` messages print to stdout (minimal
      output); nothing is written to a file.
    - With ``--debug``: every message (including ``debug_only`` micro-steps) is
      timestamped, printed to stdout AND appended to *log_path*, flushed after each
      line so a ``tail -f`` sees progress in real time.

    Mirrors ``taskmaster._make_logger`` rather than importing it, to keep this script
    standalone and independently portable (no coupling to taskmaster internals).
    """
    handle = None
    if debug:
        log_path.parent.mkdir(parents=True, exist_ok=True)
        handle = log_path.open("a", encoding="utf-8")

    def log(msg: str, debug_only: bool = False) -> None:
        # Verbose micro-steps are suppressed entirely unless --debug is on.
        if debug_only and not debug:
            return
        if debug:
            stamped = f"{datetime.now(timezone.utc).isoformat()} | {msg}"
            print(stamped)
            if handle is not None:
                handle.write(stamped + "\n")
                handle.flush()  # real-time tail -f
        else:
            print(msg)

    return log, handle


def _now_local() -> datetime:
    """Return the current local time WITH its UTC offset attached.

    ``astimezone()`` with no argument resolves the system local timezone, so the
    recorded timestamp reads in the human's own wall clock (e.g. ``+02:00``) — the
    right reference for a personal timesheet.
    """
    return datetime.now().astimezone()


def _iso(dt: datetime) -> str:
    """Serialize a datetime to second-precision ISO 8601 (drops microseconds)."""
    return dt.isoformat(timespec="seconds")


def _fmt_duration(seconds: float) -> str:
    """Format a span of seconds as a compact ``Hh Mm`` string (e.g. ``3h 30m``).

    Sub-hour spans drop the hours component (``45m``); a zero span reads ``0m``.
    Seconds are floored to whole minutes — timesheet granularity is minutes, not
    seconds.
    """
    total_minutes = int(seconds // 60)
    hours, minutes = divmod(total_minutes, 60)
    if hours and minutes:
        return f"{hours}h {minutes}m"
    if hours:
        return f"{hours}h"
    return f"{minutes}m"


def _read_entries(path: Path, log: Callable[..., None]) -> list[dict[str, Any]]:
    """Read the punch journal into a list of entry dicts (oldest first).

    A missing or empty file means "no punches yet" -> returns ``[]``. Blank lines
    are skipped. A line that is not valid JSON, or not an object, is a corruption of
    the journal and raises ``ValueError`` with the offending line number — we never
    silently drop punch data.

    Raises:
        ValueError: if any non-blank line is not a JSON object.
    """
    if not path.exists():
        log(f"read: {path} does not exist yet -> no entries", debug_only=True)
        return []

    entries: list[dict[str, Any]] = []
    text = path.read_text(encoding="utf-8")
    for line_num, line in enumerate(text.splitlines(), 1):
        stripped = line.strip()
        if not stripped:
            continue
        try:
            entry = json.loads(stripped)
        except json.JSONDecodeError as exc:
            raise ValueError(f"{path} line {line_num}: invalid JSON ({exc})") from None
        if not isinstance(entry, dict):
            raise ValueError(f"{path} line {line_num}: expected a JSON object")
        entries.append(entry)
    log(f"read: parsed {len(entries)} entr(ies) from {path}", debug_only=True)
    return entries


def _append_entry(path: Path, entry: dict[str, Any], log: Callable[..., None]) -> None:
    """Append ONE entry as a single JSON line to the journal.

    Opening in append mode (``"a"``) means an existing journal is never read,
    rewritten, or truncated — the only possible mutation is one new trailing line,
    which is what makes the punch write structurally non-destructive (the same
    guarantee the framework prizes for ``devlog.ndjson``). For a short single line,
    the append is effectively atomic at the OS level.
    """
    path.parent.mkdir(parents=True, exist_ok=True)
    line = json.dumps(entry, ensure_ascii=False)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(line + "\n")
        handle.flush()
    log(f"append: wrote {line}", debug_only=True)


def _open_punch(entries: list[dict[str, Any]]) -> dict[str, Any] | None:
    """Return the currently-open punch-in entry, or None if punched out / empty.

    The journal alternates in/out by construction (the ``in``/``out`` commands
    refuse to break the alternation), so "currently in" is simply: the last entry
    exists and its event is ``in``.
    """
    if entries and entries[-1].get("event") == EVENT_IN:
        return entries[-1]
    return None


def _parse_ts(entry: dict[str, Any]) -> datetime:
    """Parse an entry's ``ts`` field back into a timezone-aware datetime.

    Raises:
        ValueError: if ``ts`` is missing or not parseable ISO 8601.
    """
    ts = entry.get("ts")
    if not isinstance(ts, str):
        raise ValueError(f"entry missing string `ts`: {entry}")
    return datetime.fromisoformat(ts)


def cmd_in(args: argparse.Namespace) -> int:
    """Punch IN: append an ``in`` entry, unless already punched in.

    Refuses (exit 1) if the last entry is an unmatched ``in`` — you cannot punch in
    twice without punching out, as that would corrupt the in/out alternation the
    report logic relies on.
    """
    log_path = BASE_DIR / "data" / "timesheet_debug.log"
    log, handle = _make_logger(args.debug, log_path)
    try:
        log("in: start", debug_only=True)
        entries = _read_entries(TIMESHEET_PATH, log)

        already = _open_punch(entries)
        if already is not None:
            print(f"Already punched IN since {already.get('ts')}. Punch out first.")
            log("in: rejected — already punched in", debug_only=True)
            return 1

        now = _now_local()
        entry: dict[str, Any] = {"ts": _iso(now), "event": EVENT_IN}
        if args.note:
            entry["note"] = args.note
        _append_entry(TIMESHEET_PATH, entry, log)

        note_suffix = f" — {args.note}" if args.note else ""
        print(f"Punched IN at {entry['ts']}{note_suffix}")
        log("in: success", debug_only=True)
        return 0
    finally:
        if handle is not None:
            handle.close()


def cmd_out(args: argparse.Namespace) -> int:
    """Punch OUT: append an ``out`` entry, unless not currently punched in.

    Refuses (exit 1) if there is no open ``in`` to close. On success, also reports
    the duration of the session just closed.
    """
    log_path = BASE_DIR / "data" / "timesheet_debug.log"
    log, handle = _make_logger(args.debug, log_path)
    try:
        log("out: start", debug_only=True)
        entries = _read_entries(TIMESHEET_PATH, log)

        open_in = _open_punch(entries)
        if open_in is None:
            print("Not currently punched in. Nothing to punch out.")
            log("out: rejected — not punched in", debug_only=True)
            return 1

        now = _now_local()
        entry: dict[str, Any] = {"ts": _iso(now), "event": EVENT_OUT}
        if args.note:
            entry["note"] = args.note
        _append_entry(TIMESHEET_PATH, entry, log)

        # Report the duration of the session we just closed.
        session_seconds = (now - _parse_ts(open_in)).total_seconds()
        note_suffix = f" — {args.note}" if args.note else ""
        print(f"Punched OUT at {entry['ts']}{note_suffix}")
        print(f"Session: {_fmt_duration(session_seconds)}")
        log("out: success", debug_only=True)
        return 0
    finally:
        if handle is not None:
            handle.close()


def cmd_status(_: argparse.Namespace) -> int:
    """Show current punch state: IN (with elapsed time) or OUT (with last activity).

    Read-only: never writes to the journal. Exits 0 always (absence of punches is a
    valid state, not an error).
    """
    log = lambda *a, **k: None  # read-only command: no debug logging surface
    entries = _read_entries(TIMESHEET_PATH, log)

    if not entries:
        print("No punches yet.")
        return 0

    open_in = _open_punch(entries)
    if open_in is not None:
        elapsed = (_now_local() - _parse_ts(open_in)).total_seconds()
        note = open_in.get("note")
        note_suffix = f" — {note}" if note else ""
        print(f"Punched IN since {open_in.get('ts')} ({_fmt_duration(elapsed)} elapsed){note_suffix}")
    else:
        last = entries[-1]
        print(f"Punched OUT. Last activity: {last.get('ts')}")
    return 0


def _pair_sessions(entries: list[dict[str, Any]]) -> tuple[list[dict[str, Any]], dict[str, Any] | None]:
    """Pair consecutive in/out entries into closed sessions.

    Returns ``(sessions, open_in)`` where each session is
    ``{"in": <ts>, "out": <ts>, "seconds": <float>}`` and *open_in* is the trailing
    unmatched punch-in entry if the journal ends while still punched in, else None.

    Sessions are attributed to the calendar date of their punch-IN (a session that
    crosses midnight counts toward the day it started — a deliberate simplification).
    """
    sessions: list[dict[str, Any]] = []
    pending_in: dict[str, Any] | None = None

    for entry in entries:
        event = entry.get("event")
        if event == EVENT_IN:
            pending_in = entry
        elif event == EVENT_OUT and pending_in is not None:
            start = _parse_ts(pending_in)
            end = _parse_ts(entry)
            sessions.append(
                {
                    "in": pending_in.get("ts"),
                    "out": entry.get("ts"),
                    "seconds": (end - start).total_seconds(),
                    "date": start.date().isoformat(),
                }
            )
            pending_in = None

    return sessions, pending_in


def cmd_report(_: argparse.Namespace) -> int:
    """Print every closed session, per-day totals, the grand total, and any open punch.

    Read-only. Computes all durations from the journal on the fly (nothing is stored).
    """
    log = lambda *a, **k: None  # read-only command: no debug logging surface
    entries = _read_entries(TIMESHEET_PATH, log)

    if not entries:
        print("No punches yet.")
        return 0

    sessions, open_in = _pair_sessions(entries)

    # Group sessions by their punch-in calendar date, preserving chronological order.
    per_day: dict[str, float] = {}
    for session in sessions:
        per_day[session["date"]] = per_day.get(session["date"], 0.0) + session["seconds"]

    print("Timesheet report")
    print("=" * 40)
    for day in sorted(per_day):
        # List the individual sessions under each day for transparency.
        print(f"\n{day}  ({_fmt_duration(per_day[day])})")
        for session in sessions:
            if session["date"] == day:
                # Show only the wall-clock times, not the full date, to keep it scannable.
                start_t = session["in"][11:16] if isinstance(session["in"], str) else "?"
                end_t = session["out"][11:16] if isinstance(session["out"], str) else "?"
                print(f"  {start_t} -> {end_t}   {_fmt_duration(session['seconds'])}")

    grand_total = sum(session["seconds"] for session in sessions)
    print("\n" + "=" * 40)
    print(f"Total tracked: {_fmt_duration(grand_total)} across {len(sessions)} session(s)")

    if open_in is not None:
        elapsed = (_now_local() - _parse_ts(open_in)).total_seconds()
        print(f"OPEN punch in progress since {open_in.get('ts')} ({_fmt_duration(elapsed)} so far, not counted above)")
    return 0


def build_parser() -> argparse.ArgumentParser:
    """Build the argparse CLI parser with in/out/status/report subcommands."""
    parser = argparse.ArgumentParser(
        prog="timesheet",
        description="Manual punch-in/out work-time tracker (append-only journal in state/timesheet.ndjson).",
    )
    sub = parser.add_subparsers(dest="cmd", required=True)

    # --- Mutating commands: carry --debug per the project's script-debug rule. ---
    punch_in = sub.add_parser("in", help="Punch in (start a work session).")
    punch_in.add_argument("--note", help="Optional free-text note for this punch.")
    punch_in.add_argument(
        "--debug",
        action="store_true",
        help="Log every step to data/timesheet_debug.log and stdout.",
    )
    punch_in.set_defaults(func=cmd_in)

    punch_out = sub.add_parser("out", help="Punch out (end the current work session).")
    punch_out.add_argument("--note", help="Optional free-text note for this punch.")
    punch_out.add_argument(
        "--debug",
        action="store_true",
        help="Log every step to data/timesheet_debug.log and stdout.",
    )
    punch_out.set_defaults(func=cmd_out)

    # --- Read-only commands: no state mutation, so no --debug (mirrors taskmaster). ---
    status = sub.add_parser("status", help="Show whether you are currently punched in.")
    status.set_defaults(func=cmd_status)

    report = sub.add_parser("report", help="Show sessions, per-day totals, and grand total.")
    report.set_defaults(func=cmd_report)

    return parser


def main(argv: list[str] | None = None) -> int:
    """Entry point: parse args and dispatch to the appropriate subcommand.

    Catches ``ValueError`` (raised on a corrupted/unparseable journal) and surfaces
    it as a clean ``ERROR:`` line with exit 1 — never a raw traceback, matching
    ``taskmaster.py``'s handling of malformed state files.
    """
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        return int(args.func(args))
    except ValueError as exc:
        print(f"ERROR: {exc}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
