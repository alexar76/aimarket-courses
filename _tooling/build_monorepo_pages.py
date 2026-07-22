#!/usr/bin/env python3
"""Build unified GitHub Pages tree: portal landing + one sub-site per course folder."""

from __future__ import annotations

import html
import json
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PORTAL = Path(__file__).resolve().parent / "portal"
SITE = ROOT / "site"
CATALOG = ROOT / "catalog.yaml"

TRACKS: list[tuple[str, str, str, list[str]]] = [
    (
        "agents",
        "Agents & platform",
        "🤖",
        [
            "orchestration-course",
            "agent-economy-course",
            "mcp-security-course",
            "ai-factory-course",
        ],
    ),
    (
        "oracles",
        "Oracles, trust & proofs",
        "🔢",
        [
            "verifiable-randomness-course",
            "mathematics-of-trust-course",
            "optimization-with-proofs-course",
            "smart-contracts-course",
            "physics-inspired-computing-course",
        ],
    ),
    (
        "viz",
        "Visualization",
        "🌌",
        ["3d-data-viz-course"],
    ),
]

COURSE_ICONS: dict[str, str] = {
    "orchestration-course": "🎓",
    "verifiable-randomness-course": "🎲",
    "mcp-security-course": "🛡️",
    "agent-economy-course": "💰",
    "3d-data-viz-course": "👽",
    "physics-inspired-computing-course": "⚛️",
    "mathematics-of-trust-course": "📐",
    "optimization-with-proofs-course": "✓",
    "smart-contracts-course": "⛓️",
    "ai-factory-course": "🏭",
}


def _course_dirs() -> list[Path]:
    return sorted(p for p in ROOT.iterdir() if p.is_dir() and p.name.endswith("-course"))


def _load_taglines() -> dict[str, str]:
    taglines: dict[str, str] = {}
    if not CATALOG.is_file():
        return taglines
    try:
        import yaml  # type: ignore
    except ImportError:
        return taglines
    data = yaml.safe_load(CATALOG.read_text(encoding="utf-8")) or {}
    for entry in data.get("courses") or []:
        folder = entry.get("folder")
        if folder and entry.get("tagline"):
            taglines[str(folder)] = str(entry["tagline"])
    return taglines


GITHUB_REPO = "alexar76/aimarket-courses"


def _colab_url(folder: str, cfg: dict) -> str:
    """Colab requires /blob/main/…/notebook.ipynb — /tree/…/notebooks is rejected."""
    labs = cfg.get("labs") or []
    if not labs:
        return f"https://github.com/{GITHUB_REPO}/tree/main/{folder}/notebooks"
    stem = labs[0].get("stem") or labs[0].get("notebook", "").removesuffix(".ipynb")
    if not stem:
        return f"https://github.com/{GITHUB_REPO}/tree/main/{folder}/notebooks"
    return (
        f"https://colab.research.google.com/github/{GITHUB_REPO}"
        f"/blob/main/{folder}/notebooks/{stem}.ipynb"
    )


def _course_card(folder: str, cfg: dict, taglines: dict[str, str]) -> str:
    title = html.escape(cfg.get("title") or folder)
    tagline = html.escape(taglines.get(folder) or cfg.get("description") or "")
    icon = COURSE_ICONS.get(folder, "📘")
    modules = int(cfg.get("module_count") or len(cfg.get("modules") or []))
    labs = len(cfg.get("labs") or [])
    colab = _colab_url(folder, cfg)
    gh_tree = f"https://github.com/alexar76/aimarket-courses/tree/main/{folder}"
    return f"""<article class="course-card">
  <div class="top">
    <span class="ic" aria-hidden="true">{icon}</span>
    <h4><a href="{html.escape(folder)}/">{title}</a></h4>
  </div>
  <p class="tagline">{tagline}</p>
  <div class="meta">
    <span class="chip hot">{modules} modules</span>
    <span class="chip">{labs} labs</span>
    <span class="chip">EN / RU / ES</span>
    <span class="chip">Colab</span>
  </div>
  <div class="links">
    <a href="{html.escape(folder)}/">Course site ↗</a>
    <a href="{html.escape(colab)}" target="_blank" rel="noopener">Colab ↗</a>
    <a href="{html.escape(gh_tree)}" target="_blank" rel="noopener">Source ↗</a>
  </div>
</article>"""


def _track_section(
    track_id: str,
    label: str,
    icon: str,
    folders: list[str],
    by_folder: dict[str, dict],
    taglines: dict[str, str],
) -> str:
    cards = "\n".join(
        _course_card(folder, by_folder[folder], taglines)
        for folder in folders
        if folder in by_folder
    )
    return f"""<div class="track" data-track="{html.escape(track_id)}">
  <div class="track-head">
    <h3>{icon} {html.escape(label)}</h3>
    <span>{len([f for f in folders if f in by_folder])} courses</span>
  </div>
  <div class="grid">{cards}</div>
</div>"""


