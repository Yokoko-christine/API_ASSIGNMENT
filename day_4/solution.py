PAYMENT_DISCOUNT = 0.1

def _validate_amount(amount):
    if not isinstance(amount, (int, float)):
        raise TypeError("Amount must be a number")

def update_transaction(account, amount, type):
    account["transactions"].append({
        "type": type,
        "amount": amount,
        "balance": account["balance"]  # bug fix: was account.balance
    })
    return account["transactions"]

def receive_payment(account, amount):
    _validate_amount(amount)  # DRY: validation extracted
    account["balance"] += amount
    update_transaction(account, amount, "receipt")
    return account["balance"]

def make_payment(account, amount):
    _validate_amount(amount)  # DRY: reusing the same validator
    if account["balance"] < amount:
        raise ValueError("Insufficient funds")
    account["balance"] -= amount * (1 - PAYMENT_DISCOUNT)  # named constant
    update_transaction(account, amount, "payout")
    return account["balance"]