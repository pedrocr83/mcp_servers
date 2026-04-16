"""
GhostLabs Shroud MCP Server — Security and compliance tools.

Exposes Shroud's core capabilities via MCP for external AI agents:
domain security scanning, PII detection, compliance status, threat intelligence.

Port: 7012 | Transport: SSE
"""

import os
import httpx
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("ghostlabs-shroud")

SHROUD_API_URL = os.getenv("SHROUD_API_URL", "http://shroud-backend:8000/api")
SHROUD_API_KEY = os.getenv("SHROUD_API_KEY", "")

HEADERS = {"Authorization": f"Bearer {SHROUD_API_KEY}"} if SHROUD_API_KEY else {}


@mcp.tool()
async def check_domain_reputation(domain: str) -> dict:
    """Check domain reputation and security posture.

    Runs DNS, SSL, email security, and breach checks against the domain.

    Args:
        domain: Domain to check (e.g., "example.com").
    """
    async with httpx.AsyncClient(timeout=60, headers=HEADERS) as client:
        resp = await client.post(
            f"{SHROUD_API_URL}/domains/check/",
            json={"domain": domain},
        )
        resp.raise_for_status()
        return resp.json()


@mcp.tool()
async def scan_content_pii(text: str) -> dict:
    """Scan text for personally identifiable information (PII).

    Detects names, emails, phone numbers, SSNs, credit cards, and other PII
    using Presidio. Returns findings with entity types and locations.

    Args:
        text: Text to scan for PII.
    """
    async with httpx.AsyncClient(timeout=30, headers=HEADERS) as client:
        resp = await client.post(
            f"{SHROUD_API_URL}/compliance/scan-pii/",
            json={"text": text},
        )
        resp.raise_for_status()
        return resp.json()


@mcp.tool()
async def get_security_score(domain: str) -> dict:
    """Get an overall security score for a domain (A-F grade).

    Returns a composite score across DNS, SSL, email, ports, and breach categories.

    Args:
        domain: Domain to score.
    """
    async with httpx.AsyncClient(timeout=60, headers=HEADERS) as client:
        resp = await client.get(
            f"{SHROUD_API_URL}/domains/{domain}/score/",
        )
        resp.raise_for_status()
        return resp.json()


@mcp.tool()
async def check_vulnerability(service: str, version: str = "") -> dict:
    """Check for known CVE vulnerabilities for a service/software.

    Args:
        service: Service or software name (e.g., "nginx", "openssh").
        version: Optional version string (e.g., "1.25.3").
    """
    params = {"service": service}
    if version:
        params["version"] = version

    async with httpx.AsyncClient(timeout=30, headers=HEADERS) as client:
        resp = await client.get(
            f"{SHROUD_API_URL}/threats/cve/",
            params=params,
        )
        resp.raise_for_status()
        return resp.json()


@mcp.tool()
async def report_security_event(
    product: str, action: str, resource_type: str = "", resource_id: str = "", details: str = ""
) -> dict:
    """Report a security event from any GhostLabs product.

    Args:
        product: Product reporting (phantom, specter, whisper).
        action: Action that occurred (e.g., "data_access", "auth_failure").
        resource_type: Type of resource affected.
        resource_id: ID of the resource.
        details: Additional details as JSON string.
    """
    payload = {"product": product, "action": action}
    if resource_type:
        payload["resource_type"] = resource_type
    if resource_id:
        payload["resource_id"] = resource_id
    if details:
        payload["details"] = details

    async with httpx.AsyncClient(timeout=30, headers=HEADERS) as client:
        resp = await client.post(
            f"{SHROUD_API_URL}/threats/events/",
            json=payload,
        )
        resp.raise_for_status()
        return resp.json()


@mcp.tool()
async def get_compliance_status(framework: str = "nist_csf") -> dict:
    """Get current compliance status against a framework.

    Args:
        framework: Compliance framework — nist_csf, soc2, gdpr, iso27001, cis.
    """
    async with httpx.AsyncClient(timeout=30, headers=HEADERS) as client:
        resp = await client.get(
            f"{SHROUD_API_URL}/compliance/status/",
            params={"framework": framework},
        )
        resp.raise_for_status()
        return resp.json()


@mcp.tool()
async def generate_compliance_narrative(framework: str, scope: str = "") -> dict:
    """Generate an AI-powered compliance narrative for a framework.

    Returns audit-ready text per control area with evidence mapping.

    Args:
        framework: Target framework (soc2, gdpr, iso27001).
        scope: Optional scope limitation (e.g., "access_control").
    """
    async with httpx.AsyncClient(timeout=120, headers=HEADERS) as client:
        resp = await client.post(
            f"{SHROUD_API_URL}/compliance/narrative/",
            json={"framework": framework, "scope": scope},
        )
        resp.raise_for_status()
        return resp.json()


if __name__ == "__main__":
    mcp.run()
