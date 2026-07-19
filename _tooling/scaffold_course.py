#!/usr/bin/env python3
"""Scaffold AIMarket courses from courses/catalog.yaml (monorepo tooling only)."""

from __future__ import annotations

import json
import shutil
import textwrap
from pathlib import Path
from typing import Any

try:
    import yaml
except ImportError as exc:
    raise SystemExit("PyYAML required: pip install pyyaml") from exc

ROOT = Path(__file__).resolve().parents[1]
MONOREPO = ROOT.parent
ORCH = ROOT / "orchestration-course"
CATALOG = ROOT / "catalog.yaml"


def _load_catalog() -> list[dict[str, Any]]:
    data = yaml.safe_load(CATALOG.read_text(encoding="utf-8")) or {}
    return list(data.get("courses") or [])


def _module_ids(spec: dict[str, Any]) -> list[str]:
    return sorted(spec["modules"].keys(), key=lambda k: int(k[1:]))


def _i18n_base(spec: dict[str, Any]) -> dict[str, Any]:
    modules = {
        mid: {
            "title": m["title"],
            "concept": m["concept"],
            "industry": m["industry"],
        }
        for mid, m in spec["modules"].items()
    }
    mod_count = len(modules)
    return {
        "course": {"title": spec["title"], "tagline": spec["tagline"]},
        "ui": {
            "task": "task",
            "result": "result",
            "trace": "trace",
            "events": "events",
            "success": "success",
            "verify": "verify",
            "proof": "proof",
            "score": "score",
            "blocked": "blocked",
            "allowed": "allowed",
        },
        "modules": modules,
        "site": {
            "modules_heading": f"{mod_count} modules",
            "labs_heading": "Hands-on labs",
            "quickstart_heading": "Quick start",
            "quickstart_intro": "Clone the repo, install deps, and run labs locally or in Colab.",
            "quickstart_copy": "Copy commands",
            "quickstart_copied": "Copied!",
            "nav_quickstart": "Quick start",
            "nav_certificate": "Certificate",
            "nav_modules": "Modules",
            "nav_labs": "Labs",
            "stat_modules": "modules",
            "stat_labs": "hands-on labs",
            "stat_langs": "languages",
            "hero_badge": "Open course · Python 3.11+",
            "open_colab": "Open in Colab",
            "view_source": "View source",
            "run_local": "Local run",
            "has_lab": "lab",
            "coming_soon": "concept only",
            "advanced": "advanced",
            "module": "Module",
            "exercises_heading": "Exercises & certificate",
            "exercises_body": "Pass checks with <code class=\"inline\">python labs/run_exercises.py</code>.",
            "certificate_nav": "Certificate",
            "certificate_heading": "Course certificate",
            "certificate_intro": "Complete all labs and exercises to unlock your certificate.",
            "certificate_name_label": "Your name on the certificate",
            "certificate_name_placeholder": "Jane Doe",
            "certificate_progress": "Progress",
            "certificate_labs": "Labs completed",
            "certificate_exercises": "Exercises passed",
            "certificate_generate": "Get certificate",
            "certificate_locked": "Check off all labs and exercises to unlock",
            "certificate_mark_lab": "Mark complete",
            "certificate_mark_done": "Done ✓",
            "footer": spec["footer"],
        },
        "exercises": {"heading": "Exercise", "all_ok": "All exercises passed."},
        "labs": {},
    }


def _i18n_ru(spec: dict[str, Any], en: dict[str, Any]) -> dict[str, Any]:
    ru = json.loads(json.dumps(en))
    ru["course"]["title"] = spec["title"]  # keep EN title for repo consistency
    ru["course"]["tagline"] = spec["tagline"]
    ru["site"]["modules_heading"] = f"{len(spec['modules'])} модулей"
    ru["site"]["labs_heading"] = "Практические лабораторные"
    ru["site"]["quickstart_heading"] = "Быстрый старт"
    ru["site"]["footer"] = spec["footer"]
    titles_ru = {
        "m1": "Модуль 1",
        "m2": "Модуль 2",
        "m3": "Модуль 3",
        "m4": "Модуль 4",
        "m5": "Модуль 5",
        "m6": "Модуль 6",
    }
    for mid in ru["modules"]:
        if mid in titles_ru:
            ru["modules"][mid]["title"] = f"{titles_ru[mid]} — {en['modules'][mid]['title']}"
    return ru


