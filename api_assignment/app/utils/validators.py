
# Validation utility functions for payment API. No side effects or dependencies.
import uuid



def validate_amount(amount) -> bool:
    """Check if amount is a positive integer (not bool, decimal, string, or None)."""
    if not isinstance(amount, int) or isinstance(amount, bool):
        return False
    return amount >= 1



def validate_currency(currency) -> bool:
    """Check if currency is a non-empty string of exactly 3 characters."""
    if not isinstance(currency, str):
        return False
    return len(currency) == 3



def validate_email(email) -> bool:
    """Check if email contains both '@' and '.' and is a non-empty string."""
    if not isinstance(email, str) or not email:
        return False
    return "@" in email and "." in email



def generate_id(prefix: str) -> str:
    """Generate a unique string with a prefix, e.g. 'pay_a1b2c3d4'."""
    return f"{prefix}_{uuid.uuid4().hex[:8]}"
