from PasswordValidator import PasswordValidator

class SimplePasswordValidator(PasswordValidator):
    def validate(self, password: str) -> bool:
        return len(password) >= 6