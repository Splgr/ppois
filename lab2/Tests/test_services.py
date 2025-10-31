import unittest
from PharmacyService import PharmacyService
from SimpleDrugValidator import SimpleDrugValidator
from SimplePrescriptionValidator import SimplePrescriptionValidator
from ConsolePrescriptionLogger import ConsolePrescriptionLogger
from PrescriptionDrug import PrescriptionDrug
from OverTheCounterDrug import OverTheCounterDrug
from Prescription import Prescription
from exceptions import InsufficientStockError, InvalidPrescriptionError

class TestPharmacyServiceUnit(unittest.TestCase):
    
    def setUp(self):
        self.validator = SimpleDrugValidator()
        self.prescription_validator = SimplePrescriptionValidator()
        self.logger = ConsolePrescriptionLogger()
        self.service = PharmacyService(self.validator, self.prescription_validator, self.logger)
        
        self.prescription_drug = PrescriptionDrug("Антибиотик", "250mg", 300.0, "BATCH001", "room temp", "Антибиотик")
        self.otc_drug = OverTheCounterDrug("Витамин C", "500mg", 50.0, "BATCH002", "room temp", "Витамин")
        self.prescription = Prescription("Доктор Иванов", "Пациент Петров")

    def test_sell_otc_drug_success(self):
        result = self.service.sell_otc_drug(self.otc_drug, stock=5)
        self.assertIn("Продано без рецепта: Витамин C", result)

    def test_sell_otc_drug_insufficient_stock(self):
        with self.assertRaises(InsufficientStockError) as context:
            self.service.sell_otc_drug(self.otc_drug, stock=0)
        self.assertIn("Нет в наличии: Витамин C", str(context.exception))

    def test_dispense_prescription_drug_success(self):
        result = self.service.dispense_prescription_drug(self.prescription_drug, self.prescription, stock=5)
        self.assertIn("Выдано: Антибиотик", result)
        self.assertIn("Пациент Петров", result)