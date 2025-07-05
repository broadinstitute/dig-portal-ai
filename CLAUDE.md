# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

This is the DIG Portal AI project, a comprehensive system for applying Large Language Models to A2F Knowledge Portals with PIGEAN results. The repository contains three main components:

1. **Portal AI Frontend** (portal-ai/): Next.js application with OpenAI Assistants API integration
2. **KG Ingress Pipeline** (kg-ingress/): Python pipeline for processing PIGEAN data into Neo4j knowledge graphs
3. **Portal Tools** (1/): Python tool server that exposes portal endpoints as LLM tools

## Development Commands

### Portal AI Frontend (portal-ai/)
```bash
cd portal-ai
pnpm install          # Install dependencies
pnpm dev              # Start development server (localhost:3000)
pnpm build            # Build for production
pnpm start            # Start production server
pnpm lint             # Run ESLint
npx tsc --noEmit      # Type checking (no explicit script defined)
```

### KG Ingress Pipeline (kg-ingress/)
```bash
cd kg-ingress
pip install -e .                                    # Install package
python -m kg_ingress.pipeline                       # Run pipeline
python -m kg_ingress.pipeline --test --verbose      # Run in test mode
pytest kg_ingress_tests/                           # Run tests
```

### Portal Tools (portal-tools/)
```bash
cd portal-tools
uv pip install -e .                    # Install with uv
python -m portal_tools.app             # Run server
pytest                                 # Run tests (dev dependency)
```

### LinkML Model Generation
```bash
pip install linkml
gen-python portal-model.yaml > kg-ingress/kg_ingress/models/portal_model.py
```

## Architecture Overview

### Portal AI Frontend
- **Framework**: Next.js 15 with App Router, React 19, TypeScript
- **Styling**: Tailwind CSS with shadcn/ui components
- **Authentication**: NextAuth.js with Google OAuth
- **AI Integration**: OpenAI Assistants API with streaming and custom function calling
- **Key Features**: Real-time chat, tool calling for biological data queries, session management

### KG Ingress Pipeline
- **Purpose**: Processes PIGEAN results into Neo4j knowledge graphs
- **Schema**: LinkML-based model defined in portal-model.yaml
- **Data Sources**: Portal phenotypes, GCAT, Orphanet ontologies
- **Database**: Neo4j (default: bolt://localhost:7687)

### Portal Tools
- **Purpose**: Exposes portal endpoints as LLM tools
- **Framework**: Flask with CORS support
- **Dependencies**: Neo4j integration, sentence transformers, MCP CLI
- **Deployment**: Supports Docker deployment

## Key Implementation Details

### Function Registry (Portal AI)
The Portal AI frontend includes specialized functions for biological data:
- `get_top_genes` - Retrieve top genes for conditions
- `search_phenotypes` - Search phenotype descriptions
- `get_genesets` - Retrieve gene set information
- `get_factors` - Get factor data
- `run_cypher` - Execute Cypher queries against Neo4j

### API Integration
- Portal Tools API integration via `NEXT_PUBLIC_PORTAL_API_BASE_URL`
- OpenAI Assistant configured with file search and code interpreter
- Streaming responses with proper error handling

### Data Processing Pipeline
- Processes multiple data formats (CSV, TSV, OWL)
- Handles phenotype mappings and ontology relationships
- Supports incremental processing and database cleaning

## Environment Setup

### Portal AI Required Variables
```env
OPENAI_API_KEY=your_api_key
OPENAI_ASSISTANT_ID=your_assistant_id
GOOGLE_CLIENT_ID=your_google_client_id
GOOGLE_CLIENT_SECRET=your_google_client_secret
NEXTAUTH_SECRET=your_nextauth_secret
NEXTAUTH_URL=your_nextauth_url
NEXT_PUBLIC_PORTAL_API_BASE_URL=portal_tools_endpoint
```

### KG Ingress Configuration
- Neo4j connection: URI, username, password configurable in pipeline.py
- Required data files in kg-ingress/data/: phenotype mappings, GCAT data, ORDO ontology

## Development Workflow

### When Adding New Functions
1. Add function to `portal-ai/functions/index.ts`
2. Implement proper error handling and JSON formatting
3. Test with Portal Tools API endpoint
4. Update OpenAI Assistant configuration

### When Modifying Data Pipeline
1. Test with `--test` flag first (processes only 10 records)
2. Use `--verbose` for detailed logging
3. Consider `--clean-db` for fresh database state
4. Run pytest for validation

### Code Style and Patterns
- Follow existing component patterns in portal-ai/components/
- Use shadcn/ui components for UI consistency
- Implement proper TypeScript types
- Handle loading and error states appropriately
- Follow LinkML schema patterns for data modeling

## Testing

### Portal AI
```bash
cd portal-ai
# No explicit test script - verify with build and type checking
pnpm build && npx tsc --noEmit
```

### KG Ingress
```bash
cd kg-ingress
pytest kg_ingress_tests/
```

### Portal Tools
```bash
cd portal-tools
pytest  # Requires dev dependencies
```