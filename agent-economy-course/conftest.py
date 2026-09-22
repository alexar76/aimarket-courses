"""Make ``courselib`` importable and wire monorepo SDK siblings for sandbox tests."""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))

repo_root = next((p for p in ROOT.parents if (p / "aimarket-agent").is_dir()), None)
if repo_root is not None:
    for pkg in ("aimarket-agent", "aimarket-hub"):
        p = repo_root / pkg
        if p.is_dir() and str(p) not in sys.path:
            sys.path.insert(0, str(p))
