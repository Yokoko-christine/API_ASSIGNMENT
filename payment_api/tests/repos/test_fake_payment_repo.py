
# Task 3 — Tests for FakeRepository, Stub, and Spy.
import pytest
import logging
from unittest.mock import MagicMock, patch
from app.repos.fake_payment_repo import FakePaymentRepo
from app.services.payment_service import PaymentService



@pytest.fixture(autouse=True)
def repo():
    repo_instance = FakePaymentRepo()
    repo_instance.clear()
    return repo_instance


# ── FakeRepository tests ───────────────────────────────────────────────────────


def test_save_customer_stores_and_retrieves_by_id(repo):
    customer = {"id": "cus_1", "name": "Alice", "email": "alice@example.com"}
    repo.save_customer(customer)
    assert repo.find_customer_by_id("cus_1") == customer



def test_find_customer_by_id_returns_none_for_unknown_id(repo):
    assert repo.find_customer_by_id("cus_unknown") is None



def test_find_customer_by_email_returns_matching_customer(repo):
    customer = {"id": "cus_1", "name": "Alice", "email": "alice@example.com"}
    repo.save_customer(customer)
    assert repo.find_customer_by_email("alice@example.com") == customer



def test_find_customer_by_email_returns_none_when_no_match(repo):
    assert repo.find_customer_by_email("nobody@example.com") is None



def test_save_payment_stores_and_retrieves_by_id(repo):
    payment = {"id": "pay_1", "customerId": "cus_1", "amount": 1000, "status": "pending"}
    repo.save_payment(payment)
    assert repo.find_payment_by_id("pay_1") == payment



def test_find_payments_by_customer_returns_only_matching_payments(repo):
    repo.save_payment({"id": "pay_1", "customerId": "cus_1", "amount": 1000, "status": "pending"})
    repo.save_payment({"id": "pay_2", "customerId": "cus_2", "amount": 500, "status": "pending"})
    payments = repo.find_payments_by_customer("cus_1")
    assert len(payments) == 1
    assert payments[0]["id"] == "pay_1"



def test_find_refunds_by_payment_returns_all_linked_refunds(repo):
    repo.save_refund({"id": "ref_1", "paymentId": "pay_1", "amount": 500, "status": "succeeded"})
    repo.save_refund({"id": "ref_2", "paymentId": "pay_1", "amount": 200, "status": "succeeded"})
    repo.save_refund({"id": "ref_3", "paymentId": "pay_2", "amount": 300, "status": "succeeded"})
    refunds = repo.find_refunds_by_payment("pay_1")
    assert len(refunds) == 2



def test_clear_empties_all_stored_data(repo):
    repo.save_customer({"id": "cus_1", "name": "Alice", "email": "alice@example.com"})
    repo.save_payment({"id": "pay_1", "customerId": "cus_1", "amount": 1000, "status": "pending"})
    repo.clear()
    assert repo.find_customer_by_id("cus_1") is None
    assert repo.find_payment_by_id("pay_1") is None


# ── Stub test ─────────────────────────────────────────────────────────────────
# Stub the repo to return a specific payment — no real FakeRepo needed.


def test_capture_sets_status_to_succeeded_using_stub():
    stub_repo = MagicMock()
    stub_repo.find_payment_by_id.return_value = {
        "id": "pay_1", "amount": 1000, "status": "pending"
    }
    stub_repo.save_payment.side_effect = lambda payment: payment

    service = PaymentService(stub_repo)
    result = service.capture("pay_1")

    assert result["status"] == "succeeded"
    stub_repo.save_payment.assert_called_once()


# ── Spy test ──────────────────────────────────────────────────────────────────
# Spy on logger.warning to verify audit logging on payment failure.


def test_fail_calls_logger_warning_with_payment_id(repo):
    service = PaymentService(repo)
    customer = service.create_customer("Alice", "alice@example.com")
    payment = service.create_payment(customer["id"], 1000, "usd")

    with patch("app.services.payment_service.logger") as mock_logger:
        service.fail(payment["id"])
        mock_logger.warning.assert_called_once()
        log_message = mock_logger.warning.call_args[0][0]
        assert payment["id"] in log_message



def test_capture_does_not_call_logger_warning(repo):
    service = PaymentService(repo)
    customer = service.create_customer("Alice", "alice@example.com")
    payment = service.create_payment(customer["id"], 1000, "usd")

    with patch("app.services.payment_service.logger") as mock_logger:
        service.capture(payment["id"])
        mock_logger.warning.assert_not_called()
