# Ввод количества переменных
n = int(input("Enter the number of variables (max 26): "))
rows = 2 ** n

# Генерация списка переменных
variables = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'[:n]

# Ввод таблицы истинности
print("Enter the truth table rows (space-separated values):")
table = [list(map(int, input().split())) for _ in range(rows)]

# Генерация ДНФ
dnf_parts = []
for row in table:
    if row[-1] == 1:
        # Создаем коньюнкцию
        conj = [variables[i] if row[i] else f"¬{variables[i]}" for i in range(n)]
        dnf_parts.append(f"({' ∧ '.join(conj)})")

# Обьединяем в дизьюнкцию
dnf_result = " ∨ ".join(dnf_parts) if dnf_parts else "0"

print("Result:")
print(dnf_result)
