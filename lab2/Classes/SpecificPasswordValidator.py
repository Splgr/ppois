from PasswordValidator import PasswordValidator

class SpecificPasswordValidator(PasswordValidator):
    def validate(self, password: str) -> bool:
        correct_password = "alina_top"
        return password == correct_password