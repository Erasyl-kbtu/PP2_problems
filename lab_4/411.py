import json

def apply_patch(source, patch):
    for key, value in patch.items():
        if value is None:
            source.pop(key, None)
        elif isinstance(value, dict) and isinstance(source.get(key), dict):
            source[key] = apply_patch(source.get(key, {}), value)
        else:
            source[key] = value
    return source

source = json.loads(input())
patch = json.loads(input())

result = apply_patch(source, patch)

print(json.dumps(result, sort_keys=True, separators = (",", ":")))