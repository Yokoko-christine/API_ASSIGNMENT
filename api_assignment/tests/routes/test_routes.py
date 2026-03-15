
# Task 4 + Task 5 — Route tests.
# Service is always mocked. Only HTTP behavior is tested here.
# Business rules are covered in Task 2.
import pytest
from unittest.mock import MagicMock, patch
from httpx import AsyncClient, ASGITransport


#Fixtures 
@pytest.fixture
def mock_service():
    return MagicMock()



@pytest.fixture
async def client(mock_service):
    with patch("app.routes.customers.service", mock_service), \
         patch("app.routes.payments.service", mock_service), \
         patch("app.routes.refunds.service", mock_service):
        from app.main import app
        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as async_client:
            yield async_client, mock_service


# POST /customers 
async def test_post_customers_returns_201_and_customer_on_valid_input(client):
    async_client, service = client
    service.create_customer.return_value = {"id": "cus_1", "name": "Alice", "email": "alice@example.com"}
    response = await async_client.post("/customers", json={"name": "Alice", "email": "alice@example.com"})
    assert response.status_code == 201
    assert response.json()["id"] == "cus_1"



async def test_post_customers_returns_400_when_name_missing(client):
    async_client, service = client
    response = await async_client.post("/customers", json={"email": "alice@example.com"})
    assert response.status_code == 400
    service.create_customer.assert_not_called()



async def test_post_customers_returns_400_when_email_missing(client):
    async_client, service = client
    response = await async_client.post("/customers", json={"name": "Alice"})
    assert response.status_code == 400
    service.create_customer.assert_not_called()



async def test_post_customers_service_not_called_on_invalid_input(client):
    async_client, service = client
    await async_client.post("/customers", json={})
    service.create_customer.assert_not_called()


# POST /payments 

async def test_post_payments_returns_201_and_pending_payment(client):
    async_client, service = client
    service.create_payment.return_value = {
        "id": "pay_1", "customerId": "cus_1", "amount": 1000,
        "currency": "usd", "status": "pending"
    }
    response = await async_client.post("/payments", json={"customerId": "cus_1", "amount": 1000, "currency": "usd"})
    assert response.status_code == 201
    assert response.json()["status"] == "pending"



async def test_post_payments_returns_400_when_amount_missing(client):
    async_client, _ = client
    response = await async_client.post("/payments", json={"customerId": "cus_1", "currency": "usd"})
    assert response.status_code == 400



async def test_post_payments_returns_400_when_currency_missing(client):
    async_client, _ = client
    response = await async_client.post("/payments", json={"customerId": "cus_1", "amount": 1000})
    assert response.status_code == 400



async def test_post_payments_returns_400_when_customer_id_missing(client):
    async_client, _ = client
    response = await async_client.post("/payments", json={"amount": 1000, "currency": "usd"})
    assert response.status_code == 400



async def test_post_payments_returns_500_when_service_throws_unexpectedly(client):
    async_client, service = client
    service.create_payment.side_effect = Exception("DB exploded")
    response = await async_client.post("/payments", json={"customerId": "cus_1", "amount": 1000, "currency": "usd"})
    assert response.status_code == 500
    assert response.json() == {"error": "Something went wrong"}


# POST /payments/:id/capture ─

async def test_capture_returns_200_and_updated_payment(client):
    async_client, service = client
    service.capture.return_value = {"id": "pay_1", "status": "succeeded"}
    response = await async_client.post("/payments/pay_1/capture")
    assert response.status_code == 200
    assert response.json()["status"] == "succeeded"



async def test_capture_returns_404_when_payment_unknown(client):
    async_client, service = client
    service.capture.side_effect = ValueError("Payment not found")
    response = await async_client.post("/payments/pay_unknown/capture")
    assert response.status_code == 404



async def test_capture_returns_409_when_payment_cannot_be_captured(client):
    async_client, service = client
    service.capture.side_effect = ValueError("Cannot capture")
    response = await async_client.post("/payments/pay_1/capture")
    assert response.status_code == 409


# POST /refunds

