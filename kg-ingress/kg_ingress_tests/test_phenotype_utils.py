import pytest
import pandas as pd
from rdflib import Graph
import os
from unittest.mock import Mock
from kg_ingress.utils.phenotype_utils import (
    create_orphanet_phenotype,
    create_gcat_phenotype, 
    create_portal_phenotype,
    preprocess_gcat_info,
)

# Setup fixtures for data files
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
                "trait_group": "portal",
                "phenotype": "AM_broad_heavy",
                "phenotype_name": "Broad vs. Heavy alcohol consumption",
                "display_group": "NUTRITIONAL",
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
        ]
    }
    return mock_response

@pytest.fixture
def portal_phenotype_data():
    """Load portal phenotype mapping data"""
    current_dir = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(current_dir, "..", "data", "amp-traits-mapping-portal-phenotypes_06262024.csv")
    return pd.read_csv(data_path)

@pytest.fixture
def gcat_phenotype_data():
    """Load and preprocess GCAT phenotype data"""
    current_dir = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(current_dir, "..", "data", "gcat_v1.0.3.1.tsv")
    raw_data = pd.read_csv(data_path, sep="\t")
    return preprocess_gcat_info(raw_data)

@pytest.fixture
def orphanet_graph():
    """Load Orphanet OWL data"""
    current_dir = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(current_dir, "..", "data", "ORDO_en_4.5.owl")
    graph = Graph()
    graph.parse(data_path, format="xml")
    return graph

def test_create_orphanet_phenotype(sample_phenotype_api_response, orphanet_graph):
    """Test the creation of Orphanet phenotypes"""
    for item in sample_phenotype_api_response.json()["data"]:
        if 'Orphanet' in item['phenotype']:
            phenotype = create_orphanet_phenotype(orphanet_graph, item['phenotype'], item['phenotype_name'])
            print(phenotype)
            assert phenotype is not None

def test_create_gcat_phenotype(sample_phenotype_api_response, gcat_phenotype_data):
    """Test the creation of GCAT phenotypes"""
    for item in sample_phenotype_api_response.json()["data"]:
        if 'gcat_trait' in item['phenotype']:
            phenotype = create_gcat_phenotype(gcat_phenotype_data, item['phenotype'], item['phenotype_name'])
            print(phenotype)
            assert phenotype is not None

def test_create_portal_phenotype(sample_phenotype_api_response, portal_phenotype_data):
    """Test the creation of Portal phenotypes"""
    for item in sample_phenotype_api_response.json()["data"]:
        if 'Orphanet' not in item['phenotype'] and 'gcat_trait' not in item['phenotype']:
            phenotype = create_portal_phenotype(portal_phenotype_data, item['phenotype'], item['phenotype_name'])
            print(phenotype)
            assert phenotype is not None
