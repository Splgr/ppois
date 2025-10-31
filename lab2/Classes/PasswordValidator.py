from abc import ABC, abstractmethod

class PasswordValidator(ABC):
    @abstractmethod
    def validate(self, password: str) -> bool: 
        pass