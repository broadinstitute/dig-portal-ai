# Portal Tools MCP Server

A Model Context Protocol (MCP) server that exposes biological data analysis tools for AI agents. This server replaces the previous Flask-based REST API with a more efficient MCP-based architecture using FastMCP.

## Features

- **Phenotype Search**: Vector similarity search across phenotype databases
- **Gene Analysis**: Retrieve top genes for specific phenotypes
- **Factor Analysis**: Get factors associated with phenotypes
- **Gene Set Analysis**: Analyze gene sets for phenotypes
- **Cypher Queries**: Execute Neo4j Cypher queries
- **Caching**: In-memory caching of phenotype embeddings for fast searches

## Installation

### Using uv (Recommended)

```bash
cd portal-tools
uv pip install -e .
```

### Using pip

```bash
cd portal-tools
pip install -e .
```

## Usage

### Running the MCP Server

```bash
# Using the installed script (after installation)
portal-tools-mcp

# Or using Python module directly
python -m portal_tools.mcp_server

# Using uv for development
uv run python -m portal_tools.mcp_server
```

### Docker Deployment

```bash
# Build the Docker image
docker build -f Dockerfile.mcp -t portal-tools-mcp .

# Run the container
docker run -it \
  -e NEO4J_IP_PORT=localhost:7687 \
  -e NEO4J_USER=neo4j \
  -e NEO4J_PASSWORD=mysecret \
  portal-tools-mcp
```

## Environment Variables

- `NEO4J_IP_PORT`: Neo4j server address (default: localhost:7887)
- `NEO4J_USER`: Neo4j username
- `NEO4J_PASSWORD`: Neo4j password

## Available Tools

### 1. search_phenotypes
Search for phenotypes using vector similarity matching.

**Parameters:**
- `queries` (required): List of phenotype names to search for

**Returns:**
- Dictionary with `matches` containing search results for each query

### 2. get_top_genes
Get top genes for a specific phenotype.

**Parameters:**
- `phenotype_id` (required): ID of the phenotype to query
- `top_n` (optional): Number of top genes to return (default: 25)
- `metric` (optional): Ranking metric - "combined", "indirect", "direct" (default: "combined")
- `sigma` (optional): Statistical significance threshold (default: 2)
- `geneset_size` (optional): Gene set size - "small", "medium", "large" (default: "small")

**Returns:**
- Dictionary with `phenotype_id`, `top_genes`, and `parameters`

### 3. get_factors
Get factors for a specific phenotype.

**Parameters:**
- `phenotype_id` (required): ID of the phenotype to query
- `sigma` (optional): Statistical significance threshold (default: 2)
- `geneset_size` (optional): Gene set size - "small", "medium", "large" (default: "small")

**Returns:**
- Dictionary with `phenotype_id`, `factors`, and `parameters`

### 4. get_genesets
Get gene sets for a specific phenotype.

**Parameters:**
- `phenotype_id` (required): ID of the phenotype to query
- `sigma` (optional): Statistical significance threshold (default: 2)
- `geneset_size` (optional): Gene set size - "small", "medium", "large" (default: "small")
- `top_n` (optional): Number of top gene sets to return (default: 10)
- `metric` (optional): Ranking metric (default: "beta")

**Returns:**
- Dictionary with `phenotype_id`, `genesets`, and `parameters`

### 5. run_cypher_query
Execute a Cypher query against the Neo4j database.

**Parameters:**
- `cypher_query` (required): The Cypher query to execute

**Returns:**
- Dictionary with `query` and `result`

### 6. force_phenotype_embedding_update
Force update of phenotype embeddings cache.

**Parameters:** None

**Returns:**
- Dictionary with `status`, `message`, and `phenotype_count`

## MCP Client Integration

To use this server with an MCP client, configure it to connect to the server using stdio transport:

```json
{
  "mcpServers": {
    "portal-tools": {
      "command": "python",
      "args": ["-m", "portal_tools.mcp_server"]
    }
  }
}
```

## Architecture

Built with **FastMCP** for simplified MCP server implementation. The server maintains an in-memory cache of:
- Sentence transformer model (all-MiniLM-L6-v2)
- Phenotype data from bioindex API
- Pre-computed phenotype name embeddings

This caching strategy provides fast similarity searches while maintaining data freshness through the update endpoint.

### Key Features of FastMCP Implementation:
- **Simplified Setup**: No complex server initialization required
- **Type Safety**: Automatic type checking and validation
- **Clean API**: Decorator-based tool registration
- **Better Error Handling**: Automatic error response formatting

## Development

### Running Tests

```bash
cd portal-tools
pytest
```

### Legacy Flask Server

The original Flask-based REST API is still available in `portal_tools/app.py` for backward compatibility, but the MCP server is the recommended approach for new integrations.

## Dependencies

- `mcp`: Model Context Protocol framework
- `sentence-transformers`: For phenotype similarity search
- `neo4j`: Neo4j database driver
- `requests`: HTTP client for external APIs
- `numpy`: Numerical computing