# Day 4 – Refactoring & TDD Exercise

## Files

| File | Description |
|------|-------------|
| `solution.py` | Refactored source code |
| `test_solution.py` | Tests for solution.py |

---

## What Was Refactored

The original code had three issues that were fixed:

**1. DRY violation – duplicated type checking**
Every function repeated the same `isinstance` check. This was extracted into a single private helper `_validate_amount()` that all functions now call.

**2. Magic number**
The discount value `0.1` was hardcoded inside `make_payment()`. It is now a named constant `PAYMENT_DISCOUNT = 0.1` at the top of the file, making it easy to find and change.

**3. Bug – mixed access on account dict**
`update_transaction` used `account.balance` (dot notation) while the rest of the code correctly used `account["balance"]` (dict access). Since `account` is a dictionary, dot notation throws an `AttributeError` at runtime. This was corrected to be consistent.

---

## Principles Applied

- **DRY** (Don't Repeat Yourself) – validation logic lives in one place
- **Named constants** – no magic numbers buried in logic
- **Single responsibility** – `_validate_amount` does one thing
- **Consistent data access** – `account["balance"]` used throughout

---

## Running the Tests

```bash
uv run pytest test_solution.py
```

To see a more detailed output:

```bash
uv run pytest test_solution.py -v
```

---

## Test Coverage

| Function | What is tested |
|----------|---------------|
| `_validate_amount` | Rejects strings and None, accepts int and float |
| `update_transaction` | Appends to list, stores correct fields, returns transactions list |
| `receive_payment` | Increases balance, returns new balance, records transaction, rejects invalid amount |
| `make_payment` | Decreases balance with discount, returns new balance, records transaction, raises on insufficient funds, rejects invalid amount |

A `@pytest.fixture` is used to provide a fresh `account` dict to each test, preventing state from leaking between tests.
