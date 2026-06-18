from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

from dcc_mcp_core.skill import skill_entry, skill_exception, skill_success

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _nasa3d import LICENSE, download, raw_url


@skill_entry
def main(path: str, output_dir: str, **_: Any) -> dict[str, Any]:
    try:
        file_path = download(path, output_dir)
        return skill_success("NASA 3D file downloaded", file=file_path, source_url=raw_url(path), **LICENSE)
    except Exception as exc:
        return skill_exception(exc, message="Failed to download NASA 3D file")


if __name__ == "__main__":
    from dcc_mcp_core.skill import run_main

    run_main(main)

