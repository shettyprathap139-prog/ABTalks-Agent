from app.services.breeth_memory import record_fact, search_memory


record_fact(
    "Alex",
    "publishes",
    "important AI security developments"
)

record_fact(
    "Alex",
    "avoids",
    "previously published topics"
)


print("Searching Breeth...")

results = search_memory(
    "What does Alex publish?",
    limit=5
)

print("Search result:")
print(results)