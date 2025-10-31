from DoctorPrescriptionService import DoctorPrescriptionService
from Prescription import Prescription
from Patient import Patient
from exceptions import InvalidPrescriptionError

class BasicDoctorPrescriptionService(DoctorPrescriptionService):
    def write_prescription(self, patient: Patient, drug_name: str) -> Prescription:
        if not patient.name.strip():
            raise InvalidPrescriptionError("Имя пациента обязательно")
        
        prescription = Prescription(
            doctor_name="Доктор Смит",  # В реальности передавать врача
            patient_name=patient.name,
            drug_name=drug_name
        )
        patient.add_prescription(prescription)
        return prescription