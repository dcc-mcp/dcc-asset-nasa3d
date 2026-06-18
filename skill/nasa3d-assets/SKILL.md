---
name: nasa3d-assets
description: Search and download free NASA 3D Resources repository files.
metadata:
  dcc-mcp:
    version: v0.1.0
    dcc: python
    display_name: NASA 3D Assets
    group: asset.download.free
    default_icon: package
    affinity: any
    marketplace: dcc-asset-nasa3d
    tools: tools.yaml
    execution: sync
    permissions:
      - network
      - filesystem
    examples:
      - "Search NASA 3D Resources for Apollo GLB files"
      - "Download a NASA 3D file from GitHub"
    contact:
      name: dcc-mcp team
      url: https://github.com/dcc-mcp/dcc-asset-nasa3d
    install:
      add_source: "dcc-mcp-cli marketplace add dcc-mcp/dcc-asset-nasa3d"
      then_install: "dcc-mcp-cli marketplace install dcc-asset-nasa3d"
---

# NASA 3D Assets

Use this skill for files in the public NASA 3D Resources repository. Results
include a usage notice because NASA brand identifiers and endorsement rules are
separate from copyright status.

