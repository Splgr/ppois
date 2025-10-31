import unittest
from datetime import datetime, timedelta
from Batch import Batch
from Stock import Stock
from Warehouse import Warehouse
from Company import Company
from Branch import Branch
from Doctor import Doctor
from Patient import Patient
from PatientRecord import PatientRecord
from BasicDoctorPrescriptionService import BasicDoctorPrescriptionService
from LoyaltyProgram import LoyaltyProgram
from SalesAnalytics import SalesAnalytics
from DeliveryService import DeliveryService
from SecuritySystem import SecuritySystem
from MarketingCampaign import MarketingCampaign
from QualityControl import QualityControl
from Drug import Drug
from Employee import Employee
from Manager import Manager
from exceptions import BatchRecallError, ExpiredDrugError, InvalidPrescriptionError

class TestBatchUnit(unittest.TestCase):
    def test_batch_creation(self):
        batch = Batch("BATCH001", datetime(2023, 1, 1))
        self.assertEqual(batch.batch_id, "BATCH001")

    def test_batch_add_drug(self):
        batch = Batch("BATCH001", datetime(2023, 1, 1))
        drug = Drug("Аспирин", "500mg", 100.0, "BATCH001", "room temp", "Обезболивающее")
        batch.add_drug(drug)
        self.assertEqual(batch.get_drug_count(), 1)

    def test_batch_recall_success(self):
        batch = Batch("BATCH001", datetime(2023, 1, 1))
        with self.assertRaises(BatchRecallError) as context:
            batch.recall()
        self.assertIn("Партия BATCH001 отозвана", str(context.exception))
        self.assertTrue(batch._is_recalled)

    def test_batch_inspect_quality_good(self):
        batch = Batch("BATCH001", datetime(2023, 1, 1))
        result = batch.inspect_quality()
        self.assertIn("Партия BATCH001 в хорошем состоянии", result)

    def test_batch_inspect_quality_recalled(self):
        batch = Batch("BATCH001", datetime(2023, 1, 1))
        try:
            batch.recall()
        except BatchRecallError:
            pass
        result = batch.inspect_quality()
        self.assertEqual(result, "Партия отозвана")

    def test_batch_add_drug_to_recalled_raises_error(self):
        batch = Batch("BATCH001", datetime(2023, 1, 1))
        try:
            batch.recall()
        except BatchRecallError:
            pass
        drug = Drug("Аспирин", "500mg", 100.0, "BATCH001", "room temp", "Обезболивающее")
        with self.assertRaises(BatchRecallError) as context:
            batch.add_drug(drug)
        self.assertIn("Нельзя добавить лекарство в отозванную партию", str(context.exception))

class TestStockUnit(unittest.TestCase):
    def test_stock_creation(self):
        stock = Stock("STOCK001", "Холодильник", 100)
        self.assertEqual(stock.stock_id, "STOCK001")
        self.assertEqual(stock.capacity, 100)

class TestWarehouseUnit(unittest.TestCase):
    def test_warehouse_creation(self):
        warehouse = Warehouse("WARE001", 1000, True)
        self.assertEqual(warehouse.warehouse_id, "WARE001")
        self.assertTrue(warehouse.temperature_control)

class TestCompanyUnit(unittest.TestCase):
    def test_company_creation(self):
        company = Company("Фармакорп", 2000)
        self.assertEqual(company.name, "Фармакорп")
        self.assertEqual(company.founded_year, 2000)

    def test_company_hire_employee_success(self):
        company = Company("Фармакорп", 2000)
        employee = Manager("Менеджер", "Менеджер", 50000.0, "EMP001", datetime.now(), "Отдел", 5, 100000.0)
        company.hire_employee(employee)
        self.assertEqual(company.get_employee_count(), 1)

    def test_company_launch_product_success(self):
        company = Company("Фармакорп", 2000)
        drug = Drug("Аспирин", "500mg", 100.0, "BATCH001", "room temp", "Обезболивающее")
        company.launch_product(drug)
        self.assertEqual(company._products[0].name, "Аспирин")

    def test_company_add_revenue(self):
        company = Company("Фармакорп", 2000)
        company.add_revenue(50000.0)
        self.assertEqual(company.revenue, 50000.0)

    def test_company_calculate_profit(self):
        company = Company("Фармакорп", 2000)
        company.add_revenue(100000.0)
        profit = company.calculate_profit(40000.0)
        self.assertEqual(profit, 60000.0)

