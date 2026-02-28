import json

def deep_diff(a, b, path=""):
    diffs = []
    keys = set(a.keys()) | set(b.keys())
    for key in sorted(keys):
        new_path = f"{path}.{key}" if path else key
        if key not in a:
            diffs.append(f"{new_path} : <missing> -> {json.dumps(b[key])}")
        elif key not in b:
            diffs.append(f"{new_path} : {json.dumps(a[key])} -> <missing>")
        else:
            val_a, val_b = a[key], b[key]
            if isinstance(val_a, dict) and isinstance(val_b, dict):
                diffs.extend(deep_diff(val_a, val_b, new_path))
            elif val_a != val_b:
                diffs.append(f"{new_path} : {json.dumps(val_a)} -> {json.dumps(val_b)}")
    return diffs

a = json.loads(input())
b = json.loads(input())

diffs = deep_diff(a, b)

if diffs:
    for d in diffs:
        print(d)
else:
    print("No differences")
