from Drug import Drug

class PrescriptionDrug(Drug):
    def __init__(
        self, name, dosage, price, batch_code, storage_conditions, category,
        manufacture_date=None, expiration_days=1080
    ):
        super().__init__(name, dosage, price, batch_code, storage_conditions, category,
                         manufacture_date, expiration_days)
        self.requires_prescription = True