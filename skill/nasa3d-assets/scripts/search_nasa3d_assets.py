from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

from dcc_mcp_core.skill import skill_entry, skill_exception, skill_success

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _nasa3d import LICENSE, raw_url, repo_tree


@skill_entry
def main(
    query: str | None = None,
    limit: int = 10,
    extensions: list[str] | None = None,
    **_: Any,
) -> dict[str, Any]:
    try:
        allowed = {("." + e.lower().lstrip(".")) for e in (extensions or ["glb", "gltf", "obj", "fbx", "stl", "blend"])}
        needle = (query or "").lower()
        assets = []
        for item in repo_tree():
            path = item.get("path", "")
            if item.get("type") != "blob":
                continue
            if not any(path.lower().endswith(ext) for ext in allowed):
                continue
            if needle and needle not in path.lower():
                continue
            assets.append({"path": path, "url": raw_url(path), "size": item.get("size"), **LICENSE})
            if len(assets) >= limit:
                break
        return skill_success("NASA 3D assets found", assets=assets, count=len(assets))
    except Exception as exc:
        return skill_exception(exc, message="Failed to search NASA 3D Resources")


if __name__ == "__main__":
    from dcc_mcp_core.skill import run_main

    run_main(main)

