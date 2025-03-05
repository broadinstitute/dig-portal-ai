from assets import *

# Neo4j Connection Details
NEO4J_URI = "bolt://localhost:7687"  # Change this if Neo4j is hosted elsewhere
NEO4J_USER = "neo4j"
NEO4J_PASSWORD = "mysecret"


if __name__ == "__main__":
    data = fetch_phenotype_data()
    transformed = transform_phenotype_data(data)
    insert_into_neo4j(transformed, NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD)