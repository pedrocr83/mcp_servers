FROM python:3.13-slim
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv
WORKDIR /app
COPY pyproject.toml ./
RUN uv pip install --system .
COPY . .
ENV PYTHONUNBUFFERED=1
EXPOSE 7014
CMD ["fastmcp", "run", "server.py:mcp", "--transport", "sse", "--host", "0.0.0.0", "--port", "7014"]