def _i18n_es(spec: dict[str, Any], en: dict[str, Any]) -> dict[str, Any]:
    es = json.loads(json.dumps(en))
    es["site"]["modules_heading"] = f"{len(spec['modules'])} módulos"
    es["site"]["labs_heading"] = "Laboratorios prácticos"
    es["site"]["quickstart_heading"] = "Inicio rápido"
    es["site"]["footer"] = spec["footer"]
    return es


def _lab_body(stem: str, module: str, topic: str) -> str:
    return textwrap.dedent(
        f'''\
        """Lab — {stem.replace("_", " ")} ({module.upper()}).

        Run:  python labs/{stem}.py
              COURSE_LANG=ru python labs/{stem}.py
        """

        import pathlib
        import sys

        sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))

        from courselib.i18n import get_translator
        from courselib.{topic} import demo_step


        def main() -> None:
            t = get_translator()
            print(f"== {{t('modules.{module}.title')}} ==")
            print(t("modules.{module}.concept"))
            result = demo_step("{stem}")
            print(f"{{t('ui.result')}}: {{result}}")
            print(f"\\n--- {{t('exercises.heading')}} ---")
            print("Run: python labs/run_exercises.py --module {module}")


        if __name__ == "__main__":
            main()
        '''
    )


def _topic_module(topic: str) -> str:
    return textwrap.dedent(
        f'''\
        """Teaching helpers for the {topic} course track."""

        from __future__ import annotations


        def demo_step(lab_stem: str) -> str:
            """Deterministic demo output — replace with live oracle/SDK calls in advanced labs."""
            return f"{{lab_stem}}: ok (sandbox demo)"


        def exercise_check(module: str) -> None:
            """Minimal DIY check students extend in each module."""
            assert module.startswith("m"), module
            assert demo_step(f"exercise_{{module}}").endswith("(sandbox demo)")
        '''
    )


def _exercises_py(modules: list[str], topic: str) -> str:
    checks = "\n".join(
        f'''
        def exercise_{mod}() -> None:
            exercise_check("{mod}")
        '''
        for mod in modules
        if mod in {m["module"] for m in []}  # placeholder
    )
    # build from lab modules only
    return textwrap.dedent(
        f'''\
        """Hands-on exercises for each module."""

        from __future__ import annotations

        from courselib.{topic} import exercise_check

        MODULES = {tuple(modules)!r}


        def exercise_m_placeholder() -> None:
            exercise_check("m1")
        '''
    )


def _write_exercises(path: Path, modules: list[str], topic: str) -> None:
    lines = [
        '"""Hands-on exercises for each module."""',
        "",
        "from __future__ import annotations",
        "",
        f"from courselib.{topic} import exercise_check",
        "",
        f"MODULES = {modules!r}",
        "",
    ]
    for mod in modules:
        lines.extend(
            [
                f"def exercise_{mod}() -> None:",
                f'    exercise_check("{mod}")',
                "",
            ]
        )
    lines.extend(
        [
            "EXERCISES = {",
            *[f'    "{mod}": exercise_{mod},' for mod in modules],
            "}",
            "",
            "",
            "def run_all() -> dict[str, str]:",
            "    out: dict[str, str] = {}",
            "    for mod, fn in EXERCISES.items():",
            "        try:",
            "            fn()",
            "            out[mod] = 'ok'",
            "        except Exception as exc:",
            "            out[mod] = str(exc)",
            "    return out",
            "",
            "",
            "def all_passed() -> bool:",
            "    return all(v == 'ok' for v in run_all().values())",
            "",
        ]
    )
    path.write_text("\n".join(lines), encoding="utf-8")


