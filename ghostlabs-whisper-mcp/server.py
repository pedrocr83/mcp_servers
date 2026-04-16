"""
GhostLabs Whisper MCP Server — Business intelligence and data query tools.

Exposes Whisper's core capabilities via MCP for external AI agents:
natural language to SQL, document search, report generation.

Port: 7011 | Transport: SSE
"""

import os
import httpx
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("ghostlabs-whisper")

WHISPER_API_URL = os.getenv("WHISPER_API_URL", "http://whisper-backend:8000/api")
WHISPER_API_KEY = os.getenv("WHISPER_API_KEY", "")

HEADERS = {"Authorization": f"Bearer {WHISPER_API_KEY}"} if WHISPER_API_KEY else {}


@mcp.tool()
async def query_business_data(question: str, company_id: str = "") -> dict:
    """Ask a business question in natural language and get data-driven answers.

    Whisper translates your question to SQL, queries the database, and returns
    formatted results with analysis.

    Args:
        question: Natural language question (e.g., "What were total sales last month?").
        company_id: Optional company ID for multi-tenant queries.
    """
    payload = {"message": question}
    if company_id:
        payload["company_id"] = company_id

    async with httpx.AsyncClient(timeout=120, headers=HEADERS) as client:
        resp = await client.post(
            f"{WHISPER_API_URL}/chat/query/",
            json=payload,
        )
        resp.raise_for_status()
        return resp.json()


@mcp.tool()
async def search_documents(query: str, file_types: str = "") -> dict:
    """Search company documents (SharePoint, uploaded files) for relevant content.

    Args:
        query: Search query.
        file_types: Optional comma-separated file type filter (e.g., "pdf,docx").
    """
    params = {"q": query}
    if file_types:
        params["file_types"] = file_types

    async with httpx.AsyncClient(timeout=60, headers=HEADERS) as client:
        resp = await client.get(
            f"{WHISPER_API_URL}/documents/search/",
            params=params,
        )
        resp.raise_for_status()
        return resp.json()


@mcp.tool()
async def get_conversation_history(conversation_id: str, limit: int = 20) -> dict:
    """Retrieve past conversation messages for context.

    Args:
        conversation_id: The UUID of the conversation.
        limit: Maximum number of messages to return.
    """
    async with httpx.AsyncClient(timeout=30, headers=HEADERS) as client:
        resp = await client.get(
            f"{WHISPER_API_URL}/chat/conversations/{conversation_id}/messages/",
            params={"limit": limit},
        )
        resp.raise_for_status()
        return resp.json()


@mcp.tool()
async def generate_report(prompt: str, output_format: str = "markdown") -> dict:
    """Generate a formatted business report from a natural language prompt.

    Args:
        prompt: Description of the report to generate (e.g., "Monthly sales summary").
        output_format: Output format — markdown, json, pdf, or xlsx.
    """
    async with httpx.AsyncClient(timeout=120, headers=HEADERS) as client:
        resp = await client.post(
            f"{WHISPER_API_URL}/reports/generate/",
            json={"prompt": prompt, "format": output_format},
        )
        resp.raise_for_status()
        return resp.json()


@mcp.tool()
async def create_chart(data_query: str, chart_type: str = "auto") -> dict:
    """Generate a chart specification from a data query.

    Returns a Recharts-compatible JSON spec that can be rendered in a frontend.

    Args:
        data_query: Natural language description of the data to visualize.
        chart_type: Chart type — auto, line, bar, pie, area, scatter, or table.
    """
    async with httpx.AsyncClient(timeout=120, headers=HEADERS) as client:
        resp = await client.post(
            f"{WHISPER_API_URL}/visualizations/create/",
            json={"query": data_query, "chart_type": chart_type},
        )
        resp.raise_for_status()
        return resp.json()


if __name__ == "__main__":
    mcp.run()
