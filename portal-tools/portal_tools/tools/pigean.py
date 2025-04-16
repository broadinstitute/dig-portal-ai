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

def find_phenotype_data(phenotype_name, top_n=50):
    """
    Finds phenotype data for a given phenotype name.
    """
    phenotype_data = fetch_phenotype_data()
    # Initialize the sentence transformer
    model = SentenceTransformer('all-MiniLM-L6-v2')
    # Embed the phenotype name
    phenotype_name_embedding = model.encode(phenotype_name)
    # Find the phenotype with the most similar name
    portal_names = [item['phenotype_name'] for item in phenotype_data]
    portal_names_embeddings = model.encode(portal_names)
    # Calculate the cosine similarity between the phenotype name and the portal names
    similarities = model.similarity(phenotype_name_embedding, portal_names_embeddings)[-1]
    print(similarities.shape)
    # Get the indices of the top N most similar phenotypes
    top_indices = np.argsort(similarities)[-top_n:]
    top_phenotypes = []
    for i in top_indices:
        top_phenotypes.append({
            'id': phenotype_data[i]['phenotype'],
            'name': phenotype_data[i]['phenotype_name'],
            'cosine_similarity': float(similarities[i])
        })
    # Return the top N phenotype matches
    return top_phenotypes

def fetch_gene_phenotype_data(phenotype_name, sigma=2, geneset_size='small'):
    """
    Fetches gene-phenotype associations from the bioindex API for a specific phenotype.
    
    Args:
        phenotype_name: Name of the phenotype to query
        sigma: Statistical significance threshold
        geneset_size: Size of the gene set to return ('large', 'medium', 'small')
    """
    url = f"https://bioindex-dev.hugeamp.org/api/bio/query/pigean-gene-phenotype"
    q = f"{phenotype_name},{sigma},{geneset_size}"
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

def get_top_genes(phenotype_name, top_n=10, metric='combined', sigma=2, geneset_size='small'):
    """
    Fetches the top N genes for a given phenotype based on the specified metric.
    
    Args:
        phenotype_name: Name of the phenotype to query
        top_n: Number of top genes to return
        metric: Metric to use for ranking ('combined', 'indirect', 'direct')
        sigma: Statistical significance threshold, default is 2
        geneset_size: Size of the gene set to return ('large', 'small'), default is 'small'
    """
    data = fetch_gene_phenotype_data(phenotype_name, sigma, geneset_size)
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
    
    