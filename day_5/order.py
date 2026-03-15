def send_email(recipient, subject):
    # In real life, this sends an actual email
    pass

class OrderEmailService:
    def place_order(self, user_email, is_success):
        if is_success:
            send_email(user_email, "Order Placed")