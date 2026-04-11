# Idempotent Wallet API

A Python API demonstrating **Data Integrity** and **Atomicity** in financial transactions. 

## 🚀 The Problem This Solves
In distributed systems, network glitches can cause users to retry payments. Without **Idempotency**, a user might be charged multiple times for a single intent. This project implements an "Exactly-Once" processing pattern.

## 🛠️ Tech Stack
- **Framework:** FastAPI
- **Database:** SQLite (Persistent storage)
- **Concurrency:** Database Transactions (ACID compliance)

## 🏗️ Architecture
The project follows a **Layered Architecture**:
1. **Communication Layer:** FastAPI handles RESTful requests and `X-Idempotency-Key` headers.
2. **Logic Layer:** Implements a "Check-Process-Record" workflow to ensure safe state changes.
3. **Storage Layer:** Relational SQLite tables for User Balances and Idempotency Keys.

## 🚦 How to Run
1. **Setup Environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # or .\venv\Scripts\activate on Windows
   pip install -r requirements.txt

2. **Initialise Database:**
   ```bash
   python database_setup.py

3. **Start the API:**
   ```bash
   uvicorn main:app --reload

4. **Test it:**
   Open http://127.0.0.1:8000/docs and use the interactive Swagger UI

## 🧠 Key Concepts Included
**Idempotency Keys:** Preventing duplicate operations using unique request signatures.

**Race Conditions:** Using SQL Transactions to handle concurrent requests safely.

**Floating Point Errors:** Storing currency as integers (pence) to ensure precision.