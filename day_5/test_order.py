import pytest
from unittest.mock import patch
from order import OrderEmailService

@pytest.fixture
def service():
    return OrderEmailService()

@patch('order.send_email')
def test_sent_on_successful_order(mock_send_email, service):
    service.place_order(user_email="test123@gmail.com", is_success = True)
    mock_send_email.assert_called_with("test123@gmail.com", "Order Placed")

@patch('order.send_email')
def test_sent_on_failed_order(mock_send_email, service):
    service.place_order(user_email="test123@gmail.com", is_success = False)
    mock_send_email.assert_not_called()