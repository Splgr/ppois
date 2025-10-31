from datetime import datetime, timedelta
from PrescriptionValidator import PrescriptionValidator
from Prescription import Prescription
from exceptions import InvalidPrescriptionError

class SimplePrescriptionValidator(PrescriptionValidator):
    def is_valid(self, prescription: Prescription) -> bool:
        if prescription.is_used:
            return False
        if not prescription.doctor_name.strip():
            return False
        expiration = prescription.issue_date + timedelta(days=prescription.expiration_days)
        return datetime.now() <= expiration

    def verify_signature(self, prescription: Prescription) -> None:
        if not prescription.has_signature:
            raise InvalidPrescriptionError("Отсутствует подпись врача")