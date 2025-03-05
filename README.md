# Portal AI

A framework for applying Large Language Models (LLMs) to A2F Knowledge Portals, specifically designed to work with PIGEAN results.

## Overview

This repository is structured as a Turborepo project that processes PIGEAN results and builds knowledge graphs for AI-powered portals. The main components are:

- **kg-ingress**: A package for ingesting and processing PIGEAN results into a knowledge graph
- **portal-model**: LinkML schema defining the knowledge graph structure
- **docker services**: Containerized environment for running the pipeline

## Getting Started

### Prerequisites

- Docker and Docker Compose
- Python 3.9+
- [LinkML](https://linkml.io/) (`pip install linkml`)

### Model Generation

The knowledge graph schema is defined in `portal-model.yaml` using LinkML. To generate the Python model classes:

```bash
pip install linkml
```

```bash
gen-python portal-model.yaml > kg-ingress/kg_ingress/models/portal_model.py
```

### Building the Knowledge Graph

1. First, navigate to the kg-ingress directory and follow the README instructions for setting up the ingestion pipeline
2. Process your PIGEAN results through the pipeline to build the knowledge base

### Running the Services

To start all services using Docker Compose:

```bash
docker compose up -d
```

To stop the services:

```bash
docker compose down
```

## Project Structure

```
.
├── kg-ingress/          # Knowledge graph ingestion package
├── portal-model.yaml    # LinkML schema definition
├── compose.yaml         # Docker services configuration
└── README.md
```

## Development

This is a Turborepo project. For local development:

1. Install dependencies:
   ```bash
   npm install
   ```

2. Build all packages:
   ```bash
   turbo build
   ```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

[Add your license information here]
