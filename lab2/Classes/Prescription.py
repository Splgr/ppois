from datetime import datetime, timedelta
from typing import Optional
from exceptions import InvalidPrescriptionError

class Prescription:
    def __init__(
        self,
        doctor_name: str,
        patient_name: str,
        issue_date: Optional[datetime] = None,
        expiration_days: int = 30,
        drug_name: Optional[str] = None,
        has_signature: bool = True,
    ):
        if not doctor_name.strip():
            raise InvalidPrescriptionError("Имя врача обязательно")
        if not patient_name.strip():
            raise InvalidPrescriptionError("Имя пациента обязательно")

        self.doctor_name = doctor_name
        self.patient_name = patient_name
        self.issue_date = issue_date or datetime.now()
        self.expiration_days = expiration_days
        self.drug_name = drug_name
        self.has_signature = has_signature
        self._used = False

    @property
    def is_used(self) -> bool:
        return self._used