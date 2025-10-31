from datetime import datetime, timedelta
from typing import Optional
from enum import Enum
from typing import List
from typing import Dict 
from abc import ABC, abstractmethod


class InvalidDrugError(Exception): pass
class SupplierNotFoundError(Exception): pass
class CustomerNotRegisteredError(Exception): pass
class InsufficientPointsError(Exception): pass
class InsufficientStockError(Exception): pass
class ExpiredDrugError(Exception): pass
class InvalidPaymentError(Exception): pass
class OrderCancellationError(Exception): pass
class ShipmentDelayError(Exception): pass
class EmployeeAccessDeniedError(Exception): pass
class InvalidPrescriptionError(Exception): pass
class WarehouseCapacityExceededError(Exception): pass
class BatchRecallError(Exception): pass


class Drug:
    def __init__(
        self,
        name: str,
        dosage: str,
        price: float,
        batch_code: str,
        storage_conditions: str,
        category: str,
        manufacture_date: Optional[datetime] = None,
        expiration_days: int = 1080
    ):
        if not all([name, dosage, batch_code, category]):
            raise InvalidDrugError("Обязательные поля не заполнены")
        if price < 0:
            raise InvalidDrugError("Цена не может быть отрицательной")

        self.name = name
        self.dosage = dosage
        self.price = price
        self.batch_code = batch_code
        self.storage_conditions = storage_conditions
        self.category = category
        self.manufacture_date = manufacture_date or datetime.now()
        self.expiration_days = expiration_days
        self._expiration_date = self.manufacture_date + timedelta(days=expiration_days)

    @property
    def expiration_date(self) -> datetime:
        return self._expiration_date


class DrugPricingService:
    def apply_discount(self, drug: Drug, percent: float) -> None:
        if not 0 <= percent <= 100:
            raise InvalidDrugError("Скидка должна быть от 0 до 100%")
        drug.price = round(drug.price * (1 - percent / 100), 2)

    def calculate_tax(self, drug: Drug, tax_rate: float) -> float:
        return round(drug.price * (tax_rate / 100), 2)

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

class PrescriptionService:
    def mark_as_used(self, prescription: Prescription) -> None:
        if prescription.is_used:
            raise InvalidPrescriptionError("Рецепт уже использован")
        prescription._used = True

class DrugValidator(ABC):
    @abstractmethod
    def validate(self, drug: Drug) -> str: ...

    @abstractmethod
    def check_compatibility(self, drug1: Drug, drug2: Drug) -> str: ...


class PrescriptionValidator(ABC):
    @abstractmethod
    def is_valid(self, prescription: Prescription) -> bool: ...

    @abstractmethod
    def verify_signature(self, prescription: Prescription) -> None: ...


class PrescriptionLogger(ABC):
    @abstractmethod
    def log_use(self, prescription: Prescription) -> None: ...


class SimpleDrugValidator(DrugValidator):
    def validate(self, drug: Drug) -> str:
        if datetime.now() > drug.expiration_date:
            days = (datetime.now() - drug.expiration_date).days
            raise ExpiredDrugError(f"Срок годности истёк {days} дней назад")
        if "холод" in drug.storage_conditions.lower():
            raise InvalidDrugError("Требуется охлаждение")
        days_left = (drug.expiration_date - datetime.now()).days
        return f"Валидно. Осталось {days_left} дней"

    def check_compatibility(self, drug1: Drug, drug2: Drug) -> str:
        return "Совместимо" if drug1.category == drug2.category else "Несовместимо"


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


class ConsolePrescriptionLogger(PrescriptionLogger):
    def log_use(self, prescription: Prescription) -> None:
        print(f"[ЛОГ] Рецепт использован: {prescription.patient_name}, врач: {prescription.doctor_name}")


class PrescriptionDrug(Drug):
    def __init__(
        self, name, dosage, price, batch_code, storage_conditions, category,
        manufacture_date=None, expiration_days=1080
    ):
        super().__init__(name, dosage, price, batch_code, storage_conditions, category,
                         manufacture_date, expiration_days)
        self.requires_prescription = True


