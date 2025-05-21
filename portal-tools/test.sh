#! /bin/bash
# curl -X POST http://localhost:5005/get_factors -H "Content-Type: application/json" -d '{"phenotype_id": "T2D", "sigma": 2, "geneset_size": "small"}'
# curl -X POST http://localhost:5005/get_genesets -H "Content-Type: application/json" -d '{"phenotype_id": "T2D", "sigma": 2, "geneset_size": "small", "top_n": 10, "metric": "beta"}'
curl -X POST http://localhost:5005/search_phenotypes -H "Content-Type: application/json" -d '{"queries": ["T2D", "heart disease", "cancer"]}'
curl -X POST http://localhost:5005/get_cipher -H "Content-Type: application/json" -d '{"cypher_query": "MATCH (n:Trait) RETURN n.id"}'