from elasticsearch import Elasticsearch, helpers
import json

# Connect to Elasticsearch (Elastic Cloud)
base_client = Elasticsearch(
    "https://my-elasticsearch-project-a8f645.es.eu-west-1.aws.elastic.cloud:443",
    api_key="SnBsdWc1WUJSUHRUNXJ6SFF4NlM6eEZ5dDk0VFJFZTVHeWRKSzJzMm9mZw=="
)

# Add timeout and retry settings using `.options()`
client = base_client.options(request_timeout=120, max_retries=5)

# Index name and file path
index_name = "search-word"
ndjson_path = "C:/Users/Abo_Elalaa/OneDrive/Desktop/BDProject/finish/Search Engine Project/final_edit_bulk.ndjson"

# Generator to read documents line by line
def generate_actions(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            if line.strip():
                doc = json.loads(line)
                yield {
                    "_index": index_name,
                    "_source": doc
                }

# Upload documents in bulk
try:
    success, _ = helpers.bulk(
        client,
        generate_actions(ndjson_path),
        chunk_size=200  # Adjust chunk size as needed
    )
    print(f"Successfully uploaded {success} documents.")
except Exception as e:
    print("Error during bulk upload:", e)
