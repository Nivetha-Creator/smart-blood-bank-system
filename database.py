import sqlite3

DATABASE = "blood_bank.db"


def get_connection():
    connection = sqlite3.connect(DATABASE)
    connection.row_factory = sqlite3.Row
    return connection


def initialize_database():
    connection = get_connection()
    cursor = connection.cursor()

    # --------------------------------
    # BLOOD BANKS TABLE
    # --------------------------------

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS blood_banks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            location TEXT NOT NULL,
            contact TEXT,
            latitude REAL,
            longitude REAL
        )
    """)

    # --------------------------------
    # DATABASE MIGRATION
    # --------------------------------
    # Adds latitude and longitude to an
    # existing database created earlier.

    cursor.execute("PRAGMA table_info(blood_banks)")

    columns = [
        row["name"]
        for row in cursor.fetchall()
    ]

    if "latitude" not in columns:
        cursor.execute("""
            ALTER TABLE blood_banks
            ADD COLUMN latitude REAL
        """)

    if "longitude" not in columns:
        cursor.execute("""
            ALTER TABLE blood_banks
            ADD COLUMN longitude REAL
        """)

    # --------------------------------
    # INVENTORY TABLE
    # --------------------------------

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS inventory (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            blood_bank_id INTEGER NOT NULL,
            blood_group TEXT NOT NULL,
            units INTEGER NOT NULL DEFAULT 0,
            expiry_date TEXT NOT NULL,
            FOREIGN KEY (blood_bank_id)
            REFERENCES blood_banks(id)
        )
    """)

    # --------------------------------
    # BLOOD REQUESTS TABLE
    # --------------------------------

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS blood_requests (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            hospital_name TEXT NOT NULL,
            blood_group TEXT NOT NULL,
            units_required INTEGER NOT NULL,
            urgency TEXT NOT NULL,
            location TEXT NOT NULL,
            status TEXT NOT NULL DEFAULT 'PENDING',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # --------------------------------
    # ALLOCATIONS TABLE
    # --------------------------------

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS allocations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            request_id INTEGER NOT NULL,
            blood_bank_id INTEGER NOT NULL,
            blood_group TEXT NOT NULL,
            units_allocated INTEGER NOT NULL,
            allocated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (request_id)
            REFERENCES blood_requests(id),
            FOREIGN KEY (blood_bank_id)
            REFERENCES blood_banks(id)
        )
    """)

    connection.commit()
    connection.close()

    print("Database initialized successfully!")


if __name__ == "__main__":
    initialize_database()