from typing import List
from Patient import Patient
from Prescription import Prescription
from exceptions import InvalidPrescriptionError

class Doctor:
    def __init__(self, name: str, specialty: str, license: str):
        if not license.strip():
            raise Exception("Лицензия обязательна")
        
        self.name = name
        self.specialty = specialty
        self.license = license
        self.patients: List[Patient] = []

    def add_patient(self, patient: Patient) -> None:
        """Добавляет пациента к врачу"""
        if patient in self.patients:
            raise Exception("Пациент уже у этого врача")
        self.patients.append(patient)

    def remove_patient(self, patient: Patient) -> None:
        """Удаляет пациента"""
        if patient in self.patients:
            self.patients.remove(patient)

    def create_prescription(self, patient: Patient, drug_name: str, dosage: str) -> Prescription:
        """Создает рецепт (SRP)"""
        if patient not in self.patients:
            raise Exception("Пациент не найден у этого врача")
        
        if patient.has_allergy_to(drug_name):
            raise InvalidPrescriptionError(f"У пациента аллергия на {drug_name}")
        
        return Prescription(
            doctor_name=self.name,
            patient_name=patient.name,
            drug_name=drug_name
        )

    def get_patient_statistics(self) -> dict:
        """Статистика по пациентам"""
        return {
            'total_patients': len(self.patients),
            'patients_with_prescriptions': len([p for p in self.patients if p.prescriptions]),
            'average_age': sum(p.age for p in self.patients) / len(self.patients) if self.patients else 0
        }