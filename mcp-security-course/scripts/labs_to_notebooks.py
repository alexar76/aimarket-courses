#!/usr/bin/env python3
"""Convert runnable lab scripts into Colab-ready Jupyter notebooks."""

from __future__ import annotations

import ast
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LABS_DIR = ROOT / "labs"
OUT_DIR = ROOT / "notebooks"

_CFG = json.loads((ROOT / "course.config.json").read_text(encoding="utf-8"))
GITHUB_REPO = _CFG["github_repo"]
CLONE_DIR = _CFG.get("clone_dir", GITHUB_REPO.split("/")[-1])
REPO_SUBPATH = (_CFG.get("repo_subpath") or "").strip("/")
# Oracle packages (paths inside the alexar76/oracles repo) this course calls live.
# When present, the Colab setup cell clones that repo and installs them, mirroring CI —
# so "Open in Colab" gives the same live-ecosystem sandbox as a local checkout.
ORACLES = list(_CFG.get("oracles", []))
DEFAULT_EXTRA = _CFG.get("pip_extras_default", "")
LABS = [{"stem": lab["stem"], "sandbox": lab.get("sandbox", False)} for lab in _CFG["labs"]]


def _strip_bootstrap(src: str) -> str:
    """Drop sys.path bootstrap used for in-repo runs."""
    lines: list[str] = []
    for line in src.splitlines():
        stripped = line.strip()
        if "sys.path.insert" in line:
            continue
        if stripped in {"import pathlib", "import sys"}:
            continue
        lines.append(line)
    while lines and not lines[0].strip():
        lines.pop(0)
    return "\n".join(lines)


def _extract_body(stem: str) -> tuple[str, str]:
    path = LABS_DIR / f"{stem}.py"
    src = path.read_text(encoding="utf-8")
    tree = ast.parse(src)
    doc = (ast.get_docstring(tree) or "").strip()

    body_lines: list[str] = []
    in_main_guard = False
    for line in src.splitlines():
        if line.startswith('if __name__ == "__main__"'):
            in_main_guard = True
            continue
        if in_main_guard:
            continue
        body_lines.append(line)

    body = _strip_bootstrap("\n".join(body_lines)).strip()
    body = body.rstrip() + "\n\nmain()\n"
    return doc, body


def _oracle_block() -> str:
    """Top-level Colab code that clones alexar76/oracles and installs the needed packages."""
    if not ORACLES:
        return ""
    pkgs = ", ".join(f'"{p}"' for p in ORACLES)
    return (
        "\n"
        "# Live oracle sandbox — clone the AIMarket oracles this course calls, then install them.\n"
        'if not os.path.isdir("_deps/oracles"):\n'
        '    subprocess.run(["git", "clone", "-q", "--depth", "1",\n'
        '                    "https://github.com/alexar76/oracles.git", "_deps/oracles"], check=True)\n'
        f"for _pkg in [{pkgs}]:\n"
        '    subprocess.run([sys.executable, "-m", "pip", "install", "-q", "-e", f"_deps/oracles/{_pkg}"], check=True)\n'
    )


def _setup_cell(sandbox: bool | str) -> str:
    # Built as flush-left top-level code (no textwrap.dedent) so injected multi-line
    # blocks can never introduce inconsistent indentation in the Colab cell.
    if ORACLES:
        extra = DEFAULT_EXTRA or "[oracles,dev]"
        note = "# Live oracle sandbox (clones alexar76/oracles) — run once per Colab session"
    elif sandbox is True:
        extra = "[sandbox]"
        note = "# Full SDK (~50 MB) — run once per Colab session"
    elif sandbox == "hub-lite":
        extra = "[hub-lite]"
        note = "# Hub-lite (~5 MB) — fast install for hub/escrow labs"
    else:
        extra = DEFAULT_EXTRA if DEFAULT_EXTRA and DEFAULT_EXTRA != "[oracles,dev]" else ""
        note = "# Core course only — no network hub deps"
    head = (
        "# Setup — run this cell once per session\n"
        f"{note}\n"
        "import os\n"
        "import subprocess\n"
        "import sys\n"
        "\n"
        f'REPO = "https://github.com/{GITHUB_REPO}.git"\n'
        f'DEST = "/content/{CLONE_DIR}"\n'
        "\n"
        "if not os.path.isdir(DEST):\n"
        '    subprocess.run(["git", "clone", "-q", "--depth", "1", REPO, DEST], check=True)\n'
        + (
            f'WORKDIR = os.path.join(DEST, "{REPO_SUBPATH}")\n'
            "os.chdir(WORKDIR)\n"
            if REPO_SUBPATH
            else "os.chdir(DEST)\n"
        )
    )
    tail = (
        "\n"
        f'subprocess.run([sys.executable, "-m", "pip", "install", "-q", "-e", ".{extra}"], check=True)\n'
        'os.environ.setdefault("COURSE_LANG", "en")  # change to ru or es\n'
    )
    return head + _oracle_block() + tail


def _notebook(doc: str, setup: str, body: str) -> dict:
    prefix = f"{REPO_SUBPATH}/" if REPO_SUBPATH else ""
    badge = (
        f"[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)]"
        f"(https://colab.research.google.com/github/{GITHUB_REPO}/blob/main/{prefix}notebooks/{{}})"
    )
    md = f"{doc}\n\n{badge}\n"
    return {
        "nbformat": 4,
        "nbformat_minor": 5,
        "metadata": {
            "kernelspec": {
                "display_name": "Python 3",
                "language": "python",
                "name": "python3",
            },
            "language_info": {"name": "python", "pygments_lexer": "ipython3"},
            "colab": {"provenance": []},
        },
        "cells": [
            {"cell_type": "markdown", "metadata": {}, "source": md.splitlines(keepends=True)},
            {"cell_type": "code", "metadata": {}, "source": setup.splitlines(keepends=True), "outputs": [], "execution_count": None},
            {"cell_type": "code", "metadata": {}, "source": body.splitlines(keepends=True), "outputs": [], "execution_count": None},
        ],
    }


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    for spec in LABS:
        doc, body = _extract_body(spec["stem"])
        nb = _notebook(doc, _setup_cell(spec["sandbox"]), body)
        # Fix badge placeholder in markdown
        nb["cells"][0]["source"] = [
            line.replace("{{}}", f"{spec['stem']}.ipynb") for line in nb["cells"][0]["source"]
        ]
        out = OUT_DIR / f"{spec['stem']}.ipynb"
        out.write_text(json.dumps(nb, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(f"Wrote {out}")


if __name__ == "__main__":
    main()
