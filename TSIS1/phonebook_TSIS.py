import psycopg2
from psycopg2 import extras 
import os
import csv
import json
from dotenv import load_dotenv
from contextlib import closing

load_dotenv()

DATABASE_URL = os.getenv('DATABASE_URL')

def get_connection():
    return psycopg2.connect(DATABASE_URL)

# 1. Проектирование таблицы
def create_table():
    queries = """
    DROP PROCEDURE IF EXISTS upsert_contact(varchar, varchar, date, varchar, varchar, varchar);

    -- Schema creation
    CREATE TABLE IF NOT EXISTS groups (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) UNIQUE NOT NULL
);

CREATE TABLE IF NOT EXISTS contacts (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE,
    email VARCHAR(100),
    birthday DATE,
    group_id INTEGER REFERENCES groups(id) ON DELETE SET NULL,
    date_added TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS phones (
    id SERIAL PRIMARY KEY,
    contact_id INTEGER REFERENCES contacts(id) ON DELETE CASCADE,
    phone VARCHAR(20) NOT NULL,
    type VARCHAR(10) CHECK (type IN ('home', 'work', 'mobile'))
);

-- Practice 8 Procedures

-- Upsert Procedure
CREATE OR REPLACE PROCEDURE upsert_contact(
    p_name VARCHAR,
    p_email VARCHAR,
    p_birthday DATE,
    p_group_name VARCHAR,
    p_phone VARCHAR,
    p_phone_type VARCHAR
)
LANGUAGE plpgsql
AS $$
DECLARE
    v_group_id INTEGER;
    v_contact_id INTEGER;
BEGIN
    -- Handle group
    IF p_group_name IS NOT NULL THEN
        SELECT id INTO v_group_id FROM groups WHERE name = p_group_name;
        IF NOT FOUND THEN
            INSERT INTO groups (name) VALUES (p_group_name) RETURNING id INTO v_group_id;
        END IF;
    END IF;

    -- Upsert contact
    INSERT INTO contacts (name, email, birthday, group_id)
    VALUES (p_name, p_email, p_birthday, v_group_id)
    ON CONFLICT (name) DO UPDATE 
    SET email = EXCLUDED.email, 
        birthday = EXCLUDED.birthday, 
        group_id = EXCLUDED.group_id
    RETURNING id INTO v_contact_id;
    
    -- Handle phone
    IF p_phone IS NOT NULL THEN
        IF NOT EXISTS (SELECT 1 FROM phones WHERE contact_id = v_contact_id AND phone = p_phone) THEN
            INSERT INTO phones (contact_id, phone, type)
            VALUES (v_contact_id, p_phone, p_phone_type);
        END IF;
    END IF;
END;
$$;

-- Delete by Name or Phone Procedure
CREATE OR REPLACE PROCEDURE delete_contact(p_identifier VARCHAR)
LANGUAGE plpgsql
AS $$
BEGIN
    IF EXISTS (SELECT 1 FROM phones WHERE phone = p_identifier) THEN
        DELETE FROM contacts WHERE id IN (SELECT contact_id FROM phones WHERE phone = p_identifier);
    ELSE
        DELETE FROM contacts WHERE name = p_identifier;
    END IF;
END;
$$;

-- Paginated Query Function
CREATE OR REPLACE FUNCTION get_contacts_paginated(
    p_limit INTEGER,
    p_offset INTEGER,
    p_sort_col VARCHAR DEFAULT 'name'
)
RETURNS TABLE (
    contact_id INTEGER,
    name VARCHAR,
    email VARCHAR,
    birthday DATE,
    group_name VARCHAR,
    date_added TIMESTAMP
)
LANGUAGE plpgsql
AS $$
BEGIN
    -- We use dynamic SQL to allow sorting by a specified column
    RETURN QUERY EXECUTE format('
        SELECT c.id, c.name, c.email, c.birthday, g.name, c.date_added
        FROM contacts c
        LEFT JOIN groups g ON c.group_id = g.id
        ORDER BY %I
        LIMIT $1 OFFSET $2', p_sort_col)
    USING p_limit, p_offset;
END;
$$;


-- Practice 9 Procedures

-- Add Phone Procedure
CREATE OR REPLACE PROCEDURE add_phone(
    p_contact_name VARCHAR,
    p_phone VARCHAR,
    p_type VARCHAR
)
LANGUAGE plpgsql
AS $$
DECLARE
    v_contact_id INTEGER;
BEGIN
    SELECT id INTO v_contact_id FROM contacts WHERE name = p_contact_name;
    
    IF FOUND THEN
        INSERT INTO phones (contact_id, phone, type) VALUES (v_contact_id, p_phone, p_type);
    ELSE
        RAISE EXCEPTION 'Contact % not found', p_contact_name;
    END IF;
END;
$$;

-- Move to Group Procedure
CREATE OR REPLACE PROCEDURE move_to_group(
    p_contact_name VARCHAR,
    p_group_name VARCHAR
)
LANGUAGE plpgsql
AS $$
DECLARE
    v_group_id INTEGER;
BEGIN
    SELECT id INTO v_group_id FROM groups WHERE name = p_group_name;
    IF NOT FOUND THEN
        INSERT INTO groups (name) VALUES (p_group_name) RETURNING id INTO v_group_id;
    END IF;
    
    UPDATE contacts SET group_id = v_group_id WHERE name = p_contact_name;
    
    IF NOT FOUND THEN
        RAISE EXCEPTION 'Contact % not found', p_contact_name;
    END IF;
END;
$$;

-- Pattern Search Function
CREATE OR REPLACE FUNCTION search_contacts(p_query TEXT)
RETURNS TABLE (
    contact_id INTEGER,
    name VARCHAR,
    email VARCHAR,
    birthday DATE,
    group_name VARCHAR,
    phone VARCHAR,
    phone_type VARCHAR
)
LANGUAGE plpgsql
AS $$
BEGIN
    RETURN QUERY
        SELECT c.id, c.name, c.email, c.birthday, g.name, p.phone, p.type
        FROM contacts c
        LEFT JOIN groups g ON c.group_id = g.id
        LEFT JOIN phones p ON c.id = p.contact_id
        WHERE c.name ILIKE '%' || p_query || '%'
           OR c.email ILIKE '%' || p_query || '%'
           OR p.phone ILIKE '%' || p_query || '%';
END;
$$;"""

   

    with get_connection() as conn:
        with conn.cursor() as cur:
            for query in [queries]:
                cur.execute(query)
            conn.commit()
    print("Таблица готова к работе.")

