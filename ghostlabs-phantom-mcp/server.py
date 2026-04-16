"""
GhostLabs Phantom MCP Server — Lead generation and email verification tools.

Exposes Phantom's core capabilities via MCP for external AI agents:
lead search, email verification, campaign management.

Port: 7010 | Transport: SSE
"""

import os
import httpx
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("ghostlabs-phantom")

PHANTOM_API_URL = os.getenv("PHANTOM_API_URL", "http://phantom-backend:8000/api")
PHANTOM_API_KEY = os.getenv("PHANTOM_API_KEY", "")

HEADERS = {"Authorization": f"Bearer {PHANTOM_API_KEY}"} if PHANTOM_API_KEY else {}


@mcp.tool()
async def search_leads(query: str, limit: int = 10) -> dict:
    """Search for leads matching criteria in the Phantom database.

    Args:
        query: Natural language search query (e.g., "SaaS companies in fintech").
        limit: Maximum number of results (1-50).
    """
    async with httpx.AsyncClient(timeout=30, headers=HEADERS) as client:
        resp = await client.get(
            f"{PHANTOM_API_URL}/leads/prospects/",
            params={"search": query, "limit": min(limit, 50)},
        )
        resp.raise_for_status()
        return resp.json()


@mcp.tool()
async def get_lead_details(contact_id: str) -> dict:
    """Get full details for a specific lead/contact.

    Returns company info, contact details, verification status, and fit score.

    Args:
        contact_id: The UUID of the contact.
    """
    async with httpx.AsyncClient(timeout=30, headers=HEADERS) as client:
        resp = await client.get(f"{PHANTOM_API_URL}/leads/contacts/{contact_id}/")
        resp.raise_for_status()
        return resp.json()


@mcp.tool()
async def verify_email(email: str) -> dict:
    """Verify an email address using Phantom's 10-layer verification pipeline.

    Returns a deliverability score (0-100) and detailed layer results.

    Args:
        email: The email address to verify.
    """
    async with httpx.AsyncClient(timeout=60, headers=HEADERS) as client:
        resp = await client.post(
            f"{PHANTOM_API_URL}/leads/verify-email/",
            json={"email": email},
        )
        resp.raise_for_status()
        return resp.json()


@mcp.tool()
async def check_domain_email_pattern(domain: str) -> dict:
    """Detect the email naming pattern for a company domain.

    Returns the detected pattern (e.g., first.last@domain.com) and confidence.

    Args:
        domain: Company domain to check (e.g., "acme.com").
    """
    async with httpx.AsyncClient(timeout=30, headers=HEADERS) as client:
        resp = await client.get(
            f"{PHANTOM_API_URL}/leads/email-patterns/",
            params={"domain": domain},
        )
        resp.raise_for_status()
        return resp.json()


@mcp.tool()
async def create_campaign(query: str, icp_id: str = "") -> dict:
    """Create and start a new lead generation campaign.

    Args:
        query: Natural language description of the ideal customer.
        icp_id: Optional existing ICP profile ID to use.
    """
    payload = {"query": query}
    if icp_id:
        payload["icp_id"] = icp_id

    async with httpx.AsyncClient(timeout=30, headers=HEADERS) as client:
        resp = await client.post(
            f"{PHANTOM_API_URL}/leads/campaigns/",
            json=payload,
        )
        resp.raise_for_status()
        return resp.json()


@mcp.tool()
async def get_campaign_status(campaign_id: str) -> dict:
    """Check the status and progress of a lead generation campaign.

    Args:
        campaign_id: The UUID of the campaign.
    """
    async with httpx.AsyncClient(timeout=30, headers=HEADERS) as client:
        resp = await client.get(f"{PHANTOM_API_URL}/leads/campaigns/{campaign_id}/")
        resp.raise_for_status()
        return resp.json()


if __name__ == "__main__":
    mcp.run()
