from abc import ABC, abstractmethod
from Prescription import Prescription

class PrescriptionValidator(ABC):
    @abstractmethod
    def is_valid(self, prescription: Prescription) -> bool: ...

    @abstractmethod
    def verify_signature(self, prescription: Prescription) -> None: ...