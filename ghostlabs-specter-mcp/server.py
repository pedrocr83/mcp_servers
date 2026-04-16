"""
GhostLabs Specter MCP Server — Adversarial strategy analysis tools.

Exposes Specter's core capabilities via MCP for external AI agents:
adversarial testing, template library, claim extraction, red team evaluation.

Port: 7013 | Transport: SSE
"""

import os
import httpx
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("ghostlabs-specter")

SPECTER_API_URL = os.getenv("SPECTER_API_URL", "http://specter-backend:8000/api")
SPECTER_API_KEY = os.getenv("SPECTER_API_KEY", "")

HEADERS = {"Authorization": f"Bearer {SPECTER_API_KEY}"} if SPECTER_API_KEY else {}


@mcp.tool()
async def run_adversarial_test(
    query: str, template: str = "", depth: int = 3
) -> dict:
    """Run an adversarial strategy analysis on a business question or strategy.

    Executes Specter's multi-stage pipeline: strategy generation, critique,
    self-improvement, red team evaluation, and final selection.

    Args:
        query: The strategy, idea, or business question to analyze.
        template: Optional template name (e.g., "product-launch", "investment-thesis").
        depth: Analysis depth 1-5 (refinement cycles). Default 3.
    """
    payload = {"query": query, "depth": min(max(depth, 1), 5)}
    if template:
        payload["template"] = template

    async with httpx.AsyncClient(timeout=300, headers=HEADERS) as client:
        resp = await client.post(
            f"{SPECTER_API_URL}/tester/sessions/",
            json=payload,
        )
        resp.raise_for_status()
        return resp.json()


@mcp.tool()
async def get_session_results(session_id: str) -> dict:
    """Retrieve full results from a completed Specter analysis session.

    Returns strategies, critiques, red team findings, and the final selected solution.

    Args:
        session_id: The UUID of the analysis session.
    """
    async with httpx.AsyncClient(timeout=30, headers=HEADERS) as client:
        resp = await client.get(f"{SPECTER_API_URL}/tester/sessions/{session_id}/")
        resp.raise_for_status()
        return resp.json()


@mcp.tool()
async def list_templates() -> list:
    """List available analysis templates.

    Templates provide structured frameworks for specific analysis types:
    Product Launch, Investment Thesis, Competitive Response, etc.
    """
    async with httpx.AsyncClient(timeout=30, headers=HEADERS) as client:
        resp = await client.get(f"{SPECTER_API_URL}/tester/templates/")
        resp.raise_for_status()
        return resp.json()


@mcp.tool()
async def extract_claims(text: str) -> dict:
    """Extract testable claims from a business document or strategy text.

    Identifies factual, causal, assumption, and feasibility claims
    that can be individually stress-tested.

    Args:
        text: The strategy text or document content to analyze.
    """
    async with httpx.AsyncClient(timeout=120, headers=HEADERS) as client:
        resp = await client.post(
            f"{SPECTER_API_URL}/tester/extract-claims/",
            json={"text": text},
        )
        resp.raise_for_status()
        return resp.json()


@mcp.tool()
async def red_team_evaluate(
    strategy_text: str, aggressiveness: str = "balanced"
) -> dict:
    """Run only the Red Team evaluation stage on a strategy.

    A focused adversarial attack trying to break the strategy,
    without the full multi-stage pipeline.

    Args:
        strategy_text: The strategy to attack.
        aggressiveness: Attack level — balanced or aggressive.
    """
    async with httpx.AsyncClient(timeout=120, headers=HEADERS) as client:
        resp = await client.post(
            f"{SPECTER_API_URL}/tester/red-team/",
            json={
                "text": strategy_text,
                "aggressiveness": aggressiveness,
            },
        )
        resp.raise_for_status()
        return resp.json()


if __name__ == "__main__":
    mcp.run()
