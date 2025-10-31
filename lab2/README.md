# Pharmaceutical Distribution Company

## Сущности и их характеристики

| Entity | Fields | Behaviors | Associations |
|--------|--------|-----------|-------------|
| Drug | 8 | 1 | |
| PrescriptionDrug | 1 | 0 | → Drug |
| OverTheCounterDrug | 2 | 2 | → Drug |
| Antibiotic | 2 | 2 | → PrescriptionDrug |
| Painkiller | 1 | 1 | → OverTheCounterDrug |
| Vitamin | 1 | 1 | → OverTheCounterDrug |
| Vaccine | 2 | 2 | → PrescriptionDrug |
| Prescription | 6 | 1 | → Patient |
| Supplier | 6 | 3 | → Drug, PerformanceEvaluator |
| Customer | 5 | 0 | |
| Patient | 5 | 4 | → Prescription, Doctor |
| Doctor | 4 | 4 | → Patient, Prescription |
| Company | 4 | 5 | → Employee, Drug, Branch |
| Branch | 4 | 3 | → Company, Manager, Employee |
| Batch | 4 | 3 | → Drug |
| Stock | 5 | 3 | → Drug |
| TestSubject | 8 | 3 | |
| Order | 9 | 13 | → Customer, Drug, Coupon |
| PatientRecord | 5 | 4 | → Employee |
| Employee | 5 | 2 | → PasswordValidator |
| Manager | 4 | 4 | → Employee, CustomerManagerMixin |
| SalesRepresentative | 2 | 2 | → Employee, CustomerManagerMixin |
| CustomerManagerMixin | 1 | 2 | → Customer |
| Status | 6 | 0 | |

## Сервисные классы

| Entity | Fields | Behaviors | Associations |
|--------|--------|-----------|-------------|
| DrugPricingService | 0 | 2 | → Drug |
| PrescriptionService | 0 | 1 | → Prescription |
| PharmacyService | 3 | 2 | → DrugValidator, PrescriptionValidator, PrescriptionLogger |
| CouponService | 0 | 3 | → Coupon |
| SimplePatientRecordRepository | 1 | 2 | → PatientRecord |
| BasicDoctorPrescriptionService | 0 | 1 | → Patient, Prescription |
| LoyaltyProgram | 5 | 2 | → Customer |
| SalesAnalytics | 6 | 2 | |
| DeliveryService | 6 | 1 | → Order |
| Warehouse | 6 | 0 | → Stock, Drug |
| SecuritySystem | 5 | 1 | → Employee |
| MarketingCampaign | 7 | 1 | |
| QualityControl | 5 | 1 | → Batch |

## Абстрактные классы и интерфейсы

| Entity | Fields | Behaviors | Associations |
|--------|--------|-----------|-------------|
| DrugValidator | 0 | 2 | → Drug |
| PrescriptionValidator | 0 | 2 | → Prescription |
| PrescriptionLogger | 0 | 1 | → Prescription |
| PasswordValidator | 0 | 1 | |
| CustomerRepository | 0 | 1 | → Customer |
| PerformanceEvaluator | 0 | 1 | → Supplier |
| Coupon | 0 | 2 | |
| PatientRecordRepository | 0 | 2 | → PatientRecord |
| DoctorPrescriptionService | 0 | 1 | → Patient, Prescription |

## Реализации интерфейсов

| Entity | Fields | Behaviors | Associations |
|--------|--------|-----------|-------------|
| SimpleDrugValidator | 0 | 2 | → Drug |
| SimplePrescriptionValidator | 0 | 2 | → Prescription |
| ConsolePrescriptionLogger | 0 | 1 | → Prescription |
| SimplePasswordValidator | 0 | 1 | |
| StrongPasswordValidator | 0 | 1 | |
| SpecificPasswordValidator | 0 | 1 | |
| DefaultPerformanceEvaluator | 0 | 1 | → Supplier |
| PercentageCoupon | 2 | 2 | |
| FixedAmountCoupon | 3 | 2 | |
| NoCoupon | 0 | 2 | |

## Итоговая статистика

- **Поля:** 156
- **Поведения:** 104  
- **Ассоциации:** 71
- **Всего классов:** 56 классов
