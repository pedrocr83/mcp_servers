#!/bin/bash
# =============================================================================
# MCP Servers Setup Script for GenomeGuard
# Clones and configures all required MCP servers
# =============================================================================

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=============================================="
echo "🧬 MCP Servers Setup for GenomeGuard"
echo "=============================================="

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Function to clone or update repo
clone_or_update() {
    local name=$1
    local url=$2
    local dir=$3
    
    if [ -d "$dir" ]; then
        echo -e "${YELLOW}📁 $name already exists, skipping...${NC}"
    else
        echo -e "${GREEN}📥 Cloning $name...${NC}"
        git clone "$url" "$dir"
    fi
}

echo ""
echo "📦 Cloning MCP Server Repositories..."
echo "----------------------------------------------"

# Brave Search MCP Server
clone_or_update "Brave Search MCP" \
    "https://github.com/modelcontextprotocol/servers.git" \
    "brave-search-mcp-server"

# gnomAD MCP Server
clone_or_update "gnomAD MCP" \
    "https://github.com/koido/gnomad-mcp.git" \
    "gnomad-mcp"

# Genome MCP (ClinVar)
clone_or_update "Genome MCP" \
    "https://github.com/Eldergenix/GenomeMCP.git" \
    "genome_mcp"

# Paperscraper MCP
clone_or_update "Paperscraper MCP" \
    "https://github.com/MCPmed/paperscraperMCP.git" \
    "paperscraper_mcp"

# NCBI Datasets MCP Server
clone_or_update "NCBI Datasets MCP" \
    "https://github.com/Augmented-Nature/NCBI-Datasets-MCP-Server.git" \
    "NCBI-Datasets-MCP-Server"

# MCP DB Server (optional)
clone_or_update "MCP DB Server" \
    "https://github.com/Souhar-dya/mcp-db-server.git" \
    "mcp-db-server"

# Rust MCP Filesystem (optional)
clone_or_update "Rust MCP Filesystem" \
    "https://github.com/modelcontextprotocol/servers.git" \
    "rust-mcp-filesystem"

echo ""
echo "----------------------------------------------"
echo "🛠️  Creating local directories..."

# Create bio_local if not exists (local implementation)
if [ ! -d "bio_local" ]; then
    mkdir -p bio_local
    echo "Created bio_local directory"
fi

echo ""
echo "----------------------------------------------"
echo "📄 Setting up environment..."

# Create .env from template if not exists
if [ ! -f ".env" ]; then
    if [ -f "env.template" ]; then
        cp env.template .env
        echo -e "${YELLOW}⚠️  Created .env from template - please update with your API keys!${NC}"
    else
        echo -e "${RED}❌ No env.template found!${NC}"
    fi
else
    echo ".env already exists"
fi

echo ""
echo "----------------------------------------------"
echo "🐳 Building Docker images..."
echo ""

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo -e "${RED}❌ Docker is not running. Please start Docker and run:${NC}"
    echo "   docker-compose build"
else
    echo "To build all images, run:"
    echo "   docker-compose --profile brave --profile gnomad --profile biolocal --profile genome --profile paperscraper --profile ncbi build"
    echo ""
    echo "To start all services:"
    echo "   docker-compose --profile brave --profile gnomad --profile biolocal --profile genome --profile paperscraper --profile ncbi up -d"
fi

echo ""
echo "=============================================="
echo -e "${GREEN}✅ Setup complete!${NC}"
echo "=============================================="
echo ""
echo "Next steps:"
echo "1. Update .env with your API keys (BRAVE_API_KEY, NCBI_API_KEY)"
echo "2. Build Docker images: docker-compose build"
echo "3. Start services: docker-compose up -d"
echo ""
