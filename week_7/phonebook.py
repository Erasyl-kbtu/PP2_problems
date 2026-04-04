import os
import psycopg2
import csv
from dotenv import load_dotenv

# Загружаем переменные из .env
load_dotenv()
DATABASE_URL = os.getenv('DATABASE_URL')

def get_connection():
    return psycopg2.connect(DATABASE_URL)

# 1. Проектирование таблицы
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
    print("Таблица готова к работе.")

# 2. Вставка данных из CSV
def insert_from_csv(file_path):
    # Формат CSV должен быть: username,first_name,phone_number
    try:
        file_path = input("Введите путь к CSV файлу (или нажмите Enter для contacts.csv): ")
        if not file_path:
            file_path = "contacts.csv"
        with open(file_path, mode='r', encoding='utf-8') as f:
            reader = csv.reader(f)
            next(reader)
            with get_connection() as conn:
                with conn.cursor() as cur:
                    for row in reader:
                        cur.execute(
                            "INSERT INTO phonebook (username, first_name, phone_number) VALUES (%s, %s, %s) ON CONFLICT (username) DO NOTHING",
                            (row[0], row[1], row[2])
                        )
                conn.commit()
        print(f"Данные из {file_path} успешно загружены.")
    except FileNotFoundError:
        print("Файл CSV не найден.")

# 3. Вставка данных из консоли
def insert_manual():
    username = input("Введите username: ")
    first_name = input("Введите имя: ")
    phone = input("Введите номер телефона: ")
    
    query = "INSERT INTO phonebook (username, first_name, phone_number) VALUES (%s, %s, %s)"
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(query, (username, first_name, phone))
            conn.commit()
        print("Контакт успешно добавлен.")
    except Exception as e:
        print(f"Ошибка: {e}")

# 4. Обновление имени или телефона
def update_contact():
    username = input("Введите username контакта для обновления: ")
    print("Что вы хотите изменить? 1 - Имя, 2 - Телефон")
    choice = input("> ")
    
    if choice == '1':
        new_val = input("Новое имя: ")
        query = "UPDATE phonebook SET first_name = %s WHERE username = %s"
    else:
        new_val = input("Новый телефон: ")
        query = "UPDATE phonebook SET phone_number = %s WHERE username = %s"
        
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(query, (new_val, username))
        conn.commit()
    print("Данные обновлены.")

# 5. Поиск с фильтрами
def search_contacts():
    print("Поиск по: 1 - Имени, 2 - телефону")
    choice = input("> ")
    search_term = input("Введите значение для поиска: ")
    
    if choice == '1':
        query = "SELECT * FROM phonebook WHERE first_name ILIKE %s"
        param = f"%{search_term}%"
    else:
        query = "SELECT * FROM phonebook WHERE phone_number LIKE %s"
        param = f"{search_term}%"
        
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(query, (param,))
            results = cur.fetchall()
            for row in results:
                print(f"User: {row[1]} | Name: {row[2]} | Phone: {row[3]}")

# 6. Удаление контакта
def delete_contact():
    target = input("Введите username или номер телефона для удаления: ")
    query = "DELETE FROM phonebook WHERE username = %s OR phone_number = %s"
    
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(query, (target, target))
        conn.commit()
    print("Контакт удален (если он существовал).")

# Главное меню
def main():
    create_table()
    while True:
        print("\n--- PHONEBOOK MENU ---")
        print("1. Загрузить из CSV")
        print("2. Добавить вручную")
        print("3. Обновить контакт")
        print("4. Поиск")
        print("5. Удалить")
        print("0. Выход")
        
        cmd = input("Выберите действие:(номер) ")
        if cmd == '1': insert_from_csv('contacts.csv')
        elif cmd == '2': insert_manual()
        elif cmd == '3': update_contact()
        elif cmd == '4': search_contacts()
        elif cmd == '5': delete_contact()
        elif cmd == '0': break
        else: print("Неверная команда.")

if __name__ == "__main__":
    main()

