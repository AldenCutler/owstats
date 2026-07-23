import sqlite3
import sqlalchemy


DB_PATH = "/home/alden/Projects/OWStats/data/owstats.db"

def create_connection(db_file):
    """ create a database connection to a SQLite database """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()
        print("Connection is established: Database is created in memory")
    except sqlite3.Error as e:
        print(e)
    return conn, cursor

def init_db_tables(conn, cursor):
    """Initialize the database by creating necessary tables."""
    if conn:
        # Matches
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Match (
                id INTEGER PRIMARY KEY,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                map TEXT NOT NULL,
                mode TEXT NOT NULL,
                result TEXT NOT NULL,
                duration INTEGER NOT NULL
            )
        ''')
        # PlayerPerformances (one row per player per match)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS PlayerPerformance (
                id INTEGER PRIMARY KEY,
                player_id INTEGER NOT NULL,
                match_id INTEGER NOT NULL,
                kills INTEGER DEFAULT 0,
                deaths INTEGER DEFAULT 0,
                assists INTEGER DEFAULT 0,
                damage_dealt INTEGER DEFAULT 0,
                damage_taken INTEGER DEFAULT 0,
                healing_done INTEGER DEFAULT 0,
                hero TEXT NOT NULL,
                FOREIGN KEY (player_id) REFERENCES Player (id),
                FOREIGN KEY (match_id) REFERENCES Match (id)
            )
        ''')
        # Players
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Player (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL
            )
        ''')
        conn.commit()
        print("Database initialized with necessary tables.")