def _portal_index(by_folder: dict[str, dict], taglines: dict[str, str]) -> str:
    tracks_html = "\n".join(
        _track_section(track_id, label, icon, folders, by_folder, taglines)
        for track_id, label, icon, folders in TRACKS
    )
    course_count = len(by_folder)
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>AIMarket Courses — live-sandbox academies for agent builders</title>
  <meta name="description" content="Ten hands-on Python academies on agent orchestration, verifiable oracles, MCP security, agent economy, trust math, and more — EN/RU/ES labs with Colab notebooks wired to the live AIMarket ecosystem." />
  <meta property="og:type" content="website" />
  <meta property="og:title" content="AIMarket Courses" />
  <meta property="og:description" content="Learn agent orchestration against a real economy — not toy examples. Ten courses, three languages, live sandboxes." />
  <meta property="og:url" content="https://alexar76.github.io/aimarket-courses/" />
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@500;700;900&amp;family=Rajdhani:wght@400;500;600;700&amp;display=swap" rel="stylesheet" />
  <link rel="stylesheet" href="assets/portal.css" />
</head>
<body>
  <canvas id="galaxy" aria-hidden="true"></canvas>
  <div class="nebula" aria-hidden="true"></div>
  <div class="scan" aria-hidden="true"></div>
  <div class="vignette" aria-hidden="true"></div>

  <nav>
    <div class="wrap row">
      <a class="brand" href="#top"><span class="core"></span> AIMarket Courses</a>
      <div class="nav-links">
        <a href="#philosophy">Philosophy</a>
        <a href="#method">Method</a>
        <a href="#catalog">Catalog</a>
        <a class="nav-cta" href="https://github.com/alexar76/aimarket-courses" target="_blank" rel="noopener">GitHub ↗</a>
      </div>
    </div>
  </nav>

  <header class="hero wrap" id="top">
    <span class="eyebrow"><span class="pip"></span> Open source · MIT · {course_count} academies</span>
    <h1>Learn agents on a<br/><span class="grad">live economy.</span></h1>
    <p class="lede">Not slides about LangChain — runnable labs that call real oracles, open payment channels, scan MCP servers with WARDEN, and verify signed receipts.</p>
    <p class="sub">Each academy is a self-contained folder: pytest CI, graded exercises, HTML certificates, step-by-step docs, and Colab notebooks in <strong>English, Russian, and Spanish</strong>.</p>
    <div class="cta-row">
      <a class="btn btn-primary" href="#catalog">Browse {course_count} courses</a>
      <a class="btn btn-ghost" href="https://github.com/alexar76/aimarket-courses" target="_blank" rel="noopener">Clone monorepo ↗</a>
      <a class="btn btn-ghost" href="https://modeldev.modelmarket.dev/" target="_blank" rel="noopener">AIMarket ecosystem ↗</a>
    </div>
    <div class="hero-meta">
      <span><b>{course_count}</b> courses</span>
      <span><b>3</b> languages</span>
      <span><b>56+</b> Colab notebooks</span>
      <span><b>Live</b> sandboxes</span>
    </div>
  </header>

  <section id="philosophy">
    <div class="wrap">
      <div class="sec-head">
        <div class="kicker">Philosophy</div>
        <h2>Why these courses exist</h2>
        <p>Most AI tutorials stop at calling one model. We teach the layer above — discovery, trust, settlement, and verifiable math — using infrastructure you can run yourself.</p>
      </div>
      <div class="pillars">
        <article class="pillar">
          <div class="ic">🧪</div>
          <h3>Live sandbox, not mocks</h3>
          <p>Labs hit real AIMarket oracles, Hub/SDK endpoints, WARDEN, alien-monitor APIs, lottery contracts, and the AI-Factory pipeline — or embedded mocks with the same interfaces.</p>
        </article>
        <article class="pillar">
          <div class="ic">🔏</div>
          <h3>Verify, don't trust</h3>
          <p>Randomness comes with proofs. Optimization ships certificates. Agents return signed receipts. You learn to audit outputs, not just accept them.</p>
        </article>
        <article class="pillar">
          <div class="ic">💸</div>
          <h3>Real agent economics</h3>
          <p>Discover capabilities, open USDC channels, invoke metered APIs, and publish paid services other agents can buy — the same patterns as production AIMarket Protocol v2.</p>
        </article>
        <article class="pillar">
          <div class="ic">🌍</div>
          <h3>Built for builders everywhere</h3>
          <p>Full EN / RU / ES localization — lab docstrings, step-by-step guides, notebooks, and certificates. Run locally or one-click in Colab.</p>
        </article>
      </div>
    </div>
  </section>

  <section id="method">
    <div class="wrap">
      <div class="sec-head">
        <div class="kicker">Method</div>
        <h2>How every course works</h2>
        <p>Same spine across all ten academies — pick a track, run labs in order, graduate with a certificate.</p>
      </div>
      <div class="flow">
        <div class="flow-node">
          <div class="ic">📖</div>
          <h3>Read &amp; probe</h3>
          <p>Concept in the lab docstring + step-by-step guide. No black boxes.</p>
        </div>
        <div class="flow-arrow" aria-hidden="true">→</div>
        <div class="flow-node">
          <div class="ic">⌨️</div>
          <h3>Run the lab</h3>
          <p>Local Python or Colab — calls the live ecosystem sandbox for that course.</p>
        </div>
        <div class="flow-arrow" aria-hidden="true">→</div>
        <div class="flow-node">
          <div class="ic">🏅</div>
          <h3>Prove mastery</h3>
          <p>Graded exercises + HTML certificate. pytest keeps every lab green in CI.</p>
        </div>
      </div>
    </div>
  </section>

  <section id="catalog">
    <div class="wrap">
      <div class="sec-head">
        <div class="kicker">Catalog</div>
        <h2>{course_count} academies · three tracks</h2>
        <p>Agent orchestration and economy · verifiable oracles and proofs · ecosystem visualization. All in one monorepo — like desktop SKUs in aimarket-desktop.</p>
      </div>
      <div class="filters" role="group" aria-label="Filter by track">
        <button type="button" class="filter-btn active" data-filter="all">All {course_count}</button>
        <button type="button" class="filter-btn" data-filter="agents">Agents &amp; platform</button>
        <button type="button" class="filter-btn" data-filter="oracles">Oracles &amp; proofs</button>
        <button type="button" class="filter-btn" data-filter="viz">Visualization</button>
      </div>
      {tracks_html}
    </div>
  </section>

  <section>
    <div class="wrap">
      <div class="final">
        <h2>Start with any course — graduate to the live hub.</h2>
        <p>Clone the monorepo, pick a folder, <code>pip install -e ".[dev]"</code>, run <code>pytest -q</code>. The same SDK code works against a local hub and a production AIMarket deployment.</p>
        <div class="cta-row">
          <a class="btn btn-primary" href="orchestration-course/">Start: Agent Orchestration ↗</a>
          <a class="btn btn-ghost" href="https://github.com/alexar76/aimarket-courses" target="_blank" rel="noopener">GitHub monorepo ↗</a>
        </div>
      </div>
    </div>
  </section>

  <footer>
    <div class="wrap">
      <div class="foot-links">
        <a href="https://github.com/alexar76/aimarket-courses" target="_blank" rel="noopener">GitHub</a>
        <a href="https://github.com/alexar76/aicom/tree/main/courses" target="_blank" rel="noopener">Monorepo source</a>
        <a href="https://modeldev.modelmarket.dev/" target="_blank" rel="noopener">AIMarket ecosystem</a>
        <a href="https://oracles.modelmarket.dev/" target="_blank" rel="noopener">Oracles</a>
        <a href="https://magic-ai-factory.com/monitor/" target="_blank" rel="noopener">Alien Monitor</a>
      </div>
      <div class="plain">AIMarket Courses · MIT · maintained in <a href="https://github.com/alexar76/aicom" target="_blank" rel="noopener">alexar76/aicom</a> · published to <a href="https://github.com/alexar76/aimarket-courses" target="_blank" rel="noopener">aimarket-courses</a></div>
    </div>
  </footer>

  <script src="assets/portal.js"></script>
</body>
</html>
"""


def main() -> int:
    taglines = _load_taglines()
    by_folder: dict[str, dict] = {}

    if SITE.exists():
        shutil.rmtree(SITE)
    SITE.mkdir(parents=True)
    assets = SITE / "assets"
    assets.mkdir()
    shutil.copy2(PORTAL / "portal.css", assets / "portal.css")
    shutil.copy2(PORTAL / "portal.js", assets / "portal.js")

    for course_dir in _course_dirs():
        cfg_path = course_dir / "course.config.json"
        cfg = json.loads(cfg_path.read_text(encoding="utf-8"))
        by_folder[course_dir.name] = cfg
        out = SITE / course_dir.name
        print(f"==> {course_dir.name} → site/{course_dir.name}/")
        subprocess.run(
            [sys.executable, "scripts/build_site.py", "--out", str(out)],
            cwd=course_dir,
            check=True,
        )

    (SITE / "index.html").write_text(_portal_index(by_folder, taglines), encoding="utf-8")
    (SITE / ".nojekyll").touch()
    print(f"Wrote portal landing + {len(by_folder)} course sites under {SITE}/")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
