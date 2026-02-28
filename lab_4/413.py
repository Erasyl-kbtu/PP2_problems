import json
import re

def resolve_query(data, query):
    # Split into parts: keys and indices
    parts = re.findall(r'[a-zA-Z0-9_]+|\[\d+\]', query)
    current = data
    try:
        for part in parts:
            if part.startswith('[') and part.endswith(']'):
                idx = int(part[1:-1])
                if not isinstance(current, list) or idx >= len(current):
                    return "NOT_FOUND"
                current = current[idx]
            else:
                if not isinstance(current, dict) or part not in current:
                    return "NOT_FOUND"
                current = current[part]
        return json.dumps(current)
    except Exception:
        return "NOT_FOUND"

# Input
data = json.loads(input())
q = int(input())
queries = [input().strip() for _ in range(q)]

# Output
for query in queries:
    print(resolve_query(data, query))