def add_contact_interactive():
    name = input("Name: ")
    email = input("Email: ") or None
    birthday = input("Birthday (YYYY-MM-DD): ") or None
    group = input("Group (Family, Work, Friend, Other): ") or None
    phone = input("Phone: ") or None
    phone_type = input("Phone Type (home, work, mobile): ") or None

    with closing(get_connection()) as conn:
        with closing(conn.cursor()) as cur:
            cur.execute("CALL upsert_contact(%s, %s, %s, %s, %s, %s)", 
                        (name, email, birthday, group, phone, phone_type))
            conn.commit()
    print("Contact added/upserted successfully.")

def add_phone_interactive():
    name = input("Contact Name: ")
    phone = input("Phone: ")
    phone_type = input("Phone Type (home, work, mobile): ")

    with closing(get_connection()) as conn:
        with closing(conn.cursor()) as cur:
            try:
                cur.execute("CALL add_phone(%s, %s, %s)", (name, phone, phone_type))
                conn.commit()
                print("Phone added.")
            except Exception as e:
                print(f"Error: {e}")

def move_to_group_interactive():
    name = input("Contact Name: ")
    group = input("New Group Name: ")
    with closing(get_connection()) as conn:
        with closing(conn.cursor()) as cur:
            try:
                cur.execute("CALL move_to_group(%s, %s)", (name, group))
                conn.commit()
                print("Moved successfully.")
            except Exception as e:
                print(f"Error: {e}")

def search_contacts():
    query = input("Search query (name, email, or phone): ")
    with closing(get_connection()) as conn:
        with closing(conn.cursor()) as cur:
            cur.execute("SELECT * FROM search_contacts(%s)", (query,))
            rows = cur.fetchall()
            print("\nResults:")
            for r in rows:
                print(f"ID:{r[0]} | Name:{r[1]} | Email:{r[2]} | BDay:{r[3]} | Group:{r[4]} | Phone:{r[5]} ({r[6]})")
            print()

def filter_by_group():
    group_name = input("Group Name: ")
    with closing(get_connection()) as conn:
        with closing(conn.cursor()) as cur:
            cur.execute("""
                SELECT c.id, c.name, c.email, c.birthday, p.phone, p.type 
                FROM contacts c
                JOIN groups g ON c.group_id = g.id
                LEFT JOIN phones p ON c.id = p.contact_id
                WHERE g.name = %s
            """, (group_name,))
            rows = cur.fetchall()
            print(f"\nContacts in group '{group_name}':")
            for r in rows:
                print(r)
            print()

def view_paginated():
    sort_col = input("Sort by (name, birthday, date_added) [name]: ") or "name"
    limit = 5
    offset = 0

    with closing(get_connection()) as conn:
        with closing(conn.cursor()) as cur:
            while True:
                cur.execute("SELECT * FROM get_contacts_paginated(%s, %s, %s)", (limit, offset, sort_col))
                rows = cur.fetchall()
                if not rows:
                    print("No more records.")
                    if offset == 0:
                        break
                else:
                    print(f"\n--- Page {offset//limit + 1} ---")
                    for r in rows:
                        print(f"ID:{r[0]} | Name:{r[1]} | Email:{r[2]} | BDay:{r[3]} | Group:{r[4]} | Added:{r[5]}")

                cmd = input("\nCommands: [n]ext, [p]rev, [q]uit: ").lower()
                if cmd == 'n':
                    offset += limit
                elif cmd == 'p':
                    offset = max(0, offset - limit)
                elif cmd == 'q':
                    break