async def test_post_refunds_returns_201_and_refund_object(client):
    ac, svc = client
    svc.refund.return_value = {"id": "ref_1", "paymentId": "pay_1", "amount": 500, "status": "succeeded"}
    response = await ac.post("/refunds", json={"paymentId": "pay_1", "amount": 500})
    assert response.status_code == 201
    assert response.json()["id"] == "ref_1"


async def test_post_refunds_returns_400_when_payment_id_missing(client):
    ac, svc = client
    response = await ac.post("/refunds", json={"amount": 500})
    assert response.status_code == 400


async def test_post_refunds_returns_400_when_amount_missing(client):
    ac, svc = client
    response = await ac.post("/refunds", json={"paymentId": "pay_1"})
    assert response.status_code == 400


async def test_post_refunds_returns_422_when_refund_exceeds_payment(client):
    ac, svc = client
    svc.refund.side_effect = ValueError("Refund exceeds payment amount")
    response = await ac.post("/refunds", json={"paymentId": "pay_1", "amount": 9999})
    assert response.status_code == 422


# ─── GET /payments ────────────────────────────────────────────────────────────

async def test_get_payments_returns_200_and_list(client):
    ac, svc = client
    svc.get_all_payments.return_value = [{"id": "pay_1", "status": "pending"}]
    response = await ac.get("/payments")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


async def test_get_payments_returns_500_when_service_throws(client):
    ac, svc = client
    svc.get_all_payments.side_effect = Exception("Unexpected")
    response = await ac.get("/payments")
    assert response.status_code == 500
    assert response.json() == {"error": "Something went wrong"}


#  Task 5: Boundary tests 
async def test_post_payments_amount_1_is_minimum_boundary_accepted(client):
    ac, svc = client
    svc.create_payment.return_value = {"id": "pay_1", "amount": 1, "status": "pending"}
    response = await ac.post("/payments", json={"customerId": "cus_1", "amount": 1, "currency": "usd"})
    assert response.status_code == 201


async def test_post_payments_amount_0_is_rejected(client):
    ac, svc = client
    svc.create_payment.side_effect = ValueError("Invalid amount")
    response = await ac.post("/payments", json={"customerId": "cus_1", "amount": 0, "currency": "usd"})
    assert response.status_code == 400


async def test_post_payments_negative_amount_is_rejected(client):
    ac, svc = client
    svc.create_payment.side_effect = ValueError("Invalid amount")
    response = await ac.post("/payments", json={"customerId": "cus_1", "amount": -1, "currency": "usd"})
    assert response.status_code == 400


async def test_post_payments_decimal_amount_is_rejected(client):
    ac, svc = client
    svc.create_payment.side_effect = ValueError("Invalid amount")
    response = await ac.post("/payments", json={"customerId": "cus_1", "amount": 9.99, "currency": "usd"})
    assert response.status_code == 400


async def test_post_refunds_full_refund_equal_to_payment_amount_succeeds(client):
    ac, svc = client
    svc.refund.return_value = {"id": "ref_1", "paymentId": "pay_1", "amount": 1000, "status": "succeeded"}
    response = await ac.post("/refunds", json={"paymentId": "pay_1", "amount": 1000})
    assert response.status_code == 201


async def test_post_refunds_one_penny_over_payment_amount_rejected(client):
    ac, svc = client
    svc.refund.side_effect = ValueError("Refund exceeds payment amount")
    response = await ac.post("/refunds", json={"paymentId": "pay_1", "amount": 1001})
    assert response.status_code == 422


# Customer name length boundaries

async def test_post_customers_name_1_char_is_accepted(client):
    ac, svc = client
    svc.create_customer.return_value = {"id": "cus_1", "name": "A", "email": "a@example.com"}
    response = await ac.post("/customers", json={"name": "A", "email": "a@example.com"})
    assert response.status_code == 201


async def test_post_customers_name_100_chars_is_accepted(client):
    ac, svc = client
    name = "A" * 100
    svc.create_customer.return_value = {"id": "cus_1", "name": name, "email": "a@example.com"}
    response = await ac.post("/customers", json={"name": name, "email": "a@example.com"})
    assert response.status_code == 201


