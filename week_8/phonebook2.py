import os
import csv
import psycopg2
from psycopg2 import extras
from dotenv import load_dotenv

load_dotenv()
DATABASE_URL = os.getenv('DATABASE_URL')

def get_connection():
    return psycopg2.connect(DATABASE_URL)

def create_table():
    query = """
    CREATE TABLE IF NOT EXISTS phonebook (
        id SERIAL PRIMARY KEY,
        username VARCHAR(50) UNIQUE NOT NULL,
        first_name VARCHAR(100) NOT NULL,
        phone_number VARCHAR(20) NOT NULL
    );"""
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(query)
        conn.commit()
    print("База данных готова к работе.")

# 1. Поиск (Функция search_phonebook)
def search_contacts():
    pattern = input("Введите текст для поиска (имя или номер): ")
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM search_phonebook(%s)", (pattern,))
            print(f"\n{'ID':<5} | {'User':<15} | {'Name':<15} | {'Phone':<15}")
            print("-" * 55)
            for row in cur:
                print(f"{row[0]:<5} | {row[1]:<15} | {row[2]:<15} | {row[3]:<15}")

# 2. Добавление/Обновление (Процедура upsert_user)
def update_contact():
    user = input("Username: ")
    name = input("Имя: ")
    phone = input("Телефон: ")
    phones_str = "{" + ",".join(phone) + "}"
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
    "SELECT * FROM insert_many_users(%s::text[], %s::text[], %s::text[])", 
    (user, name, phones_str)
)
        conn.commit()
    print("Контакт сохранен.")

# 3. Массовая вставка (Функция insert_many_users)
def insert_from_csv(filename):
    filename = input("Введите имя CSV файла (например, contacts.csv): ") or "contacts.csv"
    if not os.path.exists(filename):
        print("Файл не найден.")
        return

    users, names, phones = [], [], []
    with open(filename, mode='r', encoding='utf-8') as f:
        reader = csv.reader(f)
        next(reader)  # Пропускаем заголовок
        for row in reader:
            if len(row) == 3:
                users.append(row[0]); names.append(row[1]); phones.append(row[2])

    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM insert_many_users(%s, %s, %s)", (users, names, phones))
            errors = cur.fetchall()
            if errors:
                print("\nномер должен быть 11 цифр:")
                for err in errors:
                    print(f"- {err[0]}: {err[1]}")
            else:
                print("Все данные успешно загружены.")
        conn.commit()

# 4. Пагинация (Функция get_phonebook_paginated)
def action_paginate():
    try:
        limit = int(input("Сколько строк вывести? "))
        offset = int(input("Сколько строк пропустить? "))
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT * FROM get_phonebook_paginated(%s, %s)", (limit, offset))
                print(f"\n{'ID':<5} | {'Name':<20} | {'Phone':<15}")
                for row in cur:
                    print(f"{row[0]:<5} | {row[1]:<20} | {row[2]:<15}")
    except ValueError:
        print("Введите корректные числа.")

# 5. Удаление (Процедура delete_entry)
def delete_contact():
    target = input("Введите username или телефон для удаления: ")
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("CALL delete_entry(%s)", (target,))
        conn.commit()
    print(f"Запрос на удаление '{target}' выполнен.")

# Главное меню
def main():
    create_table()
    while True:
        print("\n--- PHONEBOOK MENU ---")
        print("1. Загрузить из CSV")
        print("2. Вывести страницу контактов")
        print("3. Добавить илиОбновить контакт")
        print("4. Поиск")
        print("5. Удалить")
        print("0. Выход")
        
        a = input("Выберите действие:(номер) ")
        if a == '1': insert_from_csv('contacts.csv')
        elif a == '2': action_paginate()
        elif a == '3': update_contact()
        elif a == '4': search_contacts()
        elif a == '5': delete_contact()
        elif a == '0': break
        else: print("Неверная команда.")

if __name__ == "__main__":
    main()