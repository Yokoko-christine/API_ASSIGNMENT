import pytest
from user import User

# Fixture that creates a user with an initial balance of 1000
@pytest.fixture
def user_with_balance():
    return User("#67890", 1000)

# Fixture that sends money from the user and returns the modified user
@pytest.fixture
def user_after_sending(user_with_balance):
    user_with_balance.send_money(200, "#67890")
    return user_with_balance

# Fixture that receives money to the user and returns the modified user
@pytest.fixture
def user_after_receiving(user_with_balance):
    user_with_balance.receive_money("#67890", 200)
    return user_with_balance

# Test case: Verify that sending money deducts from balance and records transaction
def test_send_money(user_after_sending):
    assert user_after_sending.balance == 800
    assert len(user_after_sending.transaction_history) == 1
    assert user_after_sending.transaction_history[0]["amount"] == 200
    assert user_after_sending.transaction_history[0]["type"] == "sent"
    assert user_after_sending.transaction_history[0]["account_number"] == "#67890"

# Test case: Verify that receiving money adds to balance and records transaction
def test_receive_money(user_after_receiving):
    assert user_after_receiving.balance == 1200
    assert len(user_after_receiving.transaction_history) == 1
    assert user_after_receiving.transaction_history[0]["amount"] == 200
    assert user_after_receiving.transaction_history[0]["type"] == "received"
    assert user_after_receiving.transaction_history[0]["account_number"] == "#67890"

# Test case: Verify that sending more than available balance shows error and doesn't process
def test_insufficient_funds(user_with_balance, capsys):
    user_with_balance.send_money(1500, "#67890")
    captured = capsys.readouterr()
    assert "Insufficient funds" in captured.out
    assert user_with_balance.balance == 1000
    assert len(user_with_balance.transaction_history) == 0
