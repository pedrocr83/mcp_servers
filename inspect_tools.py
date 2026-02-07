#!/usr/bin/env python3
"""
MCP Server Tool Inspector
Lists all available tools from running MCP servers
"""

import requests
import json
import sys

# MCP Server endpoints
SERVERS = {
    "brave-search": {"port": 7000, "type": "sse", "endpoint": "/mcp"},
    "gnomad": {"port": 7001, "type": "sse", "endpoint": "/sse"},
    "bio-local": {"port": 7002, "type": "sse", "endpoint": "/sse"},
    "genome-mcp": {"port": 7003, "type": "sse", "endpoint": "/sse"},
    "paperscraper": {"port": 7004, "type": "rest", "endpoint": "/tools"},
    "ncbi-datasets": {"port": 7005, "type": "rest", "endpoint": "/health"},
}

def check_server_health(name, config):
    """Check if server is running"""
    try:
        port = config["port"]
        resp = requests.get(f"http://localhost:{port}/health", timeout=2)
        return resp.status_code == 200
    except:
        try:
            # Try SSE endpoint
            resp = requests.get(f"http://localhost:{config['port']}{config['endpoint']}", 
                              headers={"Accept": "text/event-stream"}, timeout=2, stream=True)
            return resp.status_code == 200
        except:
            return False

def get_tools_rest(port, endpoint="/tools"):
    """Get tools from REST API"""
    try:
        resp = requests.get(f"http://localhost:{port}{endpoint}", timeout=5)
        if resp.status_code == 200:
            data = resp.json()
            if "tools" in data:
                return data["tools"]
    except Exception as e:
        pass
    return None

def get_tools_sse(port, endpoint="/sse"):
    """Try to get tools via MCP protocol"""
    # For SSE servers, we need to send a tools/list request
    # This is tricky because they use the MCP protocol
    try:
        # Send JSON-RPC request to list tools
        resp = requests.post(
            f"http://localhost:{port}/messages/",
            json={"jsonrpc": "2.0", "method": "tools/list", "id": 1},
            timeout=5
        )
        if resp.status_code == 200:
            data = resp.json()
            if "result" in data and "tools" in data["result"]:
                return data["result"]["tools"]
    except:
        pass
    return None

def print_separator():
    print("=" * 70)

def main():
    print("\n🔧 MCP Server Tool Inspector\n")
    print_separator()
    
    total_tools = 0
    
    for name, config in SERVERS.items():
        port = config["port"]
        is_running = check_server_health(name, config)
        
        status = "✅ RUNNING" if is_running else "❌ OFFLINE"
        print(f"\n📦 {name.upper()} (port {port}) - {status}")
        
        if not is_running:
            continue
            
        # Try to get tools
        tools = None
        if config["type"] == "rest":
            tools = get_tools_rest(port, config.get("endpoint", "/tools"))
        else:
            tools = get_tools_sse(port, config["endpoint"])
        
        if tools:
            print(f"   Found {len(tools)} tools:")
            for tool in tools:
                tool_name = tool.get("name", "unknown")
                description = tool.get("description", "No description")[:60]
                print(f"   • {tool_name}: {description}...")
            total_tools += len(tools)
        else:
            print(f"   ⚠️  Could not retrieve tool list (server uses SSE/stdio protocol)")
    
    print_separator()
    print(f"\n📊 Summary: {total_tools} tools discovered from REST endpoints")
    print("   Note: SSE-based servers require MCP client to list tools\n")

if __name__ == "__main__":
    main()
