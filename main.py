from fastapi import FastAPI
import sqlite3

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Welcome to the Idempotent Wallet API"}

@app.get("/balance/{username}")
def get_balance(username: str):
    # Connect to the 'Storage Layer'
    conn = sqlite3.connect("wallet.db")
    cursor = conn.cursor()
    
    # Logic: Look up the user
    cursor.execute("SELECT balance FROM wallets WHERE username = ?", (username,))
    row = cursor.fetchone()
    conn.close()

    if row:
        return {"username": username, "balance_pence": row}
    return {"error": "User not found"}