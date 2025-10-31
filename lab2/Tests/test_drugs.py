import unittest
from datetime import datetime, timedelta
from Drug import Drug
from PrescriptionDrug import PrescriptionDrug
from OverTheCounterDrug import OverTheCounterDrug
from exceptions import InvalidDrugError

class TestDrugUnit(unittest.TestCase):
    
    def test_drug_creation_with_valid_data(self):
        drug = Drug("Аспирин", "500mg", 100.0, "BATCH001", "room temp", "Обезболивающее")
        self.assertEqual(drug.name, "Аспирин")
        self.assertEqual(drug.dosage, "500mg")
        self.assertEqual(drug.price, 100.0)

    def test_drug_creation_raises_error_on_negative_price(self):
        with self.assertRaises(InvalidDrugError) as context:
            Drug("Аспирин", "500mg", -100.0, "BATCH001", "room temp", "Обезболивающее")

        self.assertIn("Цена не может быть отрицательной", str(context.exception))