class TestBranchUnit(unittest.TestCase):
    def test_branch_creation(self):
        company = Company("Фармакорп", 2000)
        branch = Branch("Москва", company)
        self.assertEqual(branch.location, "Москва")

class TestDoctorUnit(unittest.TestCase):
    def test_doctor_creation(self):
        doctor = Doctor("Доктор Смит", "Кардиолог", "LIC123")
        self.assertEqual(doctor.name, "Доктор Смит")
        self.assertEqual(doctor.specialty, "Кардиолог")

    def test_doctor_create_prescription_success(self):
        doctor = Doctor("Доктор Смит", "Кардиолог", "LIC123")
        patient = Patient("Иван Иванов", 30, "Гипертония")
        doctor.add_patient(patient)
        prescription = doctor.create_prescription(patient, "Аспирин", "500mg")
        self.assertEqual(prescription.doctor_name, "Доктор Смит")
        self.assertEqual(prescription.patient_name, "Иван Иванов")

    def test_doctor_create_prescription_patient_not_found(self):
        doctor = Doctor("Доктор Смит", "Кардиолог", "LIC123")
        patient = Patient("Иван Иванов", 30, "Гипертония")
        with self.assertRaises(Exception) as context:
            doctor.create_prescription(patient, "Аспирин", "500mg")
        self.assertIn("Пациент не найден у этого врача", str(context.exception))

    def test_doctor_add_and_remove_patient(self):
        doctor = Doctor("Доктор Смит", "Кардиолог", "LIC123")
        patient = Patient("Иван Иванов", 30, "Гипертония")
        doctor.add_patient(patient)
        self.assertEqual(len(doctor.patients), 1)
        doctor.remove_patient(patient)
        self.assertEqual(len(doctor.patients), 0)

    def test_doctor_get_patient_statistics(self):
        doctor = Doctor("Доктор Смит", "Кардиолог", "LIC123")
        patient1 = Patient("Иван Иванов", 30, "Гипертония")
        patient2 = Patient("Мария Петрова", 25, "Астма")
        doctor.add_patient(patient1)
        doctor.add_patient(patient2)
        stats = doctor.get_patient_statistics()
        self.assertEqual(stats['total_patients'], 2)
        self.assertEqual(stats['average_age'], 27.5)

class TestPatientUnit(unittest.TestCase):
    def test_patient_creation(self):
        patient = Patient("Иван Иванов", 30, "Гипертония")
        self.assertEqual(patient.name, "Иван Иванов")
        self.assertEqual(patient.age, 30)

class TestPatientRecordUnit(unittest.TestCase):
    def test_patient_record_creation(self):
        record = PatientRecord("REC001", "История болезней", "Иван Иванов")
        self.assertEqual(record.rec_id, "REC001")

class TestBasicDoctorPrescriptionServiceUnit(unittest.TestCase):
    def test_write_prescription(self):
        service = BasicDoctorPrescriptionService()
        patient = Patient("Иван Иванов", 30, "Гипертония")
        prescription = service.write_prescription(patient, "Аспирин")
        self.assertEqual(prescription.patient_name, "Иван Иванов")

class TestLoyaltyProgramUnit(unittest.TestCase):
    def test_loyalty_program_creation(self):
        program = LoyaltyProgram("Золотая карта", 10, 5.0)
        self.assertEqual(program.program_name, "Золотая карта")

class TestSalesAnalyticsUnit(unittest.TestCase):
    def test_sales_analytics_creation(self):
        analytics = SalesAnalytics()
        self.assertEqual(analytics._sales_target, 100000.0)

class TestDeliveryServiceUnit(unittest.TestCase):
    def test_delivery_service_creation(self):
        delivery = DeliveryService("Быстрая доставка", 200.0, 50)
        self.assertEqual(delivery.service_name, "Быстрая доставка")

class TestSecuritySystemUnit(unittest.TestCase):
    def test_security_system_creation(self):
        security = SecuritySystem()
        self.assertFalse(security._alarm_status)

class TestMarketingCampaignUnit(unittest.TestCase):
    def test_marketing_campaign_creation(self):
        campaign = MarketingCampaign("Летняя распродажа", 50000.0, "Молодежь")
        self.assertEqual(campaign.campaign_name, "Летняя распродажа")

class TestQualityControlUnit(unittest.TestCase):
    def test_quality_control_creation(self):
        qc = QualityControl()
        batch = Batch("BATCH001", datetime(2023, 1, 1))
        result = qc.perform_inspection(batch)
        self.assertTrue(result)