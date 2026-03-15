
# Task 2 — Full TDD Cycle: PaymentService
# Tests written before implementation. Uses FakeRepository, no real DB.
import pytest
from unittest.mock import MagicMock
from app.services.payment_service import PaymentService
from app.repos.fake_payment_repo import FakePaymentRepo



@pytest.fixture
def repo():
    repo_instance = FakePaymentRepo()
    repo_instance.clear()
    return repo_instance



@pytest.fixture
def service(repo):
    return PaymentService(repo)


# ── createCustomer ─────────────────────────────────────────────────────────────


def test_create_customer_returns_customer_with_correct_name_and_email(service):
    customer = service.create_customer("Alice", "alice@example.com")
    assert customer["name"] == "Alice"
    assert customer["email"] == "alice@example.com"



def test_create_customer_generates_unique_id_prefixed_with_cus(service):
    customer = service.create_customer("Alice", "alice@example.com")
    assert customer["id"].startswith("cus_")



def test_create_customer_raises_when_name_is_empty(service):
    with pytest.raises(ValueError, match="Name is required"):
        service.create_customer("", "alice@example.com")



def test_create_customer_raises_when_email_has_no_at_symbol(service):
    with pytest.raises(ValueError, match="Invalid email"):
        service.create_customer("Alice", "aliceexample.com")



def test_create_customer_raises_when_email_already_registered(service):
    service.create_customer("Alice", "alice@example.com")
    with pytest.raises(ValueError, match="Email already exists"):
        service.create_customer("Alice2", "alice@example.com")


# ── createPayment ──────────────────────────────────────────────────────────────


def test_create_payment_returns_payment_with_status_pending(service):
    customer = service.create_customer("Alice", "alice@example.com")
    payment = service.create_payment(customer["id"], 1000, "usd")
    assert payment["status"] == "pending"



def test_create_payment_generates_unique_id_prefixed_with_pay(service):
    customer = service.create_customer("Alice", "alice@example.com")
    payment = service.create_payment(customer["id"], 1000, "usd")
    assert payment["id"].startswith("pay_")



def test_create_payment_raises_when_customer_not_found(service):
    with pytest.raises(ValueError, match="Customer not found"):
        service.create_payment("cus_unknown", 1000, "usd")



def test_create_payment_raises_when_amount_is_zero(service):
    customer = service.create_customer("Alice", "alice@example.com")
    with pytest.raises(ValueError, match="Invalid amount"):
        service.create_payment(customer["id"], 0, "usd")



def test_create_payment_raises_when_amount_is_negative(service):
    customer = service.create_customer("Alice", "alice@example.com")
    with pytest.raises(ValueError, match="Invalid amount"):
        service.create_payment(customer["id"], -1, "usd")



def test_create_payment_raises_when_amount_is_decimal(service):
    customer = service.create_customer("Alice", "alice@example.com")
    with pytest.raises(ValueError, match="Invalid amount"):
        service.create_payment(customer["id"], 9.99, "usd")



def test_create_payment_raises_when_currency_is_not_3_chars(service):
    customer = service.create_customer("Alice", "alice@example.com")
    with pytest.raises(ValueError, match="Invalid currency"):
        service.create_payment(customer["id"], 1000, "us")


# ── capture ────────────────────────────────────────────────────────────────────


def test_capture_changes_payment_status_to_succeeded(service):
    customer = service.create_customer("Alice", "alice@example.com")
    payment = service.create_payment(customer["id"], 1000, "usd")
    result = service.capture(payment["id"])
    assert result["status"] == "succeeded"



def test_capture_raises_when_payment_not_found(service):
    with pytest.raises(ValueError, match="Payment not found"):
        service.capture("pay_unknown")



def test_capture_raises_when_payment_already_succeeded(service):
    customer = service.create_customer("Alice", "alice@example.com")
    payment = service.create_payment(customer["id"], 1000, "usd")
    service.capture(payment["id"])
    with pytest.raises(ValueError, match="Cannot capture"):
        service.capture(payment["id"])



def test_capture_raises_when_payment_is_failed(service):
    customer = service.create_customer("Alice", "alice@example.com")
    payment = service.create_payment(customer["id"], 1000, "usd")
    service.fail(payment["id"])
    with pytest.raises(ValueError, match="Cannot capture"):
        service.capture(payment["id"])


# ── fail ───────────────────────────────────────────────────────────────────────


def test_fail_changes_payment_status_to_failed(service):
    customer = service.create_customer("Alice", "alice@example.com")
    payment = service.create_payment(customer["id"], 1000, "usd")
    result = service.fail(payment["id"])
    assert result["status"] == "failed"


# ── refund ─────────────────────────────────────────────────────────────────────


def test_refund_raises_when_payment_not_found(service):
    with pytest.raises(ValueError, match="Payment not found"):
        service.refund("pay_unknown", 500)



def test_refund_succeeds_for_full_refund_equal_to_payment_amount(service):
    customer = service.create_customer("Alice", "alice@example.com")
    payment = service.create_payment(customer["id"], 1000, "usd")
    service.capture(payment["id"])
    refund = service.refund(payment["id"], 1000)
    assert refund["amount"] == 1000
    assert refund["status"] == "succeeded"



def test_refund_raises_when_amount_exceeds_payment_amount(service):
    customer = service.create_customer("Alice", "alice@example.com")
    payment = service.create_payment(customer["id"], 1000, "usd")
    service.capture(payment["id"])
    with pytest.raises(ValueError, match="Refund exceeds payment amount"):
        service.refund(payment["id"], 1001)



def test_refund_raises_when_payment_is_pending(service):
    customer = service.create_customer("Alice", "alice@example.com")
    payment = service.create_payment(customer["id"], 1000, "usd")
    with pytest.raises(ValueError, match="Cannot refund"):
        service.refund(payment["id"], 500)



def test_refund_raises_when_payment_is_failed(service):
    customer = service.create_customer("Alice", "alice@example.com")
    payment = service.create_payment(customer["id"], 1000, "usd")
    service.fail(payment["id"])
    with pytest.raises(ValueError, match="Cannot refund"):
        service.refund(payment["id"], 500)
