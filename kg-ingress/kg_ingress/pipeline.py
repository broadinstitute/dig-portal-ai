from kg_ingress.assets import *
import pandas as pd
from rdflib import Graph
from neo4j import GraphDatabase
import argparse
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

logger = logging.getLogger('pipeline')

# Neo4J Connection Details
NEO4J_URI = "bolt://localhost:7687"  # Default local Neo4j connection
NEO4J_USER = "neo4j"                 # Default Neo4j username
NEO4J_PASSWORD = "mysecret"          # Neo4j password (should be configured securely in production)

# Initialize Neo4j connection
logger.info("Creating Neo4j driver")
driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))
logger.info("Neo4j driver created")

# Load required mapping files for phenotype data integration
logger.info("Loading data files")
# Portal phenotype mappings - contains standardized trait names and descriptions
portal_phenotype_info = pd.read_csv("data/amp-traits-mapping-portal-phenotypes_06262024.csv")
# GCAT phenotype mappings - contains genetic trait associations
gcat_phenotype_info = pd.read_csv("data/gcat_v1.0.3.1.tsv", sep="\t")
gcat_phenotype_info = preprocess_gcat_info(gcat_phenotype_info)
# Load Orphanet ontology for rare disease mappings
orphanet_owl = Graph()
orphanet_owl.parse("data/ORDO_en_4.5.owl", format="xml")
logger.info("Data files loaded")

if __name__ == "__main__":
    # Set up command line arguments for flexible execution
    parser = argparse.ArgumentParser()
    parser.add_argument("--test", action="store_true", help="Run in test mode")
    parser.add_argument("--verbose", action="store_true", help="Run in verbose mode")
    parser.add_argument("--clean-db", action="store_true", help="Clean the database before running")
    parser.add_argument("--log-level", type=str, default="INFO", help="Set the log level")
    args = parser.parse_args()

    # Set log level based on argument
    log_level = getattr(logging, args.log_level.upper())
    logger.setLevel(log_level)

    if args.clean_db:
        logger.warning("Cleaning database")
        with driver.session() as session:
            session.run("MATCH (n) DETACH DELETE n")
        logger.info("Database cleaned")

    # Main Pipeline Steps:
    
    # 1. Fetch phenotype data from bioindex API
    logger.info("Fetching phenotype data")
    data = fetch_phenotype_data()
    if args.test:
        logger.debug("Running in test mode")
        data = data[:10]  # Limit data for testing
        
    # 2. Transform raw phenotype data into structured objects
    logger.info("Transforming phenotype data")
    transformed = transform_phenotype_data(data, portal_phenotype_info, gcat_phenotype_info, orphanet_owl, verbose=True)
    
    # 3. Insert transformed phenotype data into Neo4j
    logger.info("Inserting data into Neo4j")
    insert_data(transformed, driver=driver)

    # 4. Process gene-phenotype associations
    # Create an index of phenotypes for quick lookup
    phenotype_index = {p.name: p for p in transformed if isinstance(p, Phenotype)}
    genes = []
    associations = []
    
    # For each phenotype, fetch and process associated genes
    for _, phenotype in tqdm.tqdm(phenotype_index.items(), desc='Processing gene phenotype associations'):
        # Fetch gene associations from bioindex API
        data = fetch_gene_phenotype_data(phenotype.name)
        if args.test:
            data = data[:10]
        # Transform gene data and create association objects
        _genes, _associations = transform_gene_phenotype_data(data, phenotype_index) 
        genes.extend(_genes)
        associations.extend(_associations)
        
    # 5. Insert genes and their associations into Neo4j
    insert_data(genes, driver=driver) 
    insert_data(associations, driver=driver)
    
    logger.info("Done")
