class Shape:
    def area(self):
        return 0

class Square(Shape):
    def __init__(self, length):
        self.length = length

    def area(self):
        return self.length ** 2

if __name__ == "__main__":
    try:
        n = int(input())
        
        square_obj = Square(n)
        
        print(square_obj.area())
    except ValueError:
        pass