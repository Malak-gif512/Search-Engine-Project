from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from elasticsearch import Elasticsearch
import requests
import re
import uvicorn
import os

app = FastAPI()

# Enable CORS so the frontend can talk to this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)

# Connect to your Elasticsearch cluster
es = Elasticsearch(
    "https://my-elasticsearch-project-a8f645.es.eu-west-1.aws.elastic.cloud:443",
    api_key="SnBsdWc1WUJSUHRUNXJ6SFF4NlM6eEZ5dDk0VFJFZTVHeWRKSzJzMm9mZw=="
)

index_name = "search-word"

# Search endpoint to get URLs and counts for a given word
@app.get("/search")
def search(q: str = Query(..., min_length=1)):
    response = es.search(
        index=index_name,
        body={
            "query": {
                "match": {
                    "word": q  # Match the given word
                }
            },
            "size": 5  # We assume one document per word
        }
    )

    hits = response.get("hits", {}).get("hits", [])
    if not hits:
        return {"results": []}

    # Get the list of URLs and counts
    occurrences = hits[0]["_source"].get("occurrences", [])
    return {"results": occurrences}

# Endpoint to fetch a webpage and highlight the searched word
@app.get("/fetch_page", response_class=HTMLResponse)
def fetch_page(url: str, q: str):
    try:
        response = requests.get(url)
        html = response.text

        # Highlight the searched word (case-insensitive) using <mark> tag
        highlighted = re.sub(
            f'({re.escape(q)})',
            r"<mark style='background: yellow'>\1</mark>",
            html,
            flags=re.IGNORECASE
        )

        # Highlight each word in the phrase separately, ensuring it is not already highlighted
        if len(q.split()) > 1:
            for word in q.split():
                # Use a lookahead/lookbehind to ensure the word is not inside a <mark> tag
                highlighted = re.sub(
                    f"(?<!<mark style='background: yellow'>)({re.escape(word)})(?!</mark>)",
                    r"<mark style='background: orange'>\1</mark>",
                    highlighted,
                    flags=re.IGNORECASE
                )


        count = len(re.findall(f'({re.escape(q)})', html, flags=re.IGNORECASE))
        print(f"Occurrences found before highlighting: {count}")


        return highlighted

    except Exception as e:
        return HTMLResponse(f"<h2>Error loading page</h2><p>{e}</p>", status_code=500)

    # cd OneDrive\Desktop\BDProject\new
    # uvicorn main_fastapi:app --reload

    if __name__ == "__main__":
        port = int(os.environ.get("PORT", 8000))
        uvicorn.run(app, host="0.0.0.0", port=port)