def _certificate_py(modules: list[str]) -> str:
    src = (ORCH / "courselib/certificate.py").read_text(encoding="utf-8")
    src = src.replace(
        'COMPLETED_MODULES = ("m1", "m2", "m3", "m4", "m5", "m6", "m7", "m8", "m9")',
        f"COMPLETED_MODULES = {tuple(modules)!r}",
    )
    return src


def _course_config(spec: dict[str, Any]) -> dict[str, Any]:
    repo = spec["repo"]
    org = "alexar76"
    modules = _module_ids(spec)
    labs = []
    for lab in spec["labs"]:
        entry = {"stem": lab["stem"], "module": lab["module"], "track": lab["track"]}
        if "sandbox" in lab:
            entry["sandbox"] = lab["sandbox"]
        labs.append(entry)
    smoke = [lab["stem"] for lab in spec["labs"] if lab.get("track") != "advanced"][:4]
    return {
        "id": spec["id"].replace("course-", ""),
        "github_repo": f"{org}/{repo}",
        "github_pages": f"https://{org}.github.io/{repo}/",
        "clone_dir": repo,
        "package_name": spec["package_name"],
        "title": spec["title"],
        "description": spec["description"],
        "pip_extras_default": spec["pip_extras_default"],
        "module_count": len(modules),
        "modules": modules,
        "labs": labs,
        "quickstart_commands": [
            f"git clone https://github.com/{org}/{repo}.git",
            f"cd {repo}",
            f'pip install -e ".{spec["pip_extras_default"]}"',
            f"python labs/{spec['labs'][0]['stem']}.py",
            "python labs/run_exercises.py",
        ],
        "smoke_labs": smoke,
    }


def _pyproject(spec: dict[str, Any]) -> str:
    repo = spec["repo"]
    desc = spec["description"].replace('"', '\\"')
    extras = spec["pip_extras_default"]
    hub_block = ""
    if "hub-lite" in extras:
        hub_block = (
            "hub-lite = [\n"
            '    "uvicorn>=0.34",\n'
            '    "httpx>=0.28",\n'
            '    "fastapi>=0.136",\n'
            "]\n"
        )
    all_extra = "hub-lite,dev" if hub_block else "dev"
    return textwrap.dedent(
        f"""\
        [build-system]
        requires = ["setuptools>=75", "wheel"]
        build-backend = "setuptools.build_meta"

        [project]
        name = "{spec["package_name"]}"
        version = "0.1.0"
        description = "{desc}"
        readme = "README.md"
        license = "MIT"
        requires-python = ">=3.11"
        authors = [{{ name = "AI-Factory" }}]
        dependencies = []

        [project.urls]
        Homepage = "https://alexar76.github.io/{repo}/"
        Documentation = "https://alexar76.github.io/{repo}/"
        Repository = "https://github.com/alexar76/{repo}"
        Issues = "https://github.com/alexar76/{repo}/issues"

        [project.optional-dependencies]
        {hub_block}dev = ["pytest>=8"]
        all = ["{spec["package_name"]}[{all_extra}]"]

        [tool.setuptools.packages.find]
        include = ["courselib*"]

        [tool.pytest.ini_options]
        testpaths = ["tests"]
        """
    )


