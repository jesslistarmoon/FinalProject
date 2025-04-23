import sqlite3

DB_PATH = "./FinalProjectDB.db"

def create_tables():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    tables = {
        "borough_population": """
            CREATE TABLE "borough_population" (
                "id"	INTEGER UNIQUE,
                "population"	INTEGER NOT NULL,
                PRIMARY KEY("id"),
                FOREIGN KEY("id") REFERENCES "boroughs"("id")
            )
            """,
        "boroughs": """
            CREATE TABLE "boroughs" (
                "id"	INTEGER UNIQUE,
                "borough_name"	TEXT NOT NULL,
                PRIMARY KEY("id" AUTOINCREMENT)
            )
            """,
        "collisions": """
            CREATE TABLE "collisions" (
                "id"	INTEGER NOT NULL UNIQUE,
                "zipcode_id"	INTEGER NOT NULL,
                "borough_id"	INTEGER NOT NULL,
                PRIMARY KEY("id"),
                FOREIGN KEY("borough_id") REFERENCES "boroughs"("id"),
                FOREIGN KEY("zipcode_id") REFERENCES "zipcodes"("id")
            )
            """,
        "parks": """
            CREATE TABLE "parks" (
                "id"	TEXT NOT NULL UNIQUE,
                "borough_id"	INTEGER,
                PRIMARY KEY("id")
            )
            """,
        "properties": """
            CREATE TABLE "properties" (
                "id"	TEXT NOT NULL UNIQUE,
                "market_value"	INTEGER NOT NULL,
                "borough_id"	INTEGER NOT NULL,
                "zipcode_id"	INTEGER NOT NULL,
                PRIMARY KEY("id"),
                FOREIGN KEY("borough_id") REFERENCES "boroughs"("id"),
                FOREIGN KEY("zipcode_id") REFERENCES "zipcodes"("id")
            )
            """,
        "zipcodes": """
            CREATE TABLE "zipcodes" (
                "id"	INTEGER UNIQUE,
                "zipcode"	INTEGER NOT NULL,
                PRIMARY KEY("id" AUTOINCREMENT)
            )
            """
    }

    for table, create_query in tables.items():
        cursor.execute("""
            SELECT name FROM sqlite_master 
            WHERE type='table' AND name=?
            """,
            (table,)
        )
        if cursor.fetchone() is None:
            print("Creating", table, "...")
            cursor.execute(create_query)
        else:
            print(table, "already exists")

    return

if __name__ == "__main__":
    create_tables()
