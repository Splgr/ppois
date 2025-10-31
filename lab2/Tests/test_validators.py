import unittest
from datetime import datetime, timedelta
from SimpleDrugValidator import SimpleDrugValidator
from SimplePrescriptionValidator import SimplePrescriptionValidator
from SimplePasswordValidator import SimplePasswordValidator
from StrongPasswordValidator import StrongPasswordValidator
from SpecificPasswordValidator import SpecificPasswordValidator
from Drug import Drug
from Prescription import Prescription

class TestSimpleDrugValidatorUnit(unittest.TestCase):
    def setUp(self):
        self.validator = SimpleDrugValidator()

    def test_check_compatibility_same_category(self):
        drug1 = Drug("Аспирин", "500mg", 100.0, "BATCH001", "room temp", "Обезболивающее")
        drug2 = Drug("Парацетамол", "500mg", 80.0, "BATCH002", "room temp", "Обезболивающее")
        result = self.validator.check_compatibility(drug1, drug2)
        self.assertEqual(result, "Совместимо")

    def test_check_compatibility_different_category(self):
        drug1 = Drug("Аспирин", "500mg", 100.0, "BATCH001", "room temp", "Обезболивающее")
        drug2 = Drug("Витамин C", "500mg", 50.0, "BATCH002", "room temp", "Витамин")
        result = self.validator.check_compatibility(drug1, drug2)
        self.assertEqual(result, "Несовместимо")

class TestSimplePrescriptionValidatorUnit(unittest.TestCase):
    def setUp(self):
        self.validator = SimplePrescriptionValidator()

    def test_is_valid_fresh_prescription(self):
        prescription = Prescription("Доктор", "Пациент")
        self.assertTrue(self.validator.is_valid(prescription))

    def test_verify_signature_with_signature(self):
        prescription = Prescription("Доктор", "Пациент", has_signature=True)
        try:
            self.validator.verify_signature(prescription)
            self.assertTrue(True)
        except:
            self.fail("verify_signature вызвал исключение")

class TestPasswordValidatorsUnit(unittest.TestCase):
    def test_simple_validator_short_password(self):
        validator = SimplePasswordValidator()
        self.assertFalse(validator.validate("123"))

    def test_simple_validator_long_password(self):
        validator = SimplePasswordValidator()
        self.assertTrue(validator.validate("123456"))

    def test_strong_validator_weak_password(self):
        validator = StrongPasswordValidator()
        self.assertFalse(validator.validate("password"))

    def test_strong_validator_strong_password(self):
        validator = StrongPasswordValidator()
        self.assertTrue(validator.validate("Password123"))

    def test_specific_validator_correct_password(self):
        validator = SpecificPasswordValidator()
        self.assertTrue(validator.validate("alina_top"))

    def test_specific_validator_incorrect_password(self):
        validator = SpecificPasswordValidator()
        self.assertFalse(validator.validate("wrong_password"))