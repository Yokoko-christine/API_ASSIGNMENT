
# Task 1 — Unit Testing Fundamentals
# Write tests before implementation. All tests should initially fail (RED).
import pytest
from app.utils.validators import (
    validate_amount,
    validate_currency,
    validate_email,
    generate_id,
)


# ── validateAmount ─────────────────────────────────────────────────────────────


def test_validate_amount_returns_true_for_100():
    assert validate_amount(100) is True



def test_validate_amount_returns_true_for_1_minimum_boundary():
    assert validate_amount(1) is True



def test_validate_amount_returns_false_for_0():
    assert validate_amount(0) is False



def test_validate_amount_returns_false_for_negative():
    assert validate_amount(-1) is False



def test_validate_amount_returns_false_for_decimal():
    assert validate_amount(9.99) is False



def test_validate_amount_returns_false_for_null():
    assert validate_amount(None) is False



def test_validate_amount_returns_false_for_string():
    assert validate_amount("100") is False


# ── validateCurrency ───────────────────────────────────────────────────────────


def test_validate_currency_returns_true_for_usd():
    assert validate_currency("usd") is True



def test_validate_currency_returns_false_for_too_short():
    assert validate_currency("us") is False



def test_validate_currency_returns_false_for_too_long():
    assert validate_currency("usdd") is False



def test_validate_currency_returns_false_for_empty_string():
    assert validate_currency("") is False


# ── validateEmail ──────────────────────────────────────────────────────────────


def test_validate_email_returns_true_for_valid_email():
    assert validate_email("alice@example.com") is True



def test_validate_email_returns_false_for_missing_at_symbol():
    assert validate_email("aliceexample.com") is False



def test_validate_email_returns_false_for_empty_string():
    assert validate_email("") is False


# ── generateId ────────────────────────────────────────────────────────────────


def test_generate_id_returns_string_starting_with_prefix():
    result = generate_id("pay")
    assert result.startswith("pay_")



def test_generate_id_returns_different_value_on_each_call():
    assert generate_id("pay") != generate_id("pay")
