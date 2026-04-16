"""
GhostLabs Skills MCP Server — Skill discovery and loading for any MCP client.

Exposes the shared Skills Engine via MCP protocol, allowing external AI agents
to find, load, and use GhostLabs skills.

Port: 7014 | Transport: SSE
"""

import os
import httpx
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("ghostlabs-skills")

SKILLS_API_URL = os.getenv("SKILLS_API_URL", "http://ghostlabs-backend:8000/api")


@mcp.tool()
async def find_skills(query: str, product: str = "", max_results: int = 3) -> dict:
    """Search for skills relevant to a query using semantic similarity.

    Returns matching skills with name, description, and similarity score.
    Use get_skill to load full instructions for a match.

    Args:
        query: Natural language description of what expertise you need.
        product: Filter by product (specter, whisper, shroud, phantom). Empty for all.
        max_results: Maximum number of results (1-10).
    """
    async with httpx.AsyncClient(timeout=30) as client:
        resp = await client.post(
            f"{SKILLS_API_URL}/skills/test_match/",
            json={"query": query, "product": product or "shared", "max_results": max_results},
        )
        resp.raise_for_status()
        return resp.json()


@mcp.tool()
async def get_skill(skill_id: str) -> dict:
    """Load full instructions for a skill by ID.

    Returns the complete SKILL.md markdown body with methodology,
    frameworks, and detailed guidance.

    Args:
        skill_id: The UUID of the skill (from find_skills results).
    """
    async with httpx.AsyncClient(timeout=30) as client:
        resp = await client.get(f"{SKILLS_API_URL}/skills/{skill_id}/")
        resp.raise_for_status()
        data = resp.json()
        return {
            "name": data["name"],
            "product": data["product"],
            "description": data["description"],
            "instructions": data["instructions"],
            "allowed_tools": data["allowed_tools"],
        }


@mcp.tool()
async def get_skill_resources(skill_id: str) -> list:
    """List available resources (scripts, references, templates) for a skill.

    Args:
        skill_id: The UUID of the skill.
    """
    async with httpx.AsyncClient(timeout=30) as client:
        resp = await client.get(f"{SKILLS_API_URL}/skills/{skill_id}/resources/")
        resp.raise_for_status()
        return resp.json()


@mcp.tool()
async def list_skills(product: str = "", source: str = "") -> list:
    """List all available skills, optionally filtered by product or source.

    Args:
        product: Filter by product (specter, whisper, shroud, phantom). Empty for all.
        source: Filter by source (builtin, customer, community). Empty for all.
    """
    params = {}
    if product:
        params["product"] = product
    if source:
        params["source"] = source

    async with httpx.AsyncClient(timeout=30) as client:
        resp = await client.get(f"{SKILLS_API_URL}/skills/", params=params)
        resp.raise_for_status()
        return resp.json()


if __name__ == "__main__":
    mcp.run()
