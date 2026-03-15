
class FakePaymentRepo:
    def __init__(self):
        self._customers = {}
        self._payments = {}
        self._refunds = {}

    def clear(self):
        """Remove all customers, payments, and refunds from the repository."""
        self._customers.clear()
        self._payments.clear()
        self._refunds.clear()


    # ── Customer Methods ──

    def save_customer(self, customer: dict) -> dict:
        """Store a customer and return it."""
        self._customers[customer["id"]] = customer
        return customer

    def find_customer_by_id(self, customer_id: str) -> dict | None:
        """Retrieve a customer by their ID."""
        return self._customers.get(customer_id)

    def find_customer_by_email(self, email: str) -> dict | None:
        """Find a customer by their email address."""
        for customer in self._customers.values():
            if customer["email"] == email:
                return customer
        return None


    # Payment Methods

    def save_payment(self, payment: dict) -> dict:
        """Store a payment and return it."""
        self._payments[payment["id"]] = payment
        return payment

    def find_payment_by_id(self, payment_id: str) -> dict | None:
        """Retrieve a payment by its ID."""
        return self._payments.get(payment_id)


    def find_payments_by_customer(self, customer_id: str) -> list[dict]:
        """Get all payments for a specific customer."""
        return [payment for payment in self._payments.values() if payment["customerId"] == customer_id]


    #  Refund Methods

    def save_refund(self, refund: dict) -> dict:
        """Store a refund and return it."""
        self._refunds[refund["id"]] = refund
        return refund

    def find_refund_by_id(self, refund_id: str) -> dict | None:
        """Retrieve a refund by its ID."""
        return self._refunds.get(refund_id)

    def find_refunds_by_payment(self, payment_id: str) -> list[dict]:
        """Get all refunds for a specific payment."""
        return [refund for refund in self._refunds.values() if refund["paymentId"] == payment_id]
