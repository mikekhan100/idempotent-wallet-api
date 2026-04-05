import sqlite3

def setup_database():
    # Connect to (or create) the database file
    connection = sqlite3.connect("wallet.db")
    cursor = connection.cursor()

    # 1. The 'wallets' table (The Balances)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS wallets (
            username TEXT PRIMARY KEY,
            balance INTEGER
        )
    """)

    # 2. The 'idempotency_keys' table (The API Memory)
    # This records every successful transaction signature.
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS idempotency_keys (
            id_key TEXT PRIMARY KEY,
            response_body TEXT,
            status_code INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Add Alice if she's not there (Starting balance: 10000 pence [£100])
    cursor.execute("INSERT OR IGNORE INTO wallets VALUES ('alice', 10000)")
    
    connection.commit()
    print("Database updated! Both tables are ready and Alice is funded.")
    connection.close()

if __name__ == "__main__":
    setup_database()