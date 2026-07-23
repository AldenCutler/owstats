import database.database as db
import sqlite3
import sqlalchemy


def main():
    conn, cursor = db.create_connection(db.DB_PATH)
    if not conn:
        print("Error! cannot create the database connection.")
        return

    db.init_db_tables(conn, cursor)
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    print("Tables in the database:")
    for table in tables:
        print(table[0])
    cursor.close()
    conn.close()


if __name__ == "__main__":
    main()