# User class to manage bank accounts and transactions
class User:
    # Initialize a new user with account number, balance, and empty transaction history
    def __init__(self, account_number, balance):
        self.account_number = account_number
        self.balance = balance
        self.transaction_history = []

    # Send money to another account
    def send_money(self, amount, account_number):
        # Check if user has enough balance
        if amount > self.balance:
            print("Insufficient funds")
            return
        
        # Deduct amount from balance
        self.balance -= amount
        # Record transaction in history
        self.transaction_history.append({"amount": amount, "type": "sent", "account_number": account_number})

    # Receive money from another account
    def receive_money(self, account_number, amount):
        # Add amount to balance
        self.balance += amount
        # Record transaction in history
        self.transaction_history.append({"amount": amount, "type": "received", "account_number": account_number})
