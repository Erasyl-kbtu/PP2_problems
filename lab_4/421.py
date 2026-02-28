import importlib
import sys

def solve():
    line = sys.stdin.readline().strip()
    if not line:
        return
    
    try:
        q = int(line)
        for _ in range(q):
            query = sys.stdin.readline().split()
            if len(query) < 2:
                continue
            
            module_path, attr_name = query[0], query[1]
            
            try:
                module = importlib.import_module(module_path)
                if hasattr(module, attr_name):
                    attr = getattr(module, attr_name)

                    if callable(attr):
                        print("CALLABLE")
                    else:
                        print("VALUE")
                else:
                    print("ATTRIBUTE_NOT_FOUND")
                    
            except ImportError:
                print("MODULE_NOT_FOUND")
                
    except ValueError:
        pass

solve()