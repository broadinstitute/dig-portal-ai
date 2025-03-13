import pytest
from unittest.mock import Mock
from kg_ingress.assets import fetch_phenotype_data, transform_phenotype_data, insert_data, fetch_gene_phenotype_data, transform_gene_phenotype_data
from kg_ingress.models.portal_model import Phenotype, Gwas, Gene, SupportAssociation
import pandas as pd
from rdflib import Graph
from kg_ingress.utils.phenotype_utils import preprocess_gcat_info
from neo4j import GraphDatabase
import requests

@pytest.fixture
def mock_api_responses(mocker, request):
    """Mock both phenotype and gene-phenotype API responses"""

    # Phenotype response
    phenotype_response = Mock()
    phenotype_response.status_code = 200
    phenotype_response.json.return_value = {
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
            "phenotype": "gcat_trait_right_ventricular_stroke_volume_measurement",
            "phenotype_name": "right ventricular stroke volume measurement",
            "display_group": "STROKE",
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

    # Gene-phenotype response
    gene_phenotype_response = Mock()
    gene_phenotype_response.status_code = 200
    gene_phenotype_response.json.return_value = {
        "data": [
            {
                "combined": 2.66,
                "gene": "ATXN2",
                "gene_set_size": "large",
                "huge_score": 2.66,
                "log_bf": 2.66,
                "n": 1469,
                "phenotype": "gcat_trait_right_ventricular_stroke_volume_measurement",
                "prior": 0.0000614,
                "sigma": 2,
                "trait_group": "gcat_trait"
            },
            {
                "combined": 1.79,
                "gene": "PTPN11",
                "gene_set_size": "large",
                "huge_score": 1.79,
                "log_bf": 1.79,
                "n": 2640,
                "phenotype": "gcat_trait_right_ventricular_stroke_volume_measurement",
                "prior": 0.00127,
                "sigma": 2,
                "trait_group": "gcat_trait"
            },
            {
                "combined": 1.54,
                "gene": "PLN",
                "gene_set_size": "large",
                "huge_score": 1.54,
                "log_bf": 1.54,
                "n": 4922,
                "phenotype": "gcat_trait_right_ventricular_stroke_volume_measurement",
                "prior": 0.00126,
                "sigma": 2,
                "trait_group": "gcat_trait"
            }
        ],
        "continuation": None
    }

    def mock_get(url, *args, **kwargs):
        if "pigean-phenotypes" in url:
            return phenotype_response
        elif "pigean-gene-phenotype" in url:
            return gene_phenotype_response
        # Return a mock for any other URL
        default_response = Mock()
        default_response.status_code = 404
        return default_response

    # Apply the mock
    mocker.patch('requests.get', side_effect=mock_get)
    
    return {
        'phenotype': phenotype_response,
        'gene_phenotype': gene_phenotype_response
    }

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

def test_fetch_phenotype_data(mock_api_responses):
    """Test the fetch_phenotype_data asset"""
    result = fetch_phenotype_data()
    
    assert isinstance(result, list)
    assert len(result) == 3
    
    # Verify we got each type of phenotype
    trait_groups = {item["trait_group"] for item in result}
    assert trait_groups == {"portal", "gcat_trait", "rare_v2"}

def test_fetch_gene_phenotype_data(mock_api_responses):
    """Test the fetch_gene_phenotype_data asset"""
    result = fetch_gene_phenotype_data("gcat_trait_right_ventricular_stroke_volume_measurement")
    print(result)
    assert isinstance(result, list)
    assert len(result) == 3
    assert result[0]["gene"] == "ATXN2"
    assert result[1]["gene"] == "PTPN11"
    assert result[2]["gene"] == "PLN"

def test_transform_phenotype_data(mock_api_responses, portal_phenotype_info, gcat_phenotype_info, orphanet_owl):
    """Test the transform_phenotype_data asset"""
    raw_data = fetch_phenotype_data()
    result = transform_phenotype_data(raw_data, portal_phenotype_info, gcat_phenotype_info, orphanet_owl)
    
    assert isinstance(result, list)
    assert all(isinstance(item, (Phenotype, Gwas)) for item in result)

def test_transform_gene_phenotype_data(mock_api_responses, portal_phenotype_info, gcat_phenotype_info, orphanet_owl):
    """Test the transform_gene_phenotype_data asset"""
    print("Running test_transform_gene_phenotype_data")
    phenotype_raw_data = fetch_phenotype_data()
    print("Fetched phenotype raw data")
    phenotypes = transform_phenotype_data(phenotype_raw_data, portal_phenotype_info, gcat_phenotype_info, orphanet_owl)
    print("Transformed phenotype data")
    raw_data = fetch_gene_phenotype_data("gcat_trait_right_ventricular_stroke_volume_measurement")
    print("Fetched gene phenotype raw data")
    result = transform_gene_phenotype_data(raw_data, phenotypes)
    print("Transformed gene phenotype data")
    
    assert isinstance(result, tuple)
    genes, associations = result
    assert all(isinstance(item, Gene) for item in genes)
    assert all(isinstance(item, SupportAssociation) for item in associations)
    assert len(genes) == 3  # ATXN2, PTPN11, PLN
    assert len(associations) == 3  # One association per gene

def test_insert_data(mock_api_responses, portal_phenotype_info, gcat_phenotype_info, orphanet_owl, neo4j_driver):
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
