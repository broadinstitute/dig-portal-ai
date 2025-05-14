from flask import Flask, request, jsonify
from flask_cors import CORS
import portal_tools.tools.pigean as pigean
from portal_tools.tools.cypher_utils import run_cypher
import os
from sentence_transformers import SentenceTransformer

app = Flask(__name__)
CORS(app)

# Setup in memory cache

model = SentenceTransformer('all-MiniLM-L6-v2')
print('Fetching phenotype data...')
portal_phenotypes = pigean.fetch_phenotype_data()
portal_names = [item['phenotype_name'] for item in portal_phenotypes]
portal_names_embeddings = model.encode(portal_names)
print('Done!')

@app.route('/search_phenotypes', methods=['POST'])
def search_phenotypes():
    data = request.get_json()
    search_query = data.get('query')
    if search_query is None:
        return jsonify({'error': 'Both "query" is required'}), 400
    result = pigean.search_phenotypes(search_query, portal_names_embeddings, model, portal_phenotypes)
    return jsonify({'result': result})

@app.route('/get_top_genes', methods=['POST'])
def get_top_genes():
    data = request.get_json()
    phenotype_id = data.get('phenotype_id')
    top_n = data.get('top_n', 25)
    metric = data.get('metric', 'combined')
    sigma = data.get('sigma', 2)
    geneset_size = data.get('geneset_size', 'small')
    if phenotype_id is None:
        return jsonify({'error': '"phenotype_id" is required'}), 400
    result = pigean.get_top_genes(phenotype_id, top_n, metric, sigma, geneset_size)
    return jsonify({'result': result})

@app.route('/get_factors', methods=['POST'])
def get_factors():
    data = request.get_json()
    phenotype_id = data.get('phenotype_id')
    sigma = data.get('sigma', 2)
    geneset_size = data.get('geneset_size', 'small')
    if phenotype_id is None:
        return jsonify({'error': '"phenotype_id" is required'}), 400
    result = pigean.get_factors(phenotype_id, sigma, geneset_size)
    return jsonify({'result': result})

@app.route('/get_genesets', methods=['POST'])
def get_genesets():
    data = request.get_json()
    phenotype_id = data.get('phenotype_id')
    sigma = data.get('sigma', 2)
    geneset_size = data.get('geneset_size', 'small')
    top_n = data.get('top_n', 10)
    metric = data.get('metric', 'beta')
    if phenotype_id is None:
        return jsonify({'error': '"phenotype_id" is required'}), 400
    result = pigean.get_gene_genesets(phenotype_id, sigma=sigma, geneset_size=geneset_size, top_n=top_n, metric=metric)
    return jsonify({'result': result})
    
    
@app.route('/get_cipher', methods=['POST'])
def get_cipher():
    data = request.get_json()
    cypher_query = data.get('cypher_query')
    if cypher_query is None:
        return jsonify({'error': '"cypher_query" is required'}), 400
    result = run_cypher(cypher_query=cypher_query)
    return jsonify({'result': result})
    


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5005))  # default to 5000 locally
    app.run(host="0.0.0.0", port=port)
