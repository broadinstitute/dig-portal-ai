import requests
from neo4j import GraphDatabase
from .models.portal_model import *
from .utils.phenotype_utils import (
    create_orphanet_phenotype,
    create_gcat_phenotype,
    create_portal_phenotype,
    preprocess_gcat_info,
    lookup_trait_with_db_refs
)
import tqdm
import uuid


def fetch_phenotype_data():
    """
    Fetches phenotype data from the bioindex API using pagination.
    Returns a list of all phenotype records from the API.
    """
    url = "https://bioindex-dev.hugeamp.org/api/bio/query/pigean-phenotypes?q=1"
    all_data = []
    
    # Initial request
    response = requests.get(url)
    if response.status_code != 200:
        raise ValueError(f"API request failed with status {response.status_code}")
        
    data = response.json()
    all_data.extend(data['data'])
    
    # Handle pagination using continuation tokens
    while data['continuation']:
        cont_url = f"https://bioindex-dev.hugeamp.org/api/bio/cont?token={data['continuation']}"
        response = requests.get(cont_url)
        if response.status_code != 200:
            raise ValueError(f"Continuation request failed with status {response.status_code}")
            
        data = response.json()
        all_data.extend(data['data'])
        
    return all_data

def fetch_gene_phenotype_data(phenotype_name, sigma=2, geneset_size='large'):
    """
    Fetches gene-phenotype associations from the bioindex API for a specific phenotype.
    
    Args:
        phenotype_name: Name of the phenotype to query
        sigma: Statistical significance threshold
        geneset_size: Size of the gene set to return ('large', 'medium', 'small')
    """
    url = f"https://bioindex-dev.hugeamp.org/api/bio/query/pigean-gene-phenotype"
    q = f"{phenotype_name},{sigma},{geneset_size}"
    response = requests.get(url, params={'q': q})
    if response.status_code != 200:
        raise ValueError(f"API request failed with status {response.status_code}")
    
    data = response.json()
    all_data = data['data']
    
    while data['continuation']:
        cont_url = f"https://bioindex-dev.hugeamp.org/api/bio/cont?token={data['continuation']}"
        response = requests.get(cont_url)
        if response.status_code != 200:
            raise ValueError(f"Continuation request failed with status {response.status_code}")
            
        data = response.json()
        all_data.extend(data['data'])
    return all_data

def transform_phenotype_data(
        fetch_phenotype_data, 
        portal_phenotype_info, 
        gcat_phenotype_info, 
        orphanet_owl,
        verbose=False):
    """
    Transforms raw phenotype data into structured model objects based on their source.
    
    Handles three types of phenotypes:
    1. Orphanet phenotypes (rare diseases)
    2. GCAT phenotypes (GWAS catalog traits)
    3. Portal phenotypes (standard portal traits)
    
    Returns a list of transformed phenotype objects and related entities.
    """
    transformed = []
    for item in tqdm.tqdm(fetch_phenotype_data, desc="Transforming phenotype data", disable=not verbose):
        # Process Orphanet rare disease phenotypes
        if "Orphanet" in item["phenotype"]:
            phenotype = create_orphanet_phenotype(orphanet_owl, item["phenotype"], item["phenotype_name"])
            if phenotype:
                transformed.append(phenotype)
        # Process GCAT genetic trait phenotypes
        elif "gcat_trait" in item["phenotype"]:
            phenotype, studies = create_gcat_phenotype(gcat_phenotype_info, item["phenotype"], item["phenotype_name"])
            if phenotype:
                transformed.append(phenotype)
                transformed.extend(studies)
        # Process standard portal phenotypes
        else:
            phenotype = create_portal_phenotype(portal_phenotype_info, item["phenotype"], item["phenotype_name"])
            if phenotype:
                transformed.append(phenotype)
    return transformed

def transform_gene_phenotype_data(gene_phenotype_data, phenotype_index):
    """
    Transforms gene-phenotype association data into Gene objects and SupportAssociation objects.
    
    Creates:
    1. Gene nodes for each unique gene
    2. SupportAssociation edges connecting genes to phenotypes with evidence scores
    """
    # Index phenotypes by name field for quick lookup
    genes, associations = {}, []
    for item in tqdm.tqdm(gene_phenotype_data, desc="Transforming gene phenotype data"):
        # Create gene node if it doesn't exist
        if item["gene"] not in genes:
            gene = Gene(
                id=item["gene"],
                symbol=item["gene"],
            )
            genes[item["gene"]] = gene
        try:
            # Create association node
            association = SupportAssociation(
                id=f'sa-{uuid.uuid4()}',
                subject=genes[item["gene"]].id,
                object=phenotype_index[item["phenotype"]].id,
                predicate="PORTALLINK:supports",
                combined_support=CombinedSupportScore(log_odds=item["combined"]),
                direct_support=DirectSupportScore(log_odds=item["log_bf"]),
                indirect_support=IndirectSupportScore(log_odds=item["prior"])
            )
            associations.append(association)
        except KeyError as e:
            print(f"Error when processing gene {item}: {e}")


    # Collect all genes
    genes = list(genes.values())
    return genes, associations

def insert_data(transformed, driver=None, neo4j_uri=None, neo4j_user=None, neo4j_password=None):
    """
    Inserts transformed data into Neo4j graph database.
    
    Handles different types of nodes and relationships:
    - Phenotype nodes
    - GWAS study nodes
    - Gene nodes
    - SupportAssociation relationships with evidence scores
    """
    if driver is None:
        driver = GraphDatabase.driver(neo4j_uri, auth=(neo4j_user, neo4j_password))
    with driver.session() as session:
            for item in transformed:
                if isinstance(item, Phenotype):
                    session.run(
                        """
                        MERGE (p:Phenotype {id: $id})
                        SET p.name = $name,
                            p.description = $description,
                            p.display_name = $display_name
                        """
                        ,
                        id=item.id,
                        name=item.name,
                        description=item.description,
                        display_name=item.display_name
                    )
                elif isinstance(item, Gwas):
                    session.run(
                        """
                        MERGE (g:Gwas {id: $id})
                        SET g.name = $name,
                            g.description = $description
                        """
                        ,
                        id=item.id,
                        name=item.name,
                        description=item.description
                    )
                elif isinstance(item, Gene):
                    session.run(
                        """
                        MERGE (g:Gene {id: $id})
                        SET g.symbol = $symbol
                        """,
                        id=item.id,
                        symbol=item.symbol
                    )
                elif isinstance(item, SupportAssociation):
                    # Build query to insert support association
                    query = """
                        MERGE (g:Gene {id: $gene_id})
                        MERGE (p:Phenotype {id: $phenotype_id})
                        MERGE (sa:SupportAssociation {id: $association_id})
                        SET sa.predicate = $predicate,
                            sa.direct_support = $direct_support,
                            sa.indirect_support = $indirect_support,
                            sa.combined_support = $combined_support
                        MERGE (sa)-[:SUBJECT]->(g)
                        MERGE (sa)-[:OBJECT]->(p)
                        """

                    session.run(
                        query,
                        gene_id=str(item.subject),
                        phenotype_id=str(item.object),
                        association_id=item.id,
                        combined_support=float(item.combined_support.log_odds),
                        direct_support=float(item.direct_support.log_odds),
                        indirect_support=float(item.indirect_support.log_odds),
                        predicate=item.predicate.split(":")[-1] # Removes curie prefix
                    ) 
                else:
                    raise ValueError(f"Unknown item type: {type(item)}")
