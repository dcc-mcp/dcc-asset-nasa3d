from __future__ import annotations

import json
import os
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any

from dcc_mcp_core.asset_import import AssetAttribution, AssetDescriptor, AssetFileVariant


REPO = "nasa/NASA-3D-Resources"
BRANCH = "master"
LICENSE = {
    "license_name": "NASA 3D Resources usage notice",
    "license_url": "https://www.nasa.gov/nasa-brand-center/images-and-media/",
    "usage_notice": "NASA 3D Resources are free and without copyright, but NASA identifiers and endorsement rules still apply.",
}


def _headers() -> dict[str, str]:
    headers = {"User-Agent": "dcc-mcp-nasa3d/0.1"}
    if os.environ.get("GITHUB_TOKEN"):
        headers["Authorization"] = f"Bearer {os.environ['GITHUB_TOKEN']}"
    return headers


def repo_tree() -> list[dict[str, Any]]:
    url = f"https://api.github.com/repos/{REPO}/git/trees/{BRANCH}?recursive=1"
    req = urllib.request.Request(url, headers=_headers())
    with urllib.request.urlopen(req, timeout=60) as resp:
        data = json.loads(resp.read().decode("utf-8"))
    return data.get("tree", [])


def raw_url(path: str) -> str:
    return f"https://raw.githubusercontent.com/{REPO}/{BRANCH}/{urllib.parse.quote(path)}"


def download(path: str, output_dir: str) -> str:
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    target = Path(output_dir) / Path(path).name
    req = urllib.request.Request(raw_url(path), headers={"User-Agent": "dcc-mcp-nasa3d/0.1"})
    with urllib.request.urlopen(req, timeout=180) as resp:
        target.write_bytes(resp.read())
    return str(target)


def asset_descriptor(path: str, local_path: str) -> dict[str, Any]:
    descriptor = AssetDescriptor(
        asset_id=f"nasa3d:{path}",
        variants=[
            AssetFileVariant(
                local_path=local_path,
                format=Path(local_path).suffix.lstrip(".").lower() or "unknown",
                preferred=True,
            )
        ],
        attribution=AssetAttribution(
            source_url=raw_url(path),
            license_text=LICENSE["usage_notice"],
            attribution_text="NASA 3D Resources — observe NASA media and insignia usage rules.",
        ),
    )
    descriptor.validate()
    return descriptor.to_dict()
