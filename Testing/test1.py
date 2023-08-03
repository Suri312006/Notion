from notion.client import NotionClient

# Obtain the `token_v2` value by inspecting your browser cookies on a logged-in (non-guest) session on Notion.so
client = NotionClient(token_v2="<token_v2>")

# Access a database using the URL of the database page or the inline block
cv = client.get_collection_view("https://www.notion.so/myorg/8511b9fc522249f79b90768b832599cc?v=8dee2a54f6b64cb296c83328adba78e1")

# List all the records with "Bob" in them
for row in cv.collection.get_rows(search="Bob"):
    print("We estimate the value of '{}' at {}".format(row.name, row.estimated_value))

# Add a new record
row = cv.collection.add_row()
row.name = "Just some data"
row.is_confirmed = True
row.estimated_value = 399
row.files = ["https://www.birdlife.org/sites/default/files/styles/1600/public/slide.jpg"]
row.person = client.current_user
row.tags = ["A", "C"]
row.where_to = "https://learningequality.org"

# Run a filtered/sorted query using a view's default parameters
result = cv.default_query().execute()
for row in result:
    print(row)

# Run an "aggregation" query
aggregations = [{
    "property": "estimated_value",
    "aggregator": "sum",
    "id": "total_value",
}]
result = cv.build_query(aggregate=aggregate_params).execute()
print("Total estimated value:", result.get_aggregate("total_value"))

# Run a "filtered" query (inspect network tab in browser for examples, on queryCollection calls)
filter_params = {
    "filters": [{
        "filter": {
            "value": {
                "type": "exact",
                "value": {"table": "notion_user", "id": client.current_user.id}
            },
            "operator": "person_contains"
        },
        "property": "assigned_to"
    }],
    "operator": "and"
}
result = cv.build_query(filter=filter_params).execute()
print("Things assigned to me:", result)

# Run a "sorted" query
sort_params = [{
    "direction": "descending",
    "property": "estimated_value",
}]
result = cv.build_query(sort=sort_params).execute()
print("Sorted results, showing most valuable first:", result)