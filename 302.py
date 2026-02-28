def is_usual(num: int) -> bool:
    
    if num <= 0:
        return False
    

    for factor in [2, 3, 5]:
        while num % factor == 0:
            num //= factor 
            
   
    return num == 1

n = int(input())
if is_usual(n):
    print("Yes")
else:
    print("No")