def _readme(spec: dict[str, Any]) -> str:
    repo = spec["repo"]
    folder = spec["folder"]
    mod_rows = "\n".join(
        f"| {mid.upper()} | {m['title']} | [`{lab['stem']}`](labs/{lab['stem']}.py) |"
        for mid, m in spec["modules"].items()
        for lab in spec["labs"]
        if lab["module"] == mid
    )
    # fallback table without lab link if no lab for module
    rows = []
    lab_by_mod = {lab["module"]: lab for lab in spec["labs"]}
    for mid, m in spec["modules"].items():
        lab = lab_by_mod.get(mid)
        lab_cell = f"[`{lab['stem']}`](labs/{lab['stem']}.py)" if lab else "—"
        rows.append(f"| {mid.upper()} | {m['title']} | {lab_cell} |")
    return textwrap.dedent(
        f'''\
        # {spec["title"]}

        **{spec["tagline"]}**

        Interactive Python course with runnable labs and full **EN / RU / ES** localization.

        | | |
        | --- | --- |
        | **Course site** | [alexar76.github.io/{repo}](https://alexar76.github.io/{repo}/) |
        | **Languages** | `COURSE_LANG=en` · `ru` · `es` |

        ## Modules

        | Module | Topic | Lab |
        | --- | --- | --- |
        {chr(10).join(rows)}

        ## Quick start

        ```bash
        git clone https://github.com/alexar76/{repo}.git
        cd {repo}
        pip install -e ".{spec["pip_extras_default"]}"
        pytest -q
        python labs/{spec["labs"][0]["stem"]}.py
        python labs/run_exercises.py
        ```

        ## Source of truth

        Developed inside the [aicom](https://github.com/alexar76/aicom) monorepo at `courses/{folder}/`, mirrored to this repository.

        ## License

        MIT — see [LICENSE](LICENSE).
        '''
    )


def _ci_yml(spec: dict[str, Any]) -> str:
    cfg = _course_config(spec)
    smoke = " ".join(cfg["smoke_labs"])
    return textwrap.dedent(
        f'''\
        name: CI

        on:
          push:
            branches: ["main"]
          pull_request:
          workflow_dispatch:

        jobs:
          pytest-course:
            runs-on: ubuntu-latest
            env:
              PYTHONPATH: ${{{{ github.workspace }}}}
            strategy:
              matrix:
                python-version: ["3.11", "3.12"]
            steps:
              - uses: actions/checkout@v4

              - uses: actions/setup-python@v5
                with:
                  python-version: ${{{{ matrix.python-version }}}}

              - name: Install
                run: |
                  python -m pip install --upgrade pip
                  pip install -e ".{spec["pip_extras_default"]}"

              - name: Test
                run: pytest -q

              - name: Verify course asset build
                run: python3 scripts/build_course_assets.py

              - name: Smoke-run labs
                run: |
                  for L in en ru es; do
                    for lab in {" ".join(cfg["smoke_labs"])}; do
                      COURSE_LANG=$L python labs/$lab.py >/dev/null
                    done
                  done
                  python labs/run_exercises.py >/dev/null
        '''
    )


