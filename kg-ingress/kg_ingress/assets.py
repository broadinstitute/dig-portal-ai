from dagster import asset
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

@asset
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

@asset
def transform_phenotype_data(fetch_phenotype_data):
    """Transform raw phenotype data into model objects"""
    transformed = []
    for item in fetch_phenotype_data:
        if "Orphanet" in item["phenotype"]:
            phenotype = create_orphanet_phenotype(item["phenotype"], item["phenotype_name"])
            if phenotype:
                transformed.append(phenotype)
        elif "gcat_trait" in item["phenotype"]:
            phenotype, studies = create_gcat_phenotype(item["phenotype"], item["phenotype_name"])
            if phenotype:
                transformed.append(phenotype)
                transformed.extend(studies)
        else:
            phenotype = create_portal_phenotype(item["phenotype"], item["phenotype_name"])
            if phenotype:
                transformed.append(phenotype)
    return transformed 