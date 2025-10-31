from abc import ABC, abstractmethod
from Prescription import Prescription
from Patient import Patient

class DoctorPrescriptionService(ABC):
    @abstractmethod
    def write_prescription(self, patient: 'Patient', drug_name: str) -> Prescription:
        pass