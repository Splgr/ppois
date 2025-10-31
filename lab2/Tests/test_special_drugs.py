import unittest
from Antibiotic import Antibiotic
from Painkiller import Painkiller
from Vitamin import Vitamin
from Vaccine import Vaccine
from TestSubject import TestSubject

class TestAntibioticUnit(unittest.TestCase):
    def test_antibiotic_creation(self):
        ab = Antibiotic("Амоксициллин", "250mg", 300.0, "BATCH004", "room temp", "широкий спектр")
        self.assertEqual(ab.spectrum, "широкий спектр")
        self.assertEqual(ab.category, "Антибиотик")

    def test_check_resistance(self):
        ab = Antibiotic("Амоксициллин", "250mg", 300.0, "BATCH004", "room temp", "широкий спектр")
        subject = TestSubject("SUBJ001")
        result = ab.check_resistance(subject)
        self.assertIn("Резистентность к широкий спектр проверена", result)
        self.assertTrue(ab._resistance_checked)

    def test_administer_without_resistance_check(self):
        ab = Antibiotic("Амоксициллин", "250mg", 300.0, "BATCH004", "room temp", "широкий спектр")
        subject = TestSubject("SUBJ001")
        result = ab.administer(subject)
        self.assertEqual(result, "Сначала проверьте резистентность")

    def test_administer_with_resistance_check(self):
        ab = Antibiotic("Амоксициллин", "250mg", 300.0, "BATCH004", "room temp", "широкий спектр")
        subject = TestSubject("SUBJ001")
        ab.check_resistance(subject)
        result = ab.administer(subject)
        self.assertIn("Антибиотик Амоксициллин введен", result)

class TestPainkillerUnit(unittest.TestCase):
    def test_painkiller_creation(self):
        pk = Painkiller("Ибупрофен", "400mg", 120.0, "BATCH005", "room temp", "средняя")
        self.assertEqual(pk.strength, "средняя")
        self.assertEqual(pk.category, "Обезболивающее")

    def test_relieve_pain(self):
        pk = Painkiller("Ибупрофен", "400mg", 120.0, "BATCH005", "room temp", "средняя")
        subject = TestSubject("SUBJ002")
        subject.pain = True
        result = pk.relieve_pain(subject)
        self.assertIn("Боль снята с помощью средняя обезболивающего", result)  # ← ИСПРАВЛЕНО
        self.assertFalse(subject.pain)

class TestVitaminUnit(unittest.TestCase):
    def test_vitamin_creation(self):
        vit = Vitamin("Витамин D", "1000IU", 80.0, "BATCH006", "room temp", "D")
        self.assertEqual(vit.vitamin_type, "D")
        self.assertEqual(vit.category, "Витамин")
    
    def test_boost_health(self):
        vit = Vitamin("Витамин D", "1000IU", 80.0, "BATCH006", "room temp", "D")
        subject = TestSubject("SUBJ003")
        result = vit.boost_health(subject)
        self.assertIn("Здоровье улучшено витамином D", result)
        self.assertEqual(subject.health, 6)  # 5 + 1 = 6
        self.assertEqual(subject.vitamins, 7)  # 5 + 1 (administer_drug) + 1 (boost_health) = 7


class TestVaccineUnit(unittest.TestCase):
    def test_vaccine_creation(self):
        vac = Vaccine("COVID-19", "0.5ml", 500.0, "BATCH007", "холод", 2)
        self.assertEqual(vac.doses_required, 2)
        self.assertEqual(vac.category, "Вакцина")

    def test_administer_first_dose(self):
        vac = Vaccine("COVID-19", "0.5ml", 500.0, "BATCH007", "холод", 2)
        subject = TestSubject("SUBJ004")
        result = vac.administer_dose(subject)
        self.assertEqual(result, "Введена доза 1 из 2")
        self.assertEqual(vac._doses_administered, 1)

    def test_administer_all_doses(self):
        vac = Vaccine("COVID-19", "0.5ml", 500.0, "BATCH007", "холод", 2)
        subject = TestSubject("SUBJ005")
        vac.administer_dose(subject)
        result = vac.administer_dose(subject)
        self.assertEqual(result, "Вакцинация завершена")
        self.assertTrue(subject.vaccinated)
        self.assertEqual(vac._doses_administered, 2)

    def test_get_vaccination_progress(self):
        vac = Vaccine("COVID-19", "0.5ml", 500.0, "BATCH007", "холод", 2)
        subject = TestSubject("SUBJ006")
        vac.administer_dose(subject)
        progress = vac.get_vaccination_progress()
        self.assertEqual(progress['doses_administered'], 1)
        self.assertEqual(progress['doses_required'], 2)
        self.assertFalse(progress['completed'])