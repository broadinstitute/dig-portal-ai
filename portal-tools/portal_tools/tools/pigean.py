from typing import List
import requests
from sentence_transformers import SentenceTransformer
import numpy as np


def fetch_phenotype_data():
    """
    Fetches phenotype data from the bioindex API using pagination.
    Returns a list of all phenotype records from the API.
    """
    url = "https://bioindex-dev.hugeamp.org/api/bio/query/pigean-phenotypes?q=1"
    all_data = []
    
    # Initial request
    response = requests.get(url)
    if response.status_code != 200:
        raise ValueError(f"API request failed with status {response.status_code}")
        
    data = response.json()
    all_data.extend(data['data'])
    
    # Handle pagination using continuation tokens
    while data['continuation']:
        cont_url = f"https://bioindex-dev.hugeamp.org/api/bio/cont?token={data['continuation']}"
        response = requests.get(cont_url)
        if response.status_code != 200:
            raise ValueError(f"Continuation request failed with status {response.status_code}")
            
        data = response.json()
        all_data.extend(data['data'])
        
    return all_data

def search_phenotypes(phenotype_name, phenotype_names_embeddings, model, phenotype_data, top_n=50):
    """
    Finds phenotype data for a given phenotype name.
    """
    # Calculate the cosine similarity between the phenotype name and the portal names
    phenotype_name_embedding = model.encode(phenotype_name)
    # Calculate the cosine similarity between the phenotype name and the portal names
    similarities = model.similarity(phenotype_name_embedding, phenotype_names_embeddings)[-1]
    # Get the indices of the top N most similar phenotypes
    top_indices = np.argsort(similarities)[-top_n:]
    top_phenotypes = []
    for i in top_indices:
        top_phenotypes.append({
            'id': phenotype_data[i]['phenotype'],
            'name': phenotype_data[i]['phenotype_name'],
            'cosine_similarity': float(similarities[i])
        })
    # Sort the top phenotypes by cosine similarity in descending order
    top_phenotypes = sorted(top_phenotypes, key=lambda x: x['cosine_similarity'], reverse=True)
    # Return the top N phenotype matches
    return top_phenotypes

def fetch_gene_phenotype_data(phenotype_id, sigma=2, geneset_size='small'):
    """
    Fetches gene-phenotype associations from the bioindex API for a specific phenotype.
    
    Args:
        phenotype_id: ID of the phenotype to query
        sigma: Statistical significance threshold
        geneset_size: Size of the gene set to return ('large', 'medium', 'small')
    """
    url = f"https://bioindex-dev.hugeamp.org/api/bio/query/pigean-gene-phenotype"
    q = f"{phenotype_id},{sigma},{geneset_size}"
    response = requests.get(url, params={'q': q})
    if response.status_code != 200:
        raise ValueError(f"API request failed with status {response.status_code}")
    
    data = response.json()
    all_data = data['data']
    
    while data['continuation']:
        cont_url = f"https://bioindex-dev.hugeamp.org/api/bio/cont?token={data['continuation']}"
        response = requests.get(cont_url)
        if response.status_code != 200:
            raise ValueError(f"Continuation request failed with status {response.status_code}")
            
        data = response.json()
        all_data.extend(data['data'])
    return all_data

def get_top_genes(phenotype_id, top_n=10, metric='combined', sigma=2, geneset_size='small'):
    """
    Fetches the top N genes for a given phenotype based on the specified metric.
    
    Args:
        phenotype_name: Name of the phenotype to query
        top_n: Number of top genes to return
        metric: Metric to use for ranking ('combined', 'indirect', 'direct')
        sigma: Statistical significance threshold, default is 2
        geneset_size: Size of the gene set to return ('large', 'small'), default is 'small'
    """
    data = fetch_gene_phenotype_data(phenotype_id, sigma, geneset_size)
    # Parse out the metric name
    if metric == 'combined':
        metric_name = 'combined'
    elif metric == 'indirect':
        metric_name = 'prior'
    elif metric == 'direct':
        metric_name = 'log_bf'
    else:
        raise ValueError(f"Invalid metric: {metric}")
    # Sort the data by the specified metric in descending order
    sorted_data = sorted(data, key=lambda x: x[metric_name], reverse=True)
    # Parse out the sorted data into a list of JSON objects
    top_genes = []
    for item in sorted_data[:top_n]:
        top_genes.append({
            "gene_id": item['gene'],
            "gene_name": item['gene'],
            "metric_value": item[metric_name],
            "metric_name": metric
        })
    # Return the top N genes
    return top_genes

def fetch_gene_genesets(phenotype_id:str, sigma=2, geneset_size='small', metric:str='beta'):
    """
    Fetches the genesets for a given gene.
    """
    url = f"https://bioindex-dev.hugeamp.org/api/bio/query/pigean-gene-set-phenotype"
    q = f"{phenotype_id},{sigma},{geneset_size}"
    response = requests.get(url, params={'q': q})
    if response.status_code != 200:
        raise ValueError(f"API request failed with status {response.status_code}")
    
    _data = response.json()
    data = []
    for item in _data['data']:
        data.append({
            "metric_value": item[metric],
            "metric_name": metric,
            "gene_set": item['gene_set'],
            "phenotype": item['phenotype'],
        })
    return data

def get_gene_genesets(phenotype_id:str, top_n:int=10, metric:str='beta', sigma:int=2, geneset_size:str='small'):
    """
    Fetches the top N genesets for a given gene based on the specified.
    """
    data = fetch_gene_genesets(phenotype_id, sigma, geneset_size, metric)
    # Sort the data by the specified metric in descending order
    sorted_data = sorted(data, key=lambda x: x['metric_value'], reverse=True)
    # Parse out the sorted data into a list of JSON objects
    return sorted_data[:top_n]

def fetch_factors(phenotype_id:str, sigma:int=2, geneset_size:str='small'):
    """
    Fetches the factors for a given phenotype.
    """
    url = f"https://bioindex-dev.hugeamp.org/api/bio/query/pigean-factor"
    q = f"{phenotype_id},{sigma},{geneset_size}"
    response = requests.get(url, params={'q': q})
    if response.status_code != 200:
        raise ValueError(f"API request failed with status {response.status_code}")
    
    _data = response.json()
    data = []
    for item in _data['data']:
        curated_item = {
            "factor_label": item['label'],
            "gene_set_score": item['gene_set_score'],
            "gene_score": item['gene_score'],
            "top_genes": [],
            "top_gene_sets": []
        }
        for gene in item['top_genes'].split(';'):
            curated_item['top_genes'].append(gene)
        for gene_set in item['top_gene_sets'].split(';'):
            curated_item['top_gene_sets'].append(gene_set)
        data.append(curated_item)
    return data

def get_factors(phenotype_id:str, sigma:int=2, geneset_size:str='small'):
    """
    Fetches the factors for a given phenotype.
    """
    data = fetch_factors(phenotype_id, sigma, geneset_size)
    # Sort the data by the gene_set_score in descending order
    sorted_data = sorted(data, key=lambda x: x['gene_set_score'], reverse=True)
    # Parse out the sorted data into a list of JSON objects
    return sorted_data
