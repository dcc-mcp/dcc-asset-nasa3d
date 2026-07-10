---
name: nasa3d-assets
description: Search and download NASA 3D Resources files as validated AssetDescriptors with usage attribution.
license: MIT
compatibility: "dcc-mcp-core 0.19+, Python 3.7+"
metadata:
  dcc-mcp:
    version: v0.1.0
    dcc: python
    layer: domain
    tags:
      - asset
      - nasa
      - space
      - 3d-models
      - download
      - free
    search-hint: "nasa 3d resources, spacecraft model, space asset, apollo, satellite, glb, stl, blend, download"
    produces: [asset_descriptor]
    tools: tools.yaml
---

# NASA 3D Assets

Use this skill for files in the public NASA 3D Resources repository. Results
include a usage notice because NASA brand identifiers and endorsement rules are
separate from copyright status.

`download_nasa3d_file` returns an `asset_descriptor` with the local file, source URL,
and NASA usage attribution. Pass that descriptor to a DCC adapter import skill; this source
skill does not modify a DCC scene.

