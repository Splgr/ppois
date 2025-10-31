from abc import ABC, abstractmethod
from Drug import Drug

class DrugValidator(ABC):
    @abstractmethod
    def validate(self, drug: Drug) -> str: ...

    @abstractmethod
    def check_compatibility(self, drug1: Drug, drug2: Drug) -> str: ...