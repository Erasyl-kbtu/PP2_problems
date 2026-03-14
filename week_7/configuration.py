import psycopg2
from configuration import load_config
def create_tables():
    config = load_config()
    conn = psycopg2.connect(**config)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS suppliers (
            supplier_id SERIAL PRIMARY KEY,
            supplier_name VARCHAR(255) NOT NULL,
            contact_name VARCHAR(255),
            address VARCHAR(255),
            city VARCHAR(255),
            postal_code VARCHAR(20),
            country VARCHAR(255),
            phone VARCHAR(20)
        );
    ''')
    conn.commit()
    cursor.close()
    conn.close()

if __name__ == '__main__':
    create_tables()

