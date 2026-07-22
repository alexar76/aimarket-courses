"""Exercise and certificate tests."""

from courselib.certificate import render_html
from courselib.exercises import EXERCISES, all_passed, run_all


def test_all_exercises_pass():
    results = run_all()
    assert all(v == "ok" for v in results.values()), results


def test_certificate_renders():
    html = render_html("Test Student", lang="en")
    assert "Test Student" in html
    assert "Verifiable Randomness" in html
