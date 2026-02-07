#!/usr/bin/env python3
"""
Sync TOOL_ flags from mcp_servers/.env to GenomeGuard/.env
"""
import os
from pathlib import Path

MCP_ENV_PATH = Path(".env")
GG_ENV_PATH = Path("../GenomeGuard/.env")

def sync_envs():
    if not MCP_ENV_PATH.exists():
        print(f"Error: {MCP_ENV_PATH} not found")
        return

    if not GG_ENV_PATH.exists():
        print(f"Error: {GG_ENV_PATH} not found")
        return

    # Read source vars
    tool_vars = []
    with open(MCP_ENV_PATH, "r") as f:
        for line in f:
            if line.strip().startswith("TOOL_"):
                tool_vars.append(line)

    print(f"Found {len(tool_vars)} tool configuration variables.")

    # Read destination
    with open(GG_ENV_PATH, "r") as f:
        gg_lines = f.readlines()

    # Find the start of the previous synced section (if any) or just remove TOOL_ vars
    # A simple approach is to remove lines starting with TOOL_
    new_gg_lines = [line for line in gg_lines if not line.strip().startswith("TOOL_")]
    
    # Remove our custom header if it exists to avoid duplication
    new_gg_lines = [line for line in new_gg_lines if not "SYNCED TOOL CONFIGURATION" in line]

    # Ensure newline at end
    if new_gg_lines and not new_gg_lines[-1].endswith("\n"):
        new_gg_lines[-1] += "\n"

    # Append new section
    new_gg_lines.append("\n# ============================================\n")
    new_gg_lines.append("# SYNCED TOOL CONFIGURATION (from mcp_servers/.env)\n")
    new_gg_lines.append("# ============================================\n")
    tool_vars_cleaned = [line for line in tool_vars if "=" in line] # Ensure valid lines
    new_gg_lines.extend(tool_vars_cleaned)

    # Write back
    with open(GG_ENV_PATH, "w") as f:
        f.writelines(new_gg_lines)
    
    print(f"Updated {GG_ENV_PATH} with tool configurations.")

if __name__ == "__main__":
    sync_envs()
