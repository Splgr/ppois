from DrugValidator import DrugValidator
from PrescriptionValidator import PrescriptionValidator
from PrescriptionLogger import PrescriptionLogger
from PrescriptionDrug import PrescriptionDrug
from OverTheCounterDrug import OverTheCounterDrug
from Prescription import Prescription
from exceptions import InsufficientStockError, InvalidPrescriptionError

class PharmacyService:
    def __init__(
        self,
        drug_validator: DrugValidator,
        prescription_validator: PrescriptionValidator,
        logger: PrescriptionLogger
    ):
        self.drug_validator = drug_validator
        self.prescription_validator = prescription_validator
        self.logger = logger

    def dispense_prescription_drug(self, drug: PrescriptionDrug, prescription: Prescription, stock: int = 1) -> str:
        if stock < 1:
            raise InsufficientStockError(f"Нет в наличии: {drug.name}")

        self.drug_validator.validate(drug)

        if not self.prescription_validator.is_valid(prescription):
            raise InvalidPrescriptionError("Рецепт недействителен")

        self.prescription_validator.verify_signature(prescription)
        self.logger.log_use(prescription)

        return f"Выдано: {drug.name} ({drug.dosage}) — {prescription.patient_name}"

    def sell_otc_drug(self, drug: OverTheCounterDrug, stock: int = 1) -> str:
        if stock < 1:
            raise InsufficientStockError(f"Нет в наличии: {drug.name}")
        self.drug_validator.validate(drug)
        return f"Продано без рецепта: {drug.name}"