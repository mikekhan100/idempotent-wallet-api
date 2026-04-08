from fastapi import FastAPI, Header, HTTPException
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
        return {"username": username, "balance_pence": row[0]}
    return {"error": "User not found"}

@app.post("/spend")
def spend_money(username: str, amount: int, x_idempotency_key: str = Header(None)):
    if not x_idempotency_key:
        raise HTTPException(status_code=400, detail="Idempotency key missing in headers")
    
    # Connect to the 'Storage Layer'
    conn = sqlite3.connect("wallet.db")
    cursor = conn.cursor()

    # ---1. The Check --- 
    # Has this idempotency key already been used?
    cursor.execute("SELECT response_body, status_code FROM idempotency_keys WHERE id_key = ?", (x_idempotency_key,))
    already_done = cursor.fetchone()

    if already_done:
        conn.close()
        # Return exactly what was sent the first time
        return {"info": "Duplicate request detected - returning cached result", "data": already_done[0]}

    # --- 2. THE PROCESS ---
    # Check if user has enough money
    cursor.execute("SELECT balance FROM wallets WHERE username = ?", (username,))
    row = cursor.fetchone()
    
    if not row or row[0] < amount:
        conn.close()
        raise HTTPException(status_code=400, detail="Insufficient funds or user not found")

    # Subtract the money
    new_balance = row[0] - amount
    cursor.execute("UPDATE wallets SET balance = ? WHERE username = ?", (new_balance, username))

    # --- 3. THE RECORD ---
    response_data = f"Success. New balance: {new_balance}p"
    cursor.execute("INSERT INTO idempotency_keys (id_key, response_body, status_code) VALUES (?, ?, ?)", 
                   (x_idempotency_key, response_data, 200))

    conn.commit()
    conn.close()

    return {"message": response_data}