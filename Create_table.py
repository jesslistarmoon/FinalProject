import sqlite3

def create_tables():
    conn = sqlite3.connect("FinalProjectDB.db")
    cur = conn.cursor()

    # Create tables
    cur.execute("""
    CREATE TABLE IF NOT EXISTS boroughs (
        id INTEGER UNIQUE,
        borough_name TEXT NOT NULL,
        PRIMARY KEY(id AUTOINCREMENT)
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS borough_population (
        id INTEGER UNIQUE,
        population INTEGER NOT NULL,
        PRIMARY KEY(id),
        FOREIGN KEY(id) REFERENCES boroughs(id)
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS collisions (
        id INTEGER NOT NULL UNIQUE,
        zipcode_id INTEGER NOT NULL,
        borough_id INTEGER NOT NULL,
        PRIMARY KEY(id),
        FOREIGN KEY(borough_id) REFERENCES boroughs(id)
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS parks (
        id TEXT NOT NULL UNIQUE,
        borough_id INTEGER,
        PRIMARY KEY(id),
        FOREIGN KEY(borough_id) REFERENCES boroughs(id)
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS properties (
        id TEXT NOT NULL UNIQUE,
        market_value INTEGER NOT NULL,
        borough_id INTEGER NOT NULL,
        zipcode_id INTEGER NOT NULL,
        PRIMARY KEY(id),
        FOREIGN KEY(borough_id) REFERENCES boroughs(id)
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS zipcodes (
        id INTEGER UNIQUE,
        zipcode INTEGER NOT NULL,
        PRIMARY KEY(id AUTOINCREMENT)
    )
    """)

    conn.commit()
    conn.close()
    print("Database and tables created successfully.")

if __name__ == "__main__":
    create_tables()
