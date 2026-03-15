import pytest
from solution import (
    _validate_amount,
    update_transaction,
    receive_payment,
    make_payment,
    PAYMENT_DISCOUNT,
)


@pytest.fixture
def account():
    return {"balance": 100, "transactions": []}


# ── _validate_amount ───────────────────────────────────────────────────────────

def test_validate_amount_raises_for_string():
    with pytest.raises(TypeError, match="Amount must be a number"):
        _validate_amount("50")

def test_validate_amount_raises_for_none():
    with pytest.raises(TypeError, match="Amount must be a number"):
        _validate_amount(None)

def test_validate_amount_accepts_int():
    _validate_amount(50)

def test_validate_amount_accepts_float():
    _validate_amount(9.99)


# ── update_transaction ─────────────────────────────────────────────────────────

def test_update_transaction_appends_to_list(account):
    update_transaction(account, 50, "receipt")
    assert len(account["transactions"]) == 1

def test_update_transaction_stores_correct_fields(account):
    update_transaction(account, 50, "receipt")
    assert account["transactions"][0] == {"type": "receipt", "amount": 50, "balance": 100}

def test_update_transaction_returns_transactions_list(account):
    result = update_transaction(account, 50, "receipt")
    assert result == account["transactions"]


# ── receive_payment ────────────────────────────────────────────────────────────

def test_receive_payment_increases_balance(account):
    receive_payment(account, 50)
    assert account["balance"] == 150

def test_receive_payment_returns_new_balance(account):
    result = receive_payment(account, 50)
    assert result == 150

def test_receive_payment_records_transaction(account):
    receive_payment(account, 50)
    assert len(account["transactions"]) == 1

def test_receive_payment_raises_for_invalid_amount(account):
    with pytest.raises(TypeError, match="Amount must be a number"):
        receive_payment(account, "fifty")


# ── make_payment ───────────────────────────────────────────────────────────────

def test_make_payment_decreases_balance(account):
    make_payment(account, 50)
    assert account["balance"] == pytest.approx(100 - 50 * (1 - PAYMENT_DISCOUNT))

def test_make_payment_returns_new_balance(account):
    result = make_payment(account, 50)
    assert result == pytest.approx(100 - 50 * (1 - PAYMENT_DISCOUNT))

def test_make_payment_records_transaction(account):
    make_payment(account, 50)
    assert len(account["transactions"]) == 1

def test_make_payment_raises_for_insufficient_funds(account):
    with pytest.raises(ValueError, match="Insufficient funds"):
        make_payment(account, 200)

def test_make_payment_raises_for_invalid_amount(account):
    with pytest.raises(TypeError, match="Amount must be a number"):
        make_payment(account, "fifty")