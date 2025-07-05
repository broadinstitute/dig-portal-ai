#!/usr/bin/env python3
"""
FastMCP Server for Portal Tools

This server exposes portal functionality as tools that can be called by MCP clients.
Uses FastMCP for simplified MCP server implementation.
"""

import logging
import os
from typing import List, Dict, Any

from fastmcp import FastMCP

# Import our existing tool modules
import portal_tools.tools.pigean as pigean
import portal_tools.tools.cypher_utils as cypher_utils
from sentence_transformers import SentenceTransformer

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create FastMCP server
mcp = FastMCP("portal-tools")

# Global state for caching
model = None
portal_phenotypes = None
portal_names = None
portal_names_embeddings = None

def initialize_neo4j_driver(neo4j_ip_port: str, neo4j_user: str, neo4j_password: str):
    """Initialize the Neo4j driver"""
    cypher_utils.initialize_neo4j_driver(neo4j_ip_port, neo4j_user, neo4j_password, log=True)

def ensure_phenotype_data():
    """Ensure phenotype data is loaded"""
    global model, portal_phenotypes, portal_names, portal_names_embeddings
    
    if model is None:
        logger.info("Loading sentence transformer model...")
        model = SentenceTransformer('all-MiniLM-L6-v2')
    
    if portal_phenotypes is None:
        logger.info("Fetching phenotype data...")
        portal_phenotypes = pigean.fetch_phenotype_data()
        portal_names = [item['phenotype_name'] for item in portal_phenotypes]
        portal_names_embeddings = model.encode(portal_names)
        logger.info("Phenotype data loaded successfully")

@mcp.tool()
def search_phenotypes(queries: List[str]) -> Dict[str, Any]:
    """Search for phenotypes using vector similarity matching
    
    Args:
        queries: List of phenotype names to search for
    
    Returns:
        Dictionary containing search results with matches for each query
    """
    global model, portal_phenotypes, portal_names_embeddings
    
    # Ensure we have the required data
    ensure_phenotype_data()
    
    if not queries or not isinstance(queries, list):
        raise ValueError("'queries' must be provided as a list of strings")
    
    result = pigean.search_phenotypes(
        queries, 
        portal_names_embeddings, 
        model, 
        portal_phenotypes
    )
    
    return {"matches": result}

@mcp.tool()
def get_top_genes(
    phenotype_id: str, 
    top_n: int = 25, 
    metric: str = "combined", 
    sigma: int = 2, 
    geneset_size: str = "small"
) -> Dict[str, Any]:
    """Get top genes for a specific phenotype
    
    Args:
        phenotype_id: ID of the phenotype to query
        top_n: Number of top genes to return (default: 25)
        metric: Metric to use for ranking - "combined", "indirect", "direct" (default: "combined")
        sigma: Statistical significance threshold (default: 2)
        geneset_size: Size of the gene set - "small", "medium", "large" (default: "small")
    
    Returns:
        Dictionary containing top genes for the phenotype
    """
    if not phenotype_id:
        raise ValueError("'phenotype_id' is required")
    
    result = pigean.get_top_genes(phenotype_id, top_n, metric, sigma, geneset_size)
    
    return {
        "phenotype_id": phenotype_id,
        "top_genes": result,
        "parameters": {
            "top_n": top_n,
            "metric": metric,
            "sigma": sigma,
            "geneset_size": geneset_size
        }
    }

@mcp.tool()
def get_factors(
    phenotype_id: str, 
    sigma: int = 2, 
    geneset_size: str = "small"
) -> Dict[str, Any]:
    """Get factors for a specific phenotype
    
    Args:
        phenotype_id: ID of the phenotype to query
        sigma: Statistical significance threshold (default: 2)
        geneset_size: Size of the gene set - "small", "medium", "large" (default: "small")
    
    Returns:
        Dictionary containing factors for the phenotype
    """
    if not phenotype_id:
        raise ValueError("'phenotype_id' is required")
    
    result = pigean.get_factors(phenotype_id, sigma, geneset_size)
    
    return {
        "phenotype_id": phenotype_id,
        "factors": result,
        "parameters": {
            "sigma": sigma,
            "geneset_size": geneset_size
        }
    }

@mcp.tool()
def get_genesets(
    phenotype_id: str, 
    sigma: int = 2, 
    geneset_size: str = "small", 
    top_n: int = 10, 
    metric: str = "beta"
) -> Dict[str, Any]:
    """Get gene sets for a specific phenotype
    
    Args:
        phenotype_id: ID of the phenotype to query
        sigma: Statistical significance threshold (default: 2)
        geneset_size: Size of the gene set - "small", "medium", "large" (default: "small")
        top_n: Number of top gene sets to return (default: 10)
        metric: Metric to use for ranking (default: "beta")
    
    Returns:
        Dictionary containing gene sets for the phenotype
    """
    if not phenotype_id:
        raise ValueError("'phenotype_id' is required")
    
    result = pigean.get_gene_genesets(phenotype_id, sigma, geneset_size, top_n, metric)
    
    return {
        "phenotype_id": phenotype_id,
        "genesets": result,
        "parameters": {
            "sigma": sigma,
            "geneset_size": geneset_size,
            "top_n": top_n,
            "metric": metric
        }
    }

@mcp.tool()
def run_cypher_query(cypher_query: str) -> Dict[str, Any]:
    """Execute a Cypher query against the Neo4j database
    
    Args:
        cypher_query: The Cypher query to execute
    
    Returns:
        Dictionary containing query results and metadata
    """
    if not cypher_query:
        raise ValueError("'cypher_query' is required")
    
    result = cypher_utils.run_cypher(cypher_query)
    
    return {
        "query": cypher_query,
        "result": result
    }

@mcp.tool()
def force_phenotype_embedding_update() -> Dict[str, str]:
    """Force update of phenotype embeddings cache
    
    Returns:
        Dictionary with update status message
    """
    global model, portal_phenotypes, portal_names, portal_names_embeddings
    
    logger.info("Forcing phenotype embedding update...")
    
    # Ensure model is loaded
    if model is None:
        model = SentenceTransformer('all-MiniLM-L6-v2')
    
    # Refresh data
    portal_phenotypes = pigean.fetch_phenotype_data()
    portal_names = [item['phenotype_name'] for item in portal_phenotypes]
    portal_names_embeddings = model.encode(portal_names)
    
    logger.info("Phenotype embeddings updated successfully")
    
    return {
        "status": "success",
        "message": "Phenotype embeddings updated successfully",
        "phenotype_count": len(portal_phenotypes)
    }

if __name__ == "__main__":
    # Initialize data on startup
    neo4j_ip_port = os.getenv('NEO4J_IP_PORT', 'bolt://localhost:7887')
    neo4j_user = os.getenv('NEO4J_USER', 'neo4j')
    neo4j_password = os.getenv('NEO4J_PASSWORD', 'password')
    initialize_neo4j_driver(neo4j_ip_port, neo4j_user, neo4j_password)
    ensure_phenotype_data()
    
    # Run the server
    logger.info("Starting MCP server...")
    mcp.run(
        transport="sse",                  # ← new: Streamable HTTP
        host="0.0.0.0",                    # default 127.0.0.1; expose to LAN if you like
        port=8080,                         # pick any open port
        path="/mcp/",                      # default; keep it unless you need a custom route
        log_level="info",                  # optional
    )