def delete_interactive():
    identifier = input("Enter Name or Phone of contact to delete: ")
    with closing(get_connection()) as conn:
        with closing(conn.cursor()) as cur:
            cur.execute("CALL delete_contact(%s)", (identifier,))
            conn.commit()
    print("Deleted successfully (if it existed).")

def export_json():
    filename = input("Filename to export to [contacts.json]: ") or "contacts.json"
    with closing(get_connection()) as conn:
        with closing(conn.cursor()) as cur:
            cur.execute("""
                SELECT c.name, c.email, TO_CHAR(c.birthday, 'YYYY-MM-DD'), g.name,
                       json_agg(json_build_object('phone', p.phone, 'type', p.type)) FILTER (WHERE p.phone IS NOT NULL) as phones
                FROM contacts c
                LEFT JOIN groups g ON c.group_id = g.id
                LEFT JOIN phones p ON c.id = p.contact_id
                GROUP BY c.id, c.name, c.email, c.birthday, g.name
            """)
            rows = cur.fetchall()
            data = []
            for r in rows:
                data.append({
                    "name": r[0],
                    "email": r[1],
                    "birthday": r[2],
                    "group": r[3],
                    "phones": r[4] or []
                })
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)
    print(f"Exported to {filename}")

def import_json():
    filename = input("Filename to import from [contacts.json]: ") or "contacts.json"
    try:
        with open(filename, 'r') as f:
            data = json.load(f)
    except Exception as e:
        print(f"Error opening file: {e}")
        return

    with closing(get_connection()) as conn:
        with closing(conn.cursor()) as cur:
            for item in data:
                name = item.get("name")
                email = item.get("email")
                birthday = item.get("birthday")
                group = item.get("group")
                phones = item.get("phones", [])
                
                # Check for existing
                cur.execute("SELECT id FROM contacts WHERE name = %s", (name,))
                if cur.fetchone():
                    choice = input(f"Contact {name} already exists. [s]kip or [o]verwrite? ").lower()
                    if choice == 's':
                        continue
                
                if not phones:
                    cur.execute("CALL upsert_contact(%s, %s, %s, %s, %s, %s)", 
                                (name, email, birthday, group, None, None))
                else:
                    first_phone = phones[0]
                    cur.execute("CALL upsert_contact(%s, %s, %s, %s, %s, %s)", 
                                (name, email, birthday, group, first_phone.get("phone"), first_phone.get("type")))
                    for p in phones[1:]:
                        cur.execute("CALL add_phone(%s, %s, %s)", (name, p.get("phone"), p.get("type")))
            conn.commit()
    print("Import completed.")

def import_csv():
    filename = input("Filename to import from [contacts.csv]: ") or "contacts.csv"
    try:
        with open(filename, 'r') as f:
            reader = csv.DictReader(f)
            with closing(get_connection()) as conn:
                with closing(conn.cursor()) as cur:
                    for row in reader:
                        cur.execute("CALL upsert_contact(%s, %s, %s, %s, %s, %s)",
                                    (row.get('name'), row.get('email'), row.get('birthday') or None, 
                                     row.get('group'), row.get('phone'), row.get('phone_type')))
                    conn.commit()
        print("CSV imported successfully.")
    except Exception as e:
        print(f"Error: {e}")

def main():
    while True:
        print("\n=== PhoneBook ===")
        print("1. Add/Upsert Contact")
        print("2. Add Phone to Contact")
        print("3. Move Contact to Group")
        print("4. Search Contacts (Pattern/Email)")
        print("5. Filter by Group")
        print("6. View Contacts (Paginated)")
        print("7. Delete Contact")
        print("8. Export to JSON")
        print("9. Import from JSON")
        print("10. Import from CSV")
        print("0. Exit")
        
        choice = input("Enter choice: ")
        
        try:
            if choice == '1': add_contact_interactive()
            elif choice == '2': add_phone_interactive()
            elif choice == '3': move_to_group_interactive()
            elif choice == '4': search_contacts()
            elif choice == '5': filter_by_group()
            elif choice == '6': view_paginated()
            elif choice == '7': delete_interactive()
            elif choice == '8': export_json()
            elif choice == '9': import_json()
            elif choice == '10': import_csv()
            elif choice == '0': break
            else: print("Invalid choice")
        except psycopg2.Error as e:
            print(f"Database error: {e}")
        except Exception as e:
            print(f"Unexpected error: {e}")

if __name__ == "__main__":
    create_table()
    main()