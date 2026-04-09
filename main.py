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
        raise HTTPException(status_code=400, detail="Idempotency key missing")

    conn = sqlite3.connect("wallet.db")
    cursor = conn.cursor()

    try:
        # 'with conn:' starts a database transaction automatically
        with conn:
            # 1. Check Idempotency (Inside the transaction to ensure atomicity)
            cursor.execute("SELECT response_body FROM idempotency_keys WHERE id_key = ?", (x_idempotency_key,))
            already_done = cursor.fetchone()
            if already_done:
                return {"info": "Duplicate", "data": already_done}

            # 2. Check Balance
            cursor.execute("SELECT balance FROM wallets WHERE username = ?", (username,))
            row = cursor.fetchone()
            if not row or row < amount:
                raise HTTPException(status_code=400, detail="Insufficient funds")

            # 3. Update Balance
            new_balance = row - amount
            cursor.execute("UPDATE wallets SET balance = ? WHERE username = ?", (new_balance, username))

            # 4. Record Key
            response_data = f"Success. New balance: {new_balance}p"
            cursor.execute("INSERT INTO idempotency_keys (id_key, response_body, status_code) VALUES (?, ?, ?)", 
                           (x_idempotency_key, response_data, 200))
            
            # When we exit this 'with' block, conn.commit() is called automatically.
            # If any error happened inside, it would auto-rollback!
            
        return {"message": response_data}

    except sqlite3.Error as e:
        raise HTTPException(status_code=500, detail=f"Database error: {e}")
    finally:
        conn.close()