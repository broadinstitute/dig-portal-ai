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

def fetch_phenotype_data():
    """Fetch phenotype data from the bioindex API"""
    url = "https://bioindex-dev.hugeamp.org/api/bio/query/pigean-phenotypes?q=1"
    all_data = []
    
    response = requests.get(url)
    if response.status_code != 200:
        raise ValueError(f"API request failed with status {response.status_code}")
        
    data = response.json()
    all_data.extend(data['data'])
    
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
    """Transform raw phenotype data into model objects"""
    transformed = []
    for item in tqdm.tqdm(fetch_phenotype_data, desc="Transforming phenotype data", disable=not verbose):
        if "Orphanet" in item["phenotype"]:
            phenotype = create_orphanet_phenotype(orphanet_owl, item["phenotype"], item["phenotype_name"])
            if phenotype:
                transformed.append(phenotype)
        elif "gcat_trait" in item["phenotype"]:
            phenotype, studies = create_gcat_phenotype(gcat_phenotype_info, item["phenotype"], item["phenotype_name"])
            if phenotype:
                transformed.append(phenotype)
                transformed.extend(studies)
        else:
            phenotype = create_portal_phenotype(portal_phenotype_info, item["phenotype"], item["phenotype_name"])
            if phenotype:
                transformed.append(phenotype)
    return transformed

def insert_data(transformed, driver=None, neo4j_uri=None, neo4j_user=None, neo4j_password=None):
    """Insert transformed phenotype data into Neo4j"""
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
                else:
                    raise ValueError(f"Unknown item type: {type(item)}")
