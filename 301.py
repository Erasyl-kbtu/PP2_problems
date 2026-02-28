def is_valid(n):
    n = abs(n)
    if n == 0: return "Valid"
    
    while n > 0:
        if (n % 10) % 2 != 0:
            return "Not valid"
        n //= 10  
    return "Valid"

n = int(input())
print(is_valid(n))