import psycopg2
from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_URL = os.getenv('DATABASE_URL')

def get_connection():
    return psycopg2.connect(DATABASE_URL)


def create_table():
    conn = get_connection()
    if not conn:
        return
    try:
        cur = conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS players (
                id SERIAL PRIMARY KEY,
                username VARCHAR(50) UNIQUE NOT NULL
            );
        """)
        cur.execute("""
            CREATE TABLE IF NOT EXISTS game_sessions (
                id SERIAL PRIMARY KEY,
                player_id INTEGER REFERENCES players(id),
                score INTEGER NOT NULL,
                level_reached INTEGER NOT NULL,
                played_at TIMESTAMP DEFAULT NOW()
            );
        """)
        conn.commit()
        cur.close()
    except Exception as e:
        print(f"Error creating tables: {e}")
    finally:
        conn.close()
        
def save_score(username, score, level):
    conn = get_connection()
    if not conn:
        return
    try:
        cur = conn.cursor()
        # Ищем или создаем игрока
        cur.execute("SELECT id FROM players WHERE username = %s;", (username,))
        result = cur.fetchone()
        
        if result:
            player_id = result[0]
        else:
            cur.execute("INSERT INTO players (username) VALUES (%s) RETURNING id;", (username,))
            player_id = cur.fetchone()[0]
            
        cur.execute("""
            INSERT INTO game_sessions (player_id, score, level_reached)
            VALUES (%s, %s, %s);
        """, (player_id, score, level))
        conn.commit()
        cur.close()
    except Exception as e:
        print(f"Error saving score: {e}")
    finally:
        conn.close()

def get_top_scores():
    conn = get_connection()
    if not conn:
        return []
    try:
        cur = conn.cursor()
        cur.execute("""
            SELECT p.username, g.score, g.level_reached, g.played_at
            FROM game_sessions g
            JOIN players p ON p.id = g.player_id
            ORDER BY g.score DESC
            LIMIT 10;
        """)
        results = cur.fetchall()
        cur.close()
        return results
    except Exception as e:
        print(f"Error fetching top scores: {e}")
        return []
    finally:
        conn.close()

def get_personal_best(username):
    conn = get_connection()
    if not conn:
        return 0
    try:
        cur = conn.cursor()
        cur.execute("""
            SELECT MAX(g.score)
            FROM game_sessions g
            JOIN players p ON p.id = g.player_id
            WHERE p.username = %s;
        """, (username,))
        result = cur.fetchone()
        cur.close()
        return result[0] if result and result[0] is not None else 0
    except Exception as e:
        print(f"Error fetching personal best: {e}")
        return 0
    finally:
        conn.close()
def init_db():
    conn = get_connection()
    if not conn:
        return
    try:
        cur = conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS players (
                id SERIAL PRIMARY KEY,
                username VARCHAR(50) UNIQUE NOT NULL
            );
        """)
        cur.execute("""
            CREATE TABLE IF NOT EXISTS game_sessions (
                id SERIAL PRIMARY KEY,
                player_id INTEGER REFERENCES players(id),
                score INTEGER NOT NULL,
                level_reached INTEGER NOT NULL,
                played_at TIMESTAMP DEFAULT NOW()
            );
        """)
        conn.commit()
        cur.close()
    except Exception as e:
        print(f"Error initializing DB: {e}")
    finally:
        conn.close()

def save_score(username, score, level):
    conn = get_connection()
    if not conn:
        return
    try:
        cur = conn.cursor()
        # Ищем или создаем игрока
        cur.execute("SELECT id FROM players WHERE username = %s;", (username,))
        result = cur.fetchone()
        
        if result:
            player_id = result[0]
        else:
            cur.execute("INSERT INTO players (username) VALUES (%s) RETURNING id;", (username,))
            player_id = cur.fetchone()[0]
            
        cur.execute("""
            INSERT INTO game_sessions (player_id, score, level_reached)
            VALUES (%s, %s, %s);
        """, (player_id, score, level))
        conn.commit()
        cur.close()
    except Exception as e:
        print(f"Error saving score: {e}")
    finally:
        conn.close()

def get_top_scores():
    conn = get_connection()
    if not conn:
        return []
    try:
        cur = conn.cursor()
        cur.execute("""
            SELECT p.username, g.score, g.level_reached, g.played_at
            FROM game_sessions g
            JOIN players p ON p.id = g.player_id
            ORDER BY g.score DESC
            LIMIT 10;
        """)
        results = cur.fetchall()
        cur.close()
        return results
    except Exception as e:
        print(f"Error fetching top scores: {e}")
        return []
    finally:
        conn.close()

def get_personal_best(username):
    conn = get_connection()
    if not conn:
        return 0
    try:
        cur = conn.cursor()
        cur.execute("""
            SELECT MAX(g.score)
            FROM game_sessions g
            JOIN players p ON p.id = g.player_id
            WHERE p.username = %s;
        """, (username,))
        result = cur.fetchone()
        cur.close()
        return result[0] if result and result[0] is not None else 0
    except Exception as e:
        print(f"Error fetching personal best: {e}")
        return 0
    finally:
        conn.close()