# DCC-MCP NASA 3D Assets

![Workflow showcase](docs/workflow-showcase.png)

Search and download files from the public
[NASA-3D-Resources](https://github.com/nasa/NASA-3D-Resources) repository.

## Install

```bash
dcc-mcp-cli marketplace add dcc-mcp/dcc-asset-nasa3d
dcc-mcp-cli marketplace install dcc-asset-nasa3d
```

## License And Usage

NASA's 3D Resources repository says the assets are "free and without
copyright", but NASA insignia, identifiers, and related imagery have separate
brand/media usage rules. Do not imply NASA endorsement and check the official
NASA Images and Media Guidelines before product, advertising, or logo use.

This skill returns `license_name`, `license_url`, and a validated `asset_descriptor` in download
results. The descriptor carries the local path, source URL, and usage attribution for a DCC
adapter import skill.

## Tools

- `search_nasa3d_assets`
- `download_nasa3d_file`
