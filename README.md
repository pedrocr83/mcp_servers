# MCP Servers for GenomeGuard

A consolidated collection of Model Context Protocol (MCP) servers for genomic analysis, containerized for easy deployment with GenomeGuard.

## 🚀 Quick Start

```bash
# 1. Run setup script to clone MCP server repos
chmod +x setup.sh
./setup.sh

# 2. Copy and configure environment
cp env.template .env
# Edit .env with your API keys (Brave, NCBI)

# 3. Build and start services
docker-compose --profile all up -d
```

## 📦 Available MCP Servers

This collection provides **65 tools** across 6 specialized servers:

| Server | Transport | Port | Description | Tools |
|--------|-----------|------|-------------|-------|
| **gnomad-mcp** | SSE | 7001 | gnomAD population variant frequencies & gene info | 12 |
| **bio-local-mcp** | SSE | 7002 | Local VCF file processing & bcftools operations | 4 |
| **genome-mcp** | SSE | 7003 | ClinVar search & variant annotations | 10 |
| **paperscraper** | HTTP | 7004 | Academic literature search (PubMed, arXiv) | 2 |
| **ncbi-datasets** | HTTP | 7005 | NCBI gene, genome, and taxonomy data | 31 |
| **brave-search** | HTTP | 7000 | Web search & intelligence via Brave API | 6 |

## 🛠️ Configuration

### Environment Variables
Copy `env.template` to `.env`. You must provide:

- `BRAVE_API_KEY`: [Get from Brave](https://brave.com/search/api/)
- `NCBI_API_KEY`: [Get from NCBI](https://www.ncbi.nlm.nih.gov/account/)

### Docker Profiles
Services are grouped by profiles. You can start specific ones or all of them:

- `all`: All servers
- `brave`: Brave Search
- `gnomad`: gnomAD
- `biolocal`: Bio Local
- `genome`: Genome MCP
- `paperscraper`: Paperscraper
- `ncbi`: NCBI Datasets

Example: `docker-compose --profile gnomad --profile ncbi up -d`

## 🔍 Inspecting Tools

You can query the running servers to list their available tools:

```bash
# Check running servers and list tools
python3 inspect_tools.py

# View complete static reference of all tools
python3 list_all_tools.py
```

## 🔧 Technical Details

- **Custom HTTP Wrappers**: `ncbi-datasets` and `brave-search` use custom Node.js wrappers (`http_server.js`) to bridge `stdio` MCP servers to HTTP/REST endpoints.
- **FastMCP CLI**: `genome-mcp` uses the `fastmcp` CLI for robust SSE streaming.
- **Dockerized**: All servers run in isolated containers, communicating via the `mcp-network`.

## 📂 File Structure

```
mcp_servers/
├── setup.sh              # Clones repositories
├── docker-compose.yml    # Orchestration
├── .env                  # Configuration (ignored)
├── env.template          # Template
├── inspect_tools.py      # Live tool inspector
├── list_all_tools.py     # Static tool reference
└── [cloned repos]/       # Source code (ignored)
```
