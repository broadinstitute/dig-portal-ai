from mcp.server.fastmcp import FastMCP
import json
import requests

# Import the tools we want to expose to the MCP server
from portal_tools.tools.pigean import find_phenotype_data, get_top_genes

mcp = FastMCP('portal-tools')

# 

# Wrap the tools in MCP tools and add them to the server
@mcp.tool()
def find_portal_phenotypes(phenotype_name:str):
    """
    This tool returns a list of phenotypes that match the provided phenotype name in the portal in the form of a list of JSON objects where each object contains the following fields:
    - id: The id of the phenotype
    - name: The name of the phenotype

    Args:
        phenotype_name: The name of the phenotype to search for
    
    Returns:
        A list of JSON objects where each object contains the following fields:
        - id: The id of the phenotype
        - name: The name of the phenotype

    Example:
    [
        {
            "id": "gcat_trait_right_ventricular_stroke_volume_measurement",
            "phenotype_name": "right ventricular stroke volume measurement",
        },
    ]
    """
    return find_phenotype_data(phenotype_name)

@mcp.tool()
def pigean_top_genes(phenotype_name:str, top_n:int, metric:str='combined', sigma:float=2, geneset_size:str='small'):
    """
    This tool returns the top N genes for a given phenotype based on the desired PIGEAN metric. This tool should be used for ranking gene relevance to a phenotype based on the associated PIGEAN metric.
    The PIGEAN metric is a combination of the indirect and direct evidence for a gene-phenotype association.
    Indirect evidence is the evidence for a gene phenotype association through a gene set that has other genes that have high genetic support for a GWAS.
    Direct evidence is the evidence for a gene phenotype association through a GWAS that has high statistical significance.

    Args:
        phenotype_name: The name of the phenotype to get the top genes for
        top_n: The number of top genes to return
        metric: The metric to use for ranking the genes, either 'combined', 'indirect', or 'direct'
        sigma: The statistical significance threshold, default is 2, should never be changed.
        geneset_size: The size of the gene set to return, either 'large' or 'small', default is 'small'
    
    Returns:
        A list of JSON objects where each object contains the following fields:
        - gene_id: The id of the gene
        - gene_name: The name of the gene
        - metric_value: The metric value for the gene
        - metric_name: The name of the metric

    Example:
    [
        {
            "gene_id": "BRCA1",
            "gene_name": "BRCA1",
            "metric_value": 3,
            "metric_name": "combined"
        },
    ]
    """
    return get_top_genes(phenotype_name, top_n, metric, sigma, geneset_size)

if __name__ == "__main__":
    mcp.run(transport='stdio')