class OverTheCounterDrug(Drug):
    def __init__(
        self, name, dosage, price, batch_code, storage_conditions, category,
        manufacture_date=None, expiration_days=1080
    ):
        super().__init__(name, dosage, price, batch_code, storage_conditions, category,
                         manufacture_date, expiration_days)
        self.requires_prescription = False

    def extend_shelf_life(self, days: int) -> None:
        if days <= 0:
            raise InvalidDrugError("Дни должны быть положительными")
        self._expiration_date += timedelta(days=days)

    def recommend_alternative(self, name: str, category: str) -> str:
        if self.name != name and self.category == category:
            return f"Рекомендуем другие препараты категории '{category}'"
        return "Альтернативы не найдены"


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

        self.prescription_validator.verify_signature(prescription)  # ✅ ИСПРАВЛЕНО!
        self.logger.log_use(prescription)

        return f"Выдано: {drug.name} ({drug.dosage}) — {prescription.patient_name}"

    def sell_otc_drug(self, drug: OverTheCounterDrug, stock: int = 1) -> str:
        if stock < 1:
            raise InsufficientStockError(f"Нет в наличии: {drug.name}")
        self.drug_validator.validate(drug)
        return f"Продано без рецепта: {drug.name}"


class Status(Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    PENDING = "pending"
    SUSPENDED = "suspended"
    TERMINATED = "terminated"
    EXPIRED = "expired"

class PasswordValidator(ABC):
    @abstractmethod
    def validate(self, password: str) -> bool: 
        pass

class CustomerRepository(ABC):
    @abstractmethod
    def get_by_id(self, customer_id) -> 'Customer': 
        pass

class PerformanceEvaluator(ABC):
    @abstractmethod
    def evaluate(self, supplier: 'Supplier') -> bool: 
        pass

class Coupon(ABC):
    @abstractmethod
    def apply(self, amount: float) -> float: 
        pass
    
    @abstractmethod
    def is_valid(self) -> bool:
        pass


class SimplePasswordValidator(PasswordValidator):
    def validate(self, password: str) -> bool:
        return len(password) >= 6

class StrongPasswordValidator(PasswordValidator):
    def validate(self, password: str) -> bool:
        if len(password) < 8:
            return False
        if not any(c.isupper() for c in password):
            return False
        if not any(c.isdigit() for c in password):
            return False
        return True

class SpecificPasswordValidator(PasswordValidator):
    def validate(self, password: str) -> bool:
        correct_password = "alina_top"
        return password == correct_password

class DefaultPerformanceEvaluator(PerformanceEvaluator):
    def evaluate(self, supplier: 'Supplier') -> bool:
        return supplier.rating > 4

class PercentageCoupon(Coupon):
    def __init__(self, discount_percent: float, expiry_date: datetime = None):
        if not 0 < discount_percent <= 100:
            raise Exception("Процент скидки должен быть от 0 до 100")
        self.discount_percent = discount_percent
        self.expiry_date = expiry_date
    
    def apply(self, amount: float) -> float:
        return amount * (1 - self.discount_percent / 100)
    
    def is_valid(self) -> bool:
        if self.expiry_date and datetime.now() > self.expiry_date:
            return False
        return True

class FixedAmountCoupon(Coupon):
    def __init__(self, discount_amount: float, min_order_amount: float = 0, expiry_date: datetime = None):
        if discount_amount <= 0:
            raise Exception("Сумма скидки должна быть положительной")
        self.discount_amount = discount_amount
        self.min_order_amount = min_order_amount
        self.expiry_date = expiry_date
    
    def apply(self, amount: float) -> float:
        new_amount = amount - self.discount_amount
        return max(new_amount, 0)
    
    def is_valid(self) -> bool:
        if self.expiry_date and datetime.now() > self.expiry_date:
            return False
        return True

class NoCoupon(Coupon):
    def apply(self, amount: float) -> float:
        return amount
    
    def is_valid(self) -> bool:
        return True

class CouponService:
    @staticmethod
    def validate_and_apply(coupon: Coupon, order_amount: float) -> float:
        if not coupon.is_valid():
            raise Exception("Купон недействителен")
        
        if isinstance(coupon, FixedAmountCoupon) and order_amount < coupon.min_order_amount:
            raise Exception(f"Минимальная сумма заказа: {coupon.min_order_amount}")
            
        return coupon.apply(order_amount)
    
    @staticmethod
    def create_percentage_coupon(discount_percent: float, days_valid: int = 30) -> PercentageCoupon:
        expiry_date = datetime.now() + timedelta(days=days_valid)
        return PercentageCoupon(discount_percent, expiry_date)
    
    @staticmethod
    def create_fixed_coupon(discount_amount: float, min_order_amount: float = 0, days_valid: int = 30) -> FixedAmountCoupon:
        expiry_date = datetime.now() + timedelta(days=days_valid)
        return FixedAmountCoupon(discount_amount, min_order_amount, expiry_date)

class Supplier:
    def __init__(
        self,
        name: str,
        contact: str,
        rating: float,
        contract_status: Status,
        supply_frequency: str,
        performance_evaluator: PerformanceEvaluator = None
    ):
        self.name = name
        self.contact = contact
        self.rating = rating
        self.contract_status = contract_status
        self.supply_frequency = supply_frequency
        self.drugs_supplied: List[Drug] = []
        self._performance_evaluator = performance_evaluator or DefaultPerformanceEvaluator()

    def add_drug(self, drug: Drug) -> None:
        self.drugs_supplied.append(drug)
        print(f"Лекарство {drug.name} добавлено к поставщику {self.name}")

    def negotiate_terms(self) -> None:
        if self.contract_status == Status.ACTIVE and self.rating >= 4:
            print(f"Условия согласованы с поставщиком {self.name}")

    def evaluate_performance(self) -> bool:
        return self._performance_evaluator.evaluate(self)

    def __str__(self) -> str:
        return f"Поставщик {self.name}, рейтинг: {self.rating}, статус: {self.contract_status.value}"

class Customer:
    def __init__(
        self,
        name: str,
        address: str,
        email: str,
        phone: str,
        budget: float
    ):
        self.name = name
        self.address = address
        self.email = email
        self.phone = phone
        self.budget = budget

class Employee(ABC):
    def __init__(
        self,
        name: str,
        position: str,
        salary: float,
        employee_id: str,
        hire_date: datetime
    ):
        self.name = name
        self.position = position
        self.salary = salary
        self.employee_id = employee_id
        self.hire_date = hire_date

    def check_password(self, password: str, validator: PasswordValidator) -> None:
        if not validator.validate(password):
            raise Exception("Доступ запрещён")
        print(f"Пароль для {self.name} подтвержден")

    @abstractmethod
    def attend_training(self) -> None: 
        pass

class CustomerManagerMixin:
    def __init__(self):
        self.managed_customers: List[Customer] = []

    def assign_customer(self, customer: Customer) -> None:
        self.managed_customers.append(customer)
        print(f"Клиент {customer.name} назначен {getattr(self, 'name', 'сотруднику')}")

class Manager(Employee, CustomerManagerMixin):
    def __init__(
        self,
        name: str,
        position: str,
        salary: float,
        employee_id: str,
        hire_date: datetime,
        department: str,
        team_size: int,
        budget: float
    ):
        Employee.__init__(self, name, position, salary, employee_id, hire_date)
        CustomerManagerMixin.__init__(self)
        self.department = department
        self.team_size = team_size
        self.budget = budget

    def approve_order(self, order: 'Order') -> None:
        if order.status != "Pending":
            raise Exception("Можно утвердить только ожидающий заказ")
        order.approve()
        print(f"Заказ {order.order_id} утвержден менеджером {self.name}")

    def allocate_budget(self, amount: float) -> None:
        if amount > self.budget:
            raise Exception("Недостаточно бюджета")
        self.budget -= amount
        print(f"Бюджет распределён: ${amount}. Остаток: ${self.budget}")

    def attend_training(self) -> None:
        print("Тренинг для менеджеров посещен")
        self.salary += 1000
        print(f"Новая зарплата: {self.salary}")

    def __str__(self) -> str:
        return f"Менеджер {self.name}, отдел: {self.department}, команда: {self.team_size} чел."

class SalesRepresentative(Employee, CustomerManagerMixin):
    def __init__(
        self,
        name: str,
        position: str,
        salary: float,
        employee_id: str,
        hire_date: datetime,
        sales_quota: float
    ):
        Employee.__init__(self, name, position, salary, employee_id, hire_date)
        CustomerManagerMixin.__init__(self)
        self.sales_quota = sales_quota

    def attend_training(self) -> None:
        print("Тренинг по продажам посещен")
        self.salary += 500
        print(f"Новая зарплата: {self.salary}")

    def __str__(self) -> str:
        return f"Продавец {self.name}, квота: {self.sales_quota}₽"

class Order:
    def __init__(
        self,
        order_id: str,
        order_date: datetime,
        priority: str = "Normal"
    ):
        self.order_id = order_id
        self.order_date = order_date
        self.priority = priority
        self._customer = None
        self._drugs: List[Drug] = []
        self._status = "Pending"
        self._total_amount = 0.0
        self._applied_coupon: Coupon = NoCoupon()
        self._shipping_cost = 200.0

    @property
    def total_amount(self) -> float:
        return self._total_amount

    @property
    def status(self) -> str:
        return self._status

    @property
    def customer(self):
        return self._customer

    @property
    def drugs(self) -> List[Drug]:
        return self._drugs.copy()

    @property
    def applied_coupon(self) -> Coupon:
        return self._applied_coupon

    @property
    def discount_amount(self) -> float:
        base_amount = sum(drug.price for drug in self._drugs)
        if isinstance(self._applied_coupon, NoCoupon):
            return 0.0
        return base_amount - self._applied_coupon.apply(base_amount)

    def set_customer(self, customer: Customer) -> None:
        if self._customer:
            raise Exception("Клиент уже назначен")
        self._customer = customer

    def remove_customer(self) -> None:
        if self._status != "Pending":
            raise Exception("Нельзя удалить клиента из активного заказа")
        self._customer = None

    def add_drug(self, drug: Drug) -> None:
        if self._status in ["Shipped", "Cancelled"]:
            raise OrderCancellationError("Нельзя менять завершённый заказ")
        
        self._drugs.append(drug)
        self._recalculate_total()

    def remove_drug(self, drug: Drug) -> None:
        if self._status in ["Shipped", "Cancelled"]:
            raise OrderCancellationError("Нельзя менять завершённый заказ")
        if drug not in self._drugs:
            raise Exception("Лекарство не в заказе")
            
        self._drugs.remove(drug)
        self._recalculate_total()
        
        if not self._drugs:
            self._status = "Cancelled"

    def _recalculate_total(self) -> None:
        base_amount = sum(drug.price for drug in self._drugs)
        
        if isinstance(self._applied_coupon, NoCoupon):
            discounted_amount = base_amount
        else:
            try:
                discounted_amount = CouponService.validate_and_apply(self._applied_coupon, base_amount)
            except Exception:
                # Если купон стал невалидным, сбрасываем его
                self._applied_coupon = NoCoupon()
                discounted_amount = base_amount
        
        self._total_amount = discounted_amount + self._shipping_cost

    def apply_coupon(self, coupon: Coupon) -> None:
        if self._status != "Pending":
            raise Exception("Купон можно применить только к ожидающему заказу")
        
        base_amount = sum(drug.price for drug in self._drugs)
        
        try:
            CouponService.validate_and_apply(coupon, base_amount)
            self._applied_coupon = coupon
            self._recalculate_total()
        except Exception as e:
            raise Exception(f"Не удалось применить купон: {e}")

    def remove_coupon(self) -> None:
        if self._status != "Pending":
            raise Exception("Купон можно удалить только из ожидающего заказа")
        self._applied_coupon = NoCoupon()
        self._recalculate_total()

    def approve(self) -> None:
        if self._status != "Pending":
            raise Exception("Можно утвердить только ожидающий заказ")
        if not self._drugs:
            raise Exception("Нельзя утвердить пустой заказ")
            
        self._status = "Approved"

    def cancel(self) -> None:
        if self._status == "Shipped":
            raise Exception("Нельзя отменить отгруженный заказ")
        self._status = "Cancelled"

    def mark_as_shipped(self) -> None:
        if self._status != "Approved":
            raise Exception("Можно отгрузить только утверждённый заказ")
        self._status = "Shipped"

    def expedite(self) -> None:
        if self._status != "Pending":
            raise Exception("Можно ускорить только ожидающий заказ")
        self.priority = "High"

    def normalize_priority(self) -> None:
        self.priority = "Normal"

    def is_empty(self) -> bool:
        return len(self._drugs) == 0

    def contains_drug(self, drug: Drug) -> bool:
        return drug in self._drugs

    def get_drug_count(self) -> int:
        return len(self._drugs)

    def __str__(self) -> str:
        customer_name = self._customer.name if self._customer else "Не назначен"
        coupon_info = f", купон: {type(self._applied_coupon).__name__}" if not isinstance(self._applied_coupon, NoCoupon) else ""
        discount_info = f", скидка: {self.discount_amount}₽" if self.discount_amount > 0 else ""
        
        return (f"Заказ {self.order_id}: {self.total_amount}₽"
                f"{discount_info}, статус: {self.status}{coupon_info}, "
                f"клиент: {customer_name}, лекарств: {len(self._drugs)}")






class PatientRecordRepository(ABC):
    @abstractmethod
    def get_record(self, patient_name: str) -> 'PatientRecord': 
        pass
    
    @abstractmethod
    def update_record(self, record: 'PatientRecord') -> None:
        pass

class DoctorPrescriptionService(ABC):
    @abstractmethod
    def write_prescription(self, patient: 'Patient', drug_name: str) -> Prescription:
        pass

class SimplePatientRecordRepository(PatientRecordRepository):
    def __init__(self):
        self._records: Dict[str, PatientRecord] = {}
    
    def get_record(self, patient_name: str) -> 'PatientRecord':
        if patient_name not in self._records:
            raise Exception("Медицинская карта не найдена")
        return self._records[patient_name]
    
    def update_record(self, record: 'PatientRecord') -> None:
        self._records[record.patient_name] = record

class BasicDoctorPrescriptionService(DoctorPrescriptionService):
    def write_prescription(self, patient: 'Patient', drug_name: str) -> Prescription:
        if not patient.name.strip():
            raise InvalidPrescriptionError("Имя пациента обязательно")
        
        prescription = Prescription(
            doctor_name="Доктор Смит",  # В реальности передавать врача
            patient_name=patient.name,
            drug_name=drug_name
        )
        patient.add_prescription(prescription)
        return prescription

class PatientRecord:
    def __init__(self, rec_id: str, details: str, patient_name: str):
        self.rec_id = rec_id
        self.details = details
        self.patient_name = patient_name
        self.authorized_employee = None
        self._access_log: List[str] = []

    def update_details(self, new_details: str) -> None:
        """Обновляет детали карты (SRP)"""
        self.details = new_details
        self._access_log.append(f"Обновлено: {datetime.now()}")

    def grant_access(self, employee: 'Employee') -> None:
        """Предоставляет доступ сотруднику"""
        self.authorized_employee = employee
        self._access_log.append(f"Доступ предоставлен {employee.name}: {datetime.now()}")

    def revoke_access(self) -> None:
        """Отзывает доступ"""
        self.authorized_employee = None
        self._access_log.append(f"Доступ отозван: {datetime.now()}")

    def get_access_log(self) -> List[str]:
        """Возвращает лог доступа (неизменяемый)"""
        return self._access_log.copy()

class Patient:
    def __init__(self, name: str, age: int, medical_history: str):
        if age < 0 or age > 150:
            raise Exception("Некорректный возраст")
        
        self.name = name
        self.age = age
        self.medical_history = medical_history
        self.prescriptions: List[Prescription] = []
        self._allergies: List[str] = []

    def add_prescription(self, prescription: Prescription) -> None:
        """Добавляет рецепт (SRP)"""
        self.prescriptions.append(prescription)

    def add_allergy(self, allergy: str) -> None:
        """Добавляет аллергию"""
        self._allergies.append(allergy.lower())

    def has_allergy_to(self, drug_category: str) -> bool:
        """Проверяет наличие аллергии на категорию лекарств"""
        return any(allergy in drug_category.lower() for allergy in self._allergies)

    def get_active_prescriptions(self) -> List[Prescription]:
        """Возвращает активные рецепты"""
        return [p for p in self.prescriptions if not p.is_used]

class Doctor:
    def __init__(self, name: str, specialty: str, license: str):
        if not license.strip():
            raise Exception("Лицензия обязательна")
        
        self.name = name
        self.specialty = specialty
        self.license = license
        self.patients: List[Patient] = []

    def add_patient(self, patient: Patient) -> None:
        """Добавляет пациента к врачу"""
        if patient in self.patients:
            raise Exception("Пациент уже у этого врача")
        self.patients.append(patient)

    def remove_patient(self, patient: Patient) -> None:
        """Удаляет пациента"""
        if patient in self.patients:
            self.patients.remove(patient)

    def create_prescription(self, patient: Patient, drug_name: str, dosage: str) -> Prescription:
        """Создает рецепт (SRP)"""
        if patient not in self.patients:
            raise Exception("Пациент не найден у этого врача")
        
        if patient.has_allergy_to(drug_name):
            raise InvalidPrescriptionError(f"У пациента аллергия на {drug_name}")
        
        return Prescription(
            doctor_name=self.name,
            patient_name=patient.name,
            drug_name=drug_name
        )

    def get_patient_statistics(self) -> dict:
        """Статистика по пациентам"""
        return {
            'total_patients': len(self.patients),
            'patients_with_prescriptions': len([p for p in self.patients if p.prescriptions]),
            'average_age': sum(p.age for p in self.patients) / len(self.patients) if self.patients else 0
        }

class Company:
    def __init__(self, name: str, founded_year: int):
        current_year = datetime.now().year
        if founded_year > current_year:
            raise Exception("Год основания не может быть в будущем")
        
        self.name = name
        self.founded_year = founded_year
        self._revenue = 0.0
        self._employees: List[Employee] = []
        self._products: List[Drug] = []

    @property
    def revenue(self) -> float:
        return self._revenue

    def add_revenue(self, amount: float) -> None:
        """Добавляет выручку"""
        if amount < 0:
            raise Exception("Выручка не может быть отрицательной")
        self._revenue += amount

    def hire_employee(self, employee: Employee) -> None:
        """Нанять сотрудника"""
        if employee in self._employees:
            raise Exception("Сотрудник уже работает в компании")
        self._employees.append(employee)

    def launch_product(self, drug: Drug) -> None:
        """Запустить продукт"""
        self._products.append(drug)
        print(f"Продукт {drug.name} запущен компанией {self.name}")

    def calculate_profit(self, expenses: float) -> float:
        """Рассчитать прибыль"""
        if expenses < 0:
            raise Exception("Расходы не могут быть отрицательными")
        return self._revenue - expenses

    def get_employee_count(self) -> int:
        return len(self._employees)

class Branch:
    def __init__(self, location: str, company: Company):
        self.location = location
        self.company = company
        self._manager: Optional[Manager] = None
        self._sales = 0.0
        self._employees: List[Employee] = []

    @property
    def manager(self) -> Optional[Manager]:
        return self._manager

    def assign_manager(self, manager: Manager) -> None:
        """Назначить менеджера"""
        if self._manager:
            raise Exception("Менеджер уже назначен")
        self._manager = manager
        self._employees.append(manager)

    def add_sale(self, amount: float) -> None:
        """Добавить продажу"""
        if amount <= 0:
            raise Exception("Сумма продажи должна быть положительной")
        self._sales += amount
        self.company.add_revenue(amount)

    def get_sales_report(self) -> dict:
        """Отчет по продажам"""
        return {
            'location': self.location,
            'total_sales': self._sales,
            'manager': self._manager.name if self._manager else 'Не назначен',
            'employee_count': len(self._employees)
        }

class Batch:
    def __init__(self, batch_id: str, production_date: datetime):
        if production_date > datetime.now():
            raise Exception("Дата производства не может быть в будущем")
        
        self.batch_id = batch_id
        self.production_date = production_date
        self.expiry_date = production_date + timedelta(days=1080)  # 3 года
        self._drugs: List[Drug] = []
        self._is_recalled = False

    def add_drug(self, drug: Drug) -> None:
        """Добавить лекарство в партию"""
        if self._is_recalled:
            raise BatchRecallError("Нельзя добавить лекарство в отозванную партию")
        self._drugs.append(drug)

    def recall(self) -> None:
        """Отозвать партию"""
        self._is_recalled = True
        raise BatchRecallError(f"Партия {self.batch_id} отозвана")

    def inspect_quality(self) -> str:
        """Проверить качество партии"""
        if self._is_recalled:
            return "Партия отозвана"
        
        if datetime.now() > self.expiry_date:
            raise ExpiredDrugError("Партия просрочена")
        
        return f"Партия {self.batch_id} в хорошем состоянии, лекарств: {len(self._drugs)}"

    def get_drug_count(self) -> int:
        return len(self._drugs)

class Stock:
    def __init__(self, stock_id: str, location: str, capacity: int):
        self.stock_id = stock_id
        self.location = location
        self.capacity = capacity
        self._quantity = 0
        self._drugs: List[Drug] = []

    @property
    def quantity(self) -> int:
        return self._quantity

    def add_drugs(self, drugs: List[Drug]) -> None:
        """Добавить лекарства на склад"""
        if self._quantity + len(drugs) > self.capacity:
            raise WarehouseCapacityExceededError(
                f"Превышена вместимость склада. Свободно: {self.capacity - self._quantity}"
            )
        
        self._drugs.extend(drugs)
        self._quantity += len(drugs)

    def remove_drugs(self, count: int) -> List[Drug]:
        """Изъять лекарства со склада"""
        if count > self._quantity:
            raise InsufficientStockError(
                f"Недостаточно на складе. Доступно: {self._quantity}, запрошено: {count}"
            )
        
        removed_drugs = self._drugs[:count]
        self._drugs = self._drugs[count:]
        self._quantity -= count
        return removed_drugs

    def get_utilization_percentage(self) -> float:
        """Процент заполнения склада"""
        return (self._quantity / self.capacity) * 100

class TestSubject:
    def __init__(self, subject_id: str):
        self.subject_id = subject_id
        self.health = 5
        self.vitamins = 5
        self.immune = 5
        self.pain = False
        self.vaccinated = False
        self.alive = True
        self._medical_history: List[str] = []

    def administer_drug(self, drug: Drug, effect: str) -> None:
        """Ввести лекарство и записать эффект"""
        if not self.alive:
            raise Exception("Нельзя вводить лекарство умершему субъекту")
        
        self._medical_history.append(f"{datetime.now()}: {drug.name} - {effect}")
        
        if "обезболивающее" in drug.category.lower():
            self.pain = False
        elif "витамин" in drug.category.lower():
            self.vitamins = min(self.vitamins + 1, 10)

    def check_vital_signs(self) -> dict:
        """Проверить жизненные показатели"""
        if self.health <= 0 or self.immune <= 0:
            self.alive = False
        
        return {
            'alive': self.alive,
            'health': self.health,
            'immune': self.immune,
            'vitamins': self.vitamins,
            'pain': self.pain,
            'vaccinated': self.vaccinated
        }

    def get_medical_history(self) -> List[str]:
        return self._medical_history.copy()

class Antibiotic(PrescriptionDrug):
    def __init__(self, name: str, dosage: str, price: float, batch_code: str, 
                 storage_conditions: str, spectrum: str):
        super().__init__(name, dosage, price, batch_code, storage_conditions, "Антибиотик")
        self.spectrum = spectrum
        self._resistance_checked = False

    def check_resistance(self, subject: TestSubject) -> str:
        """Проверить резистентность"""
        self._resistance_checked = True
        subject.administer_drug(self, "Проверка резистентности")
        return f"Резистентность к {self.spectrum} проверена"

    def administer(self, subject: TestSubject) -> str:
        """Ввести антибиотик"""
        if not self._resistance_checked:
            return "Сначала проверьте резистентность"
        
        subject.administer_drug(self, "Введение антибиотика")
        subject.immune = min(subject.immune + 2, 10)
        return f"Антибиотик {self.name} введен"

class Painkiller(OverTheCounterDrug):
    def __init__(self, name: str, dosage: str, price: float, batch_code: str, 
                 storage_conditions: str, strength: str):
        super().__init__(name, dosage, price, batch_code, storage_conditions, "Обезболивающее")
        self.strength = strength

    def relieve_pain(self, subject: TestSubject) -> str:
        """Снять боль"""
        subject.administer_drug(self, "Обезболивание")
        subject.pain = False
        return f"Боль снята с помощью {self.strength} обезболивающего"

class Vitamin(OverTheCounterDrug):
    def __init__(self, name: str, dosage: str, price: float, batch_code: str, 
                 storage_conditions: str, vitamin_type: str):
        super().__init__(name, dosage, price, batch_code, storage_conditions, "Витамин")
        self.vitamin_type = vitamin_type

    def boost_health(self, subject: TestSubject) -> str:
        """Улучшить здоровье"""
        subject.administer_drug(self, "Улучшение здоровья")
        subject.health = min(subject.health + 1, 10)
        subject.vitamins = min(subject.vitamins + 1, 10)
        return f"Здоровье улучшено витамином {self.vitamin_type}"

class Vaccine(PrescriptionDrug):
    def __init__(self, name: str, dosage: str, price: float, batch_code: str, 
                 storage_conditions: str, doses_required: int):
        super().__init__(name, dosage, price, batch_code, storage_conditions, "Вакцина")
        self.doses_required = doses_required
        self._doses_administered = 0

    def administer_dose(self, subject: TestSubject) -> str:
        """Ввести дозу вакцины"""
        if self._doses_administered >= self.doses_required:
            return "Все дозы уже введены"
        
        self._doses_administered += 1
        subject.administer_drug(self, f"Доза вакцины {self._doses_administered}/{self.doses_required}")
        
        if self._doses_administered == self.doses_required:
            subject.vaccinated = True
            subject.immune = min(subject.immune + 3, 10)
            return "Вакцинация завершена"
        
        return f"Введена доза {self._doses_administered} из {self.doses_required}"

    def get_vaccination_progress(self) -> dict:
        return {
            'completed': self._doses_administered >= self.doses_required,
            'doses_administered': self._doses_administered,
            'doses_required': self.doses_required
        }
        
class LoyaltyProgram:
    def __init__(self, program_name: str, points_per_purchase: int, discount_percentage: float):
        self.program_name = program_name
        self.points_per_purchase = points_per_purchase
        self.discount_percentage = discount_percentage
        self._members: List[Customer] = []
        self._total_points_issued = 0
        self._active_campaigns: List[str] = []

    def enroll_customer(self, customer: Customer) -> None:
        self._members.append(customer)

    def calculate_reward(self, points: int) -> float:
        return points * (self.discount_percentage / 100)

class SalesAnalytics:
    def __init__(self):
        self._daily_sales: Dict[datetime, float] = {}
        self._top_products: List[Drug] = []
        self._customer_demographics: Dict[str, int] = {}
        self._monthly_revenue: float = 0.0
        self._sales_target: float = 100000.0

    def add_sale(self, date: datetime, amount: float) -> None:
        self._daily_sales[date] = amount

    def calculate_growth_rate(self) -> float:
        return (self._monthly_revenue / self._sales_target) * 100

class DeliveryService:
    def __init__(self, service_name: str, delivery_fee: float, max_distance: int):
        self.service_name = service_name
        self.delivery_fee = delivery_fee
        self.max_distance = max_distance
        self._available_couriers: List[str] = []
        self._delivery_times: Dict[str, timedelta] = {}
        self._vehicle_types: List[str] = ["car", "bike", "walk"]

    def assign_courier(self, order: Order) -> str:
        return f"Курьер назначен для заказа {order.order_id}"

class Warehouse:
    def __init__(self, warehouse_id: str, total_capacity: int, temperature_control: bool):
        self.warehouse_id = warehouse_id
        self.total_capacity = total_capacity
        self.temperature_control = temperature_control
        self._current_stock: List[Stock] = []
        self._shelves: Dict[str, List[Drug]] = {}
        self._security_level: int = 1
        self._last_inspection: datetime = datetime.now()

class SecuritySystem:
    def __init__(self):
        self._cameras: List[str] = []
        self._access_logs: List[Dict] = []
        self._alarm_status: bool = False
        self._authorized_personnel: List[Employee] = []
        self._incident_reports: List[str] = []

    def log_access(self, employee: Employee, area: str) -> None:
        self._access_logs.append({
            'employee': employee.name,
            'area': area,
            'timestamp': datetime.now()
        })

class MarketingCampaign:
    def __init__(self, campaign_name: str, budget: float, target_audience: str):
        self.campaign_name = campaign_name
        self.budget = budget
        self.target_audience = target_audience
        self._channels: List[str] = []
        self._start_date: datetime = datetime.now()
        self._end_date: datetime = datetime.now() + timedelta(days=30)
        self._conversion_rate: float = 0.0

    def calculate_roi(self) -> float:
        return (self.budget * self._conversion_rate) / self.budget

class QualityControl:
    def __init__(self):
        self._quality_standards: List[str] = []
        self._inspection_reports: List[Dict] = []
        self._defect_rate: float = 0.0
        self._certifications: List[str] = []
        self._last_audit: datetime = datetime.now()

    def perform_inspection(self, batch: Batch) -> bool:
        return datetime.now() < batch.expiry_date

