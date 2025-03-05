from dagster import Definitions
from .assets import *

defs = Definitions(
    assets=[fetch_phenotype_data, transform_phenotype_data]
) 