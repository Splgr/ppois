from PrescriptionLogger import PrescriptionLogger
from Prescription import Prescription

class ConsolePrescriptionLogger(PrescriptionLogger):
    def log_use(self, prescription: Prescription) -> None:
        print(f"[ЛОГ] Рецепт использован: {prescription.patient_name}, врач: {prescription.doctor_name}")