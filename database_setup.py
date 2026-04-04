import sqlite3

def setup_database():
    # Connect to (or create) the database file
    connection = sqlite3.connect("wallet.db")
    cursor = connection.cursor()

    # 1. Create the Wallet table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS wallets (
            username TEXT PRIMARY KEY,
            balance INTEGER
        )
    """)

    # 2. Add a starting user if they don't exist
    cursor.execute("INSERT OR IGNORE INTO wallets VALUES ('alice', 100)")
    
    connection.commit()
    print("Database ready! Alice has £100.")
    connection.close()

if __name__ == "__main__":
    setup_database()