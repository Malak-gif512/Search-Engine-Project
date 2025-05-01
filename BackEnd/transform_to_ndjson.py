import json

# Input and output file paths
input_file = "out-search.txt"
output_file = "search_word_bulk.ndjson"

ndjson_lines = []

# Read and parse each line
with open(input_file, "r", encoding="utf-8") as file:
    for line in file:
        if '\t' not in line:
            continue
        word, urls = line.strip().split('\t', 1)
        occurrences = []

        for part in urls.split(';'):
            part = part.strip()
            if '|' in part:
                url, count = part.rsplit('|', 1)
                try:
                    occurrences.append({"url": url, "count": int(count)})
                except ValueError:
                    continue

        if occurrences:
            # Elasticsearch bulk index header
            ndjson_lines.append(json.dumps({ "index": { "_index": "search-word" } }))
            # Actual document
            ndjson_lines.append(json.dumps({ "word": word, "occurrences": occurrences }))

# Write the NDJSON lines to the output file
with open(output_file, "w", encoding="utf-8") as out_file:
    out_file.write('\n'.join(ndjson_lines) + '\n')

print(f"✅ NDJSON file created: {output_file}")