async def test_post_customers_name_101_chars_is_rejected(client):
    ac, svc = client
    response = await ac.post("/customers", json={"name": "A" * 101, "email": "a@example.com"})
    assert response.status_code == 400


# ─── Task 5: 404 tests 
async def test_get_customer_by_unknown_id_returns_404(client):
    ac, svc = client
    svc.get_customer.return_value = None
    response = await ac.get("/customers/cus_unknown")
    assert response.status_code == 404
    assert response.json() == {"error": "Customer not found"}


async def test_get_customer_payments_unknown_customer_returns_404(client):
    ac, svc = client
    svc.get_customer.return_value = None
    response = await ac.get("/customers/cus_unknown/payments")
    assert response.status_code == 404
    assert response.json() == {"error": "Customer not found"}


async def test_get_payment_by_unknown_id_returns_404(client):
    ac, svc = client
    svc.get_payment.return_value = None
    response = await ac.get("/payments/pay_unknown")
    assert response.status_code == 404
    assert response.json() == {"error": "Payment not found"}


async def test_capture_unknown_payment_returns_404(client):
    ac, svc = client
    svc.capture.side_effect = ValueError("Payment not found")
    response = await ac.post("/payments/pay_unknown/capture")
    assert response.status_code == 404
    assert response.json() == {"error": "Payment not found"}


async def test_fail_unknown_payment_returns_404(client):
    ac, svc = client
    svc.fail.side_effect = ValueError("Payment not found")
    response = await ac.post("/payments/pay_unknown/fail")
    assert response.status_code == 404
    assert response.json() == {"error": "Payment not found"}


async def test_get_refund_by_unknown_id_returns_404(client):
    ac, svc = client
    svc.get_refund.return_value = None
    response = await ac.get("/refunds/ref_unknown")
    assert response.status_code == 404
    assert response.json() == {"error": "Refund not found"}


# Task 5: Input variation tests 
async def test_post_payments_no_body_returns_400(client):
    ac, svc = client
    response = await ac.post("/payments", content=b"", headers={"content-type": "application/json"})
    assert response.status_code == 400


async def test_post_payments_null_amount_returns_400(client):
    ac, svc = client
    svc.create_payment.side_effect = ValueError("Invalid amount")
    response = await ac.post("/payments", json={"customerId": "cus_1", "amount": None, "currency": "usd"})
    assert response.status_code == 400


async def test_post_payments_empty_currency_returns_400(client):
    ac, svc = client
    svc.create_payment.side_effect = ValueError("Invalid currency")
    response = await ac.post("/payments", json={"customerId": "cus_1", "amount": 1000, "currency": ""})
    assert response.status_code == 400


async def test_post_customers_email_without_at_returns_400(client):
    ac, svc = client
    svc.create_customer.side_effect = ValueError("Invalid email")
    response = await ac.post("/customers", json={"name": "Alice", "email": "aliceexample.com"})
    assert response.status_code == 400


async def test_post_customers_duplicate_email_returns_409(client):
    ac, svc = client
    svc.create_customer.side_effect = ValueError("Email already exists")
    response = await ac.post("/customers", json={"name": "Alice2", "email": "alice@example.com"})
    assert response.status_code == 409


# Task 5: 500 tests 
async def test_get_payments_service_throws_returns_500_generic_message(client):
    ac, svc = client
    svc.get_all_payments.side_effect = Exception("DB down")
    response = await ac.get("/payments")
    assert response.status_code == 500
    assert response.json() == {"error": "Something went wrong"}


async def test_post_payments_service_throws_after_validation_returns_500(client):
    ac, svc = client
    svc.create_payment.side_effect = Exception("Unexpected DB error")
    response = await ac.post("/payments", json={"customerId": "cus_1", "amount": 1000, "currency": "usd"})
    assert response.status_code == 500
    assert response.json() == {"error": "Something went wrong"}


async def test_post_refunds_service_throws_returns_500(client):
    ac, svc = client
    svc.refund.side_effect = Exception("Unexpected")
    response = await ac.post("/refunds", json={"paymentId": "pay_1", "amount": 500})
    assert response.status_code == 500
    assert response.json() == {"error": "Something went wrong"}