def scaffold(spec: dict[str, Any], *, force: bool = False) -> Path:
    dest = ROOT / spec["folder"]
    if dest.exists() and not force:
        print(f"SKIP {dest} (exists)")
        return dest
    if dest.exists():
        shutil.rmtree(dest)

    modules = _module_ids(spec)
    exercise_modules = sorted({lab["module"] for lab in spec["labs"]}, key=lambda k: int(k[1:]))
    topic = spec["topic_module"]

    dest.mkdir(parents=True)
    (dest / "courselib").mkdir()
    (dest / "labs").mkdir()
    (dest / "i18n").mkdir()
    (dest / "scripts").mkdir()
    (dest / "tests").mkdir()
    (dest / "site_assets").mkdir()
    (dest / ".github/workflows").mkdir(parents=True)

    cfg = _course_config(spec)
    (dest / "course.config.json").write_text(json.dumps(cfg, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    en = _i18n_base(spec)
    for lab in spec["labs"]:
        mid = lab["module"]
        key = lab["stem"].replace("lab", "lab").split("_", 1)[-1]
        en["labs"][lab["stem"]] = {"hint": f"Extend {mid} concepts in {lab['stem']}."}
    (dest / "i18n/en.json").write_text(json.dumps(en, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    (dest / "i18n/ru.json").write_text(json.dumps(_i18n_ru(spec, en), indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    (dest / "i18n/es.json").write_text(json.dumps(_i18n_es(spec, en), indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    shutil.copy2(ORCH / "courselib/i18n.py", dest / "courselib/i18n.py")
    (dest / f"courselib/{topic}.py").write_text(_topic_module(topic), encoding="utf-8")
    _write_exercises(dest / "courselib/exercises.py", exercise_modules, topic)
    (dest / "courselib/certificate.py").write_text(_certificate_py(modules), encoding="utf-8")
    (dest / "courselib/__init__.py").write_text(
        textwrap.dedent(
            f'''\
            """courselib — teaching toolkit for {spec["title"]}."""

            from courselib.i18n import get_translator, resolve_lang, available_languages

            __all__ = ["get_translator", "resolve_lang", "available_languages"]
            __version__ = "0.1.0"
            '''
        ),
        encoding="utf-8",
    )

    for lab in spec["labs"]:
        (dest / "labs" / f"{lab['stem']}.py").write_text(_lab_body(lab["stem"], lab["module"], topic), encoding="utf-8")

    shutil.copy2(ORCH / "labs/run_exercises.py", dest / "labs/run_exercises.py")
    run_ex = (dest / "labs/run_exercises.py").read_text(encoding="utf-8")
    run_ex = run_ex.replace("orchestration course exercises", f"{spec['title']} exercises")
    (dest / "labs/run_exercises.py").write_text(run_ex, encoding="utf-8")

    for name in ("build_course_assets.py", "build_site.py", "labs_to_notebooks.py"):
        shutil.copy2(ORCH / "scripts" / name, dest / "scripts" / name)

    for name in ("app.js", "progress.js", "certificate.js"):
        shutil.copy2(ORCH / "site_assets" / name, dest / "site_assets" / name)

    shutil.copy2(ORCH / "conftest.py", dest / "conftest.py")
    shutil.copy2(ORCH / ".gitignore", dest / ".gitignore")
    shutil.copy2(ORCH / "LICENSE", dest / "LICENSE")
    if (ORCH / "CODE_OF_CONDUCT.md").is_file():
        shutil.copy2(ORCH / "CODE_OF_CONDUCT.md", dest / "CODE_OF_CONDUCT.md")

    shutil.copy2(ORCH / "tests/test_i18n.py", dest / "tests/test_i18n.py")
    (dest / "tests/test_labs_smoke.py").write_text(
        textwrap.dedent(
            f'''\
            """Smoke tests for generated labs."""

            import importlib
            import subprocess
            import sys
            from pathlib import Path

            ROOT = Path(__file__).resolve().parent.parent
            LABS = {cfg["smoke_labs"]!r}


            def test_exercises_pass():
                r = subprocess.run([sys.executable, "labs/run_exercises.py"], cwd=ROOT, capture_output=True, text=True)
                assert r.returncode == 0, r.stdout + r.stderr


            def test_labs_importable():
                for stem in LABS:
                    mod = importlib.import_module(f"labs.{{stem}}")
                    assert hasattr(mod, "main")
            '''
        ),
        encoding="utf-8",
    )

    (dest / "pyproject.toml").write_text(_pyproject(spec), encoding="utf-8")
    (dest / "README.md").write_text(_readme(spec), encoding="utf-8")
    (dest / ".github/workflows/ci.yml").write_text(_ci_yml(spec), encoding="utf-8")
    shutil.copy2(ORCH / ".github/workflows/pages.yml", dest / ".github/workflows/pages.yml")

    print(f"Scaffolded {dest}")
    return dest


def main() -> None:
    import argparse

    p = argparse.ArgumentParser(description="Scaffold courses from catalog.yaml")
    p.add_argument("--force", action="store_true")
    p.add_argument("--id", help="Single course id from catalog")
    args = p.parse_args()

    for spec in _load_catalog():
        if args.id and spec["id"] != args.id:
            continue
        scaffold(spec, force=args.force)


if __name__ == "__main__":
    main()
