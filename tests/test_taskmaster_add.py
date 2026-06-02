#!/usr/bin/env python3
"""Tests for taskmaster.py `add` — the deterministic, non-destructive task-write path.

Role in the architecture: `taskmaster add` is the ONLY state-mutating command and the
write primitive behind the /capture-task skill. Because it is the first-ever writer to
roadmap.json, it gets real coverage — silent loss/mutation of an existing task is the
exact failure this command exists to prevent (it must never happen undetected).

Two layers:
- Pure-core tests on `add_task(roadmap, task)` (no I/O) — fast, exhaustive on the rules.
- Integration tests on `cmd_add(args)` — exercise read → validate → atomic write → re-validate
  against a throwaway temp state dir, so the real roadmap.json is never touched.

Run: `python3 -m unittest discover -s tests` (or `python3 tests/test_taskmaster_add.py`).
No third-party test infra is used — stdlib unittest only, matching the project's
zero-dependency posture for taskmaster.py.
"""
from __future__ import annotations

import argparse
import contextlib
import io
import json
import sys
import tempfile
import unittest
from pathlib import Path

# taskmaster.py lives at the repository root, one level up from this tests/ dir.
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import taskmaster as tm  # noqa: E402


def make_task(**overrides):
    """Return a minimal VALID active task object; override any field via kwargs."""
    base = {
        "id": "T-002",
        "title": "Example task",
        "depends_on": [],
        "priority": "P1",
        "status": "todo",
        "owner": "ai",
        "intent": "Demonstrate a conformant active task.",
        "deliverable": "A thing that exists.",
        "acceptance_criteria": ["The thing exists."],
        "verification": ["Observe the thing."],
    }
    base.update(overrides)
    return base


def roadmap_with(*tasks):
    """Return a minimal valid roadmap dict containing *tasks*."""
    return {"meta": {}, "open_questions": [], "decisions": [], "tasks": list(tasks)}


def errors_of(issues):
    """Return only the error-level issues from an add_task/validate result."""
    return [i for i in issues if i.level == "error"]


class AddTaskPureTests(unittest.TestCase):
    """Exercise the pure core: append + combined validation, no I/O."""

    def test_appends_valid_task(self):
        roadmap = roadmap_with(make_task(id="T-001"))
        issues, new_roadmap = tm.add_task(roadmap, make_task(id="T-002"))
        self.assertEqual(errors_of(issues), [])
        self.assertEqual(len(new_roadmap["tasks"]), 2)
        self.assertEqual(new_roadmap["tasks"][-1]["id"], "T-002")

    def test_preserves_existing_tasks_by_reference(self):
        # The non-destructive guarantee: existing rows are the SAME objects, unchanged.
        original = make_task(id="T-001")
        roadmap = roadmap_with(original)
        _, new_roadmap = tm.add_task(roadmap, make_task(id="T-002"))
        self.assertIs(new_roadmap["tasks"][0], original)
        self.assertEqual(new_roadmap["tasks"][:1], roadmap["tasks"])

    def test_does_not_mutate_input_roadmap(self):
        roadmap = roadmap_with(make_task(id="T-001"))
        tm.add_task(roadmap, make_task(id="T-002"))
        self.assertEqual(len(roadmap["tasks"]), 1)  # input untouched

    def test_rejects_duplicate_id(self):
        roadmap = roadmap_with(make_task(id="T-001"))
        issues, _ = tm.add_task(roadmap, make_task(id="T-001"))
        self.assertTrue(any("duplicate id" in i.message for i in errors_of(issues)))

    def test_rejects_active_task_missing_acceptance_criteria(self):
        roadmap = roadmap_with()
        bad = make_task(id="T-001")
        del bad["acceptance_criteria"]
        issues, _ = tm.add_task(roadmap, bad)
        self.assertTrue(errors_of(issues))

    def test_rejects_empty_acceptance_criteria(self):
        roadmap = roadmap_with()
        issues, _ = tm.add_task(roadmap, make_task(id="T-001", acceptance_criteria=[]))
        self.assertTrue(any("acceptance_criteria" in i.message for i in errors_of(issues)))

    def test_rejects_self_dependency(self):
        roadmap = roadmap_with()
        issues, _ = tm.add_task(roadmap, make_task(id="T-001", depends_on=["T-001"]))
        self.assertTrue(any("itself" in i.message for i in errors_of(issues)))

    def test_rejects_missing_dependency(self):
        roadmap = roadmap_with()
        issues, _ = tm.add_task(roadmap, make_task(id="T-001", depends_on=["T-999"]))
        self.assertTrue(any("missing task" in i.message for i in errors_of(issues)))

    def test_accepts_dependency_on_existing_task(self):
        roadmap = roadmap_with(make_task(id="T-001"))
        issues, new_roadmap = tm.add_task(roadmap, make_task(id="T-002", depends_on=["T-001"]))
        self.assertEqual(errors_of(issues), [])
        self.assertEqual(len(new_roadmap["tasks"]), 2)

    def test_rejects_non_dict_task(self):
        roadmap = roadmap_with()
        issues, _ = tm.add_task(roadmap, ["not", "a", "task"])
        self.assertTrue(errors_of(issues))


