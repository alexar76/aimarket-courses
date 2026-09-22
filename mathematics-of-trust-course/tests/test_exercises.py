"""Tests for DIY exercises and certificate generation.

CI runs the reference solutions. Learners fill courselib/exercises.py stubs.
"""

from courselib import exercise_solutions as solutions
from courselib.certificate import certificate_id, render_html, write_certificate


def test_all_reference_exercises_pass():
    results = solutions.run_all()
    assert solutions.all_passed(results), results


def test_student_stubs_are_unimplemented():
    """Stubs must fail until the learner fills them — otherwise certs are free."""
    from courselib import exercises as student

    results = student.run_all()
    assert not student.all_passed(results)
    assert any(str(v).startswith("fail:") for v in results.values())


def test_certificate_html_contains_name():
    html = render_html("Ada Lovelace", lang="en")
    assert "Ada Lovelace" in html


def test_certificate_id_is_stable():
    assert certificate_id("Test User") == certificate_id("Test User")


def test_write_certificate_requires_exercises(tmp_path):
    out = tmp_path / "cert.html"
    try:
        write_certificate(out, "Demo Learner", require_exercises=True)
        assert False, "expected failure without passing student exercises"
    except Exception:
        assert not out.exists() or "Demo Learner" not in out.read_text(encoding="utf-8")
