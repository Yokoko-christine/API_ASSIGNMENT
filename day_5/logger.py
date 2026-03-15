def log_warning(message):
    print(f"WARNING: {message}")

class InputValidator:
    def validate(self, text):
        if not text:
            log_warning("Empty input received!")
            return False
        return True
