import pytest
from unittest.mock import Mock
from kg_ingress.assets import fetch_phenotype_data, transform_phenotype_data
from kg_ingress.models.portal_model import Phenotype, Gwas

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

def test_fetch_phenotype_data(sample_phenotype_api_response):
    """Test the fetch_phenotype_data asset"""
    context = build_op_context()
    result = fetch_phenotype_data(context)
    
    assert isinstance(result, list)
    assert len(result) == 3
    
    # Verify we got each type of phenotype
    trait_groups = {item["trait_group"] for item in result}
    assert trait_groups == {"portal", "gcat_trait", "rare_v2"}

def test_transform_phenotype_data(sample_phenotype_api_response):
    """Test the transform_phenotype_data asset"""
    context = build_op_context()
    raw_data = fetch_phenotype_data(context)
    result = transform_phenotype_data(context, raw_data)
    
    assert isinstance(result, list)
    assert all(isinstance(item, (Phenotype, Gwas)) for item in result) 