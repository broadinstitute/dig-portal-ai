# KG Ingress Pipeline

This pipeline processes phenotype data and loads it into a Neo4j graph database. It handles data from multiple sources including portal phenotypes, GCAT, and Orphanet ontologies.

## Prerequisites

- Python 3.8+
- Neo4j Database (running locally or accessible remotely)
- Required data files in `data/` directory:
  - `amp-traits-mapping-portal-phenotypes_06262024.csv`
  - `gcat_v1.0.3.1.tsv`
  - `ORDO_en_4.5.owl`

## Installation

1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -e .
   ```

## Configuration

The pipeline uses the following default Neo4j connection settings:
- URI: `bolt://localhost:7687`
- Username: `neo4j`
- Password: `mysecret`

To modify these settings, update the constants in `kg_ingress/pipeline.py`.

## Running the Pipeline

Basic usage:

## Usage
```bash
python -m kg_ingress.pipeline
```

### Command Line Options

- `--test`: Run in test mode (processes only 10 records)
- `--verbose`: Enable verbose logging
- `--clean-db`: Clean the database before running the pipeline
- `--log-level`: Set logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)

Example with options:
```bash
python -m kg_ingress.pipeline --test --verbose --clean-db --log-level DEBUG
```

## Pipeline Steps

1. Loads and preprocesses source data files
2. Fetches phenotype data
3. Transforms the phenotype data using various mappings
4. Inserts the transformed data into Neo4j

## Project Structure

```
kg-ingress/
├── kg_ingress/
│   ├── pipeline.py       # Main pipeline script
│   ├── assets.py         # Core assets and functions
│   └── utils/
│       └── phenotype_utils.py  # Phenotype-specific utilities
|   └── models/
|       └── portal_model.py  # Current Portal Model file generated from portal-model.yaml LinkML model
├── kg_ingress_tests/
│   ├── test_assets.py
│   └── test_phenotype_utils.py
└── data/                 # Data directory for required files
```

## Data Files

The pipeline requires the following data files in the `data/` directory:

- `amp-traits-mapping-portal-phenotypes_06262024.csv`: Portal phenotype mappings
- `gcat_v1.0.3.1.tsv`: GCAT phenotype information
- `ORDO_en_4.5.owl`: Orphanet ontology file

## Logging

The pipeline logs its progress to stdout with timestamps and log levels. You can adjust the logging level using the `--log-level` argument.

## Error Handling

If any required data files are missing or if there are connection issues with Neo4j, the pipeline will log appropriate error messages and exit.

## Development

To run tests:

```bash
pytest kg_ingress_tests/
```

## License

[MIT License](LICENSE)
