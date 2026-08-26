from __future__ import annotations

import builtins
import importlib.util
import json
import os
import sys
import tempfile
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skill" / "nasa3d-assets"
SCRIPTS = SKILL / "scripts"


class FakeResponse:
    def __init__(self, payload: bytes):
        self.payload = payload

    def __enter__(self):
        return self

    def __exit__(self, *_: object) -> None:
        return None

    def read(self) -> bytes:
        return self.payload


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


def assert_runtime_restores_sys_path(
    script_name: str, params: dict[str, object]
) -> dict:
    from dcc_mcp_core._server import run_skill_script

    path_identity = sys.path
    path_snapshot = list(sys.path)
    script_dir_count = sys.path.count(str(SCRIPTS))
    result = run_skill_script(str(SCRIPTS / script_name), params)
    assert sys.path is path_identity
    assert sys.path == path_snapshot
    assert sys.path.count(str(SCRIPTS)) == script_dir_count
    return result


def runtime_import_smoke() -> None:
    tree = json.dumps(
        {
            "tree": [
                {"path": "models/apollo.glb", "type": "blob", "size": 7},
                {"path": "models/readme.txt", "type": "blob", "size": 3},
            ]
        }
    ).encode("utf-8")
    with patch("urllib.request.urlopen", return_value=FakeResponse(tree)):
        result = assert_runtime_restores_sys_path(
            "search_nasa3d_assets.py",
            {"query": "Apollo", "limit": 1},
        )
    assert result["success"], result
    assert result["context"]["assets"][0]["path"] == "models/apollo.glb"

    with tempfile.TemporaryDirectory() as output_dir:
        with patch("urllib.request.urlopen", return_value=FakeResponse(b"mesh")):
            result = assert_runtime_restores_sys_path(
                "download_nasa3d_file.py",
                {"path": "models/apollo.glb", "output_dir": output_dir},
            )
        assert result["success"], result
        assert Path(result["context"]["file"]).read_bytes() == b"mesh"


def runtime_import_failure_smoke() -> None:
    real_import = builtins.__import__

    def reject_helper(name: str, *args: object, **kwargs: object):
        if name == "_nasa3d":
            raise ModuleNotFoundError("synthetic missing sibling helper")
        return real_import(name, *args, **kwargs)

    path_identity = sys.path
    path_snapshot = list(sys.path)
    script_dir_count = sys.path.count(str(SCRIPTS))
    with patch("builtins.__import__", side_effect=reject_helper):
        try:
            from dcc_mcp_core._server import run_skill_script

            run_skill_script(str(SCRIPTS / "search_nasa3d_assets.py"), {})
        except ModuleNotFoundError as exc:
            assert str(exc) == "synthetic missing sibling helper"
        else:
            raise AssertionError("missing sibling helper must fail import")
    assert sys.path is path_identity
    assert sys.path == path_snapshot
    assert sys.path.count(str(SCRIPTS)) == script_dir_count


def live_smoke() -> None:
    if os.environ.get("RUN_LIVE_API_SMOKE") != "true":
        print("skip live NASA 3D smoke")
        return
    from dcc_mcp_core._server import run_skill_script

    result = run_skill_script(
        str(SCRIPTS / "search_nasa3d_assets.py"),
        {"query": "Apollo", "limit": 1},
    )
    assert result["success"], result
    assert result["context"]["assets"], result


def main() -> None:
    validate_skill()
    descriptor_smoke()
    runtime_import_smoke()
    runtime_import_failure_smoke()
    live_smoke()


if __name__ == "__main__":
    main()
