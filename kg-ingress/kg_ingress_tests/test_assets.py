import pytest
from unittest.mock import Mock
from kg_ingress.assets import fetch_phenotype_data, transform_phenotype_data, insert_data
from kg_ingress.models.portal_model import Phenotype, Gwas
import pandas as pd
from rdflib import Graph
from kg_ingress.utils.phenotype_utils import preprocess_gcat_info
from neo4j import GraphDatabase

@pytest.fixture
def sample_phenotype_api_response(mocker):
    """Mock the API response for phenotype data"""
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "data": [
            {
                "trait_group": "portal",
                "phenotype": "eGFRcrcys",
                "phenotype_name": "eGFRcr-cys (serum creatinine and cystatin C)",
                "display_group": "RENAL",
                "dummy": 1
            },
            {
                "trait_group": "gcat_trait",
                "phenotype": "gcat_trait_trait_in_response_to_platinum",
                "phenotype_name": "trait in response to platinum",
                "display_group": "PHARMACOGENOMICS",
                "dummy": 1
            },
            {
                "trait_group": "rare_v2",
                "phenotype": "Genetic_cerebral_small_vessel_disease_Orphanet_477754",
                "phenotype_name": "Genetic cerebral small vessel disease",
                "display_group": "STROKE",
                "dummy": 1
            }
        ],
        "continuation": None
    }
    mocker.patch('requests.get', return_value=mock_response)
    return mock_response

@pytest.fixture
def portal_phenotype_info():
    """Load portal phenotype mapping data"""
    return pd.read_csv("data/amp-traits-mapping-portal-phenotypes_06262024.csv")

@pytest.fixture
def gcat_phenotype_info():
    """Load and preprocess GCAT phenotype data"""
    gcat_info = pd.read_csv("data/gcat_v1.0.3.1.tsv", sep="\t")
    return preprocess_gcat_info(gcat_info)

@pytest.fixture
def orphanet_owl():
    """Load Orphanet OWL data"""
    owl_graph = Graph()
    owl_graph.parse("data/ORDO_en_4.5.owl", format="xml")
    return owl_graph

@pytest.fixture
def neo4j_uri():
    """Neo4j URI"""
    return "bolt://localhost:7687"

@pytest.fixture
def neo4j_user():
    """Neo4j user"""
    return "neo4j"

@pytest.fixture
def neo4j_password():
    """Neo4j password"""
    return "mysecret"

@pytest.fixture
def neo4j_driver(neo4j_uri, neo4j_user, neo4j_password):
    """Neo4j driver"""
    return GraphDatabase.driver(neo4j_uri, auth=(neo4j_user, neo4j_password))

def test_fetch_phenotype_data(sample_phenotype_api_response):
    """Test the fetch_phenotype_data asset"""
    result = fetch_phenotype_data()
    
    assert isinstance(result, list)
    assert len(result) == 3
    
    # Verify we got each type of phenotype
    trait_groups = {item["trait_group"] for item in result}
    assert trait_groups == {"portal", "gcat_trait", "rare_v2"}

def test_transform_phenotype_data(sample_phenotype_api_response, portal_phenotype_info, gcat_phenotype_info, orphanet_owl):
    """Test the transform_phenotype_data asset"""
    raw_data = fetch_phenotype_data()
    result = transform_phenotype_data(raw_data, portal_phenotype_info, gcat_phenotype_info, orphanet_owl)
    
    assert isinstance(result, list)
    assert all(isinstance(item, (Phenotype, Gwas)) for item in result)

def test_insert_data(sample_phenotype_api_response, portal_phenotype_info, gcat_phenotype_info, orphanet_owl, neo4j_driver):
    """Test the insert_data asset"""
    raw_data = fetch_phenotype_data()
    result = transform_phenotype_data(raw_data, portal_phenotype_info, gcat_phenotype_info, orphanet_owl)
    # Delete all data from the database
    with neo4j_driver.session() as session:
        session.run("MATCH (n) DETACH DELETE n")
    insert_data(result, driver=neo4j_driver)
    # Verify that the data was inserted correctly
    with neo4j_driver.session() as session:
        result = session.run("MATCH (p:Phenotype) RETURN p.name")
        assert result.single()[0] == "eGFRcrcys"
