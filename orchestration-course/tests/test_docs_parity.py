"""Parity guard for the hand-maintained step-by-step guides.

The structured ``i18n/*.json`` catalogs are already guarded by ``test_i18n.py``.
This adds the *prose* layer, which drifts because the guides are maintained by
hand (EN first, then RU/ES) — exactly the workflow that left ES marking shipped
labs as "coming soon" and left dead ``../../docs`` links that 404 in the
published standalone repo.

Each language guide must:
  * reference all 8 labs (lab01..lab08),
  * carry a heading for every module M1..M9,
  * use no parent-relative (``../../``) links — those escape the published
    ``courses/orchestration-course`` repo root and 404 on GitHub. Use absolute URLs instead.
"""

import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"
GUIDES = ["step-by-step.md", "step-by-step.ru.md", "step-by-step.es.md"]
# Markdown published at the standalone-repo root, where ``../../`` escapes it.
PUBLISHED_MD = [DOCS / g for g in GUIDES] + [DOCS / "README.md", ROOT / "README.md"]


def _read(p: pathlib.Path) -> str:
    return p.read_text(encoding="utf-8")


def test_each_guide_references_all_eight_labs() -> None:
    for g in GUIDES:
        text = _read(DOCS / g)
        missing = [f"lab0{n}" for n in range(1, 9) if f"lab0{n}" not in text]
        assert not missing, f"{g} is missing references to {missing}"


def test_each_guide_covers_all_nine_modules() -> None:
    for g in GUIDES:
        headings = "\n".join(re.findall(r"^##.*$", _read(DOCS / g), flags=re.M))
        missing = [f"M{n}" for n in range(1, 10) if not re.search(rf"\bM{n}\b", headings)]
        assert not missing, f"{g} headings are missing modules {missing}"


def test_no_parent_relative_links_in_published_docs() -> None:
    offenders = [p.name for p in PUBLISHED_MD if "](../../" in _read(p)]
    assert not offenders, (
        f"parent-relative links 404 in the published repo: {offenders} — "
        "use absolute https URLs to the monorepo instead"
    )
