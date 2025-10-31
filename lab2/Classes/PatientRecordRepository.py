from abc import ABC, abstractmethod
from PatientRecord import PatientRecord

class PatientRecordRepository(ABC):
    @abstractmethod
    def get_record(self, patient_name: str) -> 'PatientRecord': 
        pass
    
    @abstractmethod
    def update_record(self, record: 'PatientRecord') -> None:
        pass