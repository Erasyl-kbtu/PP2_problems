def solve_303():
    # Словарь соответствия кодов цифрам
    code_to_digit = {
        'ZER': '0', 'ONE': '1', 'TWO': '2', 'THR': '3', 'FOU': '4',
        'FIV': '5', 'SIX': '6', 'SEV': '7', 'EIG': '8', 'NIN': '9'
    }

    digit_to_code = {v: k for k, v in code_to_digit.items()}
    
    try:
        s = input().strip()
    except EOFError:
        return

    # 1. Находим оператор и разделяем строку на два числа
    operator = None
    for op in ['+', '-', '*']:
        if op in s:
            operator = op
            parts = s.split(op)
            break
    
    if not operator:
        return

    # 2. Функция для конвертации строки триплетов в число (int)
    def decode_string(code_str):
        digits = ""
        for i in range(0, len(code_str), 3):
            triplet = code_str[i:i+3]
            digits += code_to_digit[triplet]
        return int(digits)

    num1 = decode_string(parts[0])
    num2 = decode_string(parts[1])

    # 3. Выполняем арифметическое действие
    if operator == '+':
        result = num1 + num2
    elif operator == '-':
        result = num1 - num2
    else:
        result = num1 * num2

    # 4. Конвертируем результат обратно в буквенные триплеты
    res_str = str(result)
    final_output = ""
    
    for char in res_str:
        if char == '-':
            final_output += "-" 
        else:
            final_output += digit_to_code[char]
            
    print(final_output)

solve_303()