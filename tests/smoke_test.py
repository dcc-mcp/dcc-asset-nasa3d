from __future__ import annotations

import importlib.util
import os
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skill" / "nasa3d-assets"
SCRIPTS = SKILL / "scripts"


def load(name: str):
    spec = importlib.util.spec_from_file_location(name, SCRIPTS / f"{name}.py")
    module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(module)
    return module


def validate_skill() -> None:
    from dcc_mcp_core import validate_skill

    report = validate_skill(str(SKILL))
    assert not report.has_errors, report


def descriptor_smoke() -> None:
    helper = load("_nasa3d")
    descriptor = helper.asset_descriptor("models/apollo.glb", "/tmp/apollo.glb")
    assert descriptor["variants"][0]["local_path"] == "/tmp/apollo.glb"
    assert descriptor["attribution"]["source_url"].endswith("models/apollo.glb")
    assert descriptor["attribution"]["license_text"]


def live_smoke() -> None:
    if os.environ.get("RUN_LIVE_API_SMOKE") != "true":
        print("skip live NASA 3D smoke")
        return
    result = load("search_nasa3d_assets").main(query="Apollo", limit=1)
    assert result["success"], result
    assert result["context"]["assets"], result


def main() -> None:
    validate_skill()
    descriptor_smoke()
    live_smoke()


if __name__ == "__main__":
    main()

