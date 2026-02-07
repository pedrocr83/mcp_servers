# MCP Servers for GenomeGuard

A consolidated collection of Model Context Protocol (MCP) servers for genomic analysis.

## Quick Start

```bash
# Clone this repo
git clone <your-repo-url>
cd mcp_servers

# Run setup script to clone MCP server repos
chmod +x setup.sh
./setup.sh

# Copy and configure environment
cp env.template .env
# Edit .env with your API keys

# Build and start services
docker-compose --profile brave --profile gnomad --profile biolocal --profile genome --profile paperscraper --profile ncbi up -d
```

## Available MCP Servers

| Server | Port | Description |
|--------|------|-------------|
| brave-search-mcp | 7000 | Web search via Brave API |
| gnomad-mcp | 7001 | gnomAD variant database |
| bio-local-mcp | 7002 | Local VCF file processing |
| genome-mcp | 7003 | ClinVar and variant annotations |
| paperscraper-mcp | 7004 | Academic literature search |
| ncbi-datasets-mcp | 7005 | NCBI gene and genome data |

## Environment Variables

See `env.template` for all available configuration options.

**Required API Keys:**
- `BRAVE_API_KEY` - [Get from Brave](https://brave.com/search/api/)
- `NCBI_API_KEY` - [Get from NCBI](https://www.ncbi.nlm.nih.gov/account/)

## Tools Overview

Run `python3 list_all_tools.py` to see all available tools across servers.

**Active tools (optimized for GenomeGuard):** 27 tools
**Total available:** 67 tools

## Commands

```bash
# Start all services
docker-compose --profile brave --profile gnomad --profile biolocal --profile genome --profile paperscraper --profile ncbi up -d

# Stop all services
docker-compose down

# View logs
docker-compose logs -f

# Check status
docker ps
```

## File Structure

```
mcp_servers/
├── setup.sh              # Setup script
├── docker-compose.yml    # Docker configuration
├── .env                  # Environment variables (not in git)
├── env.template          # Environment template
├── .gitignore            # Git ignore rules
├── inspect_tools.py      # Check running servers
├── list_all_tools.py     # List all tools
└── [cloned repos]/       # MCP server repos (not in git)
```
