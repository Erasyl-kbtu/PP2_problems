class StringHandler:
    def __init__(self):
        self.s = ""

    def getString(self):
        # Принимает строку из консоли
        self.s = input()

    def printString(self):
        # Выводит строку в верхнем регистре
        print(self.s.upper())

# Пример использования:
handler = StringHandler()
handler.getString()
handler.printString()