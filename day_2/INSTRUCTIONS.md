## 📝 Exercise: Account Management with Transactions

Implement a simple user account system that supports sending and receiving money. The objective is to apply **Test-Driven Development (TDD)** principles by developing functions for balance updates and transaction tracking.

### ✅ Functional Requirements

1. **Account model**
   - Each user must have:
     - a unique account number
     - a current balance
     - a transaction history (initially empty)

2. **Operations**
   - **Send money**
     - Accepts an amount and the recipient’s account number.
     - Decreases the sender’s balance.
     - Appends a "sent" entry to the transaction history.
     - If the available balance is insufficient, display an error message and leave state unchanged.
   - **Receive money**
     - Accepts the sender’s account number and an amount.
     - Increases the receiver’s balance.
     - Appends a "received" entry to the transaction history.

3. **Transaction entries**
   - Represented as dictionaries with the following keys:
     - `amount` – numeric value of the transfer
     - `type` – either `"sent"` or `"received"`
     - `account_number` – the counterparty’s account identifier

---

### 🛠 Environment & Testing Setup

1. **Initialize project**
   - Create a Python virtual environment (`python -m venv .venv`).
   - Activate it (`.venv\Scripts\Activate.ps1` on Windows).
   - Install dependencies: `pip install pytest`.

2. **Implement the solution**
   - Write the `User` class and related functions in `user.py`.
   - Keep code clean, well-documented, and idiomatic.

3. **Write tests first**
   - Create `user_test.py` to import `User` and define tests for:
     - Successful send/receive operations
     - Correct balance adjustments
     - Accurate transaction history entries
     - Handling of insufficient funds (asserting error output and no state change)

4. **Execute tests**
   - Run `pytest` from the project root to validate behavior.

5. **Optional (JavaScript variant)**
   - Install Node.js and initialize a package (`npm init -y`).
   - Install Jest (`npm install jest --save-dev`).
   - Create corresponding JS files and tests following the same logic.

---

### 📂 Recommended Structure

```
day_2/
│
├── INSTRUCTIONS.md   ← polished guidelines
├── user.py           ← account implementation
└── user_test.py      ← pytest suite
```

> **Tip:** Embrace TDD by writing tests before implementation; this ensures professional, reliable code as you evolve the exercise.