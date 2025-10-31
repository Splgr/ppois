from abc import ABC, abstractmethod
from Prescription import Prescription

class PrescriptionLogger(ABC):
    @abstractmethod
    def log_use(self, prescription: Prescription) -> None: ...