class CmdAddIntegrationTests(unittest.TestCase):
    """Exercise cmd_add end-to-end against a throwaway temp state dir."""

    def setUp(self):
        # Redirect taskmaster's BASE_DIR/STATE_DIR at module level to a temp sandbox,
        # so the real repo roadmap.json and data/ are never touched. Restored in tearDown.
        self._tmp = tempfile.TemporaryDirectory()
        self._base = Path(self._tmp.name)
        self._state = self._base / "state"
        self._state.mkdir()
        self._orig_base, self._orig_state = tm.BASE_DIR, tm.STATE_DIR
        tm.BASE_DIR, tm.STATE_DIR = self._base, self._state

    def tearDown(self):
        tm.BASE_DIR, tm.STATE_DIR = self._orig_base, self._orig_state
        self._tmp.cleanup()

    def _write_roadmap(self, roadmap):
        (self._state / "roadmap.json").write_text(json.dumps(roadmap, indent=2), encoding="utf-8")

    def _write_task_file(self, task):
        path = self._base / "task.json"
        path.write_text(json.dumps(task), encoding="utf-8")
        return path

    def _read_roadmap(self):
        return json.loads((self._state / "roadmap.json").read_text(encoding="utf-8"))

    def _args(self, task_path, debug=False):
        return argparse.Namespace(file=str(task_path), debug=debug)

    def _run(self, args):
        """Call cmd_add with its stdout suppressed (keeps test output readable)."""
        with contextlib.redirect_stdout(io.StringIO()):
            return tm.cmd_add(args)

    def test_happy_path_writes_task(self):
        self._write_roadmap(roadmap_with(make_task(id="T-001")))
        rc = self._run(self._args(self._write_task_file(make_task(id="T-002"))))
        self.assertEqual(rc, 0)
        tasks = self._read_roadmap()["tasks"]
        self.assertEqual([t["id"] for t in tasks], ["T-001", "T-002"])

    def test_rejected_task_leaves_file_unchanged(self):
        self._write_roadmap(roadmap_with(make_task(id="T-001")))
        before = self._read_roadmap()
        rc = self._run(self._args(self._write_task_file(make_task(id="T-001"))))  # dup id
        self.assertEqual(rc, 1)
        self.assertEqual(self._read_roadmap(), before)  # untouched

    def test_baseline_corruption_aborts_without_blaming_new_task(self):
        # Pre-existing invalid task (active, missing deliverable) → baseline fails.
        bad = make_task(id="T-001")
        bad["deliverable"] = ""
        self._write_roadmap(roadmap_with(bad))
        before = self._read_roadmap()
        rc = self._run(self._args(self._write_task_file(make_task(id="T-002"))))
        self.assertEqual(rc, 1)
        self.assertEqual(self._read_roadmap(), before)  # untouched

    def test_missing_task_file_returns_error(self):
        self._write_roadmap(roadmap_with())
        rc = self._run(self._args(self._base / "does_not_exist.json"))
        self.assertEqual(rc, 1)

    def test_debug_writes_log_file(self):
        self._write_roadmap(roadmap_with())
        rc = self._run(self._args(self._write_task_file(make_task(id="T-001")), debug=True))
        self.assertEqual(rc, 0)
        self.assertTrue((self._base / "data" / "taskmaster_debug.log").exists())


if __name__ == "__main__":
    unittest.main()
