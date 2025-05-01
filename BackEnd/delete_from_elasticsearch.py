from elasticsearch import Elasticsearch

# Connect to Elasticsearch
client = Elasticsearch(
    "https://my-elasticsearch-project-a8f645.es.eu-west-1.aws.elastic.cloud:443",
    api_key="SnBsdWc1WUJSUHRUNXJ6SFF4NlM6eEZ5dDk0VFJFZTVHeWRKSzJzMm9mZw=="
)

# Name of the index
index_name = "search-word"

# Delete all documents from the index
response = client.delete_by_query(
    index=index_name,
    body={
        "query": {
            "match_all": {}
        }
    }
)

print("Delete response:", response)
