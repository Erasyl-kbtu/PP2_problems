import re
import json

def parse_receipt_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Извлекаем дату и время
    datetime_pattern = r'Время:\s*(\d{2}\.\d{2}\.\d{4})\s*(\d{2}:\d{2}:\d{2})'
    dt_match = re.search(datetime_pattern, content)
    date = dt_match.group(1) if dt_match else None
    time = dt_match.group(2) if dt_match else None

    # 2. Извлекаем метод оплаты
    payment_method = "Банковская карта" if "Банковская карта" in content else "Наличные"

    # 3. Извлекаем названия товаров и цены
    item_pattern = r'\d+\.\n(.*?)\n\d+,\d+ x ([\d\s,]+)\n'
    items_raw = re.findall(item_pattern, content)

    products = []

    for name, price_str in items_raw:
        # Очищаем цену от пробелов и меняем запятую на точку для float
        clean_price = float(price_str.replace(' ', '').replace(',', '.'))
        
        products.append({
            "product_name": name.strip(),
            "price_per_unit": clean_price
        })

    # 4. Извлекаем итоговую сумму (ИТОГО:)
    total_pattern = r'ИТОГО:\s*([\d\s,]+)'
    total_match = re.search(total_pattern, content)
    total_amount = float(total_match.group(1).replace(' ', '').replace(',', '.')) if total_match else 0.0

    # Формируем результат
    receipt_data = {
        "metadata": {
            "date": date,
            "time": time,
            "payment_method": payment_method,
            "location": "Нур-Султан, Казахстан"
        },
        "items": products,
        "total_amount": total_amount
    }

    return receipt_data

result = parse_receipt_file('raw.txt')
print(json.dumps(result, indent=4, ensure_ascii=False))