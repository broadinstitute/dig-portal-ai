# Portal AI

A framework for applying Large Language Models (LLMs) to A2F Knowledge Portals, specifically designed to work with PIGEAN results.

## Table of Contents
- [Overview](#overview)
- [Components](#components)
  - [KG Ingress](#kg-ingress)
  - [Portal AI Frontend](#portal-ai-frontend)
  - [Portal Tools](#portal-tools)
- [Getting Started](#getting-started)
- [Development](#development)
- [Contributing](#contributing)

## Overview

This repository processes PIGEAN results and builds knowledge graphs for AI-powered portals. The project consists of three main components:

1. **KG Ingress**: Processes PIGEAN results into a knowledge graph
2. **Portal AI Frontend**: Next.js application for interacting with the knowledge graph
3. **Portal Tools**: Tool server that exposes portal endpoints as LLM tools

## Components

### KG Ingress

The knowledge graph ingestion package processes PIGEAN results into a structured knowledge graph using LinkML schemas.

#### Prerequisites
- Python 3.9+
- [LinkML](https://linkml.io/) (`pip install linkml`)

#### Model Generation

The knowledge graph schema is defined in `portal-model.yaml` using LinkML. To generate the Python model classes:

```bash
pip install linkml
gen-python portal-model.yaml > kg-ingress/kg_ingress/models/portal_model.py
```

#### Building the Knowledge Graph

1. Navigate to the kg-ingress directory
2. Follow the README instructions for setting up the ingestion pipeline
3. Process your PIGEAN results through the pipeline to build the knowledge base

### Portal AI Frontend

A modern Next.js application built with Tailwind CSS and shadcn/ui components for interacting with the knowledge graph.

#### Prerequisites
- Node.js 18+
- pnpm

#### Installation

```bash
cd portal-ai
pnpm install
```

#### Development

```bash
# Start the development server
pnpm dev

# Build for production
pnpm build

# Start production server
pnpm start
```

### Portal Tools

A tool server that wraps various portal endpoints and exposes them as tools for LLMs through the Portal AI frontend.

#### Prerequisites
- Python 3.9+
- [uv](https://github.com/astral-sh/uv) (Python package installer and resolver)
- Docker (optional)

#### Installation

```bash
cd portal-tools

# Install dependencies using uv
uv pip install -e .

# Or if you want to create a virtual environment first
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
uv pip install -e .
```

#### Running the Server

```bash
# Using Python directly
python -m portal_tools/app.py

# Using Docker
docker build -t portal-tools .
docker run -p 8000:8000 portal-tools
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request
