from elasticsearch import Elasticsearch, helpers
import json

# Connect to Elasticsearch
client = Elasticsearch(
    "https://my-elasticsearch-project-a8f645.es.eu-west-1.aws.elastic.cloud:443",
    api_key="SnBsdWc1WUJSUHRUNXJ6SFF4NlM6eEZ5dDk0VFJFZTVHeWRKSzJzMm9mZw=="
)

index_name = "search-word"
ndjson_path = "search_word_bulk.ndjson"

# Read .ndjson file and prepare actions
actions = []
with open(ndjson_path, 'r', encoding='utf-8') as f:
    for line in f:
        if line.strip():
            doc = json.loads(line)
            actions.append({
                "_index": index_name,
                "_source": doc
            })

# Upload documents in bulk
response = helpers.bulk(client, actions)
print("Bulk insert response:", response)
