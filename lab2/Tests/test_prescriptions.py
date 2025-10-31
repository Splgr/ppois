import unittest
from datetime import datetime, timedelta
from Prescription import Prescription
from PrescriptionService import PrescriptionService 
from exceptions import InvalidPrescriptionError

class TestPrescriptionUnit(unittest.TestCase):
    
    def test_prescription_creation_valid(self):
        prescription = Prescription("Доктор Иванов", "Пациент Петров")
        self.assertEqual(prescription.doctor_name, "Доктор Иванов")
        self.assertEqual(prescription.patient_name, "Пациент Петров")
        self.assertFalse(prescription.is_used)

    def test_prescription_creation_raises_error_empty_doctor(self):
        with self.assertRaises(InvalidPrescriptionError) as context:
            Prescription("", "Пациент Петров")
        self.assertIn("Имя врача обязательно", str(context.exception))

    def test_prescription_creation_raises_error_empty_patient(self):
        with self.assertRaises(InvalidPrescriptionError) as context:
            Prescription("Доктор Иванов", "")
        self.assertIn("Имя пациента обязательно", str(context.exception))

    def test_prescription_is_valid_when_fresh(self):
        prescription = Prescription("Доктор Иванов", "Пациент Петров")
        self.assertTrue(prescription.issue_date <= datetime.now())

    def test_prescription_with_drug_name(self):
        prescription = Prescription("Доктор Иванов", "Пациент Петров", drug_name="Аспирин")
        self.assertEqual(prescription.drug_name, "Аспирин")

class TestPrescriptionServiceUnit(unittest.TestCase):
    """Unit тесты для PrescriptionService"""
    
    def test_mark_as_used_success(self):
        prescription = Prescription("Доктор Иванов", "Пациент Петров")
        service = PrescriptionService()
        
        service.mark_as_used(prescription)
        
        self.assertTrue(prescription.is_used)

    def test_mark_as_used_raises_error_when_already_used(self):
        prescription = Prescription("Доктор Иванов", "Пациент Петров")
        service = PrescriptionService()
        service.mark_as_used(prescription)
        
        with self.assertRaises(InvalidPrescriptionError) as context:
            service.mark_as_used(prescription)
        self.assertIn("Рецепт уже использован", str(context.exception))