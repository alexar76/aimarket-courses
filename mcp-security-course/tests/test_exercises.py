"""Tests for DIY exercises — CI uses reference solutions."""

from courselib import exercise_solutions as solutions
from courselib.certificate import certificate_id, render_html, write_certificate


def test_all_reference_exercises_pass():
    results = solutions.run_all()
    assert all(v == "ok" for v in results.values()), results


def test_student_stubs_are_unimplemented():
    from courselib import exercises as student
    results = student.run_all()
    assert not all(v == "ok" for v in results.values())


def test_certificate_html_contains_name():
    html = render_html("Ada Lovelace", lang="en")
    assert "Ada Lovelace" in html


def test_certificate_id_is_stable():
    assert certificate_id("Test User") == certificate_id("Test User")
