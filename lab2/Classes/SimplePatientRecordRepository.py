from typing import Dict
from PatientRecordRepository import PatientRecordRepository
from PatientRecord import PatientRecord

class SimplePatientRecordRepository(PatientRecordRepository):
    def __init__(self):
        self._records: Dict[str, PatientRecord] = {}
    
    def get_record(self, patient_name: str) -> PatientRecord:
        if patient_name not in self._records:
            raise Exception("Медицинская карта не найдена")
        return self._records[patient_name]
    
    def update_record(self, record: PatientRecord) -> None:
        self._records[record.patient_name] = record