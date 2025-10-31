from Prescription import Prescription
from exceptions import InvalidPrescriptionError

class PrescriptionService:
    def mark_as_used(self, prescription: Prescription) -> None:
        if prescription.is_used:
            raise InvalidPrescriptionError("Рецепт уже использован")
        prescription._used = True